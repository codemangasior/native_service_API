from django.conf import settings
import json
from urllib import parse
import requests
import hashlib


def get_token(order_data):
    """
    Function requests PayU for necessary token to make payment.

    return is a dict with the following keys:
    'access_token' - main result to make payment
    'token_type' - type of token
    'refresh_token' - refresh token
    'expires_in' - expires time
    """

    request_headers = {
        "Cache-Control": "no-cache",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    query = f"grant_type=trusted_merchant&client_id={settings.CLIENT_ID}&client_secret={settings.CLIENT_SECRET}&email={order_data['email']}&ext_customer_id={order_data['secret_key']}"
    # Encoding query request
    request_values = parse.quote(query)
    token_request = requests.post(
        settings.PAYU_TOKEN_ENDPOINT_URL, data=request_values, headers=request_headers
    )
    token_response_utf8 = token_request.content.decode("utf-8")
    # Changing JSON string into python dict
    token_response = json.decoder.JSONDecoder().decode(token_response_utf8)
    return token_response


def payu_token_data_set_example():
    """
    Function requests PayU for necessary token to make payment.

    return is a dict with the following keys:
    'access_token' - main result to make payment
    'token_type' - type of token
    'refresh_token' - refresh token
    'expires_in' - expires time
    """

    request_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    query = f"grant_type=client_credentials&client_id=145227&client_secret=12f071174cb7eb79d4aac5bc2f07563f"
    print(query)
    # Encoding query request
    request_values = parse.quote(query)
    token_request = requests.post(
        "https://private-anon-0da3a83725-payu21.apiary-mock.com/pl/standard/user/oauth/authorize",
        data=request_values,
        headers=request_headers,
    )
    token_response_utf8 = token_request.content.decode("utf-8")
    # Changing JSON string into python dict
    token_response = json.decoder.JSONDecoder().decode(token_response_utf8)
    if token_request.status_code == 401:
        return token_request.status_code, token_response
    else:
        return token_response


def order_request(order_data, token_data):
    values = {
        "notifyUrl": "https://nativeservice.pl",
        "customerIp": "188.146.97.129",
        "merchantPosId": f"{settings.POS_ID}",
        "description": f"{order_data['secret_key']}",
        "currencyCode": "PLN",
        "totalAmount": f"{order_data['price']}00",
        "products": [
            {
                "name": f"{order_data['title']}",
                "unitPrice": f"{order_data['price']}00",
                "quantity": "1",
            }
        ],
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"{token_data['token_type'].capitalize()} {token_data['access_token']}",
    }

    values2 = {
        "notifyUrl": "https://your.eshop.com/notify",
        "customerIp": "188.146.97.129",
        "merchantPosId": "145227",
        "description": "RTV market",
        "currencyCode": "PLN",
        "totalAmount": "21000",
        "products": [
            {"name": "Wireless mouse", "unitPrice": "15000", "quantity": "1"},
            {"name": "HDMI cable", "unitPrice": "6000", "quantity": "1"},
        ],
    }
    headers2 = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 3e5cac39-7e38-4139-8fd6-30adc06a61bd",
    }

    json_values = json.dumps(values)
    r = requests.post(
        settings.PAYU_ORDER_ENDPOINT_URL, data=json_values, headers=headers
    )

    return r.url


def sign_algorithm(data):
    """ PayU integration """

    customerip = "185.21.84.12"
    merchantposid = str(settings.POS_ID)
    description = data["secret_key"]
    totalamount = data["price"]
    currencycode = "PLN"
    productname = data["secret_key"]
    productprice = data["price"]
    productquantity = "1"
    notifyurl = "https://nativeservice.pl"
    continueurl = f"{settings.HOST_URL}/payment_done/{data['secret_key']}/"
    encrypt_value = hashlib.sha256()

    concatenation = parse.quote_plus(
        f"continueUrl={continueurl}&currencyCode={currencycode}&customerIp={customerip}&description={description}&merchantPosId={merchantposid}&notifyUrl={notifyurl}&products[0].name={productname}&products[0].quantity={productquantity}&products[0].unitPrice={productprice}&totalAmount={totalamount}&{settings.MD5}"
    )
    print(concatenation)
    encrypt_value.update(concatenation.encode("utf-8"))
    print(encrypt_value)
    print(encrypt_value.hexdigest())

    data_set = {
        "continueUrl": continueurl,
        "currencyCode": currencycode,
        "customerIp": customerip,
        "description": description,
        "merchantPosId": settings.POS_ID,
        "notifyUrl": notifyurl,
        "productname": productname,
        "productquantity": productquantity,
        "productunitPrice": productprice,
        "totalAmount": totalamount,
        "signature": encrypt_value.hexdigest(),
    }

    data.update(data_set)

    return data
