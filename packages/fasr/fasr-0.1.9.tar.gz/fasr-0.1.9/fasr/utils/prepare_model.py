from pathlib import Path


DEFAULT_CACHE_DIR = Path.home() / ".cache" / "fasr" / "checkpoints"  # 默认缓存目录


def prepare_offline_models(cache_dir: str | Path = DEFAULT_CACHE_DIR):
    """Prepare offline models for building pipeline"""
    from modelscope import snapshot_download

    models = [
        "iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch",
        "iic/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
        "iic/SenseVoiceSmall",
    ]
    for model in models:
        snapshot_download(model_id=model, cache_dir=cache_dir)


def prepare_online_models(cache_dir: str | Path = DEFAULT_CACHE_DIR):
    """
    Prepare online models for building pipeline
    """
    from modelscope import snapshot_download

    models = [
        "iic/SenseVoiceSmall",
        "iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-online",
    ]
    for model in models:
        snapshot_download(model_id=model, cache_dir=cache_dir)


def download(
    model: str, revision: str = None, cache_dir: str | Path = DEFAULT_CACHE_DIR
):
    """Download model from modelscope"""
    from modelscope import snapshot_download

    model = snapshot_download(model, cache_dir=cache_dir, revision=revision)
