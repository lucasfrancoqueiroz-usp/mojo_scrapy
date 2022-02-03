import scrapy
import pandas as pd
import os

# scrapy runspider mojo_spider.py -o movies.json
class MojoSpider(scrapy.Spider):
    name = 'mojo'

    def start_requests(self):
        movies = self.__get_movies()
        for movie in movies:
            url = self.__get_movieurlsearch(movie['name'])
            yield scrapy.Request(url=url, callback=self.parse, meta=movie)

    def __get_movies(self):
        '''
        Get movies from "MoviesNames_2004_2019_totalGrosses_wide" spreadsheet that haven't been loaded in movies.jl file
        :return: dict
        '''
        df_movies = pd.read_excel('MoviesNames_2004_2019_totalGrosses_wide_total.xlsx')

        if os.path.isfile('movies.jl'):
            df_moviesjl = pd.read_json('movies.jl', lines=True)
            if not df_moviesjl.empty:
                del df_moviesjl['number_results']
                df_movies = pd.concat([df_movies, df_moviesjl])
                df_movies.drop_duplicates(keep=False, inplace=True)

        return df_movies[['name','year']].to_dict(orient='records')

    def __get_movieurlsearch(self, movie_name):
        base_url = 'https://www.boxofficemojo.com/search/?q='
        return f'{base_url}{movie_name}'

    def parse(self, response):
        movie_name = response.meta.get('name')
        movie_year = response.meta.get('year')
        number_results = len(response.xpath(f"//*[@class='a-fixed-left-grid-inner'][div/a/text()='{movie_name}']"))

        yield {
            'name': movie_name,
            'year': movie_year,
            'number_results': number_results
        }