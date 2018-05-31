import aiosqlite
from datetime import datetime

async def insertCmd(userid, command):
    async with aiosqlite.connect("Commands.db") as db:
        timestamp = str(datetime.now())
        await db.execute("INSERT INTO commands (userid, cmd, timestamp) VALUES (?,?,?)",(userid, command, timestamp))
        await db.commit()
        
async def getCmd():
    async with aiosqlite.connect("Commands.db") as db:
        cursor = await db.execute("SELECT * FROM commands ORDER BY timestamp ASC LIMIT 1")
        data = await cursor.fetchone()
        await cursor.close()
        if data is None:
            return False, "0", "0", "0"
        else:
            userid = data[0]
            command = data[1]
            timestamp = data[2]
            return True, userid, command, timestamp
            
async def delCmd(userid, command, timestamp):
    datetime_object = datetime.strptime(str(timestamp)[0:19], '%Y-%m-%d %H:%M:%S')
    async with aiosqlite.connect("Commands.db") as db:
        await db.execute("delete from commands where userid=? and cmd=? and timestamp=? ", (userid,command,timestamp))
        await db.commit()
        
def getHelp(userid):
    msgcolor = 8311585 #Green
    msgname = "系統訊息"
    msgdisc = "<@" + userid + "> 安安喵，\n"
    msgdisc = msgdisc + "歡迎使用喵公爵虛擬交易所，這裡顯示所有的功能\n\n"
    msgdisc = msgdisc + "`b!help` :這個指令會顯示這則訊息\n"
    msgdisc = msgdisc + "`b!gdpr` :個資相關說明\n"
    msgdisc = msgdisc + "`b!signup` :註冊帳號、初始 10000¢\n"
    msgdisc = msgdisc + "`b!delete_account` :清空帳號\n"
    msgdisc = msgdisc + "`b!daily` :每日簽到 +1500¢ 及帳戶資訊 \n"
    msgdisc = msgdisc + "`b!tran @使用者 [金額]` :轉帳給其他使用者\n"
    msgdisc = msgdisc + "`b!buy [商品代號] [單位價格] [數量]` :委託買進商品\n"
    msgdisc = msgdisc + "`b!buy 0050.tw 80.75 10`\n"
    msgdisc = msgdisc + "`b!sell [商品代號] [單位價格] [數量]` :委託賣出商品\n"
    msgdisc = msgdisc + "`b!sell 0050.tw 80.75 10`\n"
    msgdisc = msgdisc + "`b!inv`: 查看庫存\n"
    msgdisc = msgdisc + "\n如果有疑問請私訊 Herzogmeow\n\n"
    return msgdisc, msgcolor, msgname
    
def getGDPR(userid):
    msgcolor = 4886754 #Blue
    msgname = "系統訊息"
    msgdisc = "<@" + userid + "> 安安喵，\n"
    msgdisc = msgdisc + "網路系統因安全需要會記錄基本的來往訊息\n\n"
    msgdisc = msgdisc + "請確認同意我們收集資料再建帳號\n"
    msgdisc = msgdisc + "\n如果有疑問請私訊 Herzogmeow"
    return msgdisc, msgcolor, msgname
    
async def insertUser(userid):
    async with aiosqlite.connect("Users.db") as db:
        timestamp = str(datetime.now())
        gdpr = "signup "+str(datetime.now())
        check = datetime.now().strftime("%Y-%m-%d")
        await db.execute("INSERT INTO account (userid, balance, gdpr, checkin) VALUES (?,?,?,?)",(userid, 10000, gdpr,check))
        await db.commit()
        return True
        
async def getUser(userid):
    async with aiosqlite.connect("Users.db") as db:
        cursor = await db.execute("SELECT * FROM account WHERE userid=?", (userid,))
        data = await cursor.fetchone()
        await cursor.close()
        if data is None:
            return False, "0", "0", "0", "0"
        else:
            userid = data[0]
            balance = data[1]
            checkin = data[2]
            gdpr = data[3]
            return True, userid, balance, checkin, gdpr
    
def accMsg(userid, balance, checkin, gdpr):
    msgcolor = 8311585 #Green
    msgname = "個人資訊"
    msgdisc = "<@" + userid + "> 安安喵，\n"
    msgdisc = msgdisc + "\n\n"
    msgdisc = msgdisc + "`你目前帳戶餘額: " + str(balance) + "¢\n"
    msgdisc = msgdisc + "上次簽到時間: " + str(checkin)
    return msgdisc, msgcolor, msgname
    
async def getSignup(userid):
    msgcolor = 8311585 #Green
    msgname = "系統訊息"
    ux, guserid, balance, checkin, gdpr = await getUser(userid)
    if guserid == "0":
         op = await insertUser(userid)
         if op:
            msgdisc = "<@" + userid + "> 註冊成功\n"
            return msgdisc, msgcolor, msgname
    return "0", msgcolor, msgname
    
async def delUser(userid):
    msgcolor = 13632027
    msgname = "系統訊息"
    msgdisc = "<@" + userid + "> 刪除帳號"
    async with aiosqlite.connect("Users.db") as db:
        await db.execute("delete from account where userid=?", (userid,))
        await db.commit()
    return msgdisc, msgcolor, msgname

async def updateUser(userid, balance, gdpr, checkin):
    async with aiosqlite.connect("Users.db") as db:
        await db.execute("UPDATE account SET balance=?, gdpr=?, checkin=? WHERE userid=?",(balance,gdpr,checkin,userid))
        await db.commit()
        return True
    
async def dailyUser(userid):
    ux, guserid, balance, checkin, gdpr = await getUser(userid)
    msgcolor = 8311585
    msgname = "個人資訊"
    if guserid != "0":
        today = datetime.now().strftime("%Y-%m-%d")
        if checkin != today:
            balance = float(balance) + 1500
            update = await updateUser(userid, str(balance), gdpr, today)
        msgdisc = "<@" + userid + "> 帳戶資訊:\n"
        msgdisc = msgdisc + "\n"
        msgdisc = msgdisc + "金額: " + str(balance) + "¢\n"
        msgdisc = msgdisc + "上次簽到: " + str(checkin) + "\n"
        msgdisc = msgdisc + "註冊時間: " + str(gdpr) + "\n"
        return msgdisc, msgcolor, msgname
    return "0", msgcolor, msgname
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False  
    
async def tranAmt(giver, msgtitleA):
    receiver = msgtitleA[1][2:-1]
    amount = msgtitleA[2]
    if is_number(amount):
        Gux, Guserid, Gbalance, Gcheckin, Ggdpr = await getUser(giver)
        Rux, Ruserid, Rbalance, Rcheckin, Rgdpr = await getUser(receiver)
        if (Guserid != "0") & (Ruserid != "0"):
            Gbalance = float(Gbalance) - float(amount)
            Gupdate = await updateUser(Guserid, str(Gbalance), Ggdpr, Gcheckin)
            Rbalance = float(Rbalance) + float(amount)
            Rupdate = await updateUser(Ruserid, str(Rbalance), Rgdpr, Rcheckin)
            return Guserid, str(Gbalance), Ggdpr, Gcheckin, Ruserid, str(Rbalance), Rgdpr, Rcheckin
    return "0", "0", "0", "0", "0", "0", "0", "0"
    
def getAlphaNum():
    import random, string
    x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
    return x
    
async def getNearOrder(bors, symbol):
    async with aiosqlite.connect("Order.db") as db:
        if bors == "buy":
            cursor = await db.execute("SELECT * FROM orders WHERE bors=? AND symbol=? ORDER BY price DESC", (bors,symbol))
        elif bors == "sell":
            cursor = await db.execute("SELECT * FROM orders WHERE bors=? AND symbol=? ORDER BY price ASC", (bors,symbol))
        data = await cursor.fetchone()
        await cursor.close()
        if data is None:
            return False, "0", "0", "0", "0", "0", "0", "0"
        else:
            orderid = data[0]
            symbol  = data[1]
            buyer   = data[2]
            bors    = data[3]
            price   = data[4]
            qty     = data[5]
            timestamp  = data[6]
            return True, orderid, symbol, buyer, bors, price, qty, timestamp

async def updateOrder(orderid, symbol, buyer, bors, price, qty, timestamp):
    async with aiosqlite.connect("Order.db") as db:
        await db.execute("UPDATE orders SET symbol=?, buyer=?, bors=?, price=?, qty=?, timestamp=? WHERE orderid=?",(symbol, buyer, bors, price, qty, timestamp, orderid))
        await db.commit()

async def delOrder(orderid):
    async with aiosqlite.connect("Order.db") as db:
        await db.execute("delete from orders where orderid=?", (orderid,))
        await db.commit()

async def chkInv(userid, symbol):
    async with aiosqlite.connect("Inventory.db") as db:
        cursor = await db.execute("SELECT * FROM inventory WHERE userid=? AND symbol=?", (userid, symbol))
        data = await cursor.fetchone()
        await cursor.close()
        if data is None:
            return False, "0", "0", "0", "0"
        else:
            symbol = data[0]
            qty = data[1]
            userid = data[2]
            date = data[3]
            return True, symbol, qty, userid, date
            
async def updateInv(symbol, qty, userid, date):
    async with aiosqlite.connect("Inventory.db") as db:
        await db.execute("UPDATE inventory SET qty=?, date=? WHERE symbol=? AND userid=?",(qty, date, symbol, userid))
        await db.commit()

async def insertInv(symbol, qty, userid):
    async with aiosqlite.connect("Inventory.db") as db:
        date = datetime.now().strftime("%Y-%m-%d")
        await db.execute("INSERT INTO inventory (symbol, qty, userid, date) VALUES (?,?,?,?)",(symbol, qty, userid, date))
        await db.commit()

async def exchange(qty, buyerData, sellerData):
    Box, Borderid, Bsymbol, Bbuyer, Bbors, Bprice, Bqty, Btimestamp, Bux, Buserid, Bbalance, Bcheckin, Bgdpr = buyerData
    Sox, Sorderid, Ssymbol, Sseller, Sbors, Sprice, Sqty, Stimestamp, Sux, Suserid, Sbalance, Scheckin, Sgdpr = sellerData
    Bbalance = Bbalance - (Sqty*Sprice)
    Bupdate = await updateUser(Buserid, Bbalance, Bgdpr, Bcheckin)
    Sbalance = Sbalance + (Sqty*Sprice)
    Supdate = await updateUser(Suserid, Sbalance, Sgdpr, Scheckin)
    
    Bix, BsymbolI, BqtyI, BuseridI, BdateI = await chkInv(Bbuyer, Bsymbol)
    Six, SsymbolI, SqtyI, SuseridI, SdateI = await chkInv(Sseller, Ssymbol)
    if Bix:
        BqtyI = float(BqtyI) + float(qty)
        await updateInv(BsymbolI, str(BqtyI), BuseridI, BdateI)
    else:
        await insertInv(Bsymbol, qty, Buserid)
    if Bix:
        SqtyI = float(SqtyI) - float(qty)
        await updateInv(SsymbolI, str(SqtyI), SuseridI, SdateI)
    else:
        qty = 0 - qty
        await insertInv(Ssymbol, qty, Suserid)

async def delOrderByUser(userid):
    async with aiosqlite.connect("Order.db") as db:
        await db.execute("delete from orders where userid=?", (userid,))
        await db.commit()

async def insertRec(symbol, price, qty, buyer, seller):
    async with aiosqlite.connect("Record.db") as db:
        timestamp = str(datetime.now())
        await db.execute("INSERT INTO record (symbol, price, qty, timestamp, buyer, seller) VALUES (?,?,?,?,?,?)",(symbol, price, qty, timestamp, buyer, seller))
        await db.commit()
            
async def matchOrder(symbol):
    Box, Borderid, Bsymbol, Bbuyer, Bbors, Bprice, Bqty, Btimestamp = await getNearOrder("buy", symbol)
    Sox, Sorderid, Ssymbol, Sseller, Sbors, Sprice, Sqty, Stimestamp = await getNearOrder("sell", symbol)
    if float(Bprice) >= float(Sprice):
        Bux, Buserid, Bbalance, Bcheckin, Bgdpr = await getUser(Bbuyer)
        Sux, Suserid, Sbalance, Scheckin, Sgdpr = await getUser(Sseller)
        if Bux & Sux:
            if Bqty == Sqty:
                buyerData = (Box, Borderid, Bsymbol, Bbuyer, Bbors, Bprice, Bqty, Btimestamp, Bux, Buserid, Bbalance, Bcheckin, Bgdpr)
                sellerData = (Sox, Sorderid, Ssymbol, Sseller, Sbors, Sprice, Sqty, Stimestamp, Sux, Suserid, Sbalance, Scheckin, Sgdpr)
                await delOrder(Borderid)
                await delOrder(Sorderid)
                await exchange(Bqty, buyerData, sellerData)
                await insertRec(Bsymbol, Sprice, Bqty, Bbuyer, Sseller)
            elif Bqty >= Sqty:
                Bqty = float(Bqty) - float(Sqty)
                await updateOrder(Borderid, Bsymbol, Bbuyer, Bbors, Bprice, str(Bqty), Btimestamp)
                await delOrder(Sorderid)
                await exchange(Bqty, buyerData, sellerData)
                await insertRec(Bsymbol, Sprice, Bqty, Bbuyer, Sseller)
            elif Bqty <= Sqty:    
                Sqty = float(Sqty) - float(Bqty)
                await updateOrder(Sorderid, Ssymbol, Sseller, Sbors, Sprice, str(Sqty), Stimestamp)
                await delOrder(Borderid)
                await exchange(Sqty, buyerData, sellerData)
                await insertRec(Bsymbol, Sprice, Sqty, Bbuyer, Sseller)
        elif not Bux:
            await delOrderByUser(Bbuyer)
        elif not Sux:
            await delOrderByUser(Sseller)
        return True
    else:
        return False
    
async def addOrder(userid, msgtitleA):
    match = True
    timestamp = str(datetime.now())
    orderid = getAlphaNum()
    bs = ['buy','sell']
    symbol = msgtitleA[1]
    if is_number(msgtitleA[2]) & is_number(msgtitleA[3]) & (str(msgtitleA[0]) in bs):
        price = float(msgtitleA[2])
        qty = float(msgtitleA[3])
        bors = msgtitleA[0]
        async with aiosqlite.connect("Order.db") as db:
            await db.execute("INSERT INTO orders (orderid, symbol, userid, bors, price, qty, timestamp) VALUES (?,?,?,?,?,?,?)",(orderid, symbol, userid, bors, price, qty, timestamp))
            await db.commit()
            if match:
                match = await matchOrder(symbol)
            return True, orderid
    else:
        return False, orderid
        
async def selfOrder(userid):
    async with aiosqlite.connect("Order.db") as db:
        orderid = []
        symbol = []
        bors = []
        price = []
        qty = []
        timestamp = []
        cursor = await db.execute("SELECT * FROM orders WHERE userid=?", (userid,))
        datas = await cursor.fetchall()
        await cursor.close()
        if datas is None:
            return False, "0", "0", "0", "0", "0", "0"
        else:
            datar = [list(elem) for elem in datas]
            for data in datar:
                orderid.append(str(data[0]))
                symbol.append(str(data[1]))
                bors.append(str(data[3]))
                price.append(str(data[4]))
                qty.append(str(data[5]))
                timestamp.append(str(data[6]))
            return True, orderid, symbol, bors, price, qty, timestamp
            
async def selfInv(userid):
    async with aiosqlite.connect("Inventory.db") as db:
        symbol = []
        qty = []
        date = []
        cursor = await db.execute("SELECT * FROM inventory WHERE userid=?", (userid,))
        datas = await cursor.fetchall()
        await cursor.close()
        if datas is None:
            return False, "0", "0", "0"
        else:
            datar = [list(elem) for elem in datas]
            for data in datar:
                symbol.append(str(data[0]))
                qty.append(str(data[1]))
                date.append(str(data[3]))
            return True, symbol, qty, date