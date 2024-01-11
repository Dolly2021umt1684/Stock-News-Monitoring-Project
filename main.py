import requests
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_key= os.getenv("STOCK_API_key")
NEW_API_KEY=os.getenv("NEW_API_KEY")

Auth_Token=os.getenv("Auth_Token")
My_Twilio_phone_number=os.getenv("My_Twilio_phone_number")
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
TO_PHONE_NO=os.getenv("TO_PHONE_NO")

SYMBOL_UP='⬆️'
SYMBOL_DOWN="⬇️"


stock_params={
'function':'TIME_SERIES_DAILY',
'symbol': STOCK_NAME,
    'apikey':STOCK_API_key,
}

stock_response=requests.get(url=STOCK_ENDPOINT,params=stock_params)
stock_response.raise_for_status()
stock_data=stock_response.json()




# getting hold of the close of each day in a list
stock_closes=[float(value["4. close"]) for (key,value) in stock_data["Time Series (Daily)"].items()]
# print(stock_closes)
last_day_close=stock_closes[0]
day_before_last_close=stock_closes[1]
print(last_day_close)
print(day_before_last_close)



percentage_diff=round((abs(last_day_close-day_before_last_close)/day_before_last_close)*100,0)
print(percentage_diff)



news_params={
    'qInTitle':COMPANY_NAME,
'sortBy':'publishedAt',
    'apiKey':NEW_API_KEY
}

news_response=requests.get(url=NEWS_ENDPOINT,params=news_params)
news_response.raise_for_status()
news_data=news_response.json()
# print(news_data)



# getting first 3 articles from the news
article_list=[]
for article in news_data['articles'][:3]:
    article_list.append(article)

# print(article_list)

headline_list=[]
description_list=[]

for article in article_list:
    headline_list.append(article['title'])
    description_list.append(article['description'])

# print(headline_list)
# print(description_list)


def send_sms(headline,description,symbol):

    account_sid = ACCOUNT_SID
    auth_token = Auth_Token
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f'TSLA:{symbol}{percentage_diff}% \nHeadline:{headline}\n Brief:{description}',
        from_=My_Twilio_phone_number,
        to=TO_PHONE_NO
    )
    print(message.status)


diff = day_before_last_close-last_day_close
if diff<0:
    symbol=SYMBOL_DOWN
else:
    symbol=SYMBOL_UP

if percentage_diff>5:
    for i in range(0,3):
        send_sms(headline_list[i],description_list[i],symbol)




