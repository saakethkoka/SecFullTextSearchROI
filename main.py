from tda import auth, client
import TDA_config
# from Scraper import ticker_dict
import datetime as dt

try:
    c = auth.client_from_token_file(TDA_config.token_path, TDA_config.api_key)
except FileNotFoundError:
    from selenium import webdriver
    with webdriver.Chrome(executable_path= '/Users/saakethkoka/Documents/Stonks/Code/GammaSqueezeIdentifier/chromedriver') as driver:
        c = auth.client_from_login_flow(
            driver, TDA_config.api_key, TDA_config.redirect_uri, TDA_config.token_path)

import json
date = dt.datetime.today() - dt.timedelta(days=5)

date = dt.datetime.fromtimestamp(1624319940000 / 1e3)
end_date = date + dt.timedelta(days=4)
print(str(date))
date = dt.datetime.fromtimestamp(1624319880000 / 1e3)
print(str(date))


response = c.get_price_history("AAPL", period_type=c.PriceHistory.PeriodType.WEEK)
print(json.dumps(response.json(), indent=4))

for item in response.json()["candles"]:
    date = dt.datetime.fromtimestamp(item["datetime"] / 1e3)
    print(str(date))

curr_date = dt.datetime.today()
 # ticker_list = ticker_dict.keys()
# price_list = c.get_price_history(ticker_list)
# print(price_list)
# for ticker in ticker_dict.keys():
#     date = ticker_dict[ticker]