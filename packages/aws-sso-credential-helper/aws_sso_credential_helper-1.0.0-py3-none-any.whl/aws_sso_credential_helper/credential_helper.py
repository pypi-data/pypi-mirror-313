import time
import boto3
import botocore
import webbrowser
import json
import os
import pathlib
import hashlib

class CredentialHelper:
    _token = None

    def __init__(self, start_url:str, region_name:str):
        self.start_url = start_url
        self.region_name = region_name
        file_key = hashlib.md5(f"{start_url}{region_name}".encode()).hexdigest()
        self._cache_file = pathlib.Path.home().joinpath(f".credential_helper_cache_{file_key}.json")
        if os.path.exists(self._cache_file):
            with open(self._cache_file) as f:
                self.role_credentials = json.load(f)
        else:
            self.role_credentials = {}

    def _save_role_credentials(self):
        with open(self._cache_file, "w") as f:
            json.dump(self.role_credentials, f, indent=2)

    def _get_sso_token(self):
        if self._token:
            return self._token

        ssooidc_client = boto3.client("sso-oidc", region_name=self.region_name)
        register_client_response = ssooidc_client.register_client(
            clientName="SSO_CREDENTIAL_HELPER",
            clientType="public",
        )

        start_device_authorization_response = ssooidc_client.start_device_authorization(
            clientId=register_client_response["clientId"],
            clientSecret=register_client_response["clientSecret"],
            startUrl=self.start_url,
        )

        webbrowser.open(start_device_authorization_response["verificationUriComplete"])
        interval = start_device_authorization_response.get("interval", 5)

        while True:
            try:
                create_token_response = ssooidc_client.create_token(
                    clientId=register_client_response["clientId"],
                    clientSecret=register_client_response["clientSecret"],
                    grantType="urn:ietf:params:oauth:grant-type:device_code",
                    deviceCode=start_device_authorization_response["deviceCode"],
                )
                self._token = create_token_response["accessToken"]
                return self._token
            except ssooidc_client.exceptions.SlowDownException:
                interval += self._SLOW_DOWN_DELAY
            except ssooidc_client.exceptions.AuthorizationPendingException:
                pass
            except ssooidc_client.exceptions.ExpiredTokenException:
                raise botocore.exceptions.PendingAuthorizationExpiredError()
            time.sleep(interval)

    def get_sso_credentials(self, sso_account_id:str, sso_role_name:str):
        '''
        sso_account_id: str Account ID
        sso_role_name: str  Role Name
        '''
        print(sso_account_id)
        print(sso_role_name)
        if self.role_credentials.get(sso_account_id, {}).get(sso_role_name):

            # 有効期限切れてなければキャッシュから取得
            if self.role_credentials[sso_account_id][sso_role_name]["expiration"] > int(time.time() * 1000):
                return self.role_credentials[sso_account_id][sso_role_name]
        sso_client = boto3.client("sso", region_name=self.region_name)
        get_role_credentials_response = sso_client.get_role_credentials(
            roleName=sso_role_name,
            accountId=sso_account_id,
            accessToken=self._get_sso_token(),
        )
        # print(get_role_credentials_response)
        self.role_credentials.setdefault(sso_account_id, {})
        self.role_credentials[sso_account_id][sso_role_name] = get_role_credentials_response["roleCredentials"]
        self._save_role_credentials()
        return get_role_credentials_response["roleCredentials"]

    def get_swrole_credentials(self, sso_account_id:str, sso_role_name: str, sw_role_arn:str):
        '''
        sso_account_id: str Account ID
        sso_role_name: str  Role Name
        sw_role_arn: str  Role ARN to assume
        '''
        sso_credentials = self.get_sso_credentials(sso_account_id, sso_role_name)
        sts_client = boto3.client(
            "sts",
            aws_access_key_id=sso_credentials.get("accessKeyId"),
            aws_secret_access_key=sso_credentials.get("secretAccessKey"),
            aws_session_token=sso_credentials.get("sessionToken"),
        )
        response = sts_client.assume_role(RoleArn=sw_role_arn, RoleSessionName="session")
        return response["Credentials"]
