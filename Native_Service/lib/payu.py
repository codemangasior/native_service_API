import json

from django.conf import settings

from Native_Service.lib.native_service import ProgressStages
import requests


def get_token():
    """
    Function requests PayU for necessary token to make payment.

    return is a dict with the following keys:
    'access_token' - main result to make payment,
    'token_type' - type of token,
    'expires_in' - expires time,
    'grant_type' - the type of grant.
    """

    request_headers = {
        "Cache-Control": "no-cache",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    query = f"grant_type=client_credentials&client_id={settings.CLIENT_ID}&client_secret={settings.CLIENT_SECRET}"
    s = requests.Session()
    s.headers.update(request_headers)
    token_request = s.post(settings.PAYU_TOKEN_ENDPOINT_URL, data=query)
    token_response_utf8 = token_request.content.decode("utf-8")

    # Changing JSON string into python dict
    token_response = json.decoder.JSONDecoder().decode(token_response_utf8)
    return token_response


def order_request(order_data, token_data):
    """ Function makes request to PayU and returns response with url to redirect user. """

    values = {
        "notifyUrl": f"{order_data['notify_url']}",
        "continueUrl": f"{order_data['successful_url']}",
        "customerIp": "185.21.84.215",
        "merchantPosId": f"{settings.POS_ID}",
        "description": f"{order_data['secret_key']}",
        "currencyCode": "PLN",
        "totalAmount": f"{order_data['price']}00",
        # "extOrderId": f"{order_data['secret_key']}",
        "products": [
            {
                "name": f"{order_data['title']}",
                "unitPrice": f"{order_data['price']}00",
                "quantity": "1",
            }
        ],
        "buyer": {
            "email": f"{order_data['email']}",
            "phone": f"{order_data['phone']}",
            "firstName": f"{order_data['name']}",
            "lastName": f"{order_data['last_name']}",
            "language": "pl",
        },
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"{token_data['token_type'].capitalize()} {token_data['access_token']}",
    }
    json_values = json.dumps(values)
    s = requests.Session()
    s.headers.update(headers)
    token_request = s.post(settings.PAYU_ORDER_ENDPOINT_URL, data=json_values)

    return token_request.url


def handle_response(_response, data, secret_key, url):
    """
    Function handles PayU POST response to the 'notify' endpoint.

    '_response' - is a python dictionary send to NativeService as a JSON,
    'data' - is a 'nativepost' model order record filtered with secret_key,
    'secret_key' - is a secret key of valuation and an order,
    'url' - is an url for performer to set stage on 'in_progress'.

    The Function returns one of the statuses current payment: PENDING, COMPLETED, CANCELED,
    if something went wrong then returns: ERROR.
    """
    status = _response["order"]["status"]

    if status == "PENDING":
        stage = status
    elif status == "COMPLETED":
        stage = status
        # Setting stage on PAYMENT_DONE
        ProgressStages().payment_done(data=data, secret_key=secret_key, url=url)
    elif status == "CANCELED":
        stage = status
        ProgressStages().payment_rejected(data=data, secret_key=secret_key)
    else:
        stage = "ERROR"
    return print(stage)
