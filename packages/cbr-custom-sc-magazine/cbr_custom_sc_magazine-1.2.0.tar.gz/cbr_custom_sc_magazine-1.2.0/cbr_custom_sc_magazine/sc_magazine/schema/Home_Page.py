from typing                                                  import List
from osbot_utils.base_classes.Type_Safe                      import Type_Safe
from cbr_custom_sc_magazine.sc_magazine.schema.Article       import Article
from cbr_custom_sc_magazine.sc_magazine.schema.Webinar       import Webinar
from cbr_custom_sc_magazine.sc_magazine.schema.Video         import Video
from cbr_custom_sc_magazine.sc_magazine.schema.Expert_Report import Expert_Report

class Home_Page(Type_Safe):
    featured_article : Article
    latest_articles  : List[Article      ]
    upcoming_webinars: List[Webinar      ]
    expert_reports   : List[Expert_Report]
    news_briefs      : List[Article      ]
    videos           : List[Video        ]
