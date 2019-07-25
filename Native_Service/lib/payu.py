from django.conf import settings
import json
from urllib import parse
import requests


def payu_token_data_set(order_data):
    """
    Function requests PayU for necessary token to make payment.

    return is a dict with the following keys:
    'access_token' - main result to make payment
    'token_type' - type of token
    'refresh_token' - refresh token
    'expires_in' - expires time
    """

    request_headers = {"Cache-Control": "no-cache", "Content-Type": "application/x-www-form-urlencoded"}
    query = f"grant_type=trusted_merchant&client_id={settings.CLIENT_ID}&client_secret={settings.CLIENT_SECRET}&email={order_data['email']}&ext_customer_id={order_data['secret_key']}"
    print(query)
    # Encoding query request
    request_values = parse.quote(query)
    token_request = requests.post(
        settings.PAYU_TOKEN_ENDPOINT_URL, data=request_values, headers=request_headers
    )
    token_response_utf8 = token_request.content.decode("utf-8")
    # Changing JSON string into python dict
    token_response = json.decoder.JSONDecoder().decode(token_response_utf8)
    if token_request.status_code == 401:
        return token_request.status_code, token_response
    else:
        return token_response
