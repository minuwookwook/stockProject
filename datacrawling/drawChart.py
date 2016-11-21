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

    def drawGraph(self):
        plt.plot(self.list1, self.list2)
        plt.show()

    def drawGraph2(self):
        top_axes = plt.subplot2grid((6, 6), (0, 0), rowspan=2, colspan=6)
        top_axes.set_title("KOSPI")
        top_axes.plot(self.list1, self.list2)
        mid_axes = plt.subplot2grid((6, 6), (2, 0), rowspan=2, colspan=6)
        mid_axes.set_title("KOSDAQ")
        mid_axes.plot(self.list3, self.list4)
        bot_axes = plt.subplot2grid((6, 6), (4, 0), rowspan=2, colspan=6)
        bot_axes.set_title("KOSPI200")
        bot_axes.plot(self.list5, self.list6)

        plt.tight_layout()
        plt.show()
