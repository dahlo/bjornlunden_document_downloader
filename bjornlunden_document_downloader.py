import argparse
import requests
import yaml
import time
import os
from pprint import pprint
import pdb

TOKEN_FILE = 'token_cache.txt'


def fetch_api_token(base_url_auth, client_id, client_secret):
    payload = {
        'grant_type': 'client_credentials',
#        'scope': '',
        'client_id': client_id,
        'client_secret': client_secret
    }

    response = requests.post(f'{base_url_auth}/token', data=payload)
    print(response.json())

    if response.status_code == 200:
        api_token = response.json().get('access_token')
        expiration_time = time.time() + 3600  # Token is valid for 1 hour

        with open(TOKEN_FILE, 'w') as file:
            file.write(f'{api_token}\n{expiration_time}')

        os.chmod(TOKEN_FILE, 0o600)  # Set file permissions to allow only the user to read

        print(f'API Token: {api_token}')
        return api_token
    else:
        print(f'Failed to fetch API token. Status code: {response.status_code}')
        return None


def list_connected_companies(base_url, api_token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }

    response = requests.get(f'{base_url}/common/client', headers=headers)

    if response.status_code == 200:
        connected_companies = response.json()
        print('Connected Companies:')
        for company in connected_companies:
            print(company)
    else:
        print(f'Failed to list connected companies. Status code: {response.status_code}')


def get_company_details(base_url, api_token, user_key):
    headers = {
        'Content-Type': 'application/json',
        'User-Key': user_key,
        'Authorization': f'Bearer {api_token}'
    }

    response = requests.get(f'{base_url}/details', headers=headers)

    if response.status_code == 200:
        company_details = response.json()
        print('Company Details:')
        print(company_details)
    else:
        print(f'Failed to get company details. Status code: {response.status_code}')
        pdb.set_trace()


def get_cached_token():
    try:
        with open(TOKEN_FILE, 'r') as file:
            api_token, expiration_time = file.read().splitlines()

        if float(expiration_time) > time.time():
            return api_token
    except (FileNotFoundError, ValueError):
        pass

    return None

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Fetch API token using client ID and client secret from config YAML file')
    parser.add_argument('config_file', help='Path to the config YAML file')
    args = parser.parse_args()

    # Read the config file
    with open(args.config_file, 'r') as file:
        config = yaml.safe_load(file)

    base_url_auth = config.get('base_url_auth')
    client_id = config.get('client_id')
    client_secret = config.get('client_secret')
    base_url = config.get('base_url')
    user_key = config.get('user_key')


    if not all([base_url_auth, client_id, client_secret, base_url, user_key]):
        print('Missing required information in the config file.')
    else:
        cached_token = get_cached_token()

        if cached_token:
            print(f'Using cached API Token: {cached_token}')
        else:
            cached_token = fetch_api_token(base_url_auth, client_id, client_secret)

        if cached_token:
            list_connected_companies(base_url, cached_token)
            get_company_details(base_url, cached_token, user_key)

