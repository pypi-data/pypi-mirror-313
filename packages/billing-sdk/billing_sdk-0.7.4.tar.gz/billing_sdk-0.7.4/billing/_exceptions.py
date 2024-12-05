from typing import Optional


class BillingError(Exception):
    default_message: Optional[str] = None

    def __init__(self, message: Optional[str] = None) -> None:
        super().__init__(message or self.default_message)


class SignatureVerificationError(BillingError):
    pass


class BillingAPIError(BillingError):
    default_message = "API error"

    def __init__(
        self,
        message: Optional[str] = None,
        *,
        status_code: int,
        response_text: str,
    ) -> None:
        final_message = (
            f"Error message - {message or self.default_message}."
            f" Status code - {status_code}. Response text - {response_text}."
        )
        super().__init__(final_message)

        self._status_code = status_code
        self._response_text = response_text

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def response_text(self) -> str:
        return self._response_text


class AuthenticationError(BillingAPIError):
    default_message = "Authentication error"


class RateLimitError(BillingAPIError):
    default_message = "Rate limit exceeded"


class FeatureUsageLimitExceededError(RateLimitError):
    default_message = "Feature usage limit exceeded"
