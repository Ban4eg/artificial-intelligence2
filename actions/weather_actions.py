from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from .storage import update_user_data, get_user_data
from .base_actions import *
import re
import requests


class ActionGetWeather(Action):
    def name(self) -> Text:
        return "action_get_weather"

    def extract_city(self, text: str) -> str:
        
        patterns = [
            r'погод[а-я]* в (?:городе )?([а-яё-]+)',
            r'в (?:городе )?([а-яё-]+)',
            r'город[а-я]* ([а-яё-]+)'
        ]

        text = text.lower()
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).capitalize()
        return None

    def get_weather_data(self, city: str) -> Dict:
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception:
            return None

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_id = tracker.sender_id
        user_data = get_user_data(user_id)

        
        city = (
                next(tracker.get_latest_entity_values("city"), None) or  # Из entities
                self.extract_city(tracker.latest_message.get("text", "")) or  # Из текста
                user_data.get("city")  # Из сохранённых данных
        )

        if not city:
            dispatcher.utter_message(
                text="Пожалуйста, укажите город, например: 'Какая погода в Москве?' или скажите 'Мой город Москва'"
            )
            return []

        city = city.capitalize()

        
        update_user_data(user_id, "city", city)

        
        weather_data = self.get_weather_data(city)

        if not weather_data:
            dispatcher.utter_message(
                text=f"Не удалось получить погоду для {city}. Проверьте название города."
            )
            return [SlotSet("city", None)]

        
        temp = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]
        feels_like = weather_data["main"]["feels_like"]
        humidity = weather_data["main"]["humidity"]

        message = (
            f"В городе {city} сейчас {description}.\n"
            f"🌡 Температура: {temp:.1f}°C (ощущается как {feels_like:.1f}°C)\n"
            f"💧 Влажность: {humidity}%"
        )

        dispatcher.utter_message(text=message)
        return [SlotSet("city", city)]
