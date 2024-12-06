import hashlib
import hmac
import time
from typing import Optional, Union

from billing._constants import TERMINAL_WEBHOOK_SECRET_KEY_PREFIX
from billing._exceptions import SignatureVerificationError
from billing._utils import json_loads
from billing.types import WebhookEvent


class Webhook:
    DEFAULT_TOLERANCE_SECONDS = 300

    @classmethod
    def construct_event(
        cls,
        payload: Union[bytes, str],
        signature: str,
        signature_timestamp: Union[str, int],
        terminal_webhook_secret_key: str,
        tolerance_seconds: Optional[int] = DEFAULT_TOLERANCE_SECONDS,
    ) -> WebhookEvent:
        if not terminal_webhook_secret_key.startswith(TERMINAL_WEBHOOK_SECRET_KEY_PREFIX):
            raise ValueError(
                f"Invalid terminal webhook secret key. Must starts with `{TERMINAL_WEBHOOK_SECRET_KEY_PREFIX}`."
            )

        if isinstance(payload, bytes):
            payload = payload.decode("utf-8")

        cls.verify_signature(
            payload=payload,
            signature=signature,
            signature_timestamp=signature_timestamp,
            terminal_webhook_secret_key=terminal_webhook_secret_key,
            tolerance_seconds=tolerance_seconds,
        )

        return WebhookEvent.parse(json_loads(payload))

    @classmethod
    def verify_signature(
        cls,
        payload: str,
        signature: str,
        signature_timestamp: Union[str, int],
        terminal_webhook_secret_key: str,
        tolerance_seconds: Optional[int] = None,
    ) -> None:
        if tolerance_seconds and int(signature_timestamp) < time.time() - tolerance_seconds:
            raise SignatureVerificationError(f"Timestamp ({signature_timestamp}) outside of the tolerance zone.")

        excepted_signature = cls._compute_excepted_signature(
            payload=payload,
            signature_timestamp=signature_timestamp,
            terminal_webhook_secret_key=terminal_webhook_secret_key,
        )

        if not hmac.compare_digest(signature, excepted_signature):
            raise SignatureVerificationError("Signature verification failed for given payload.")

    @staticmethod
    def _compute_excepted_signature(
        payload: str,
        signature_timestamp: Union[str, int],
        terminal_webhook_secret_key: str,
    ) -> str:
        secret = f"{signature_timestamp}.{payload}".encode()
        mac = hmac.new(
            terminal_webhook_secret_key.encode("utf-8"),
            msg=secret,
            digestmod=hashlib.sha256,
        )
        return mac.hexdigest()
