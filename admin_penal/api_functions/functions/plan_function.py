from admin_penal.api_functions.models.plan_models import SubscriptionPlan


class SubscriptionService:
    def __init__(self, db):
        self.db = db

    def create_subscription(self, data):
        # If it's a trial plan, remove price and price_crossed
        if data.get('is_trial'):
            data.pop('price', None)
            data.pop('price_crossed', None)
        else:
            # Ensure price and price_crossed are present for non-trial plans
            if 'price' not in data or 'price_crossed' not in data:
                raise ValueError("Price and Price Crossed are required for non-trial plans.")

        # Create and insert the subscription plan
        plan = SubscriptionPlan(**data)
        result = self.db['plans'].insert_one(plan.to_dict())
        return str(result.inserted_id)


