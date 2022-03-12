import scrapy
import re
import logging
import pandas as pd

# scrapy runspider movies_day_list_spider.py -o movies.json
class MovieListSpider(scrapy.Spider):
    '''
    Extracts all movies per day
    '''

    name = 'movielistspider'

    days = pd.date_range(start="2004-01-01",end="2019-12-31").astype(str).tolist()

    def _get_loaded_days(self):
        df = pd.read_json('movies.jl', lines=True)
        if not df.empty:
            days_loaded = df['day'].drop_duplicates().values.tolist()
            return days_loaded
        return []

    def _get_not_loaded_days(self):
        days_loaded = self._get_loaded_days()
        return [day for day in self.days if day not in days_loaded]

    def start_requests(self):
        days = self._get_not_loaded_days()
        for day in days:
            url = f"https://www.boxofficemojo.com/date/{day}/"
            yield scrapy.Request(url, meta={'day': day}, callback=self.parse)

    def parse(self, response):

        day = response.meta.get('day')

        RANK_INDEX = 0
        RELEASE_INDEX = 2
        DAILY_GROSS_INDEX = 3
        GROSS_INDEX = 5 # Gross in the month
        THEATERS_INDEX = 6
        PER_TH_AVG_GROSS = 7
        GROSS_TO_DAY = 8
        RELEASE_DAYS = 9
        DISTRIBUTOR_INDEX = 10

        trs = response.xpath("//*[@id='table']/div/table/tr[position()>1]")
        for tr in trs:
            tds = tr.xpath("td")

            rank = tds[RANK_INDEX].xpath("descendant-or-self::*/text()").extract_first()
            daily_gross = tds[DAILY_GROSS_INDEX].xpath("descendant-or-self::*/text()").extract_first()
            release = tds[RELEASE_INDEX].xpath("descendant-or-self::*/text()").extract_first()
            url = tds[RELEASE_INDEX].xpath("descendant-or-self::*/a/@href").extract_first()
            release_id = re.search(r"rl\d+", url)[0]
            gross = tds[GROSS_INDEX].xpath("descendant-or-self::*/text()").extract_first()
            theaters = tds[THEATERS_INDEX].xpath("descendant-or-self::*/text()").extract_first()
            per_th_avg_gross = tds[PER_TH_AVG_GROSS].xpath("descendant-or-self::*/text()").extract_first()
            gross_to_day = tds[GROSS_TO_DAY].xpath("descendant-or-self::*/text()").extract_first()
            release_days = tds[RELEASE_DAYS].xpath("descendant-or-self::*/text()").extract_first()
            distributor = tds[DISTRIBUTOR_INDEX].xpath("descendant-or-self::*/text()").extract_first()

            yield {
                "rank": rank,
                "release": release,
                "url": url,
                "release_id": release_id,
                "daily_gross": daily_gross,
                "gross": gross,
                "th": theaters,
                "per_th_avg_gross": per_th_avg_gross,
                "gross_to_day": gross_to_day,
                "release_days": release_days,
                "distributor": distributor,
                "day": day
            }
