import scrapy
import re
import pandas as pd
import os

# scrapy runspider movies_title_summary_spider.py -o moviessummary.json
class MovieTitleSummarySpider(scrapy.Spider):
    name = "movietitlesummary"
    movies_file = "movies.jl"
    moviesfinance_file = "moviessummary.jl"

    def __init__(self):
        self.start_urls = self.__get_movies_url()

    def __get_movies_url(self):
        url_base = "https://www.boxofficemojo.com/"

        # movies.jl is generating running spider scripts, example:
        # scrapy runspider movies_list_spider.py -o movies.json
        df = pd.read_json(self.movies_file, lines=True)

        # Could be necessary execute more than one time to get all records
        # This happens because Mojo Box Office blocks continuous access
        # The following code prevents to get just the not loaded movies
        if os.path.isfile(self.moviesfinance_file):
            df_moviesfinance = pd.read_json(self.moviesfinance_file, lines=True)
            not_loaded_realeases_ids = ~df['release_id'].isin(df_moviesfinance['release_id'].values)
            df = df[not_loaded_realeases_ids]

        return (url_base + df['url']).to_list()

    def parse(self, response, **kwargs):

        DISTRIBUTOR_INDEX = 1
        OPENING_INDEX = 3
        BUGET_INDEX = 5
        RELEASE_INDEX = 7
        MPAA_INDEX = 9
        RUNNING_TIME_INDEX = 11
        GENRES_INDEX = 13
        IN_RELEASE_INDEX = 15
        WIDEST_INDEX = 17

        release_id = re.search(r"rl\d+", response.url)[0]

        summary = response.xpath("//*[@class='a-section a-spacing-none mojo-summary-values mojo-hidden-from-mobile']/div/span")
        distribuitor = summary[DISTRIBUTOR_INDEX].xpath("./text()").get()
        opening = summary[OPENING_INDEX]
        opening_theaters = opening.xpath("./text()").get()
        opening_money = opening.xpath("./span/text()").get()
        buget = summary[BUGET_INDEX].xpath("./span/text()").get()
        release = summary[RELEASE_INDEX]
        release_start = release.xpath("./a/text()")[0].get()
        release_end = release.xpath("./a/text()")[1].get()
        mpaa = summary[MPAA_INDEX].xpath("./text()").get()
        running_time = summary[RUNNING_TIME_INDEX].xpath("./text()").get()
        genres = summary[GENRES_INDEX].xpath("./text()").get()
        in_release = summary[IN_RELEASE_INDEX].xpath("./text()").get()
        widest_release = summary[WIDEST_INDEX].xpath("./text()").get()

        yield {
            'distributor': distribuitor,
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



