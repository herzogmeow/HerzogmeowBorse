import time
from cmd import *
from acc import *
from chk import *

functions = {
    'help': HELP,
    'signup': SIGNUP,
    'delete_account': DELETE_ACCOUNT,
    'daily': DAILY,
    'tran': TRAN,
    'order': ORDER,
    'buy': BORS,
    'sell': BORS,
    'inv': INV,
    'gdpr': GDPR,
}

def call(a, var):
    return functions[a](var)

async def reply():
    ack, userid, command, timestamp = await getCmd()
    if ack:
        await delCmd(userid, command, timestamp)
        msgtitle = str(command).lower()
        msgtime = Str2Datetime(timestamp)
        msgtitleA = msgtitle.split(" ")
        msgtitleA = list(filter(None, msgtitleA)) #清除空格
        msgtitle = str(msgtitleA[0])
        
        var = (userid, msgtitleA, msgtime)
        msgtitle, msgdisc, msgcolor, msgname, msgtime = await call(msgtitle, var)
        return msgtitle, msgdisc, msgcolor, msgname, msgtime
    return "0", "0", 13632027, "0", "0"
    