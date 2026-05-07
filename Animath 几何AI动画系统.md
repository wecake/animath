# Animath 几何AI动画系统

# 项目介绍

Animath 是一款针对初中几何题的全流程自动化AI动画生成系统，基于 Qwen3\.5\-Plus 多模态大模型 \+ Manim 动画引擎 \+ Edge\-TTS 语音合成 \+ ffmpeg 音视频合成，实现从题目识图到最终成片的一站式生成。

系统采用模块化拆分设计，各模块独立运行、无缝衔接，可单独调试，也可通过一键启动脚本完成全流程，适配初中几何常见题型（阿氏圆、将军饮马、胡不归等）。

# 核心功能

- 识图解题：上传几何题目图片，自动识别题意、生成解题步骤和最终答案

- 文案生成：根据解题步骤，自动生成分镜脚本和配音解说文案

- 语音字幕：将配音文案转换为标准SRT字幕和自然中文旁白音频

- 视频合成：将Manim渲染的动画视频、旁白音频、字幕合并为最终成片

- 模块化设计：各功能独立拆分，可单独运行、灵活扩展

# 项目架构

## 目录结构

```plain text
animath/
├─ app/
│  └─ llm.py           # 大模型接口封装（识图、解题、分镜、文案生成）
├─ run_webui.py        # 前端界面 + 文案生成模块（识图→解题→分镜→配音文案）
├─ run_voice.py        # 语音字幕模块（生成SRT字幕、Edge-TTS旁白音频）
├─ run_artifact.py     # 最终成片模块（合并视频+音频+字幕，输出成品）
├─ start.bat           # 一键启动脚本（自动执行全流程）
├─ output/             # 中间文件&成品目录（自动生成）
│  ├─ answer.txt       # 解题答案（run_webui.py生成）
│  ├─ steps.txt        # 解题步骤（run_webui.py生成）
│  ├─ scripts.txt      # 配音文案（run_webui.py生成）
│  ├─ storyboard.txt   # 动画分镜（run_webui.py生成）
│  ├─ subtitle.srt     # 字幕文件（run_voice.py生成）
│  ├─ voice.mp3        # 旁白音频（run_voice.py生成）
│  └─ final_video.mp4  # 最终成片（run_artifact.py生成）
├─ media/              # Manim动画渲染缓存目录（自动生成）
├─ .env                # 环境变量配置（存放QWEN_API_KEY）
└─ README.md           # 项目说明文档
```

## 模块分工（严格按流程拆分）

|模块文件|核心功能|输入|输出|
|---|---|---|---|
|run\_webui\.py|识图 → 解题 → 动画分镜 → 配音文案|几何题目图片、辅助说明、题型选择|answer\.txt、steps\.txt、scripts\.txt、storyboard\.txt|
|run\_voice\.py|字幕生成（SRT）、音频生成（旁白）|output/scripts\.txt（配音文案）|subtitle\.srt（字幕）、voice\.mp3（音频）|
|run\_artifact\.py|合并视频\+音频\+字幕，生成最终成片|Manim渲染视频、voice\.mp3、subtitle\.srt|final\_video\.mp4（最终成品）|
|start\.bat|一键启动全流程，自动执行3个模块|无（需提前配置环境）|全流程自动执行，生成最终成片|

# 环境部署

## 1\. 依赖安装

先创建虚拟环境（可选但推荐），再安装所需依赖，推荐使用以下适配版本（避免版本冲突）：

```bash
# 1. 创建虚拟环境（Windows）
python -m venv .venv
.venv\Scripts\activate

# 2. 安装适配版本依赖（推荐版本，无冲突）
pip install gradio==4.28.3 pillow==10.3.0 python-dotenv==1.0.1
pip install requests==2.31.0 edge-tts==6.1.1 ffmpeg-python==0.2.0 manim==0.20.0
```

说明：ffmpeg 需额外安装（Windows可下载ffmpeg\.exe，配置环境变量；Linux/Mac可通过包管理器安装），推荐ffmpeg版本为5\.1\.3（适配当前依赖，稳定性最佳）。

### 依赖版本说明

各依赖版本适配项目功能，避免版本过高/过低导致异常，具体说明如下：

- gradio==4\.28\.3：适配Web界面正常启动，避免高版本兼容性问题，确保上传图片、步骤显示正常

- pillow==10\.3\.0：用于图片读取与Base64转换，适配识图功能，稳定无报错

- python\-dotenv==1\.0\.1：用于读取\.env文件中的API\_KEY，版本稳定，适配所有Python环境

- requests==2\.31\.0：用于调用Qwen3\.5\-Plus API，避免高版本请求格式不兼容问题

- edge\-tts==6\.1\.1：用于生成旁白音频，适配中文语音，无发音异常、生成失败问题

- ffmpeg\-python==0\.2\.0：用于音视频合成，适配ffmpeg 5\.1\.3版本，确保字幕、音频、视频正常合并

- manim==0\.20\.0：用于渲染几何动画，适配项目代码，避免低版本缺少核心函数、高版本语法变更问题

## 2\. 环境变量配置

在项目根目录创建 `\.env` 文件，填写通义千问API\_KEY（用于识图、解题、文案生成）：

```plain text
QWEN_API_KEY=你的通义千问API_KEY（从阿里云百炼平台获取）
```

# 使用方法

## 方法一：一键启动全流程（推荐）

1. 确保 `\.env` 文件已配置API\_KEY，依赖已安装完成。

2. 双击项目根目录的 `start\.bat` 文件，自动启动所有模块。

3. 启动后会自动打开浏览器（地址：http://0\.0\.0\.0:7860），在Web界面上传几何题目图片，填写辅助说明、选择题型，点击「开始解析」。

4. Web界面完成文案生成后，`run\_voice\.py` 和`run\_artifact\.py` 会自动执行，最终在`output` 目录生成 `final\_video\.mp4`（最终成片）。

## 方法二：单独运行各模块（用于调试）

### 1\. 运行文案生成模块（run\_webui\.py）

```bash
python run_webui.py
```

打开浏览器访问 http://0\.0\.0\.0:7860，完成识图、解题、分镜、配音文案生成，生成的中间文件会保存到 `output` 目录。

### 2\. 运行语音字幕模块（run\_voice\.py）

```bash
python run_voice.py
```

自动读取 `output/scripts\.txt`，生成字幕（subtitle\.srt）和旁白音频（voice\.mp3），保存到 `output` 目录。

### 3\. 运行最终成片模块（run\_artifact\.py）

```bash
python run_artifact.py
```

自动读取Manim渲染的视频、output目录的音频和字幕，合并生成最终成片（final\_video\.mp4），保存到 `output` 目录。

# 关键说明

- Manim渲染：`run\_artifact\.py` 会自动搜索 `media/videos` 目录下Manim渲染的 `MathAnimation\.mp4` 视频，无需手动指定路径。

- 异常处理：若某模块执行失败，可单独运行该模块排查问题（如语音生成失败，可单独运行 `python run\_voice\.py` 查看报错）。

- 参数调整：字幕显示时长、旁白语音类型可在 `run\_voice\.py` 中修改（如修改 `start \+= 4` 调整字幕每句显示4秒，修改 `zh\-CN\-YunxiNeural` 更换语音）。

- 中间文件：`output` 目录下的中间文件（步骤、文案、字幕等）可保留，便于后续重新生成音频、成片，无需重复执行Web界面解析。

# 常见问题

## 1\. Web界面无法打开

检查是否启动成功，若提示端口被占用，可修改 `run\_webui\.py` 中 `server\_port=7860` 为其他端口（如7861）。

## 2\. 语音生成失败

确保已安装 edge\-tts，且网络正常（Edge\-TTS需要联网）；若语音类型报错，可更换 `run\_voice\.py` 中的语音参数（如 `zh\-CN\-WangYuNeural`）。

## 3\. 最终成片合成失败

检查 `output` 目录是否有 `voice\.mp3` 和`subtitle\.srt`，且 `media` 目录下有Manim渲染的视频；确保ffmpeg已配置环境变量。

## 4\. 识图/解题失败

检查 `\.env` 文件中的API\_KEY是否正确，且网络正常；确保上传的题目图片清晰、无遮挡，题型选择正确。

## 5\. 依赖安装失败/版本冲突

卸载当前冲突依赖，严格按照上述推荐版本重新安装，命令：`pip install 依赖名==版本号`；若仍失败，可升级pip至24\.0版本（`pip install \-\-upgrade pip`）后重试。

# 后续可扩展方向

- 增加历史记录功能，保存过往解题和成片记录

- 支持自定义动画风格、字幕样式、旁白语速

- 接入更多题型（如全等三角形、相似三角形等）

- 增加成片预览功能，支持在线编辑字幕和音频

> （注：文档部分内容可能由 AI 生成）
