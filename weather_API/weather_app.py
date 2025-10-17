import requests 
import json
from datetime import datetime

# Weather CLI Application

API_KEY = 'create your own API' # get yours at openweathermap.org
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    '''Fetch weather data for a city'''
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric" # Celsius
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return {"error": "City not found"}
        elif response.status_code == 401:
            return {"error": "Invalid API key"}
        else:
            return {"error": f"Error: {response.status_code}"}
    
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Check your internet connection."}
    except requests.exceptions.ConnectionError:
        return {"error": "Connection error. Check your internet connection."}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}
    
def display_weather(data):
    '''display weather information'''
    if 'error' in data:
        print(f'\n❌ {data['error']}')
        return
    
    # Extract data
    city = data['name']
    country = data['sys']['country']
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    humidity = data['main']['humidity']
    pressure = data['main']['pressure']
    description = data['weather'][0]['description'].title()
    wind_speed = data['wind']['speed']

    # display
    print(f'''\n
        {'='*50}\n
              🌤️  WEATHER IN {city.upper()}, {country}\n
        {'='*50}\n
        🌡️  Temperature:    {temp}°C (feels like {feels_like}°C)\n
        ☁️  Condition:      {description}\n
        💧 Humidity:       {humidity}%\n
        🌬️  Wind Speed:     {wind_speed} m/s\n
        🔽 Pressure:       {pressure} hPa\n
        {'='*50}
''')
    
    # Temperature advice
    if temp < 10:
        print("🥶 It's cold! Wear warm clothes.")
    elif temp < 20:
        print("😊 Pleasant weather!")
    elif temp < 30:
        print("☀️  Warm weather. Stay hydrated!")
    else:
        print("🔥 Very hot! Stay cool and drink water!")

def save_search_history(city, data):
    # save search to history file
    try:
        # Load existing history
        try:
            with open('weather_history.json', 'r') as file:
                history = json.load(file)
        except FileNotFoundError:
            history = []

        # add new search
        if 'error' not in data:
            search_record = {
                "city": city,
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            history.append(search_record)

            #keep only last 20 searches
            if len(history) > 20:
                history = history[-20:]
            
            # save
            with open('weather_history.json', 'w') as file:
                json.dump(history, file, indent=2)

    except Exception as e:
        print(f"⚠️  Could not save history: {e}")

def show_history():
    # dispatch search history
    try:
        with open('weather_history.json') as file:
            history = json.load(file)

        if not history:
            print("\n📭 No search history")
            return

        print(f'''\n
{'='*70}\n
                    🕐 SEARCH HISTORY\n
{'='*70}\n
{'City':<20} {'Temp':<10} {'Description':<20} {'Time':<20}\n
{"="*70}
''')
        
        for record in reversed(history): #show most recent first
            city = f'{record['city']}, {record['country']}'
            temp = f'{record['temperature']}°C'
            desc = record['description'][:18]
            time = record['timestamp']
            print(f"{city:<20} {temp:<10} {desc:<20} {time:<20}")

        print("="*70)

    except FileNotFoundError:
        print("\n📭 No search history")
    except Exception as e:
        print(f"\n❌ Error loading history: {e}")

def main():
    print("👋 Welcome to Weather CLI App!")
    print("   Powered by OpenWeatherMap")

    # check if API key is set
    if API_KEY != 'create your own API at': # get yours at openweathermap.org
        print("\n⚠️  Please set your API key first!")
        print("   1. Go to: https://openweathermap.org/api")
        print("   2. Sign up for free account")
        print("   3. Get your API key")
        print("   4. Replace 'your_api_key_here' in the code")
        return
    
    while True:
        print("\n" + "="*50)
        print("1. 🔍 Check Weather")
        print("2. 📜 View Search History")
        print("3. 🚪 Exit")
        print("="*50)

        choice = input("\nChoose option (1-3): ").strip()

        if choice == "1":
            city = input('\nEnter city name: ').strip()
            if city:
                print("\n⏳ Fetching weather data...")
                data = get_weather(city)
                display_weather(data)
                save_search_history(city, data)
            
        elif choice == '2':
            show_history()

        elif choice == '3':
            print("\n👋 Thanks for using Weather CLI!")
            print("   Stay weather-wise! 🌤️")
            break
        
        else:
            print("❌ Invalid choice!")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()

        