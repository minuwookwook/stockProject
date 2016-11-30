from matplotlib import pyplot as plt

class Graph:
    indexlist = []
    datalist = []

    def __init__(self, list1 = None, list2 = None, list3 = None, list4 = None, list5 = None, list6 = None):
        self.list1 = list1
        self.list2 = list2
        self.list3 = list3
        self.list4 = list4
        self.list5 = list5
        self.list6 = list6

    def drawGraph(self, stockName):
        top_axes = plt.subplot2grid((6, 6), (0, 0), rowspan=4, colspan=6)
        top_axes.set_title(stockName + " : " + str(self.list2[len(self.list2)-1]))
        top_axes.ticklabel_format(useOffset=False)
        top_axes.plot(self.list1, self.list2)
        plt.xlabel('Time')
        plt.ylabel('Excuted Price')
        mid_axes = plt.subplot2grid((6, 6), (4, 0), rowspan=2, colspan=6)
        mid_axes.set_title("Volume")
        plt.xlabel('Time')
        mid_axes.bar(self.list1, self.list3, width =0.05)
        plt.tight_layout()
        plt.show()

    def drawGraph2(self):
        top_axes = plt.subplot2grid((6, 6), (0, 0), rowspan=2, colspan=6)
        top_axes.set_title("KOSPI" + " : " + str(self.list2[len(self.list2)-1]))
        top_axes.ticklabel_format(useOffset=False)
        top_axes.plot(self.list1, self.list2)
        plt.xlabel('Time')
        plt.ylabel('Excuted Price')
        mid_axes = plt.subplot2grid((6, 6), (2, 0), rowspan=2, colspan=6)
        mid_axes.set_title("KOSDAQ" + " : " + str(self.list4[len(self.list4)-1]))
        plt.xlabel('Time')
        plt.ylabel('Excuted Price')
        mid_axes.plot(self.list3, self.list4)
        bot_axes = plt.subplot2grid((6, 6), (4, 0), rowspan=2, colspan=6)
        bot_axes.set_title("KOSPI200" + " : " + str(self.list6[len(self.list6)-1]))
        bot_axes.plot(self.list5, self.list6)
        plt.xlabel('Time')
        plt.ylabel('Excuted Price')
        plt.tight_layout()
        plt.show()
