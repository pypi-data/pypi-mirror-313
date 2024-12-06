import re
from bs4                                                        import BeautifulSoup
from typing                                                     import List, Optional, Dict, Any
from cbr_custom_sc_magazine.sc_magazine.schema.Article          import Article
from cbr_custom_sc_magazine.sc_magazine.schema.Articles_Page    import Articles_Page
from cbr_custom_sc_magazine.sc_magazine.schema.Expert_Report    import Expert_Report
from cbr_custom_sc_magazine.sc_magazine.schema.Home_Page        import Home_Page
from cbr_custom_sc_magazine.sc_magazine.schema.Menu_Item        import Menu_Item
from cbr_custom_sc_magazine.sc_magazine.schema.Navigation       import Navigation
from cbr_custom_sc_magazine.sc_magazine.schema.Page_Metadata    import Page_Metadata
from cbr_custom_sc_magazine.sc_magazine.schema.Social_Link      import Social_Link
from cbr_custom_sc_magazine.sc_magazine.schema.Speaker          import Speaker
from cbr_custom_sc_magazine.sc_magazine.schema.Video            import Video
from cbr_custom_sc_magazine.sc_magazine.schema.Video_Platform   import Video_Platform
from cbr_custom_sc_magazine.sc_magazine.schema.Webinar          import Webinar


class SC_Magazine_Parser:                                       # Parser for SC Magazine HTML content

    def __init__(self, html_content: str):
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.base_url = "https://insight.scmagazineuk.com"

    def parse_homepage(self) -> Home_Page:
        return Home_Page(featured_article   = self._parse_featured_article(),
                         latest_articles    = self._parse_latest_articles (),
                         upcoming_webinars  = self._parse_webinars        (),
                         expert_reports     = self._parse_expert_reports  (),
                         news_briefs        = self._parse_news_briefs     (),
                         videos             = self._parse_videos          ())

    def parse_metadata(self) -> Page_Metadata:
        return Page_Metadata(title          = self._get_meta_content("og:title") or self.soup.title.text,
                            description     = self._get_meta_content("og:description"   ),
                            og_title        = self._get_meta_content("og:title"         ),
                            og_description  = self._get_meta_content("og:description"   ),
                            og_image        = self._get_meta_content("og:image"         ),
                            twitter_card    = self._get_meta_content("twitter:card"     ),
                            canonical_url   = self._get_meta_content("canonical", "link"))

    def parse_navigation(self) -> Navigation:
        nav = self.soup.find('nav', class_='nav--on-page')
        if not nav:
            return Navigation(main_menu=[], social_links=[])

        return Navigation(
            main_menu=self._parse_menu_items(nav),
            social_links=self._parse_social_links()
        )

    def _parse_featured_article(self) -> Article:
        """Parse featured article from homepage"""
        featured = self.soup.find('article', class_='card-highlighted')
        if featured:
            return self._create_article_from_card(featured)

    def _parse_latest_articles(self) -> List[Article]:
        """Parse latest articles list"""
        articles = []
        article_cards = self.soup.find_all('article', class_='card-list--article')

        for card in article_cards[:5]:  # Limit to first 5 articles
            try:
                articles.append(self._create_article_from_card(card))
            except ValueError as e:
                print(f"Warning: Skipping article due to error: {e}")

        return articles

    def _parse_webinars(self) -> List[Webinar]:
        """Parse webinars from homepage"""
        webinars = []
        webinar_cards = self.soup.find_all('div', class_='event-horizontal-card')

        for card in webinar_cards:
            try:
                webinars.append(self._create_webinar_from_card(card))
            except ValueError as e:
                print(f"Warning: Skipping webinar due to error: {e}")

        return webinars

    def _parse_expert_reports(self) -> List[Expert_Report]:
        """Parse expert reports section"""
        reports = []
        report_cards = self.soup.find_all('div', class_='card-basic--document')

        for card in report_cards:
            try:
                reports.append(self._create_expert_report_from_card(card))
            except ValueError as e:
                print(f"Warning: Skipping report due to error: {e}")

        return reports

    def _parse_news_briefs(self) -> List[Article]:
        """Parse news briefs section"""
        briefs = []
        brief_cards = self.soup.find_all('a', class_='card-list-view')

        for card in brief_cards:
            try:
                briefs.append(self._create_news_brief_from_card(card))
            except ValueError as e:
                print(f"Warning: Skipping news brief due to error: {e}")

        return briefs

    def _parse_videos(self) -> List[Video]:
        """Parse videos section"""
        videos = []
        video_cards = self.soup.find_all('div', class_='card-basic')

        for card in video_cards:
            if 'wistia_responsive_padding' in str(card):
                try:
                    videos.append(self._create_video_from_card(card))
                except ValueError as e:
                    print(f"Warning: Skipping video due to error: {e}")

        return videos

    def _create_article_from_card(self, card) -> Article:
        """Create Article instance from card element"""
        title = card.find('h3').get_text(strip=True)
        link = card.find('a', class_='block-link')
        url = self._make_absolute_url(link['href'])

        # Extract date
        date_elem = card.find('time')
        if date_elem:
            date = date_elem.string #parse_date(date_elem['datetime']) if date_elem else datetime.now()
        else:
            date = None

        # Extract description
        desc_elem = card.find('div', class_='card-excerpt')
        description = desc_elem.get_text(strip=True) if desc_elem else None

        # Extract image
        img = card.find('img')
        image_url = img.get('src') if img else None

        # Extract tags
        tags = [tag.get_text(strip=True) for tag in card.find_all('a', class_='term-badge')]

        return Article(
            title=title,
            url=url,
            date=date,
            description=description,
            image_url=image_url,
            tags=tags,
            author="Staff Writer",  # Default author if not specified
            content="",  # Content would need separate page fetch
            category=tags[0] if tags else "Uncategorized"
        )

    def _create_webinar_from_card(self, card) -> Webinar:
        """Create Webinar instance from card element"""
        title = card.find('h3', class_='event-horizontal-card__title').get_text(strip=True)
        link = card.find('a', class_='event-horizontal-card__more-btn')
        url = self._make_absolute_url(link['href'])

        # Parse datetime
        time_elem = card.find('time')
        date = time_elem.string if time_elem else None
        # start_time = time_elem #parse_date(time_elem['datetime']) if time_elem else datetime.now()
        # end_time = start_time.replace(hour=start_time.hour + 1)  # Assume 1 hour duration

        # Parse speakers
        speakers = []
        speaker_elements = card.find_all('span', class_='card-live-session__speaker')
        for speaker_elem in speaker_elements:
            tooltip = speaker_elem['data-tooltip']
            name = re.search(r'<strong>(.*?)</strong>', tooltip).group(1)
            title_match = re.search(r'</strong><br />(.*?)<br />', tooltip)
            company_match = re.search(r'<br />(.*?)$', tooltip)

            speakers.append(Speaker(
                name=name,
                title=title_match.group(1) if title_match else "Speaker",
                company=company_match.group(1) if company_match else "",
                image_url=speaker_elem.find('img')['src']))

        return Webinar(
            title=title,
            url=url,
            date=date,
            # start_time=start_time,
            # end_time=end_time,
            speakers=speakers,
            registration_url=url
        )

    def _create_expert_report_from_card(self, card) -> Expert_Report:
        """Create ExpertReport instance from card element"""
        title = card.find('a', class_='block-link').get_text(strip=True)
        link = card.find('a', class_='block-link')
        url = self._make_absolute_url(link['href'])

        # Extract PDF URL from image source
        img = card.find('img')
        pdf_url = img['src'] if img else None

        return Expert_Report(
            title=title,
            url=url,
            #date=datetime.now(),  # Publication date not readily available
            file_url=pdf_url,
            file_type="pdf",
            authors=["SC Magazine"]  # Default author
        )

    def _create_news_brief_from_card(self, card) -> Article:
        """Create Article instance from news brief card element"""
        title = card.find('h3', class_='card-list-view__title').get_text(strip=True)
        url = self._make_absolute_url(card['href'])

        # Extract image
        img = card.find('img', class_='responsive-img')
        image_url = img['src'] if img else None

        # News briefs don't typically show date on homepage, use current date

        # Description is not typically shown in news brief cards
        description = None

        return Article(
            title           = title,
            url             = url,
            #date=date,
            description     = description,
            image_url       = image_url,
            tags            = ["News Brief"],  # Default category for news briefs
            author          = "SC Magazine Staff",  # Default author
            content         = "",  # Content would need separate page fetch
            category        = "News Brief"
        )

    def _create_video_from_card(self, card) -> Video:
        """Create Video instance from card element"""
        title = card.find('a', class_='block-link').get_text(strip=True)
        link = card.find('a', class_='block-link')
        url = self._make_absolute_url(link['href'])

        # Extract Wistia video ID
        video_div = card.find('div', class_='wistia_embed')
        video_id = video_div['class'][1].split('_')[1] if video_div else ""

        return Video(
            title=title,
            url=url,
            #date=datetime.now(),  # Publication date not readily available
            duration=0,  # Would need API call to get duration
            video_url=f"https://fast.wistia.net/embed/iframe/{video_id}",
            video_platform=Video_Platform.WISTIA
        )

    def _parse_menu_items(self, nav) -> List[Menu_Item]:
        """Parse navigation menu items"""
        menu_items = []
        main_items = nav.find_all('li', recursive=False)

        for item in main_items:
            link = item.find('a')
            if link:
                children = []
                dropdown = item.find('ul', class_='dropdown-content')
                if dropdown:
                    children = self._parse_menu_items(dropdown)

                menu_items.append(Menu_Item(
                    text=link.get_text(strip=True),
                    url=self._make_absolute_url(link['href']),
                    children=children,
                    is_active='active' in item.get('class', [])
                ))

        return menu_items

    def _parse_social_links(self) -> List[Social_Link]:
        """Parse social media links"""
        social_links = []
        social_nav = self.soup.find('ul', class_='top-nav__social-nav')

        if social_nav:
            for link in social_nav.find_all('a'):
                icon = link.find('i')
                if icon:
                    platform = icon['class'][1].replace('fa-', '')
                    social_links.append(Social_Link(
                        platform=platform,
                        url=link['href'],
                        icon=icon['class'][1]
                    ))

        return social_links

    def _get_meta_content(self, property_name: str, tag_name: str = "meta") -> Optional[str]:
        """Helper to get meta tag content"""
        if tag_name == "meta":
            meta = self.soup.find(tag_name, property=property_name) or \
                   self.soup.find(tag_name, attrs={"name": property_name})
            return meta['content'] if meta else None
        else:
            link = self.soup.find(tag_name, rel=property_name)
            return link['href'] if link else None

    def _make_absolute_url(self, url: str) -> str:
        """Convert relative URLs to absolute"""
        if url.startswith('http'):
            return url
        return f"{self.base_url.rstrip('/')}/{url.lstrip('/')}"

    def parse_articles_page(self) -> Articles_Page:                                             # Parse the articles listing page and return a list of article objects
        articles_page = Articles_Page()
        articles      = articles_page.articles
        article_cards = self.soup.find_all('article')
        for card in article_cards:
            try:
                articles.append(self._parse_article_card(card))
            except ValueError as e:
                print(f"Warning: Skipping article due to error: {e}")

        return articles_page

    def parse_article_detail(self) -> Article:
        """Parse a single article detail page"""
        # Find main article content
        article_content = self.soup.find('article', class_='article-detail')
        if not article_content:
            raise ValueError("Could not find article content")

        # Get title
        title_elem = article_content.find('h1', class_='article-detail__title')
        title = title_elem.get_text(strip=True) if title_elem else ""

        # Get author
        author_elem = article_content.find('div', class_='article-detail__author')
        author = author_elem.get_text(strip=True) if author_elem else "Staff Writer"

        # Get date
        date_elem = article_content.find('time')
        date = date_elem.get('datetime') if date_elem else None

        # Get content
        content_elem = article_content.find('div', class_='article-detail__content')
        content = content_elem.get_text(strip=True) if content_elem else ""

        # Get image
        img = article_content.find('img', class_='article-detail__image')
        image_url = img.get('src') if img else None

        # Get tags/categories
        tags = []
        tag_elements = article_content.find_all('a', class_='term-badge')
        if tag_elements:
            tags = [tag.get_text(strip=True) for tag in tag_elements]
            category = tags[0] if tags else "Uncategorized"
        else:
            category = "Uncategorized"

        # Get description/excerpt
        description_elem = article_content.find('div', class_='article-detail__excerpt')
        description = description_elem.get_text(strip=True) if description_elem else None

        return Article(
            title=title,
            url=self._make_absolute_url(self.soup.find('link', rel='canonical')['href']) if self.soup.find('link', rel='canonical') else "",
            date=date,
            description=description,
            image_url=image_url,
            tags=tags,
            author=author,
            content=content,
            category=category
        )

    def _parse_article_card(self, card) -> Article:
        """Parse an individual article card from the listing page"""
        # Get title
        title = card.find('h3').get_text(strip=True)

        # Get link
        link = card.find('a', class_='block-link')
        url = self._make_absolute_url(link['href']) if link else ""

        # Get date
        date_elem = card.find('time', class_='card-list__date')
        date = date_elem.get_text(strip=True) if date_elem else None

        # Get description
        desc_elem = card.find('div', class_='card-list__description')
        description = desc_elem.get_text(strip=True) if desc_elem else None

        # Get image
        img = card.find('img', class_='card__rich-media__image')
        image_url = img.get('src') if img else None

        # Get tags/category
        tags = []
        tag_elements = card.find_all('a', class_='term-badge')
        if tag_elements:
            tags = [tag.get_text(strip=True) for tag in tag_elements]
            category = tags[0] if tags else "Uncategorized"
        else:
            category = "Uncategorized"

        # For listing pages, we don't have full content
        content = ""

        return Article(
            title=title,
            url=url,
            date=date,
            description=description,
            image_url=image_url,
            tags=tags,
            author="Staff Writer",  # Default author for listing pages
            content=content,
            category=category
        )