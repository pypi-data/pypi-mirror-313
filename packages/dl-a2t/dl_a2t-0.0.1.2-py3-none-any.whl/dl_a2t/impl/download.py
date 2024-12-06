def extract_audio(url: str, output_path: str):
    from yt_dlp import YoutubeDL

    ydl_opts = {"format": "bestaudio/best", "outtmpl": output_path}

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
