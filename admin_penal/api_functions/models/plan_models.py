from bson import ObjectId

from admin_penal.db_config import manage_plan

class SubscriptionPlan:
    def __init__(self, title=None, is_trial=None, price=None, price_crossed=None, duration_in_days=30,
                 short_description='', allow_chat_tags=False, allow_chat_note=False,
                 allow_wa_chatbot=False):
        self.title = title
        self.is_trial = is_trial
        self.price = price
        self.price_crossed = price_crossed
        self.duration_in_days = duration_in_days
        self.short_description = short_description
        self.allow_chat_tags = allow_chat_tags
        self.allow_chat_note = allow_chat_note
        self.allow_wa_chatbot = allow_wa_chatbot

    def save(self):
        result = manage_plan.insert_one({
            "title": self.title,
            "is_trial": self.is_trial,
            "price": self.price,
            "price_crossed": self.price_crossed,
            "duration_in_days": self.duration_in_days,
            "short_description": self.short_description,
            "allow_chat_tags": self.allow_chat_tags,
            "allow_chat_note": self.allow_chat_note,
            "allow_wa_chatbot": self.allow_wa_chatbot
        })
        return str(result.inserted_id)

    def get_all_plans(self):
        plans = manage_plan.find({})
        # Convert ObjectId to string for each plan
        return [{**plan, "_id": str(plan["_id"])} for plan in plans]

    def create_plan(self, plan_data):
        # Safely get 'price' and 'price_crossed' to avoid KeyError
        plan = {
            "title": plan_data["title"],
            "is_trial": plan_data["is_trial"],
            "price": plan_data.get("price"),  # Use .get() to avoid KeyError
            "price_crossed": plan_data.get("price_crossed"),
            "duration_in_days": plan_data["duration_in_days"],
            "short_description": plan_data.get("short_description", ''),
            "allow_chat_tags": plan_data["allow_chat_tags"],
            "allow_chat_note": plan_data["allow_chat_note"],
            "allow_wa_chatbot": plan_data["allow_wa_chatbot"]
        }
        result = manage_plan.insert_one(plan)
        return str(result.inserted_id)

    def delete_plan(self,plan_id):
       result = manage_plan.delete_one({'_id':ObjectId(plan_id)})
       return  result.deleted_count