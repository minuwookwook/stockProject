import datacrawling

class Real:

    def __init__(self, id = None, point = None):
        self.id = id
        self.point = point
        self.stock_list = []  # 구매목록 tuple형식 (종목이름, 총 가격, 구입량)

    def setPoint(self, point = None):
        self.point = self.point + point

    def getPoint(self):
        return self.point

    def purchase(self, name = None, price = None, volume = None):
        total = price * volume
        check = None
        for i in range(0, len(self.stock_list)):
            if self.stock_list[i][0] == name :
                check = i

        if check == None:
            if self.getPoint() > total:
                self.setPoint(total * -1)
                self.stock_list.append((name, total, volume))
            else:
                print("포인트가 부족합니다.")
        else:
            if self.getPoint() > total:
                self.setPoint(total * -1)
                total = self.stock_list[check][1] + total
                volume = self.stock_list[check][2] + volume
                self.stock_list.append((name, total, volume))
                self.stock_list.remove(self.stock_list[check])

            else:
                print("포인트가 부족합니다.")

    def sell(self, name = None, price = None, volume = None):
        check = None
        total = price * volume
        for i in range(0, len(self.stock_list)):
            if self.stock_list[i][0] == name :
                check = i

        if check == None:
            print("구매목록에 없습니다.")

        else:
            if volume > self.stock_list[check][2]:
                print("판매량이 보유량을 초과합니다.")

            elif volume == self.stock_list[check][2]:
                self.setPoint(total)
                self.stock_list.remove(self.stock_list[check])

            else:
                self.setPoint(total)
                total = self.stock_list[check][1] - total
                volume = self.stock_list[check][2] - volume
                self.stock_list.append((name, total, volume))
                self.stock_list.remove(self.stock_list[check])

    def showList(self):
        for i in range(0, len(self.stock_list)):
            print(str(self.stock_list[i]))



if __name__ == '__main__':
    #예시
    a = Real('ysoo14', 100000000)
    a.purchase('삼성전자', 1000000, 4)
    a.purchase('삼성전자', 1000000, 4)
    a.purchase('현대건설', 500000, 20)
    a.sell('삼성전자',1250000,8)
    a.sell('현대건설',1000000,20)
    print(a. getPoint())
    a.showList()






