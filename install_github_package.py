import boto3
import subprocess
import sys
import os
import json
from botocore.exceptions import ClientError


def get_secret(secret_name=None, region_name="us-east-2"):

    # secret_name = "duaa_eddtools_credentials"
    # region_name = "us-east-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']
    return json.loads(secret)

def install_package_from_github(secret_name):
    secret_name = "duaa_eddtools_credentials"
    creds = get_secret(secret_name)
   
    if not creds:
        print("GitHub credentials not found in AWS Secrets Manager.")
        sys.exit(1)

    username = creds.get("GITHUB_USERNAME")
    token = creds.get("GITHUB_TOKEN")
    repo_url = creds.get("GITHUB_REPO_URL")

    if not username or not token or not repo_url:
        print("GitHub credentials not found in AWS Secrets Manager.")
        sys.exit(1)
    # Insert credentials into repo URL
    if repo_url.startswith("https://"):
        auth_repo_url = repo_url.replace("https://", f"https://{username}:{token}@")
    else:
        print("Repository URL must start with https://")
        sys.exit(1)
    
    print("REPO URL:", auth_repo_url)

    # Install the package using pip
    subprocess.check_call([sys.executable, "-m", "pip", "install", f"git+{auth_repo_url}"])

if __name__ == "__main__":
    install_package_from_github(os.environ.get("DUAA_EDTOOLS_SECRET_NAME"))
