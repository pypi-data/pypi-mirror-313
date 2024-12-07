import boto3
import json
import jwt
from datetime import datetime, timezone
from botocore.exceptions import ClientError

class BorneoAuthProviderConfig:
    def __init__(self, config):
        self.token = config['token']
        self.region = config['region']
        self.clientId = config['clientId']
        self.secretHash = config['secret']
        self.apiEndpoint = config['apiEndpoint']
        self.idToken = None
        self.client = boto3.client('cognito-idp', region_name=config['region'])

    @staticmethod
    def fromConfigFile(config_file_path):
        try:
            with open(config_file_path, 'r') as file:
                config = json.load(file)
            return BorneoAuthProviderConfig(config)
        except FileNotFoundError:
            print("Config file not found.")
            return None
        except json.JSONDecodeError:
            print("Error reading config file. Make sure it's in JSON format.")
            return None

    def get_api_key(self):
        if self.idToken is not None and self._is_token_expired() is False:
            return self.idToken
        else:
            return self._generate_id_token()

    def get_api_endpoint(self):
        try:
            return self.apiEndpoint

        except ClientError as e:
            print("Error:", e.response['Error']['Message'])
            return None

    def _generate_id_token(self):
        try:
            response = self.client.initiate_auth(
                AuthFlow='REFRESH_TOKEN_AUTH',
                AuthParameters={
                    'REFRESH_TOKEN': self.token,
                    'CLIENT_ID': self.clientId,
                    'SECRET_HASH': self.secretHash
                },
                ClientId=self.clientId
            )

            self.idToken = response['AuthenticationResult']['IdToken']
            return self.idToken

        except ClientError as e:
            print("Error:", e.response['Error']['Message'])
            return None

    def _is_token_expired(self):
        try:
            decoded_token = jwt.decode(self.idToken, algorithms=['RS256'], options={'verify_signature': False})
            exp_timestamp = decoded_token.get('exp')
            if exp_timestamp:
                exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
                return exp_datetime <= datetime.now(timezone.utc)
            else:
                return False  # No expiration claim
        except jwt.ExpiredSignatureError:
            return True  # Token is expired
        except jwt.InvalidTokenError:
            return True  # Token is invalid
