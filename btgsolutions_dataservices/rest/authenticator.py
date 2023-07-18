import requests
import json
import jwt
import time
from ..config import url_apis
from ..exceptions import BadResponse

class Authenticator:
    def __init__(self, api_key) -> None:
        self.api_key = api_key
        self._token = self.get_new_token()

    def get_new_token(self):
        url = f"{url_apis}/authenticate"
        headersList = {
            "Content-Type": "application/json" 
        }
        payload = json.dumps({
            "api_key": self.api_key,
            "client_id": f"btgsolutions-client-python"
        })
        response = requests.request("POST", url, data=payload,  headers=headersList)
        if response.status_code == 200:
            token =  json.loads(response.text).get('AccessToken')
            if not token:
                raise Exception('Something has gone wrong while authenticating: No token as response.')
        else:
            response = json.loads(response.text)
            raise BadResponse(f'Error: {response.get("ApiClientError")}.\n{response.get("SuggestedAction")}')
        
        return token
    
    @property
    def token(self):
        token_decoded = jwt.decode(self._token, options={"verify_signature": False})
        exp = token_decoded.get("exp")
        
        if int(time.time()) >= exp:
            self._token = self.get_new_token()
        
        return self._token
    
