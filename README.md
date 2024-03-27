# bjornlunden_document_downloader

A python script to download and organize documents from Bjorn Lundén API.


## First time setup

#### Get API access

Get an API key (integratörskonto) by filling out the form at https://developer.bjornlunden.se/get-started/

#### Enable endpoints

Once you have the API key you will have to email api@bjornlunden.se and ask them to enable to following endpoints for your API clientId:

```
POST: /token
GET: /common/client
GET: /details
GET: /document
GET: /account
GET: /journal/entry/batch
GET: /document/{id}/meta
GET: /document/asPdf/{id}
```

#### Add integration in your Björn Lundén app

You will need to manually activate the integration on the live database. This is done by following these steps:

1. Log in to the company that will activate the connection - either in BL Administration or BL App
1. Click on "additional services" (in BL Administration) or "integrations" (in BL app)
1. Click on the gear icon in the upper right corner
1. Under "connect integrator" paste the integration's Public_key (The integrator can retrieve this public_key by hitting GET common/me via the API.)
1. Then click "activate integration"
1. Done.

To get the `Public_key` in step 4, run the script with the `-m` option to print out the response from `common/me` endpoint:

```bash
python3 bjornlunden_document_downloader.py -c config.yaml -o tmp -m
```

## Usage

```bash
python3 bjornlunden_document_downloader.py [-h] -c CONFIG -o OUTPUT_DIR [-s STARTDATE] [-e ENDDATE] [-m]

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to the config YAML file
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Path to the output directory
  -s STARTDATE, --startdate STARTDATE
                        Start date for journal entries. Default is {year-1}-01-01.
  -e ENDDATE, --enddate ENDDATE
                        End date for journal entries. Default is {year-1}-12-31.
  -m, --me              Print out information about your own API user and exits.

```

It will use the credentials stored in the `CONFIG` file and save all documents in `OUTPUT_DIR`, organized by account. Each document will be named

`{date}_{amount}_{description}.pdf`

which is compatible to be loaded into [Forbok](https://github.com/dahlo/forbok-cli), a script to generate a [förenklad bokslut](https://www.google.com/search?q=f%C3%B6renklat+bokslut).

## Config file

Make a copy of the template file and modify it:

```bash
cp config.yaml.dist config.yaml
vim config.yaml
```

The `user_key` will have to be fetched, unless you already have it. Run the script once without `user_key` defined and the script will print out a list of all connected compaines and their `publicKeys`. Take the `publicKey` for the company you want to interact with and set as `user_key` in `config.yaml`.

```bash
# run
python3 bjornlunden_document_downloader.py -c config.yaml -o test

# output
Missing user key in the config file. Select one from the list of connected companies:
SandboxCompany:	2466f56-3hws-afaf3-fake-userkeyjhk
```



