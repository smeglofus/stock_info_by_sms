import requests
from datetime import datetime, timedelta
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
poslat = False

parameters_chart = {
"apikey": "SLUTC0FD1J5DFYOH",
"function": "TIME_SERIES_DAILY",
"symbol": STOCK,
"outputsize": "compact"
}

parameters_news = {
"apiKey": "562c0969ca10422c869bf291a925a917",
"q": COMPANY_NAME,
}

#Datum dnesek a vcerejsek
now = datetime.now()
dnesek = now.strftime("%Y-%m-%d")
vcera_datum = now - timedelta(days= 1)
vcerejsek = vcera_datum.strftime("%Y-%m-%d")
predvcerejsek_datum = vcera_datum - timedelta(days=1)
predvcerejsek = predvcerejsek_datum.strftime("%Y-%m-%d")


#data z tesly
data = requests.get(STOCK_ENDPOINT, params=parameters_chart)
stock_data = data.json()
vcera_close = float(stock_data["Time Series (Daily)"][vcerejsek]["4. close"])
predvcera_close = float(stock_data["Time Series (Daily)"][predvcerejsek]["4. close"])


#pokud je rozdíl včera a předevčírem větší než 5%, napíšeme Get News, v opačném případě prdlačku
rozdil = vcera_close - predvcera_close
print(rozdil)
procento = float((vcera_close / 100) * 5)
pohyb = "roste"



if procento < 0:
    procento *= -1
    pohyb = "klesá"

if rozdil > procento:
    print("Get News")
    poslat = True
else:
    print(f"Prdlačku, rozdíl je {rozdil} a na 5 % je to {procento}")


#zprávy z tesly prevede do sms
sms = f"Tesla {pohyb} o {procento}. Zde jsou nejnovější zprávy: \n"
data_news = requests.get(NEWS_ENDPOINT, params=parameters_news)
news = data_news.json()
for i in range(2):
    sms += news["articles"][i]["title"] + " "
    sms += news["articles"][i]["url"]
    sms += "\n"


print(sms)

# pošle sme přes twilio.com


account_sid = 'AC6cd2a153d3510d14ead3b486ead116ff'
auth_token = "4ec95d016cae95c445c0c56cd09bf410"

if poslat:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=sms,
        from_="+17087874972",
        to='+420799520302',
                              )
    print(message.status)

