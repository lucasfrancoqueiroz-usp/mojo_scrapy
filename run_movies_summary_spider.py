from subprocess import check_output, STDOUT
movies_summary_json = 'movies_summary.jl'
movies_summary_log = 'movies_summary.log'
cmd = f"scrapy runspider movies_summary_spider.py -o {movies_summary_json} --logfile {movies_summary_log}"
check_output(cmd, stderr=STDOUT, shell=True, universal_newlines=True)
