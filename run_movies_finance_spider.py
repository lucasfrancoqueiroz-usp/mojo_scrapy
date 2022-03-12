from subprocess import check_output, STDOUT
movies_finance_json = 'movies_finance.jl'
movies_finance_log = 'movies_finance.log'
cmd = f"scrapy runspider movies_finance_spider.py -o {movies_finance_json} --logfile {movies_finance_log}"
check_output(cmd, stderr=STDOUT, shell=True, universal_newlines=True)