from .base_actions import *
import datetime

class ActionGetTime(Action):
    def name(self) -> Text:
        return "action_get_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_time = datetime.datetime.now().strftime("Сейчас %H:%M")
        dispatcher.utter_message(text=current_time)
        return []

class ActionGetDate(Action):
    def name(self) -> Text:
        return "action_get_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_date = datetime.datetime.now().strftime("Сегодня %d.%m.%Y")
        dispatcher.utter_message(text=current_date)
        return []

class ActionGetDayOfWeek(Action):
    def name(self) -> Text:
        return "action_get_day_of_week"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        day = DAYS_RU[datetime.datetime.now().strftime('%A')]
        dispatcher.utter_message(text=f"Сегодня {day}.")
        return []