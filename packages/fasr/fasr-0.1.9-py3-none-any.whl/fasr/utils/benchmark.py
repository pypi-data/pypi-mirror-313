from pathlib import Path
import time
from loguru import logger
from tqdm import tqdm, trange


def benchmark_pipeline(
    urls: str,
    batch_size: int = 2,
    num_threads: int = 2,
    asr_batch_s: int = 80,
    num_samples: int | None = None,
    model_dir: str = "checkpoints/iic/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
    vad_model_dir: str = "checkpoints/iic/speech_fsmn_vad_zh-cn-16k-common-pytorch",
    punc_model_dir: str = "checkpoints/iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch",
):
    """对比测试fasr与funasr pipeline(load -> vad -> asr -> punc)的性能.

    Args:
        urls (str): url文件路径.
        batch_size (int, optional): 批处理大小. Defaults to 2.
        num_threads (int, optional): 并行处理的工作线程数. Defaults to 2.
        asr_batch_s (int, optional): asr模型的批处理大小. Defaults to 80.
        vad_batch_s (float, optional): vad模型的批处理大小. Defaults to 2400.
        num_samples (int, optional): 采样数量. Defaults to 100.
        model_dir (str, optional): 语音识别模型目录. Defaults to "checkpoints/iic/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch".
        vad_model_dir (str, optional): 语音检测模型目录. Defaults to "checkpoints/iic/speech_fsmn_vad_zh-cn-16k-common-pytorch".
        punc_model_dir (str, optional): 标点符号模型目录. Defaults to "checkpoints/iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch".
    """
    from funasr import AutoModel
    from fasr import AudioPipeline
    from fasr.data import Audio, AudioChannel

    if not Path(urls).exists():
        raise FileNotFoundError(f"{urls} not found")
    if Path(urls).is_dir():
        urls = [
            str(p) for p in Path(urls).iterdir() if p.is_file() and p.suffix == ".wav"
        ]
    else:
        with open(urls, "r") as f:
            urls = f.readlines()
        urls = [url.strip() for url in urls]
    if num_samples:
        urls = urls[:num_samples]
    base_model = AutoModel(
        model=model_dir, vad_model=vad_model_dir, punc_model=punc_model_dir
    )
    asr = AudioPipeline()
    duration = 0
    for idx in range(0, len(urls), batch_size):
        batch_urls = urls[idx : idx + batch_size]
        audios = asr.run(batch_urls)
        for audio in audios:
            duration += audio.duration * len(audio.channels)
    asr = (
        AudioPipeline()
        .add_pipe(
            "detector",
            num_threads=num_threads,
            compile=True,
            model_dir=vad_model_dir,
            batch_size=batch_size,
        )
        .add_pipe(
            "recognizer",
            model_dir=model_dir,
            batch_size_s=asr_batch_s,
            batch_size=batch_size,
        )
        .add_pipe("sentencizer", model_dir=punc_model_dir)
    )

    def run_funasr(urls):
        start = time.perf_counter()
        for url in tqdm(urls):
            audio = Audio(url=url).load()
            for channel in audio.channels:
                channel: AudioChannel
                _ = base_model.generate(
                    input=channel.waveform,
                    fs=channel.sample_rate,
                    batch_size_s=asr_batch_s,
                )
        end = time.perf_counter()
        took = round(end - start, 2)
        return took

    def run_fasr(urls):
        start = time.perf_counter()
        _ = asr.run(urls)
        end = time.perf_counter()
        took = round(end - start, 2)
        return took

    # warm up
    url = urls[0]
    _ = run_funasr([url])
    _ = run_fasr([url])

    # benchmark
    funasr_took = run_funasr(urls)
    fasr_took = run_fasr(urls)
    # 所有通道的总时长
    logger.info(f"All channels duration: {round(duration, 2)} seconds")
    logger.info(
        f"funasr: took {funasr_took} seconds, speedup: {round(duration/funasr_took, 2)}, 1x"
    )
    logger.info(
        f"fasr: took {fasr_took} seconds, speedup: {round(duration/fasr_took, 2)}, {round(funasr_took/fasr_took, 2)}x"
    )


def benchmark_vad(
    urls: str,
    batch_size: int = 2,
    num_threads: int = 2,
    num_samples: int | None = None,
    model_dir: str = "checkpoints/iic/speech_fsmn_vad_zh-cn-16k-common-pytorch",
):
    """对比测试fasr与funasr pipeline(load -> vad)的性能.

    Args:
        urls (str): url文件路径.
        batch_size (int, optional): 批处理大小. Defaults to 2.
        num_threads (int, optional): 并行处理的工作线程数. Defaults to 2.
        num_samples (int, optional): 采样数量. Defaults to 100.
        model_dir (str, optional): 语音检测模型目录. Defaults to "checkpoints/iic/speech_fsmn_vad_zh-cn-16k-common-pytorch".
    """
    from funasr import AutoModel
    from fasr.data import Audio, AudioChannel, AudioList
    from fasr import AudioPipeline

    if not Path(urls).exists():
        raise FileNotFoundError(f"{urls} not found")
    if Path(urls).is_dir():
        urls = [
            str(p) for p in Path(urls).iterdir() if p.is_file() and p.suffix == ".wav"
        ]
    else:
        with open(urls, "r") as f:
            urls = f.readlines()
        urls = [url.strip() for url in urls]
    if num_samples:
        urls = urls[:num_samples]

    asr = AudioPipeline()
    audios = AudioList[Audio]()
    duration = 0
    for idx in range(0, len(urls), batch_size):
        batch_urls = urls[idx : idx + batch_size]
        batch_audios = asr(batch_urls)
        for audio in batch_audios:
            duration += audio.duration * len(audio.channels)
        audios.extend(batch_audios)
    base_model = AutoModel(model=model_dir)
    asr = AudioPipeline().add_pipe(
        "detector", compile=True, num_threads=num_threads, model_dir=model_dir
    )

    def run_funasr(audios: AudioList[Audio]) -> float:
        start = time.perf_counter()
        for i in trange(len(audios)):
            audio = audios[i]
            audio: Audio
            for channel in audio.channels:
                channel: AudioChannel
                _ = base_model.generate(input=channel.waveform, fs=channel.sample_rate)
        end = time.perf_counter()
        took = round(end - start, 2)
        return took

    def run_fasr(audios: AudioList[Audio]) -> float:
        start = time.perf_counter()
        for i in trange(0, len(audios), batch_size):
            _audios = audios[i : i + batch_size]
            result = asr.run(_audios)
        end = time.perf_counter()
        took = round(end - start, 2)
        return took

    # warm up
    _ = run_funasr(audios[0:1])
    _ = run_fasr(audios[0:1])

    # benchmark
    funasr_took = run_funasr(audios)
    fasr_took = run_fasr(audios)
    logger.info(f"All channels duration: {round(duration, 2)} seconds")
    logger.info(
        f"funasr: took {funasr_took} seconds, speedup: {round(duration/funasr_took, 2)}, 1x"
    )
    logger.info(
        f"fasr: took {fasr_took} seconds, speedup: {round(duration/fasr_took, 2)}, {round(funasr_took/fasr_took, 2)}x"
    )
