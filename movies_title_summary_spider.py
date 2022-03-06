import scrapy

class MovieTitleSummarySpider(scrapy.Spider):
    name = "movietitlesummary"

    start_urls = [
        "https://www.boxofficemojo.com//release/rl2557314561/?ref_=bo_md_table_11"
    ]

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
            'widest_release': widest_release
        }



