# bjornlunden_document_downloader

A python script to download and organize documents from Bjorn Lundén API.

## Usage

```bash
python3 bjornlunden_document_downloader.py [-h] -c CONFIG -o OUTPUT_DIR [-s STARTDATE] [-e ENDDATE]

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
SandboxCompany:	2466f56-jsfd-45f7-jse7-345346jhk
```



