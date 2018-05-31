from chk import *
from cmd import *

async def HELP(var):
    userid, msgtitleA, msgtime = var
    msgtitle = str(msgtitleA[0])
    msgdisc, msgcolor, msgname = getHelp(userid)
    return msgtitle, msgdisc, msgcolor, msgname, msgtime
    
async def SIGNUP(var):
    userid, msgtitleA, msgtime = var
    msgtitle = str(msgtitleA[0])
    msgdisc, msgcolor, msgname = await getSignup(userid)
    if msgdisc != "0":
        return msgtitle, msgdisc, msgcolor, msgname, msgtime
    return "0", "0", 13632027, "0", "0"
    
async def DELETE_ACCOUNT(var):
    userid, msgtitleA, msgtime = var
    msgtitle = str(msgtitleA[0])
    msgdisc, msgcolor, msgname = await delUser(userid)
    return msgtitle, msgdisc, msgcolor, msgname, msgtime
    
async def DAILY(var):
    userid, msgtitleA, msgtime = var
    msgtitle = str(msgtitleA[0])
    msgdisc, msgcolor, msgname = await dailyUser(userid)
    if msgdisc != "0":
        return msgtitle, msgdisc, msgcolor, msgname, msgtime
    return "0", "0", 13632027, "0", "0"
    
async def TRAN(var):
    userid, msgtitleA, msgtime = var
    msgtitle = str(msgtitleA[0])
    msgcolor = 16312092
    msgname = "轉帳訊息"
    if len(msgtitleA) == 3:
        Guserid, Gbalance, Ggdpr, Gcheckin, Ruserid, Rbalance, Rgdpr, Rcheckin = await tranAmt(userid, msgtitleA)
        if Guserid != "0":
            msgdisc = "<@" + Guserid + "> 帳戶資訊:\n"
            msgdisc = msgdisc + "金額: " + str(Gbalance) + "¢\n"
            msgdisc = msgdisc + "\n"
            msgdisc = msgdisc + "<@" + Ruserid + "> 帳戶資訊:\n"
            msgdisc = msgdisc + "金額: " + str(Rbalance) + "¢\n"
            return msgtitle, msgdisc, msgcolor, msgname, msgtime
    return "0", "0", 13632027, "0", "0"
    
async def ORDER(var):
    userid, msgtitleA, msgtime = var
    msgtitle = str(msgtitleA[0])
    msgcolor = 9131818
    msgname = "交易所訊息"
    ox, orderid, symbol, bors, price, qty, timestamp = await selfOrder(str(userid))
    if ox:
        msgdisc = "<@" + userid + "> \n\n商品代號 , 買/賣 , 單價 , 數量 ,                時間                ,                委託編號                \n"
        for ind, item in enumerate(orderid):
            msgdisc = msgdisc +str(symbol[ind])+" , "+str(bors[ind])+"  ,  "+str(price[ind])+" , "+str(qty[ind])+" , "+str(timestamp[ind])+" , "+str(orderid[ind])+"\n"
        return msgtitle, msgdisc, msgcolor, msgname, msgtime
    return "0", "0", 13632027, "0", "0"
    
async def INV(var):
    userid, msgtitleA, msgtime = var
    msgtitle = str(msgtitleA[0])
    msgcolor = 9131818
    msgname = "交易所訊息"
    si, symbol, qty, date = await selfInv(str(userid))
    if si:
        msgdisc = "<@" + userid + "> \n\n商品代號 , 數量 , 日期\n"
        for ind, item in enumerate(symbol):
            msgdisc = msgdisc +str(symbol[ind])+" , "+str(qty[ind])+"  ,  "+str(date[ind])
        return msgtitle, msgdisc, msgcolor, msgname, msgtime
    return "0", "0", 13632027, "0", "0"
    
async def BORS(var):
    userid, msgtitleA, msgtime = var
    msgtitle = str(msgtitleA[0])
    msgcolor = 16777215
    msgname = "交易所訊息"
    if len(msgtitleA) == 4:
        ordSucc, orderid = await addOrder(userid, msgtitleA)
        msgdisc = "<@" + userid + "> \n委託編號:\n"
        msgdisc = msgdisc + orderid
        return msgtitle, msgdisc, msgcolor, msgname, msgtime
    
async def GDPR(var):
    userid, msgtitleA, msgtime = var
    msgtitle = str(msgtitleA[0])
    msgdisc, msgcolor, msgname = getGDPR(userid)
    return msgtitle, msgdisc, msgcolor, msgname, msgtime