import anvil.server
import anvil.http
import json

# Configure with your PayPal credentials
PAYPAL_CLIENT_ID = "AYyCqWPxgAwALbUI3nzjfDdGmJQoY4nvnKitD9UsqMzZ7h4aw4H905M8n2SRueEuu3pXzclUC4lMNIBU"
PAYPAL_SECRET = "EFXEaY9axulWHy6LFlsOIhDy-jazYoPLZijnIVrWcRFfk1qOxbiLljkQIaIP5k5AXsH8Egr1TXxe393c"
PAYPAL_BASE_URL = "https://api-m.sandbox.paypal.com"  # Change to https://api.paypal.com for live

import anvil.server
import anvil.http
import json
import base64

def _get_auth_token():
    """Get OAuth2 token from PayPal"""
    auth_str = f"{PAYPAL_CLIENT_ID}:{PAYPAL_SECRET}"
    auth_bytes = base64.b64encode(auth_str.encode('ascii')).decode('ascii')
    
    headers = {
        "Authorization": f"Basic {auth_bytes}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        response = anvil.http.request(
            url=f"{PAYPAL_BASE_URL}/v1/oauth2/token",
            method="POST",
            headers=headers,
            data="grant_type=client_credentials"
        )
        return response['access_token']
    except anvil.http.HttpError as e:
        raise Exception(f"Failed to get auth token: {str(e)}")

@anvil.server.callable
def create_payment(amount, currency="USD", description=""):
    """Create a PayPal payment"""
    import requests


    order_response = requests.post(
        f"{PAYPAL_BASE_URL}/v2/checkout/orders",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {'A21AAJ4tNNbs59iiCR60gXbkTzWQR9fiKaO3sHS9kFd3eB-63WaJdbYfhTaO3hJc-iYlPTluzbt-xQfX9BiNxD4Yq1xh5PL4g'}"
        },
        json={
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": currency,
                        "value": str(5)
                    }
                }
            ]
        }
    )
    print("order respoinseL ", order_response)
    print("linkss  ",order_response.json()['links'])
    auth_response = requests.post(
            f"{PAYPAL_BASE_URL}/v1/oauth2/token",
            auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={"grant_type": "client_credentials"}
        )
    print("Auth: ", auth_response)
    print("Auth token: ", auth_response.json()["access_token"])
    try:
        access_token = _get_auth_token()
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
            "PayPal-Request-Id": anvil.server.context.get_client_ip_address()
        }
        
        payload = {
            "intent": "CAPTURE",  # Changed from "sale" to "CAPTURE" for current API
            "purchase_units": [{
                "amount": {
                    "currency_code": currency,
                    "value": str(amount)
                },
                "description": description
            }],
            "application_context": {
                "return_url": anvil.server.get_api_origin() + "/paypal/success",
                "cancel_url": anvil.server.get_api_origin() + "/paypal/cancel",
                "brand_name": "Your Business Name"  # Customize this
            }
        }
        
        response = anvil.http.request(
            url=f"{PAYPAL_BASE_URL}/v2/checkout/orders",
            method="POST",
            headers=headers,
            data=json.dumps(payload))
        
        # Find approval URL in response
        for link in response['links']:
            if link['rel'] == 'approve':
                return {'status': 'success', 'approval_url': link['href']}
        
        return {'status': 'error', 'message': 'No approval URL found'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@anvil.server.http_endpoint("/paypal/success")
def paypal_success(**params):
    """Handle successful PayPal payment"""
    payment_id = params.get('paymentId')
    payer_id = params.get('PayerID')
    
    # Execute the payment
    auth = anvil.http.basic_auth(user=PAYPAL_CLIENT_ID, password=PAYPAL_SECRET)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {auth}"
    }
    
    try:
        execute_response = anvil.http.request(
            url=f"{PAYPAL_BASE_URL}/v1/payments/payment/{payment_id}/execute",
            method="POST",
            headers=headers,
            data=json.dumps({"payer_id": payer_id}))
        
        # Process the successful payment here
        # You might want to update your database, send confirmation emails, etc.
        
        return anvil.server.HttpResponse(302, headers={"Location": "/payment-success"})
    
    except anvil.http.HttpError as e:
        return anvil.server.HttpResponse(302, headers={"Location": f"/payment-error?message={str(e.content)}"})

@anvil.server.http_endpoint("/paypal/cancel")
def paypal_cancel(**params):
    """Handle cancelled PayPal payment"""
    return anvil.server.HttpResponse(302, headers={"Location": "/payment-cancelled"})