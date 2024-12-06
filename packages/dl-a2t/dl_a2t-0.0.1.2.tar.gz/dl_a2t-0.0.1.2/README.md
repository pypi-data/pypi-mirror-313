# dl-a2t

dl-a2t 是一个从 YouTube 下载音频并转录为文本的工具。它使用 yt-dlp 下载音频，并使用 OpenAI 的 Whisper 模型进行转录。

## 使用方法

使用 dl-a2t 需要 Python 3.12 或更高版本。首先，确保你已经安装了 Python 和 pip。然后，使用以下命令安装 dl-a2t：

```sh
pip install dl-a2t
```

安装完成后，你可以使用以下命令来下载音频并转录为文本：

```sh
dl-a2t run url_of_video output_file
```

也可以输入一个文件，每行是一个 url

```sh
dl-a2t batch input_file output_file
```

获取详细的 API 文档：

```sh
dl-a2t --help
dl-a2t run --help
dl-a2t batch --help
```

## Options

- `--model`：选择 Whisper 模型大小，默认为 `tiny`

## 依赖项

dl-a2t 依赖以下库：

-`yt-dlp`：用于下载 YouTube 视频的音频
-`OpenAI Whisper`：用于转录音频为文本
-`Typer`：用于命令行界面

## 文件结构

dl-a2t 的文件结构如下：

-`cli.py`：命令行界面
-`pyproject.toml`：项目配置文件
-`impl/download.py`：用于下载音频的实现
-`impl/transcript.py`：用于转录音频为文本的实现
