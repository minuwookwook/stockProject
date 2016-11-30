# Create your views here.
#i-*-coding: utf-8-*-
from django.shortcuts import render

from stocks.forms import NumForm
import bs4
from urllib2 import urlopen
import time
import csv



def calculate(request):
    stockResult = {}
    newsResult = {}
    if request.method == "GET":
        _numform = NumForm()
    elif request.method == "POST":
        _numform = NumForm(request.POST)
        if _numform.is_valid():
            stock = _numform.cleaned_data['stock']
            if stock.isdigit():
                stockResult = currentStock(stock)
                newsResult = currentNews(stock)
            else:
                temp = getStockCode(stock)
                if temp == None:
                    stockResult
                    newsResult
                else:
                    stockResult = currentStock(temp)
                    newsResult = currentNews(temp)

    return render(request, 'stock/calculate.html', {'form': _numform, 'stockResult': stockResult, 'newsResult': newsResult})

def currentStock(stock_code):
    url = 'http://finance.daum.net/item/main.daum?code=' + stock_code
    html = urlopen(url).read()
    soup = bs4.BeautifulSoup(html, "html.parser")
    i = 0
    j = 0
    k = 0
    l = 0
    stock = {}
    result = ""
    # 현재가
    if(soup.find_all('em', 'curPrice up')):
        for temp in soup.find_all('em', 'curPrice up'):
            stock['currentPrice'] = temp.text
            result = temp.text
    else:
        for temp in soup.find_all('em', 'curPrice down'):
            stock['currentPrice'] = temp.text
            result = temp.text

    # 전일대비
    if(soup.find_all('span', 'sise down')):
        for temp in soup.find_all('span', 'sise down'):
            stock['netChange'] = '-' + temp.text
    else:
        for temp in soup.find_all('span', 'sise up'):
            stock['netChange'] = '+' + temp.text

    # 전일대비 변화율
    if(soup.find_all('span', 'rate down')):
        for temp in soup.find_all('span', 'rate down'):
            stock['rate'] = temp.text
    else:
        for temp in soup.find_all('span', 'rate up'):
            stock['rate'] = temp.text

    # 거래량, 거래대금
    for temp in soup.find_all('span', 'num_trade'):
        if(j == 0):
            stock['tradingVolume'] = temp.text
            j += 1
        elif(j == 1):
            stock['tradingValue'] = temp.text

    # 거래량 전일 대비율
    for temp in soup.find_all('span', 'txt_rate'):
        stock['tradingVolumeRate'] = temp.text

    # 전일, 고가, 상한가, 시가, 저가, 하한가
    for temp in soup.find_all('dd', 'txt_price'):
        if(i == 0):
            stock['yesterday'] = temp.text
            i += 1
        elif(i == 1):
            stock['highPrice'] = temp.text
            i += 1
        elif(i == 2):
            stock['upperLimit'] = temp.text
            i += 1
        elif(i == 3):
            stock['marketPrice'] = temp.text
            i += 1
        elif(i == 4):
            stock['lowPrice'] = temp.text
            i += 1
        elif(i == 5):
            stock['lowLimit'] = temp.text
            i += 1
        else:
            break

    # 외국인 비율, 시가 총액, 52주 최고, ESP/PER, 52주 최저, BSP/PBR, 종목, WICS
    for temp in soup.find_all('dd'):
        if (k == 11):
            stock['foreignerRate'] = temp.text
            k += 1
        elif(k == 13):
            stock['marketCapitalization'] = temp.text
            k += 1
        elif(k == 14):
            stock['highest52'] = temp.text
            k += 1
        elif(k == 15):
            stock['EPSPER'] = temp.text
            k += 1
        elif(k == 16):
            stock['lowest52'] = temp.text
            k += 1
        elif(k == 17):
            stock['BPSPBR'] = temp.text
            k += 1

        else:
            k += 1

    return stock

def currentNews(stock_code):
    url = 'http://finance.daum.net/item/news.daum?code=' + stock_code
    html = urlopen(url).read()
    soup = bs4.BeautifulSoup(html, "html.parser")
    news = {}
    i = 1
    j = 1
    # 뉴스 타이틀
    for temp in soup.find_all('a', 'cTt'):
        news[i] = temp.text
        i = i + 1

    # 뉴스 하이퍼링크
    for temp in soup.find_all('a', 'cTt', href=True):
        news[i] = "http://finance.daum.net" + temp['href']
        i = i + 1

    return news

def getStockCode(stock):
    stockDict = {}

    # 2016년 11월 17일 기준 KOSPI, KOSDAQ 종목
    with open('/home/jeongwook/stockProject-pr/20161117_Combine.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            stockDict[row[1]] = row[0]

    if stock in stockDict:
        return stockDict.get(stock)
    else:
        return None
