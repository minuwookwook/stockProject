class IList:


    def __init__(self, list1 = None, list2 = None, list3 = None):
        self.list1 = list1
        self.list2 = list2
        self.list3 = list3
        self.priceList = []
        self.timeList = []
        self.vlist = []

    def setEnd(self, List):
        for a in range(0, 1000):
            try:
                if List[a]:
                    endPoint = a

            except IndexError:
                break


        return endPoint

    def setPList(self):
        for i in range(0, self.setEnd(self.list1)+1):
            self.priceList.append(self.list1[self.setEnd(self.list1)-i])

    def setTList(self):
        for i in range(0, self.setEnd(self.list2)+1):
            self.timeList.append(self.list2[self.setEnd(self.list2)-i])
    def setVList(self):
        for i in range(0, self.setEnd(self.list3)+1):
            self.vlist.append(self.list3[self.setEnd(self.list3)-i])

    def getPList(self):
        self.setPList()
        return self.priceList

    def getTList(self):
        self.setTList()
        return self.timeList

    def getVList(self):
        self.setVList()
        return self.vlist