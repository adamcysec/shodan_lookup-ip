# Shodan api

# lookup-ip.py

## Synopsis
This script uses the Shodan api to lookup one or more IPs.

## Description
This script looks up one or more ips in Shodan using a free account.

You can utilize parameter `--bulk` if you have a paid account.

## Usage

**Parameter -ip**
- type : str
- one or more ips in csv format

**Parameter -f, --file**
- type : str
- the file path of your txt with one ip per line

**Parameter -b, --bulk**
- type : boolean
- use shodan's builk lookup api

**Example 1**

`py lookup-ip.py -ip "8.8.8.8`

- look up on ip

**Example 2**

`py lookup-ip.py -ip "8.8.8.8, 8.8.4.4`

- look up 2 or more ips in csv format

**Example 3**

`py lookup-ip.py -f ./ips.txt`

- look up all ips in a txt
- one ip per line
