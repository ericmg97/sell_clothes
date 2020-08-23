import time

def log(path, *args, **kwargs):
    date = time.asctime(time.localtime())
    logfile = open(path,"a")
    kwargs.update(dict(file=logfile))
    print(
        f"{date}",
        *args,
        **kwargs,
    )
    logfile.flush()
    logfile.close()

def create_path(name, venta):
    return f'./{name}_{venta}'
