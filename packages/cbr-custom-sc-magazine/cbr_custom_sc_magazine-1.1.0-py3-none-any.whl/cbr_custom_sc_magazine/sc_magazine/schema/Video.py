from cbr_custom_sc_magazine.sc_magazine.schema.Video_Platform import Video_Platform
from cbr_custom_sc_magazine.sc_magazine.schema.Content_Item   import Content_Item


class Video(Content_Item):
    duration      : int  # in seconds
    video_url     : str
    video_platform: Video_Platform


    def duration_formatted(self) -> str:
        """Return duration in HH:MM:SS format"""
        hours = self.duration // 3600
        minutes = (self.duration % 3600) // 60
        seconds = self.duration % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
