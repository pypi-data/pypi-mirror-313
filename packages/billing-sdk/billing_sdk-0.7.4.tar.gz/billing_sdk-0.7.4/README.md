# Billing Python Library

The Billing Python library provides convenient access to the Billing API from applications written in the Python language. It includes a pre-defined set of classes for API resources that initialize themselves dynamically from API responses which makes it compatible with a wide range of versions of the Billing API.

## Installation
If you just want to use the package, run:
```shell
pip install --upgrade billing-sdk
```
## Requirements
- Python 3.8 or higher
- pip (Python package installer)

## Configuration

---

### Configuring Billing client
```python
from billing import BillingClient

billing_client = BillingClient(
    terminal_id="...",
    terminal_secret_key="tr_sk__...",
)
```

#### Choosing Between Sync and Async Clients
You can configure the SDK to use either synchronous or asynchronous requests:
- **Synchronous Requests Only**:
  ```python
    billing_client = BillingClient(
        ...
        setup_sync_client=True,
    )
    ```
- **Asynchronous Requests Only**:
  ```python
    billing_client = BillingClient(
        ...
        setup_async_client=True,
    )
    ```
- **Both Synchronous and Asynchronous Requests**:
  ```python
    billing_client = BillingClient(
        ...
        setup_sync_client=True,
        setup_async_client=True,
    )
    ```

### Custom HTTPX client
If you have already initialized an `httpx` client in your application, you can reuse it in the `BillingClient` to avoid unnecessary resource allocation:
```python
import httpx
from billing import BillingClient

reusable_sync_client = httpx.Client()

billing_client = BillingClient(
    ...
    sync_client=reusable_sync_client,
)

# and/or

reusable_async_client = httpx.AsyncClient()

billing_client = BillingClient(
    ...
    async_client=reusable_async_client,
)
```
> ⚠️ **Warning:** Ensure that your custom `httpx` client is not pre-configured with a `base_url`, `headers`, or other settings that may cause unexpected errors when making API calls.

### Configuring Automatic Retries

Enable automatic retries for transient network errors by setting the `max_network_retries` parameter:
```python
billing_client = BillingClient(
    ...
    max_network_retries=3,
)
```

## Usage
You can access various API methods through the `BillingClient` properties. For example, to interact with the Agreement API:

### Sync Usage
```python
agreements = billing_client.agreements.list(page_number=1, page_size=20)
```

### Async Usage
```python
agreements = await billing_client.agreements.list_async(page_number=1, page_size=20)
```

For now Billing SDK support the following API methods:
- `Agreement`
    - `retrieve`
    - `list`
- `Feature`
    - `retrieve_usage_summary`
    - `list_usage_summary`
    - `record_usage`
- `Invoice`
    - `retrieve`
    - `list`
- `Offer`
    - `retrieve`
    - `list`
    - `cancel`
- `Order`
    - `retrieve`
    - `list`
    - `create`
- `Product`
    - `retrieve`
    - `list`

### Webhook Event Construction
When you receive a webhook from Billing, it is highly recommended to verify its Signature to ensure the integrity and authenticity of the event. The Billing SDK provides built-in support for webhook signature verification and event construction, making it easy to validate and process webhooks securely.

#### Example: Handling Webhooks with FastAPI
Below is an example of how to set up a webhook handler using [FastAPI](https://github.com/fastapi/fastapi):
```python
from billing import Webhook, SignatureVerificationError
from fastapi import FastAPI, HTTPException, Header, Request, status

# Define your webhook secret key
terminal_webhook_secret_key = "tr_wsk__..."

# Initialize the FastAPI application
app = FastAPI(...)

@app.post("billing/webhook", status_code=status.HTTP_200_OK)
async def handle_billing_webhook(
    request: Request,
    x_billing_signature: str = Header(..., alias="X-Billing-Signature"),
    x_billing_signature_timestamp: str = Header(..., alias="X-Billing-Signature-Timestamp"),
) -> None:
    try:
        # Construct the webhook event with verification
        webhook_event = Webhook.construct_event(
            payload=await request.body(),  # The raw request body as payload
            signature=x_billing_signature,  # The signature from the header
            signature_timestamp=x_billing_signature_timestamp,  # The timestamp from the header
            terminal_webhook_secret_key=terminal_webhook_secret_key,  # Your secret key for verification
        )

        # ###################### Handling logic ######################
        # Process the event here, e.g., logging, updating database, etc.
        print("Received webhook event:", webhook_event)
    except SignatureVerificationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid webhook signature"
        )
```

## License
The Billing SDK is licensed under the MIT License. See the `LICENSE` file for more information.
