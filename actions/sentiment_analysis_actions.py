from .base_actions import *
from textblob import TextBlob
import random


class ActionAnalyzeSentiment(Action):
    def name(self) -> Text:
        return "action_analyze_sentiment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        text = tracker.latest_message.get('text', '').lower()

        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity

            positive_words = ['хорошо', 'прекрасно', 'отлично', 'счастлив', 'рад', 'восторг', 'люблю', 'нравится',
                              'класс', 'супер']
            negative_words = ['плохо', 'грустно', 'ужасно', 'злюсь', 'ненавижу', 'разочарован', 'обижен', 'одинок',
                              'расстроен', 'печаль']

            positive_count = sum(1 for word in positive_words if word in text)
            negative_count = sum(1 for word in negative_words if word in text)

            if positive_count > negative_count or polarity > 0.3:
                response = random.choice([
                    "Вы звучите позитивно! 😊 Чем могу помочь?",
                    "Отличное настроение! Как я могу вас порадовать ещё?",
                ])
            elif negative_count > positive_count or polarity < -0.3:
                response = random.choice([
                    "Вы расстроены? Хотите поговорить об этом? 😔",
                    "Я чувствую, что вам грустно. Может, я чем-то помогу?",
                ])
            else:
                response = random.choice([
                    "Я вас слушаю. Чем могу помочь?",
                    "Интересно! Расскажите подробнее.",
                ])

        except Exception as e:
            response = "Я вас понял. Чем ещё могу помочь?"

        dispatcher.utter_message(text=response)
        return []