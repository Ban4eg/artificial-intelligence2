import re
import ast
import random
import datetime
import webbrowser
import requests
import spacy
from googletrans import Translator
from textblob import TextBlob
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

nlp = spacy.load("ru_core_news_sm")
translator = Translator()

API_KEY = "16096f9c40048c4f62d4bdba2b5f73ce"

DAYS_RU = {
    "Monday": "понедельник",
    "Tuesday": "вторник",
    "Wednesday": "среда",
    "Thursday": "четверг",
    "Friday": "пятница",
    "Saturday": "суббота",
    "Sunday": "воскресенье",
}