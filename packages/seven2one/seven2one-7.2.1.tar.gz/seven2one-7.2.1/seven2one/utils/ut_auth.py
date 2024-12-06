class AuthData:
    
    def __init__(self, client_id, token_url, token, service_account_name, service_account_secret):
        self.client_id = client_id
        self.token_url = token_url
        self.token = token
        self.service_account_name = service_account_name
        self.service_account_secret = service_account_secret

    def get_client_id(self):
        return self.client_id

