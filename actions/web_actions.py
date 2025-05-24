from .base_actions import *
import webbrowser

class ActionSearchWeb(Action):
    def name(self) -> Text:
        return "action_search_web"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        query = next(tracker.get_latest_entity_values("query"), None) or tracker.latest_message.get("text")
        if not query:
            dispatcher.utter_message(text="Что вам нужно найти?")
            return []

        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        dispatcher.utter_message(text=f"Ищу в интернете: {query}")
        return [SlotSet("query", query)]