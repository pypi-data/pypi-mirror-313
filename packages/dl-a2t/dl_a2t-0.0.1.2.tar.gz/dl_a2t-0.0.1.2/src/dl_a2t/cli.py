from hashlib import md5
from json import dumps
from pathlib import Path
from tempfile import TemporaryDirectory
from traceback import format_exception
from typing import Annotated

from typer import FileText, Option, Typer

from .impl.download import extract_audio
from .impl.transcript import transcribe_audio

app = Typer(no_args_is_help=True, add_completion=False)


@app.command()
def run(
    input_url: str,
    output_file: Path,
    *,
    model: Annotated[str, Option(help="Whisper model to use")] = "tiny",
):
    """下载音频并转录为文本"""
    with TemporaryDirectory() as temp_dir:
        filename = f"{temp_dir}/audio.webm"
        extract_audio(input_url, filename)
        result = transcribe_audio(filename, model)

    if output_file.name.endswith(".json"):
        output_file.write_text(dumps(result, ensure_ascii=False, indent=2))
    else:
        output_file.write_text(result["text"])


@app.command()
def batch(
    input_file: FileText,
    output_dir: Path,
    *,
    model: Annotated[str, Option(help="Whisper model to use")] = "tiny",
):
    """批量下载音频并转录为文本"""

    if not output_dir.is_dir():
        if output_dir.exists():
            raise ValueError("Output must be a directory")
        else:
            output_dir.mkdir(parents=True)

    with (output_dir / "results.jsonl").open("wt", encoding="utf-8") as f:
        for line in input_file:
            url = line.strip()
            print(url)

            name = md5(url.encode()).hexdigest()
            audio_filename = str(output_dir.resolve() / f"{name}.webm")
            data = {"url": url, "audio": audio_filename}

            try:
                extract_audio(url, audio_filename)
                result = transcribe_audio(audio_filename, model)
                data |= {"transcript": result}
            except Exception as e:
                data |= {"error": format_exception(e)}

            print(dumps(data, ensure_ascii=False), file=f)


if __name__ == "__main__":
    app()
