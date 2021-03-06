# DEPRECATED REASON
# Wide released extracted yearly is incomplete, mojo truncates information

import scrapy
import re
import logging

# scrapy runspider movies_year_list_spider.py -o movies.json
class MovieListSpider(scrapy.Spider):
    '''
    Extract JUST WIDE movies per year
    '''

    name = 'movielistspider'

    years = range(2004, 2020)

    start_urls = [
        f'https://www.boxofficemojo.com/year/{year}/?grossesOption=totalGrosses&releaseScale=wide' for year in years
    ]

    def parse(self, response):

        RANK_INDEX = 0
        RELEASE_INDEX = 1
        GROSS_INDEX = 5
        MAX_TH_INDEX = 6
        OPENING_INDEX = 7
        PERC_OF_TOTAL_INDEX = 8
        OPEN_TH_INDEX = 9
        OPEN_INDEX = 10
        CLOSE_INDEX = 11
        DISTRIBUTOR_INDEX = 12

        trs = response.xpath("//*[@id='table']/div/table/tr[position()>1]")
        for tr in trs:
            tds = tr.xpath("td")

            rank = tds[RANK_INDEX].xpath("descendant-or-self::*/text()").extract_first()
            release = tds[RELEASE_INDEX].xpath("descendant-or-self::*/text()").extract_first()
            url = tds[RELEASE_INDEX].xpath("descendant-or-self::*/a/@href").extract_first()
            release_id = re.search(r"rl\d+", url)[0]
            gross = tds[GROSS_INDEX].xpath("descendant-or-self::*/text()").extract_first()
            max_th = tds[MAX_TH_INDEX].xpath("descendant-or-self::*/text()").extract_first()
            opening = tds[OPENING_INDEX].xpath("descendant-or-self::*/text()").extract_first()
            perc_of_total = tds[PERC_OF_TOTAL_INDEX].xpath("descendant-or-self::*/text()").extract_first()
            open_th = tds[OPEN_TH_INDEX].xpath("descendant-or-self::*/text()").extract_first()
            open = tds[OPEN_INDEX].xpath("descendant-or-self::*/text()").extract_first()
            close = tds[CLOSE_INDEX].xpath("descendant-or-self::*/text()").extract_first()
            distributor = tds[DISTRIBUTOR_INDEX].xpath("descendant-or-self::*/text()").extract_first()

            yield {
                "rank": rank,
                "release": release,
                "url": url,
                "release_id": release_id,
                "gross": gross,
                "max_th": max_th,
                "opening": opening,
                "perc_of_total": perc_of_total,
                "open_th": open_th,
                "open": open,
                "close": close,
                "distributor": distributor
            }