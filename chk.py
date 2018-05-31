from datetime import datetime

def Str2Datetime(timestamp):
    msgtime = datetime.strptime(timestamp[0:19], '%Y-%m-%d %H:%M:%S')
    return msgtime