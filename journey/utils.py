from pytube import YouTube
import os
import re

class YouTubeDownloader:
    def __init__(self, url, output_path='media/sounds/journey'):
        self.url = url
        self.output_path = output_path
        self.audio_path = None
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def sanitize_filename(self, filename):
        return re.sub(r'[\\/*?:"<>|]', "", filename)
    
    def download_audio(self):
        yt = YouTube(self.url)
        title = self.sanitize_filename(yt.title)
        audio_stream = yt.streams.filter(only_audio=True).first()
        self.audio_path = os.path.join(self.output_path, f"{title}_audio.mp4")
        audio_stream.download(output_path=self.output_path, filename=f"{title}_audio.mp4")
        print(f"Audio downloaded to {self.audio_path}")
        return self.audio_path
