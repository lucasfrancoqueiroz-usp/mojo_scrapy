import scrapy
import re
import pandas as pd
import os
import logging

# scrapy runspider movies_finance_spider.py -o moviesfinance.jl
class MovieFinanceSpider(scrapy.Spider):
    name = "moviefinance"

    def __init__(self):
        self.start_urls = self.__get_movies_url()

    def __get_movies_url(self):
        url_base = "https://www.boxofficemojo.com/"

        # movies.jl is generating running movies_list_spider
        # scrapy runspider movies_list_spider.py -o movies.json
        df = pd.read_json('movies.jl', lines=True)

        # Could be necessary execute more than one time to get all records
        # This happens because Mojo Box Office blocks continuous access
        # The following code prevents to get just the not loaded movies
        if os.path.isfile("moviesfinance.jl"):
            df_moviesfinance = pd.read_json('moviesfinance.jl', lines=True)
            not_loaded_realeases_ids = ~df['release_id'].isin(df_moviesfinance['release_id'].values)
            df = df[not_loaded_realeases_ids]

        return (url_base + df['url']).to_list()

    def parse(self, response, **kwargs):
        MONTH_DAY_INDEX = 0
        DAY_OF_WEEK_INDEX = 1
        CONCURRANCY_RANK_INDEX = 2
        DAILY_GROSS_INDEX = 3
        PERCENT_GROSS_CHANGE_PER_DAY_INDEX = 4
        PERCENT_GROSS_CHANGE_PER_WEEK_INDEX = 5
        NUMBER_OF_THEATERS_INDEX = 6
        PER_THEATER_AVERAGE_GROSS_INDEX = 7
        GROSS_UNTIL_CURRENT_DAY_INDEX = 8
        ORDINAL_DAY_INDEX = 9

        trs = response.xpath("//*[@id='table']/div/table/tr[position()>1]")
        release_id = re.search(r"rl\d+", response.url)[0]
        for tr in trs:
            tds = tr.xpath("td")

            month_day = tds[MONTH_DAY_INDEX].xpath("descendant-or-self::*/text()").extract_first()
            day_of_week = tds[DAY_OF_WEEK_INDEX].xpath("descendant-or-self::*/text()").extract_first()
            concurrancy_rank = tds[CONCURRANCY_RANK_INDEX].xpath("descendant-or-self::*/text()").extract_first()
            daily_gross = tds[DAILY_GROSS_INDEX].xpath("descendant-or-self::*/text()").extract_first()
            percent_gross_change_per_day = tds[PERCENT_GROSS_CHANGE_PER_DAY_INDEX].xpath(
                "descendant-or-self::*/text()").extract_first()
            percent_gross_change_per_week = tds[PERCENT_GROSS_CHANGE_PER_WEEK_INDEX].xpath(
                "descendant-or-self::*/text()").extract_first()
            number_of_theaters = tds[NUMBER_OF_THEATERS_INDEX].xpath("descendant-or-self::*/text()").extract_first()
            per_theater_average_gross = tds[PER_THEATER_AVERAGE_GROSS_INDEX].xpath(
                "descendant-or-self::*/text()").extract_first()
            gross_until_current_day = tds[GROSS_UNTIL_CURRENT_DAY_INDEX].xpath(
                "descendant-or-self::*/text()").extract_first()
            ordinal_day = tds[ORDINAL_DAY_INDEX].xpath("descendant-or-self::*/text()").extract_first()

            yield {
                "month_day": month_day,
                "day_of_week": day_of_week,
                "concurrancy_rank": concurrancy_rank,
                "daily_gross": daily_gross,
                "percent_gross_change_per_day": percent_gross_change_per_day,
                "percent_gross_change_per_week": percent_gross_change_per_week,
                "number_of_theaters": number_of_theaters,
                "per_theater_average_gross": per_theater_average_gross,
                "gross_until_current_day": gross_until_current_day,
                "ordinal_day": ordinal_day,
                "release_id": release_id
            }
