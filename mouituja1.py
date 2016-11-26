import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

class AX:
    def __init__(self):
        self.now = datetime.datetime.now()
        self.start = self.now - datetime.timedelta(days=30)
        self.data = web.DataReader("005930.KS", "yahoo", self.start, self.now)
        self.day_list = []
        self.name_list = []
        self.price_list = []
        self.price = []
        self.day = []

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


a = AX()
a.connect()

