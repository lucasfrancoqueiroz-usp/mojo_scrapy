import scrapy
import re
import pandas as pd
import os

# scrapy runspider movies_title_summary_spider.py -o movies_summary.json
class MovieTitleSummarySpider(scrapy.Spider):
    name = "movietitlesummary"
    movies_file = "movies_wide.jl"
    movies_summary_file = "movies_summary.jl"

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None  # Force quick fail
        }
    }

    def __init__(self):
        self.start_urls = self.__get_movies_url()

    def __get_movies_url(self):
        url_base = "https://www.boxofficemojo.com/"
        df = pd.read_json(self.movies_file, lines=True)

        scrapped = 0
        not_scrapped = len(df)

        # Could be necessary execute more than one time to get all records
        # This happens because Mojo Box Office blocks continuous access
        # The following code prevents to get just the not loaded movies
        if os.path.isfile(self.movies_summary_file):
            df_movies_summary = pd.read_json(self.movies_summary_file, lines=True)
            loaded_releases_ids = df_movies_summary['release_id'].unique()
            not_loaded_realeases_mask = ~df['release_id'].isin(loaded_releases_ids)
            df = df[not_loaded_realeases_mask]
            not_loaded_realeases_ids = df['release_id'].unique()

            scrapped = len(loaded_releases_ids)
            not_scrapped = len(not_loaded_realeases_ids)

        self.logger.info(f"# movies scrapped: {scrapped}")
        self.logger.info(f"# movies to be scrapped: {not_scrapped}")

        return (url_base + df['url']).to_list()

    def parse(self, response, **kwargs):

        self.logger.info(f"{response.url}")

        DISTRIBUTOR_STR = 'Distributor'
        OPENING_STR = 'Opening'
        BUGET_STR = 'Budget'
        RELEASE_STR = 'Release Date'
        MPAA_STR = 'MPAA'
        RUNNING_TIME_STR = 'Running Time'
        GENRES_STR = 'Genres'
        IN_RELEASE_STR = 'In Release'
        WIDEST_STR = 'Widest Release'

        release_id = re.search(r"rl\d+", response.url)[0]

        xpath_item = "//div/span[contains(text(), '%s')]/following-sibling::*"
        summary = response.xpath("//*[@class='a-section a-spacing-none mojo-summary-values mojo-hidden-from-mobile']")
        distributor = summary.xpath(xpath_item % DISTRIBUTOR_STR).xpath("./text()").get()
        opening = summary.xpath(xpath_item % OPENING_STR)
        opening_theaters = opening.xpath("./text()").get()
        opening_money = opening.xpath("./span/text()").get()
        buget = summary.xpath(xpath_item % BUGET_STR).xpath("./span/text()").get()
        release = summary.xpath(xpath_item % RELEASE_STR).xpath("./a/text()")
        release_start = release[0].get()
        release_end = release[len(release) - 1].get()
        mpaa = summary.xpath(xpath_item % MPAA_STR).xpath("./text()").get()
        running_time = summary.xpath(xpath_item % RUNNING_TIME_STR).xpath("./text()").get()
        genres = summary.xpath(xpath_item % GENRES_STR).xpath("./text()").get()
        in_release = summary.xpath(xpath_item % IN_RELEASE_STR).xpath("./text()").get()
        widest_release = summary.xpath(xpath_item % WIDEST_STR).xpath("./text()").get()

        yield {
            'distributor': distributor,
            'opening_theaters': opening_theaters,
            'opening_money': opening_money,
            'buget': buget,
            'release_start': release_start,
            'release_end': release_end,
            'mpaa': mpaa,
            'running_time': running_time,
            'genres': genres,
            'in_release': in_release,
            'widest_release': widest_release,
            'release_id': release_id
        }
