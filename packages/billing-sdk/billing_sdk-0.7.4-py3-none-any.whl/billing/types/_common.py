from typing import Literal

HTTPMethod = Literal["GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"]

PeriodType = Literal["day", "week", "month", "year"]

PaymentMethod = Literal["stripe", "yookassa", "telegram_stars"]

CancellationFeedback = Literal[
    "customer_service",
    "low_quality",
    "missing_features",
    "switched_service",
    "too_complex",
    "too_expensive",
    "unused",
    "other",
]
