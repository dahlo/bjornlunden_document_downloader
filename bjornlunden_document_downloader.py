import argparse
import requests
import yaml
import time
import os
from pprint import pprint
import pdb

TOKEN_FILE = 'token_cache.txt'


def create_file(file_path):
    """
    Creates a file if it doesn't exist
    :param file_path: The path to the file
    """

    with open(file_path, 'a'):
        pass


def fetch_api_token(base_url_auth, client_id, client_secret):
    """
    Fetches an API token using the client ID and client secret provided
    :param base_url_auth: The base URL for the authentication endpoint
    :param client_id: The client ID
    :param client_secret: The client secret
    :return: The API token if successful, None otherwise
    """

    # Set the payload
    payload = {
        'grant_type': 'client_credentials',
        'scope': None,
        'client_id': client_id,
        'client_secret': client_secret
    }

    # Make the request
    response = requests.post(f'{base_url_auth}/token', data=payload)

    # Check the response
    if response.status_code == 200:
        api_token = response.json().get('access_token')
        expiration_time = time.time() + 3600  # Token is valid for 1 hour

        # Create the token file if it doesn't exist
        create_file(TOKEN_FILE)

        # Set the file permissions
        os.chmod(TOKEN_FILE, 0o600)  # Set file permissions to allow only the user to read

        # Cache the token
        with open(TOKEN_FILE, 'w') as file:
            file.write(f'{api_token}\n{expiration_time}')


        return api_token
    else:
        print(f'Failed to fetch API token. Status code: {response.status_code}')
        return None


def get_connected_companies(base_url, api_token):
    """
    Lists the companies connected to the API token
    :param base_url: The base URL for the API
    :param api_token: The API token
    :return: A list of connected companies if successful, None otherwise
    """

    # Set the headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }

    # Make the request
    response = requests.get(f'{base_url}/common/client', headers=headers)

    # Check the response
    if response.status_code == 200:
        connected_companies = response.json()
        return connected_companies
    else:
        print(f'Failed to list connected companies. Status code: {response.status_code}')


def get_company_details(base_url, api_token, user_key):
    """
    Fetches details about the company
    :param base_url: The base URL for the API
    :param api_token: The API token
    :param user_key: The user key
    :return: Company details if successful, None otherwise
    """

    # Set the headers
    headers = {
        'Content-Type': 'application/json',
        'User-Key': user_key,
        'Authorization': f'Bearer {api_token}'
    }

    # Make the request
    response = requests.get(f'{base_url}/details', headers=headers)

    # Check the response
    if response.status_code == 200:
        company_details = response.json()
        return company_details
    else:
        print(f'Failed to get company details. Status code: {response.status_code}')


def get_documents(base_url, api_token, user_key):
    """
    Fetches all documents
    :param base_url: The base URL for the API
    :param api_token: The API token
    :param user_key: The user key
    :return: A list of documents if successful, None otherwise
    """

    # Set the headers
    headers = {
        'Content-Type': 'application/json',
        'User-Key': user_key,
        'Authorization': f'Bearer {api_token}'
    }

    # Make the request
    response = requests.get(f'{base_url}/document', headers=headers)

    # Check the response
    if response.status_code == 200:
        documents = response.json()
        return documents
    else:
        print(f'Failed to get documents. Status code: {response.status_code}')


def get_document_metadata(base_url, api_token, user_key, id):
    """
    Fetches metadata about a document
    :param base_url: The base URL for the API
    :param api_token: The API token
    :param user_key: The user key
    :param id: The document ID
    :return: Document metadata if successful, None otherwise
    """

    # Set the headers
    headers = {
        'Content-Type': 'application/json',
        'User-Key': user_key,
        'Authorization': f'Bearer {api_token}'
    }

    # Make the request
    response = requests.get(f'{base_url}/document/{id}/meta', headers=headers)

    # Check the response
    if response.status_code == 200:
        document = response.json()
        return document
    else:
        print(f'Failed to get document "{id}". Status code: {response.status_code}')


def get_accounts(base_url, api_token, user_key):
    """
    Fetches all accounts
    :param base_url: The base URL for the API
    :param api_token: The API token
    :param user_key: The user key
    :return: A list of accounts if successful, None otherwise
    """

    # Set the headers
    headers = {
        'Content-Type': 'application/json',
        'User-Key': user_key,
        'Authorization': f'Bearer {api_token}'
    }

    # Make the request
    response = requests.get(f'{base_url}/account', headers=headers)

    if response.status_code == 200:
        accounts_raw = response.json()

        # create a dictionary with account id as key
        accounts = { account['id']: account for account in accounts_raw }
        return accounts
    else:
        print(f'Failed to get document "{id}". Status code: {response.status_code}')


def fetch_journal_entries(base_url, api_token, user_key, startdate, enddate, rows=1000):
    """
    Fetches journal entries between two dates
    :param base_url: The base URL for the API
    :param api_token: The API token
    :param user_key: The user key
    :param startdate: The start date in the format 'YYYY-MM-DD'
    :param enddate: The end date in the format 'YYYY-MM-DD'
    :param rows: The number of rows to fetch
    :return: A list of journal entries if successful, None otherwise
    """

    # Set the headers
    headers = {
        'Content-Type': 'application/json',
        'User-Key': user_key,
        'Authorization': f'Bearer {api_token}'
    }

    # Make the request
    response = requests.get(f'{base_url}/journal/entry/batch?startdate={startdate}&enddate={enddate}&rows={rows}', headers=headers)

    # Check the response
    if response.status_code == 200:
        journal_entries = response.json()['data']
        return journal_entries
    else:
        print(f'Failed to get journal entries. Status code: {response.status_code}')


def save_document_pdf(base_url, api_token, user_key, id, file_name):
    """
    Fetches a document as PDF and saves it to a file
    :param base_url: The base URL for the API
    :param api_token: The API token
    :param user_key: The user key
    :param id: The document ID
    :param file_name: The name of the file to save the PDF to
    """

    # Set the headers
    headers = {
        'Content-Type': 'application/json',
        'User-Key': user_key,
        'Authorization': f'Bearer {api_token}'
    }

    # Make the request
    response = requests.get(f'{base_url}/document/asPdf/{id}', headers=headers)

    # Check the response
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
    else:
        print(f'Failed to get document "{id}". Status code: {response.status_code}')


# broken, use save_document_pdf instead
def get_document(base_url, api_token, user_key, id):
    """
    Fetches a document
    :param base_url: The base URL for the API
    :param api_token: The API token
    :param user_key: The user key
    :param id: The document ID
    :return: The document if successful, None otherwise
    """

    # Set the headers
    headers = {
        'Content-Type': 'application/json',
        'User-Key': user_key,
        'Authorization': f'Bearer {api_token}'
    }

    # Make the request
    response = requests.get(f'{base_url}/document/{id}', headers=headers)

    # Check the response
    if response.status_code == 200:
        document = response.json()
        return document
    else:
        print(f'Failed to get document "{id}". Status code: {response.status_code}')


def get_cached_token():
    """
    Reads the cached API token from the token file
    :return: The API token if it's still valid, None otherwise
    """

    # Check if the token file exists and if the token is still valid
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

    # Extract the required information from the config file
    base_url_auth = config.get('base_url_auth')
    client_id = config.get('client_id')
    client_secret = config.get('client_secret')
    base_url = config.get('base_url')
    user_key = config.get('user_key')

    # Extract the output directory
    output = args.output_dir

    # Check if all required information is present
    if not all([base_url_auth, client_id, client_secret, base_url]):
        print('Missing required information in the config file. Required fields: base_url_auth, client_id, client_secret, base_url')

    # Check if the user key is missing
    elif not user_key:
        print('Missing user key in the config file. Select one from the list of connected companies:')
        connected_companies = get_connected_companies(base_url, fetch_api_token(base_url_auth, client_id, client_secret))
        for company in connected_companies:
            print(f'{company["name"]}:\t{company["publicKey"]}')

    else:

        # Fetch the API token
        cached_token = get_cached_token()

        # Fetch the API token if it's not cached
        if not cached_token:
            cached_token = fetch_api_token(base_url_auth, client_id, client_secret)

        if cached_token:

            # Get company details
            #pprint(get_connected_companies(base_url, cached_token))
            #pprint(get_company_details(base_url, cached_token, user_key))
            #pdb.set_trace()

            # get all account data
            accounts = get_accounts(base_url, cached_token, user_key)

            # get all journal entries
            journal_entries = fetch_journal_entries(base_url, cached_token, user_key, '1920-01-01', '2023-12-31')

            # find the ones with documents
            journal_with_documents = [entry for entry in journal_entries if entry['documentIds']]
            for journal in journal_with_documents:

                # get the metadata for each document
                for document_id in journal['documentIds']:
                    document = get_document_metadata(base_url, cached_token, user_key, document_id)

                    # save the document as pdf
                    for entry in journal['ledgerEntries']:

                        # get the account name
                        account = accounts[entry['accountId']]

                        # create the output directory if it doesn't exist
                        os.makedirs(f'{output}/{account["name"]} - {account["id"]}', exist_ok=True)

                        # save the document as pdf
                        print(f'Saving document {document_id} as {output}/{account["name"]} - {account["id"]}/{entry["date"]}_{entry["amount"]}_{journal["journalEntryText"]} - {journal["journalName"]} - {entry["text"]}.pdf')
                        save_document_pdf(base_url, cached_token, user_key, document_id, f'{output}/{account["name"]} - {account["id"]}/{entry["date"]}_{entry["amount"]}_{journal["journalEntryText"]} - {journal["journalName"]} - {entry["text"]}.pdf')



        else:
            print('Failed to fetch API token. Exiting...')

