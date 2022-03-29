import shodan
import argparse
import textwrap

def get_args():
    parser = argparse.ArgumentParser(
        description="Bulk IP lookup in Shodan",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''
        py lookup-ip.py -ip "8.8.8.8"
        py lookup-ip.py -ip "8.8.8.8, 8.8.4.4"
        py lookup-ip.py -f ./ips.txt
        ''')
    )

    parser.add_argument('-ip', action='store', type=str, required=False, help="one or more ips to lookup in csv format")
    parser.add_argument('-f', '--file', action='store', type=str, required=False, help="file containing one or more ips per line")

    args = parser.parse_args()

    args_dict = vars(args)

    return args_dict


def read_api_key():
    """read the api_key.txt file in the current directory

    returns:
    -------
    api_key : str
        the shodan api key
    """

    try:
        # windows compatible
        f = open('.//api_key.txt')
    except:
       # linux compatible
       f = open('./api_key.txt')

    line = f.read()
    api_key = line.strip()
        
    return api_key


def main():
    args = get_args()
    ip_file_path = args['file']
    
    if ip_file_path:
        ip_lookups = read_ip_file(ip_file_path)
    else:
        ips = args['ip']
        ip_lookups = parse_ips(ips) # return a list of ips to lookup

    # read api key can authenticate
    api_key = read_api_key()
    shodanObj = shodan.Shodan(api_key)
    
    # look up ips
    hosts = lookup_ips(shodanObj, ip_lookups)
    
    # print shodan url for hosts found in shodan
    for host in hosts:
        ipAdress = host['ip_str']
        print(f"https://www.shodan.io/host/{ipAdress}")


def parse_ips(ips):
    """parse the commandline ips supplied

    parameters:
    -----------
    ips : str
        one or more ips in csv format

    returns:
    --------
    list_ips : list
        contains ips to use with shodan
    """

    list_ips = []

    parts = ips.split(',')
    for part in parts:
        ip = part.strip()
        list_ips.append(ip)
    
    return list_ips

def lookup_ips(shodanObj, ips):
    """query ip in shodan

    parameters:
    -----------
    shodanObj : shodan
        shodan api obj
    ips : list
        contains ips to lookup in shodan
    
    returns:
    --------
    hostObjs : list
        one or more shodan host json objs
    """

    hostObjs = []

    for ip in ips:
        host = shodanObj.host(ip)
        hostObjs.append(host)

    return hostObjs

def bulk_lookup_ips(shodanObj, ips):
    """query many ips in shodan

    Paid account only access

    parameters:
    -----------
    shodanObj : shodan
        shodan api obj
    ips : list
        contains ips to lookup in shodan

    returns:
    --------
    hostObjs : list
        many shodan host json objs
    """

    hosts = shodanObj.host(ips)

    return hostObjs

def read_ip_file(ip_file_path):
    """read ips from txt file

    parameters:
    -----------
    ip_file_path : str
        file path to txt with one or more ips

    returns:
    --------
    ip_list : list
        contains ips to lookup in shodan
    """

    ip_list = []

    with open(ip_file_path) as f:
        lines = f.readlines()
        
        for line in lines:
            ip = line.strip()
            ip_list.append(ip)
    
    return ip_list


if __name__ == "__main__" :
    main()