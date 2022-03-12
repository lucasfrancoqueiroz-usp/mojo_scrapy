## Execution order

###1- Step
Run `python run_movies_spider.py` OR `scrapy runspider movies_spider.py -o movies.jl` they do the same thing.

Check if there are 35787 in `movies.jl`, if not try to execute again.

This execution will extract all movies per month

###2- Step
Run `python movies_filter.py`

This execution will filter spurious records, not wide releases and duplications.
At the end will be created a `movies_wide.jl` file.

###3- Step
Run `python run_movies_finance_spider.py` or `scrapy runspider movies_finance_spider.py -o movies_finance.jl --logfile movies_finance.log`

This execution will extract daily financial information from the movies and
create two files: `movies_finance.jl` and `movies_finance.log`

Look for `# movies to be scrapped` in the `movies_finance.log` file. If the
number aside is not zero repeat the execution until the last appearance has 
zero.

