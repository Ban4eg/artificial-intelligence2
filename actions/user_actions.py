from .base_actions import *
from .storage import get_user_data, update_user_data
from typing import Text, Dict, List, Any


class ActionSaveName(Action):
    def name(self) -> Text:
        return "action_save_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_id = tracker.sender_id
        name = next(tracker.get_latest_entity_values("name"), None)

        if name:
            update_user_data(user_id, "name", name)
            dispatcher.utter_message(text=f"Хорошо, я запомнил ваше имя: {name}!")
        else:
            dispatcher.utter_message(text="Не удалось распознать имя. Пожалуйста, повторите.")

        return []


class ActionGetSavedName(Action):
    def name(self) -> Text:
        return "action_get_saved_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_id = tracker.sender_id
        user_data = get_user_data(user_id)
        name = user_data.get("name")

        if name:
            dispatcher.utter_message(text=f"Я помню вас, {name}! Чем могу помочь?")
        else:
            dispatcher.utter_message(text="Я не знаю вашего имени. Можете его назвать?")

        return []


class ActionGetSavedCity(Action):
    def name(self) -> Text:
        return "action_get_saved_city"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_id = tracker.sender_id
        user_data = get_user_data(user_id)
        city = user_data.get("city")

        if city:
            dispatcher.utter_message(text=f"Ваш сохранённый город: {city}.")
        else:
            dispatcher.utter_message(text="Я не знаю ваш город. Укажите его, например: 'Мой город — Москва'.")

        return []


class ActionSaveCity(Action):
    def name(self) -> Text:
        return "action_save_city"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_id = tracker.sender_id
        city = next(tracker.get_latest_entity_values("city"), None)

        if not city:
           
            text = tracker.latest_message.get('text', '').lower()
            if "город" in text:
                city = text.split("город")[-1].strip(" -").capitalize()

        if city:
            update_user_data(user_id, "city", city.capitalize())
            dispatcher.utter_message(text=f"Хорошо, сохранил ваш город: {city.capitalize()}!")
            return [SlotSet("city", city.capitalize())]
        else:
            dispatcher.utter_message(text="Пожалуйста, укажите город в формате: 'Мой город Москва'")
            return []
