import bs4
from urllib.request import urlopen
import datetime
import makeList as ml
import drawChart as dc

mainUrl = 'http://finance.naver.com/sise/sise_index_time.nhn?code='

class Data: # 종목 가져오기


    def __init__(self, rate):
        self.stockName = rate
        self.rateUrl = mainUrl + rate
        self.timeInfo = []
        self.price = []

    def setUrl(self):
        now = datetime.datetime.now()

        if now.hour < 9:
            now = now - datetime.timedelta(1)
            now = now.replace(hour=23)
        if now.weekday() == 5:
            now = now - datetime.timedelta(1)
            now = now.replace(hour=23)
        if now.weekday() == 6:
            now = now - datetime.timedelta(2)
            now = now.replace(hour=23)

        targetUrl = self.rateUrl + "&thistime=" + str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(
            now.minute) + str(now.second)
        return targetUrl

    def strToint(self, price):
        integer = ""
        for i in range(0,5):
            try:
                a = price.split(',')[i]
                integer = integer + price.split(',')[i]
            except IndexError:
                break
        return integer

    def getData(self):
        a = 0
        check = 0
        check2 = 0
        endPage = 0

        aimUrl = self.setUrl()
        html = urlopen(aimUrl).read()
        soup = bs4.BeautifulSoup(html, 'html.parser')
        for table in soup.find_all('table', 'Nnavi'):
            for num in table.find_all('td', 'pgRR'):
                page = num.find('a')
                endPage = page.get('href').split('page=')[1]
                endPage = int(endPage) - 1
                if endPage != 0:
                    break
            if endPage != 0:
                break
        while 1:
            a = a + 1
            aimUrl = self.setUrl() + '&page=' + str(a)
            stop = 1
            html = urlopen(aimUrl).read()
            soup = bs4.BeautifulSoup(html, 'html.parser')
            for j in soup.find_all('tr'):
                if len(j.find_all('td','date')) == 1:
                    for i in j.find_all('td', 'date'):
                        if i.text == '\xa0':
                            break

                        hour = self.strToint(i.text.split(':')[0])
                        minute = self.strToint(i.text.split(':')[1])
                        timeIndex = float(hour) + float(minute) / 60
                        self.timeInfo.append(timeIndex)

                    for i in j.find_all('td', 'number_1')[:1]:
                        if i.text == '\xa0':
                            stop=0
                            break
                        mainValue = self.strToint(i.text)
                        self.price.append(float(mainValue))

            if stop == 0:
                break
            elif a == endPage:
                break

    def getTimeList(self):
        return self.timeInfo

    def getPriceList(self):
        return self.price


kospi= Data("KOSPI")
kospi.getData()
priceList1 = kospi.getPriceList()
timeList1 = kospi.getTimeList()

kosdaq= Data("KOSDAQ")
kosdaq.getData()
priceList2 = kosdaq.getPriceList()
timeList2 = kosdaq.getTimeList()

kpi200= Data("KPI200")
kpi200.getData()
priceList3 = kpi200.getPriceList()
timeList3 = kpi200.getTimeList()

b1 = ml.IList(priceList1, timeList1)
nPriceList1 = b1.getPList()
nTimeList1 = b1.getTList()

b2 = ml.IList(priceList2, timeList2)
nPriceList2 = b2.getPList()
nTimeList2 = b2.getTList()

b3 = ml.IList(priceList3, timeList3)
nPriceList3 = b3.getPList()
nTimeList3 = b3.getTList()

c = dc.Graph(nTimeList1, nPriceList1, nTimeList2, nPriceList2, nTimeList3, nPriceList3)
c.drawGraph2()
