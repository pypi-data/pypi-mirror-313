# AWS SSO Credential Helper

AWSの認証を、AWS SSO (IAM Identity Center)を使って組織のユーザーディレクトリと連携されているケースは多いのではないでしょうか。  
また、SSOでの認証後、各プロダクト・プロジェクト毎の専用ロールへスイッチロールが必要な場合も多いかと思います。

AWS SSO Credential Helperは、AWS SSOを通した認証と、その後のスイッチロールでの一時認証情報の取得を助けます。  

実行時には、必要に応じてブラウザにて認証確認を求められますので、許可して下さい。  
AWS SSOの認証tokenはファイルにキャッシュし、有効期間内であれば再利用します。  
また、キャッシュはホームディレクトリにファイルとして保存し、Credential Helperを使った複数のプログラムで共有して利用することができます。

## Pypi
https://pypi.org/project/aws-sso-credential-helper/

## Usage

### 1. Create Instance
```python
from aws_sso_credential_helper import CredentialHelper

credential_helper = CredentialHelper(
    start_url="d-xxxxxxxxxx.awsapps.com/start",
    region_name="ap-northeast-1"
    )
```
 - start_url : AWSアクセスポータルのURL
 - region_name : 対象とするIAM Identity Centerのリージョン

### 2. Get Credentials
```python
credentials = credential_helper.get_swrole_credentials(
    sso_account_id="123456789",
    sso_role_name="ssoRoleName",
    sw_role_arn="arn:aws:iam::123456789012:role/sw-role-name"
    )
```
 - sso_account_id : アクセスポータルのあるAWSアカウントID
 - sso_role_name : SSOでログインするロール
 - sw_role_arn : SSOでログイン後、スイッチロールする先のロールのARN

### 3. Create boto3 client with credentials
```python
lambda_client = boto3.client(
    "lambda",
    region_name="ap-northeast-1",
    aws_access_key_id=credentials["AccessKeyId"],
    aws_secret_access_key=credentials["SecretAccessKey"],
    aws_session_token=credentials["SessionToken"],
    )
```
### Credentials
```python
{
    'AccessKeyId': 'XXXXXXXXXXXXX',
    'SecretAccessKey': 'YYYYYYYYY',
    'SessionToken': 'ZZZZZZZZZZ',
    'Expiration': 有効期限,
}
```

## How to install

install from pypi
```python
pip install aws-sso-credential-helper
```

