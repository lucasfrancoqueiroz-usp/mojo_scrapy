from subprocess import check_output, STDOUT
movies_json = 'movies.jl'
cmd = f"scrapy runspider movies_spider.py -o {movies_json}"
check_output(cmd, stderr=STDOUT, shell=True, universal_newlines=True)
