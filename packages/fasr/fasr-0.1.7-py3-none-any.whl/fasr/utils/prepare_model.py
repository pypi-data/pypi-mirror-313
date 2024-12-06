def prepare_offline_models(cache_dir: str = "checkpoints"):
    """Prepare offline models for building pipeline"""
    from modelscope import snapshot_download

    models = [
        "iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch",
        "iic/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
        "iic/SenseVoiceSmall",
        "iic/speech_fsmn_vad_zh-cn-16k-common-onnx",
    ]
    for model in models:
        snapshot_download(model_id=model, cache_dir=cache_dir)


def prepare_online_models(cache_dir: str = "checkpoints"):
    """
    Prepare online models for building pipeline
    """
    from modelscope import snapshot_download

    models = [
        "iic/SenseVoiceSmall",
        "iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-online",
        "iic/speech_fsmn_vad_zh-cn-16k-common-pytorch",
    ]
    for model in models:
        snapshot_download(model_id=model, cache_dir=cache_dir)


def download(model: str, revision: str = None, cache_dir: str = "checkpoints"):
    """Download model from modelscope"""
    from modelscope import snapshot_download

    model = snapshot_download(model, cache_dir=cache_dir, revision=revision)
