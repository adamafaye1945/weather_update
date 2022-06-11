import time
from config import MY_KEY
import requests
from twilio.rest import Client
from selenium import webdriver
from selenium.webdriver.common.by import By
# Initializing class that hold my api keys
key = MY_KEY()
# Weather data form open weather api

weather_url ='https://api.openweathermap.org/data/3.0/onecall'
my_api_key = key.open_weather_api_key
parameters = {
	"lat": 40.730610,
	"lon":-73.935242,
	"appid":my_api_key,
	"units":"imperial",
}
data = requests.get(url=weather_url, params=parameters).json()
current_weather = data["current"]["weather"][0]
current_temp = round(float(data["current"]["temp"]))
feels_like_temp = round(float(data["current"]["feels_like"]))
weather_description = current_weather["description"]

weather_message_in_english = f"hello user,\nToday the weather description is {weather_description}" \
					 f". We have the temperature at {current_temp} Fahrenheit but it will feels like {feels_like_temp} Fahrenheit "

# ----------------------------------------------------------------------------------------------------
# translator using selenium
GOOGLE_TRANSLATOR_URL = "https://translate.google.com/?sl=en&tl=es&op=translate"
CHROME_DRIVER_PATH = '/Users/adama/Documents/chromedriver'
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
driver.get(GOOGLE_TRANSLATOR_URL)
search_area = driver.find_element(By.XPATH, value="//*[@id='yDmH0d']/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[1]/span/span/div/textarea")
search_area.send_keys(weather_message_in_english)
time.sleep(5)
weather_message_in_spanish = driver.find_element(By.XPATH, value="//*[@id='yDmH0d']/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[2]/div[8]/div/div[1]").text
time.sleep(5)



# ----------------------------------------------------------------------------------------------------
#Message sending api to the phone
account_SID =key.twilio_api_SID
auth_token= key.twilio_auth_token
client = Client(account_SID, auth_token)

message = client.messages \
                .create(
                     body=f"{weather_message_in_english}\n\n{weather_message_in_spanish}",
                     from_='+17575305819',
                     to='+13476989958'
                 )
