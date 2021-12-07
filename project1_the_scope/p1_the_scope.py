import click
import requests
import configparser

from netaddr import *
from prettytable import PrettyTable

cfg = configparser.ConfigParser()
cfg.read('ipgeo.cfg')

API_KEY = cfg.get('KEYS','API_KEY',raw='')
base_url = f'https://api.ipgeolocation.io/ipgeo?apiKey={API_KEY}'


def get_ipgeolocation(ipaddr):
    r = requests.get(base_url + f'&ip={ipaddr}')
    results = r.json()
    x = PrettyTable()
    x.field_names = ['Key','Value']

    for item in results:
        if item in ['ip','isp','country_name','city','state_prov','latitude','longitude']:
            x.add_row([item, results.get(item)])
    
    linebreak = '-**-'*20
    print(f'IP:\t{ipaddr}')
    print(f'{x}\n\n{linebreak}\n')


@click.command()
@click.option('-i', '--ip', 'ipaddr')
@click.option('-f', '--filename', 'filename')
@click.option('-t', '--type', 'option_type', required=True)
def main(option_type, ipaddr, filename):
    print('********** SCOPE **********\n')
    if option_type == 'ip':
        if IPAddress(ipaddr):
            get_ipgeolocation(ipaddr)
    elif option_type == 'file':
        with open(filename, 'r') as f:
            ip_list = [line.strip() for line in f]
        for ip in ip_list:
            if IPAddress(ip):
                get_ipgeolocation(ip)
    elif option_type == 'all':
        with open(filename,'r') as f:
            all_list = [line.strip() for line in f]
        for line in all_list:
            if IPSet([line]):
                for ip in IPSet([line]):
                    # print(ip)
                    get_ipgeolocation(line)
                    

if __name__ == '__main__':
    main()
