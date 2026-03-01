import stripe

from app.core.config import get_settings

settings = get_settings()
if settings.stripe_secret_key:
    stripe.api_key = settings.stripe_secret_key


def create_payment_intent(amount_inr: float, metadata: dict[str, str] | None = None) -> str | None:
    if not settings.stripe_secret_key:
        return None
    intent = stripe.PaymentIntent.create(
        amount=int(amount_inr * 100),
        currency='inr',
        metadata=metadata or {},
        automatic_payment_methods={'enabled': True},
    )
    return intent.id
