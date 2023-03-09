# Veracode Generate SCA fix report

A simple example script that a csv report with SCA findings and their fix version and latest safe version.  
It can also produce an on screen report.

## Setup

Clone this repository:

    git clone https://github.com/christyson/GenerateSCAFixReport.git
	
Install dependencies:

    cd GenerateSCAFixReport
    pip install -r requirements.txt

(Optional) Save Veracode API credentials in `~/.veracode/credentials`

    [default]
    veracode_api_key_id = <YOUR_API_KEY_ID>
    veracode_api_key_secret = <YOUR_API_KEY_SECRET>

## Usage for a single app profile or and app profile with a sandbox

`generate_SCA_FixReport.py [-h] <arguments>`

Arguments:
*  -h, --help            show this help message and exit
*  -w WORKSPACE_NAME, --workspace_name WORKSPACE_NAME
*  Works Space name to generate Issues for or by default it will do the whole organization
*  -c, --csv             Set to save the output as a CSV file.
*  -nt, --no_table       If selected a table will be output to the screen

usage: generate_SCA_FixReport.py [-h] [-w WORKSPACE_NAME] [-c] [-nt]

This script builds a csv report with SCA findings and fix version and latest safe version.


## Run

If you have saved credentials as above you can run:

`python generate_SCA_FixReport.py -c`

Otherwise you will need to set environment variables as follows:

```
export VERACODE_API_KEY_ID=<YOUR_API_KEY_ID>
export VERACODE_API_KEY_SECRET=<YOUR_API_KEY_SECRET>
python  generate_SCA_FixReport.py -c
```

Both of these methods will work.  

Note: If you specify to create a csv then the file will be in the form SCA_Fix-{}.csv
Where the {} is replaced with the time of the report.
