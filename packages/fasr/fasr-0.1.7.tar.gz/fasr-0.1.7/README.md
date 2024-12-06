# 🪐 项目: fasr

Fast Auto Speech Recognition

## 📋 简介

    fasr是一款快速且易于使用的python库，它源于FunASR，专注于推理性能，目标是成为一个工业级别的python语音识别推理库。

[`文档地址`](https://docs.58corp.com/#/space/1830509042628354051?goindex=true)

## 📋 安装

### wpai
- 在wpai平台选择pytorch镜像后，执行以下命令安装所有依赖
```bash
bash install.sh
```

### 本地
fasr可以通过直接通过pip安装，但是如果需要使用gpu，需要安装pytorch和onnxruntime-gpu
- 安装pytorch： 通过[官网](https://pytorch.org/get-started/locally/)安装对应cuda版本
- 安装onnxruntime-gpu: 通过[官网](https://onnxruntime.ai/docs/install/)安装对应cuda版本
- 安装fasr
```bash
pip install fasr
```



## 📋 使用

- 下载模型
```bash
fasr prepare
```
- 构建pipeline
```python
from fasr import AudioPipeline

# 语音识别pipeline
asr = AudioPipeline().add_pipe('detector').add_pipe('recognizer').add_pipe('sentencizer')

# 准备音频数据url或者本地路径
urls = get_urls()

# 运行
audios = asr.run(urls)

# 打印结果
for audio in audios:
    for channel in audio.channels:
        print(channel.text)

```


## 📋 性能测试

###  双通道音频

**vad->asr->punc**


测试结果

cpu: Intel(R) Xeon(R) Silver 4210 CPU @ 2.20GHz (wpai cpu 2核)

gpu: rtx6000 （wpai vgpu 20）

| 框架 | 耗时 | 推理速度 | 加速比 |
|:----|:----|:----|----:|
|funasr|368.8s|46.34| 1.0|
|fasr|153.92s|111.03| 2.4|


###  vad


测试结果

cpu: Intel(R) Xeon(R) Silver 4210 CPU @ 2.20GHz (wpai cpu 2核)

gpu: rtx6000 （wpai vgpu 20）

| 框架 | 耗时 | 推理速度 | 加速比 |
|:----|:----|:----|----:|
|funasr|219.8s|77.75| 1.0|
|fasr|86.32s|197.98| 2.55|


## 单通道音频

###  pipeline

**vad->asr->punc**


测试结果

cpu: Intel(R) Xeon(R) Silver 4210 CPU @ 2.20GHz (wpai cpu 2核)

gpu: rtx6000 （wpai vgpu 20）

| 框架 | 耗时 | 推理速度 | 加速比 |
|:----|:----|:----|----:|
|funasr|123.8s|22.05| 1.0|
|fasr|59.04s|46.24| 2.1|


###  vad


测试结果

cpu: Intel(R) Xeon(R) Silver 4210 CPU @ 2.20GHz (wpai cpu 2核)

gpu: rtx6000 （wpai vgpu 20）

| 框架 | 耗时 | 推理速度 | 加速比 |
|:----|:----|:----|----:|
|funasr|59.26s|46.07| 1.0|
|fasr|36.84s|74.1| 1.61|


## AISHELL

###  pipeline

**vad->asr->punc**

测试结果

cpu: Intel(R) Xeon(R) Silver 4210 CPU @ 2.20GHz (wpai cpu 2核)

gpu: rtx6000 （wpai vgpu 20）

| 框架 | 耗时 | 推理速度 | 加速比 |
|:----|:----|:----|----:|
|funasr|123.8s|18.65| 1.0|
|fasr|59.04s|32.71| 1.8|