from .base_actions import *
import re


class ActionCalculate(Action):
    def name(self) -> Text:
        return "action_calculate"

    def safe_eval(self, expr: Text) -> Any:
        try:
            expr = re.sub(r'[^\d+\-*/(). ]', '', expr)
            if not re.search(r'[\+\-\*/]', expr):
                return None

            allowed_chars = set('0123456789+-*/.() ')
            if not all(c in allowed_chars for c in expr):
                return None

            return eval(expr, {'__builtins__': None}, {})
        except:
            return None

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get('text', '')
        expr_match = re.search(r'(\d+\.?\d*\s*[\+\-\*\/]\s*\d+\.?\d*)', user_message)

        if not expr_match:
            nums = re.findall(r'\d+', user_message)
            if len(nums) >= 2:
                if "умнож" in user_message or "*" in user_message:
                    expr = f"{nums[0]}*{nums[1]}"
                elif "дел" in user_message or "/" in user_message:
                    expr = f"{nums[0]}/{nums[1]}"
                elif "слож" in user_message or "+" in user_message:
                    expr = f"{nums[0]}+{nums[1]}"
                elif "выч" in user_message or "-" in user_message:
                    expr = f"{nums[0]}-{nums[1]}"
                else:
                    dispatcher.utter_message(text="Пожалуйста, укажите операцию (+, -, *, /)")
                    return []
            else:
                dispatcher.utter_message(text="Не могу найти числа для вычисления")
                return []
        else:
            expr = expr_match.group(1)

        expr = expr.replace(' ', '').replace('x', '*').replace('×', '*').replace('÷', '/')
        result = self.safe_eval(expr)

        if result is not None:
            dispatcher.utter_message(text=f"Результат: {expr} = {result}")
        else:
            dispatcher.utter_message(
                text="Не могу вычислить это выражение. Пожалуйста, укажите в формате '5+5' или '10 умножить на 2'")

        return []