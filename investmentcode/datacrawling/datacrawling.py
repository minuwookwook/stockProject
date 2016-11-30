import bs4
from urllib.request import urlopen
import datetime
import makeList as ml
import drawChart as dc

mainUrl = 'http://finance.naver.com/'
stockUrl1 = 'http://finance.naver.com/item/sise_time.nhn?'

class Data: # 종목 가져오기
    timeInfo = []
    price = []
    volumeList =[]

    def __init__(self, stockName = None):
        self.stockName = stockName
        if stockName == None:
            self.stockName = input("종목을 입력하세요 : ")
            self.getData()
        else:
            self.stockName = stockName

    def getStockName(self):
        return self.stockName

    def findStock(self):
        index = 'sise/entryJongmok.nhn'
        url = mainUrl + index
        code = 'Not'
        for a in range(1, 21):
            aimUrl = url + '?&page=' + str(a)
            html = urlopen(aimUrl).read()
            soup = bs4.BeautifulSoup(html, 'html.parser')
            for i in soup.find_all('td', 'ctg'):
                if i.text == self.stockName:
                    code = "code=" + i.a['href'].split("code=")[1]
                    break
            if code != 'Not':
                break

        stockUrl2 = stockUrl1 + code

        if code != 'Not':
            return stockUrl2
        else:
            print("No data. Check the Stock Name")
            self.stockName = input("주식 종목 : ")
            return self.findStock()


    def strToint(self, price):
        integer = ""
        for i in range(0,5):
            try:
                a = price.split(',')[i]
                integer = integer + price.split(',')[i]
            except IndexError:
                break
        return float(integer)


    def getData(self):

        now = datetime.datetime.now()

        if now.hour < 9 :
            now = now - datetime.timedelta(1)
            now = now.replace(hour=23)
        if now.weekday() == 5:
            now = now - datetime.timedelta(1)
            now = now.replace(hour=23)
        if now.weekday() == 6:
            now = now - datetime.timedelta(2)
            now = now.replace(hour=23)

        url = self.findStock() + "&thistime=" + str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second)

        print(url)
        a = 1
        check = 1
        check2 = 1
        while 1:
            aimUrl = url + '?&page=' + str(a)
            a = a+1
            html = urlopen(aimUrl).read()
            soup = bs4.BeautifulSoup(html, 'html.parser')
            for j in soup.find_all('tr'):
                partition = 1
                check2 = 1
                for i in j.find_all('span'):
                    if partition == 1:
                        if i.text == '09:00':
                            check = 0
                        hour = self.strToint(i.text.split(':')[0])
                        minute = self.strToint(i.text.split(':')[1])
                        timeIndex = float(hour) + float(minute)/60
                    elif partition == 2:
                        mainValue = self.strToint(i.text)

                    elif partition == 4:
                        sellPrice = self.strToint(i.text)

                    elif partition == 5:
                        buyPrice = self.strToint(i.text)

                    elif partition == 6:
                        volume = self.strToint(i.text)

                    elif partition == 7:
                        variation = self.strToint(i.text)

                    check2 = 0
                    partition = partition +1

                if check2 == 0:

                    self.timeInfo.append(timeIndex)
                    self.price.append(mainValue)
                    self.volumeList.append(volume)

            if check == 0:
                break



    def getTList(self):
        return self.timeInfo
    def getPList(self):
        return self.price
    def getVList(self):
        return self.volumeList


if __name__ == '__main__':

    a = Data()
    priceList = a.getPList()
    timeList = a.getTList()
    volumeList = a.getVList()

    b = ml.IList(priceList, timeList, volumeList)
    nPriceList = b.getPList()
    nTimeList = b.getTList()
    nVolumeList = b.getVList()

    c = dc.Graph(nTimeList, nPriceList, nVolumeList)
    c.drawGraph(a.getStockName())





