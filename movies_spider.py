import scrapy
import re
import pandas as pd

# scrapy runspider movies_month_list_spider.py -o movies.json
class MovieListSpider(scrapy.Spider):
    '''
    Extract movies per month
    '''

    name = 'movielistspider'
    movies_json = 'movies.jl'

    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
              'november', 'december']
    years = range(2004, 2020)

    def _get_loaded_months(self):
        df = pd.read_json(self.movies_json, lines=True)
        if not df.empty:
            yms_loaded = df[['year', 'month']].drop_duplicates().values.tolist()
            return yms_loaded
        return []

    def _get_not_loaded_months(self):
        yms = [[year, month] for year in self.years for month in self.months]
        yms_loaded = self._get_loaded_months()
        yms_not_loaded = []

        for ym in yms:
            found = False
            for ym_loaded in yms_loaded:
                if ym == ym_loaded:
                    found = True
                    break
            if not found:
                yms_not_loaded.append(ym)

        return yms_not_loaded

    def start_requests(self):
        ym = self._get_not_loaded_months()
        for year, month in ym:
            url = f"https://www.boxofficemojo.com/month/{month}/{year}/?grossesOption=calendarGrosses"
            yield scrapy.Request(url, meta={'month': month, 'year': year}, callback=self.parse)

    def parse(self, response):

        year = response.meta.get('year')
        month = response.meta.get('month')

        RANK_INDEX = 0
        RELEASE_INDEX = 1
        GROSS_INDEX = 5 # Gross in the month
        MAX_TH_INDEX = 6
        TOTAL_GROSS = 7 # full gross regardless month
        RELEASE_DATE = 8
        DISTRIBUTOR_INDEX = 9

        trs = response.xpath("//*[@id='table']/div/table/tr[position()>1]")
        for tr in trs:
            tds = tr.xpath("td")

            rank = tds[RANK_INDEX].xpath("descendant-or-self::*/text()").extract_first()
            release = tds[RELEASE_INDEX].xpath("descendant-or-self::*/text()").extract_first()
            url = tds[RELEASE_INDEX].xpath("descendant-or-self::*/a/@href").extract_first()
            release_id = re.search(r"rl\d+", url)[0]
            gross = tds[GROSS_INDEX].xpath("descendant-or-self::*/text()").extract_first()
            max_th = tds[MAX_TH_INDEX].xpath("descendant-or-self::*/text()").extract_first()
            total_gross = tds[TOTAL_GROSS].xpath("descendant-or-self::*/text()").extract_first()
            release_date = tds[RELEASE_DATE].xpath("descendant-or-self::*/text()").extract_first()
            distributor = tds[DISTRIBUTOR_INDEX].xpath("descendant-or-self::*/text()").extract_first()

            yield {
                "rank": rank,
                "release": release,
                "url": url,
                "release_id": release_id,
                "gross": gross,
                "max_th": max_th,
                "total_gross": total_gross,
                "release_date": release_date,
                "distributor": distributor,
                "month": month,
                "year": year
            }
