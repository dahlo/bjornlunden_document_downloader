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
        'scope': None,
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

        return api_token
    else:
        print(f'Failed to fetch API token. Status code: {response.status_code}')
        return None


def get_connected_companies(base_url, api_token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }

    response = requests.get(f'{base_url}/common/client', headers=headers)

    if response.status_code == 200:
        connected_companies = response.json()
        return connected_companies
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
        return company_details
    else:
        print(f'Failed to get company details. Status code: {response.status_code}')


def get_documents(base_url, api_token, user_key):
    headers = {
        'Content-Type': 'application/json',
        'User-Key': user_key,
        'Authorization': f'Bearer {api_token}'
    }

    response = requests.get(f'{base_url}/document', headers=headers)

    if response.status_code == 200:
        documents = response.json()
        return documents
    else:
        print(f'Failed to get documents. Status code: {response.status_code}')


def get_document_metadata(base_url, api_token, user_key, id):
    headers = {
        'Content-Type': 'application/json',
        'User-Key': user_key,
        'Authorization': f'Bearer {api_token}'
    }

    response = requests.get(f'{base_url}/document/{id}/meta', headers=headers)

    if response.status_code == 200:
        document = response.json()
        return document
    else:
        print(f'Failed to get document "{id}". Status code: {response.status_code}')


def get_accounts(base_url, api_token, user_key):
    headers = {
        'Content-Type': 'application/json',
        'User-Key': user_key,
        'Authorization': f'Bearer {api_token}'
    }

    response = requests.get(f'{base_url}/account', headers=headers)

    if response.status_code == 200:
        accounts_raw = response.json()
        accounts = { account['id']: account for account in accounts_raw }
        return accounts
    else:
        print(f'Failed to get document "{id}". Status code: {response.status_code}')


def fetch_journal_entries(base_url, api_token, user_key, startdate, enddate, rows=1000):
    headers = {
        'Content-Type': 'application/json',
        'User-Key': user_key,
        'Authorization': f'Bearer {api_token}'
    }

    response = requests.get(f'{base_url}/journal/entry/batch?startdate={startdate}&enddate={enddate}&rows={rows}', headers=headers)

    if response.status_code == 200:
        journal_entries = response.json()['data']
        return journal_entries
    else:
        print(f'Failed to get journal entries. Status code: {response.status_code}')


def save_document_pdf(base_url, api_token, user_key, id, file_name):
    headers = {
        'Content-Type': 'application/json',
        'User-Key': user_key,
        'Authorization': f'Bearer {api_token}'
    }

    response = requests.get(f'{base_url}/document/asPdf/{id}', headers=headers)

    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)

    else:
        print(f'Failed to get document "{id}". Status code: {response.status_code}')


# broken, use save_document_pdf instead
def get_document(base_url, api_token, user_key, id):
    headers = {
        'Content-Type': 'application/json',
        'User-Key': user_key,
        'Authorization': f'Bearer {api_token}'
    }

    response = requests.get(f'{base_url}/document/{id}', headers=headers)

    if response.status_code == 200:
        document = response.json()
        return document
    else:
        print(f'Failed to get document "{id}". Status code: {response.status_code}')


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
    parser.add_argument('-c', '--config', help='Path to the config YAML file', required=True)
    parser.add_argument('-o', '--output-dir', help='Path to the output directory', required=True)
    args = parser.parse_args()

    # Read the config file
    with open(args.config, 'r') as file:
        config = yaml.safe_load(file)

    base_url_auth = config.get('base_url_auth')
    client_id = config.get('client_id')
    client_secret = config.get('client_secret')
    base_url = config.get('base_url')
    user_key = config.get('user_key')

    output = args.output_dir

    if not all([base_url_auth, client_id, client_secret, base_url, user_key]):
        print('Missing required information in the config file.')
    else:
        cached_token = get_cached_token()

        if not cached_token:
            cached_token = fetch_api_token(base_url_auth, client_id, client_secret)

        if cached_token:
            #pprint(get_connected_companies(base_url, cached_token))
            #pprint(get_company_details(base_url, cached_token, user_key))

            # get all account data
            accounts = get_accounts(base_url, cached_token, user_key)

            # get all journal entries
            journal_entries = fetch_journal_entries(base_url, cached_token, user_key, '1920-01-01', '2023-12-31')

            # find the ones with documents
            journal_with_documents = [entry for entry in journal_entries if entry['documentIds']]
            for journal in journal_with_documents:
                for document_id in journal['documentIds']:
                    document = get_document_metadata(base_url, cached_token, user_key, document_id)

                    for entry in journal['ledgerEntries']:
                        account = accounts[entry['accountId']]

                        os.makedirs(f'{output}/{account["name"]} - {account["id"]}', exist_ok=True)
                        print(f'Saving document {document_id} as {output}/{account["name"]} - {account["id"]}/{entry["date"]}_{entry["amount"]}_{journal["journalEntryText"]} - {journal["journalName"]} - {entry["text"]}.pdf')
                        save_document_pdf(base_url, cached_token, user_key, document_id, f'{output}/{account["name"]} - {account["id"]}/{entry["date"]}_{entry["amount"]}_{journal["journalEntryText"]} - {journal["journalName"]} - {entry["text"]}.pdf')



        else:
            print('Failed to fetch API token. Exiting...')

