from .utils.prepare_model import download, prepare_offline_models, prepare_online_models
from .utils.benchmark import benchmark_pipeline, benchmark_vad
from jsonargparse import CLI


commands = {
    "prepare": {
        "offline": prepare_offline_models,
        "online": prepare_online_models,
    },
    "download": download,
    "benchmark": {
        "pipeline": benchmark_pipeline,
        "vad": benchmark_vad,
        "_help": "benchmark the pipeline or vad",
    },
}


def run():
    """命令行"""
    CLI(components=commands)


if __name__ == "__main__":
    run()
