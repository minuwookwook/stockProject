import pandas_datareader.data as web
import pandas_datareader._utils
import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datacrawling

class Mock:
    def __init__(self,code):
        self.day_list = []
        self.name_list = []
        self.price_list = []
        self.price = []
        self.day = []
    def purchase(self):
        self.start = input("구입할 날짜를 입력하시오. (xxxx-xx-xx) : ")
        try:
            self.year = int(self.start.split('-')[0])
            self.month = int(self.start.split('-')[1])
            self.day = int(self.start.split('-')[2])
            self.start = datetime.datetime(self.year, self.month, self.day)
            self.end = self.start - datetime.timedelta(days=30)
            self.data = web.DataReader(code, "yahoo", self.end, self.start)
            self.connect()
        except IndexError :
            print("날짜를 다시 확인하세요")
            self.purchase()

        self.day_list = []
        self.name_list = []
        self.price_list = []
        self.sell()

    def sell(self):
        self.end = self.start
        self.start = input("판매할 날짜를 입력하시오. (xxxx-xx-xx) : ")
        self.year = int(self.start.split('-')[0])
        self.month = int(self.start.split('-')[1])
        self.day = int(self.start.split('-')[2])
        self.start = datetime.datetime(self.year, self.month, self.day)
        try:
            self.data = web.DataReader(code, "yahoo", self.end, self.start)
        except:
            print("날짜를 다시 확인하세요")
            return self.sell()

        self.predictPrice = input("예측되는 가격 : ")
        self.connect()
        self.difference()

    def difference(self):

        diff = int(self.price_list[len(self.price_list)-1]) - int(self.predictPrice)

        if(diff < 0):
            diff =  diff * -1

        print("결과 : ", diff,"만큼 차이가 납니다.")
    def makeGraph(self):
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111)
        count = 0
        for i, day in enumerate(self.data.index):
            self.price_list.append(self.data['Close'][count])
            count = count + 1
            self.day_list.append(i)
            self.name_list.append(day.strftime('%m-%d'))

        ax.xaxis.set_major_locator(ticker.FixedLocator(self.day_list))
        ax.xaxis.set_major_formatter(ticker.FixedFormatter(self.name_list))
        ax.plot(self.day_list, self.price_list, '-o', picker=5)

        return fig

    def onpick(self, event):
        thisline = event.artist
        xdata = thisline.get_xdata()
        ydata = thisline.get_ydata()
        ind = event.ind
        self.day.append(int(xdata[ind]))
        self.price.append(int(ydata[ind]))
        if len(self.price) > 0 and len(self.price) % 2 == 0:
            purchaseDay = self.day[len(self.price) - 2]
            sellDay = self.day[len(self.price) - 1]
            print("Purchase Day : ", self.name_list[purchaseDay])
            print("Sell Day : ", self.name_list[sellDay])
            rate = (self.price[len(self.price) - 1] - self.price[len(self.price) - 2]) / self.price[len(self.price) - 2] * 100
            print("수익률 : ", round(rate, 2), "%")

    def connect(self):
        fig = self.makeGraph()
        fig.canvas.mpl_connect('pick_event', self.onpick)
        plt.show()

if __name__ == '__main__':

    stockName = input("종목 이름 : ")
    data = datacrawling.Data(stockName)
    code = data.findStock()
    code = code.split("code=")[1]
    code = code + '.KS'
    a = Mock(code)
    a.purchase()

