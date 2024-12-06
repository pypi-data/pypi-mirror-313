from typing                                                 import List
from cbr_custom_sc_magazine.sc_magazine.schema.Content_Item import Content_Item
from cbr_custom_sc_magazine.sc_magazine.schema.Speaker      import Speaker

class Webinar(Content_Item):
    start_time      : str
    end_time        : str
    speakers        : List[Speaker]
    registration_url: str
    is_upcoming     : bool


    def duration_minutes(self) -> int:
        """Calculate webinar duration in minutes"""
        return int((self.end_time - self.start_time).total_seconds() / 60)
