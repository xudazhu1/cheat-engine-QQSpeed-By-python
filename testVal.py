import psutil

for proc in psutil.process_iter():
    try:
        proc
        p_info = proc.as_dict(attrs=['pid', 'name'])
    except psutil.NoSuchProcess:
        pass
    else:
        print(p_info)
