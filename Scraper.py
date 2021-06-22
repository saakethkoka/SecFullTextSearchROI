import requests
import datetime as dt
import json

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.sec.gov',
    'Content-Length': '141',
    'Accept-Language': 'en-us',
    'Host': 'efts.sec.gov',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Referer': 'https://www.sec.gov/edgar/search/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

data = '{"q":"\\"To the extent aggregate short exposure exceeds the number of shares\\"","dateRange":"10y","startdt":"2011-06-22","enddt":"2021-06-22"}'

response = requests.post('https://efts.sec.gov/LATEST/search-index', headers=headers, data=data)

ticker_dict = {

}

def get_ticker(string):
    index = string.find("(")
    ticker = string[index+1:]
    comma_index = ticker.find(",")
    if(comma_index != -1):
        index = ticker.find(",")
    else:
        index = ticker.find(")")
    ticker = ticker[:index]
    return ticker

def scrape_page(response):
    for item in response.json()["hits"]["hits"]:
        ticker = get_ticker(item["_source"]["display_names"][0])
        if 'CIK' in ticker:
            continue
        date_str = item["_source"]["file_date"]
        date = dt.datetime.strptime(date_str, '%Y-%m-%d')
        try:
            if ticker_dict[ticker] > date:
                ticker_dict[ticker] = date
        except:
            ticker_dict[ticker] = date
        print(ticker, date_str)

def get_page(page_num):
    data_start = '{"q":"\\"To the extent aggregate short exposure exceeds the number of shares\\"","dateRange":"10y","page":"'
    data_end = '","from":100,"startdt":"2011-06-22","enddt":"2021-06-22"}'
    new_data = data_start + str(page_num) + data_end
    return requests.post('https://efts.sec.gov/LATEST/search-index', headers=headers, data=new_data)


scrape_page(response)
scrape_page(get_page(2))
