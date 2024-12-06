import os
from .credential_helper import CredentialHelper

def main():
    credential_helper = CredentialHelper(
        start_url=os.environ["SSO_START_URL"],
        region_name=os.environ["SSO_REGION_NAME"]
    )
    credentials = credential_helper.get_swrole_credentials(
        sso_account_id=os.environ["SSO_ACCOUNT_ID"],
        sso_role_name=os.environ["SSO_ROLE_NAME"],
        sw_role_arn=os.environ["SSO_SW_ROLE_ARN"])
    print(credentials)

if __name__ == "__main__":
    main()