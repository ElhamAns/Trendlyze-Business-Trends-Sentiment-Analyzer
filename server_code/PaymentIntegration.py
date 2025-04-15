import anvil.files
from anvil.files import data_files
import anvil.server
import anvil.http
import json
import requests
import base64
from anvil.tables import app_tables
from datetime import datetime
# Configure with your PayPal credentials
PAYPAL_CLIENT_ID = "AYyCqWPxgAwALbUI3nzjfDdGmJQoY4nvnKitD9UsqMzZ7h4aw4H905M8n2SRueEuu3pXzclUC4lMNIBU"
PAYPAL_SECRET = "EFXEaY9axulWHy6LFlsOIhDy-jazYoPLZijnIVrWcRFfk1qOxbiLljkQIaIP5k5AXsH8Egr1TXxe393c"
PAYPAL_BASE_URL = "https://api-m.sandbox.paypal.com"  # Change to https://api.paypal.com for live


def _get_auth_token():
    """Get OAuth2 token from PayPal"""
    auth_str = f"{PAYPAL_CLIENT_ID}:{PAYPAL_SECRET}"
    auth_bytes = base64.b64encode(auth_str.encode('ascii')).decode('ascii')
    
    headers = {
        "Authorization": f"Basic {auth_bytes}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        print("in try")
        response = requests.post(
            url=f"{PAYPAL_BASE_URL}/v1/oauth2/token",
            headers=headers,
            data="grant_type=client_credentials"
        )
        return response.json()['access_token']
    except anvil.http.HttpError as e:
        raise Exception(f"Failed to get auth token: {str(e)}")

@anvil.server.callable
def create_payment(amount, currency="USD", description=""):
    """Create a PayPal payment"""
    try:
        print("here")
        access_token = _get_auth_token()
        print("here")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        
        payload = {
            "intent": "CAPTURE", 
            "purchase_units": [{
                "amount": {
                    "currency_code": currency,
                    "value": str(amount)
                },
                "description": description
            }],
            "application_context": {
                "return_url": anvil.server.get_app_origin() + "/#success-payment",
                "cancel_url": anvil.server.get_app_origin() + "/#cancel-payment",
                "brand_name": "Business Trend"  # Customize this
            }
        }
        print("origin: ", anvil.server.get_app_origin())
        print("header: ", headers)
        response = requests.post(
            url=f"{PAYPAL_BASE_URL}/v2/checkout/orders",
            headers=headers,
            data=json.dumps(payload)
        )
        print("response: ", response)
        # Find approval URL in response
        for link in response.json()['links']:
            if link['rel'] == 'approve':
                return {'status': 'success', 'approval_url': link['href']}
        
        return {'status': 'error', 'message': 'No approval URL found'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}



@anvil.server.callable
def test_cancel_endpoint():
    """Test the cancel endpoint directly"""
    return anvil.server.call('paypal_cancel')


@anvil.server.callable
def update_user_payment(token):
  url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{token}"
  auth_str = f"{PAYPAL_CLIENT_ID}:{PAYPAL_SECRET}"
  auth_bytes = base64.b64encode(auth_str.encode('ascii')).decode('ascii')
    
  headers = {
        "Authorization": f"Basic {auth_bytes}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
  response = requests.get(url, headers=headers)
  if response.json().get('status') and response.json().get('status') == 'APPROVED':
    client = anvil.server.call('get_current_client')
    amount = response.json()['purchase_units'][0]['amount']['value']
    subscription_package = app_tables.subscription_types.get(amount=amount)
    if client and subscription_package:
      client['subscription_package'] = subscription_package
      client['subsribed_at'] = datetime.now()
      


@anvil.server.callable
def update_users_trail_payment():
  client = anvil.server.call('get_current_client')
  subscription_package = app_tables.subscription_types.get(type='Trial')
  client['subscription_package'] = subscription_package
  client['subsribed_at'] = datetime.now()