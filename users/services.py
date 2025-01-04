import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(course):
    """Создание продукта в Stripe"""
    try:
        product = stripe.Product.create(name=course.title)
        return product["id"]
    except stripe.error.StripeError as e:
        raise ValueError(f"Ошибка создания продукта в Stripe: {str(e)}")


def create_stripe_price(product_id, amount):
    """Создание цены для продукта в Stripe"""
    try:
        if not isinstance(amount, (int, float)):
            raise ValueError(f"Некорректное значение для amount: {amount}")
        price = stripe.Price.create(
            product=product_id,
            unit_amount=int(amount * 100),  # Преобразование в копейки
            currency="rub",
        )
        return price["id"]
    except stripe.error.StripeError as e:
        raise ValueError(f"Ошибка создания цены в Stripe: {str(e)}")


def create_stripe_session(price_id):
    """Создание сессии оплаты в Stripe"""
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            success_url="https://127.0.0.1:8000/success/",
            cancel_url="https://127.0.0.1:8000/cancel/",
            line_items=[
                {
                    "price": price_id,
                    "quantity": 1,
                }
            ],
            mode="payment",
        )
        return session.get("id"), session.get("url")
    except stripe.error.StripeError as e:
        raise ValueError(f"Ошибка создания сессии оплаты в Stripe: {str(e)}")
