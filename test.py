def callback(**kwargs):
    print(kwargs['url'])

def caller(callback, **kwargs):
    callback(kwargs)

caller(lambda x:callback(url='tchau'))
#caller(callback)