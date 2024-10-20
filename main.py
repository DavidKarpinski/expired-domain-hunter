#!/usr/bin/env python3

import whois
import datetime
import argparse


def check_domain_status(domain):
    try:
        domain_info = whois.whois(domain)
        expiration_date = domain_info.expiration_date

        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]

        today = datetime.datetime.today()

        if expiration_date:
            days_to_expire = (expiration_date - today).days

            if days_to_expire < 0:
                return expiration_date, 'Expired'
            elif days_to_expire < 30:
                return expiration_date, 'Close to expiration'
            else:
                return expiration_date, 'Up to date'
        else:
            return None, 'Not Avaiable'
    except KeyboardInterrupt:
        print('EXITING')
        exit(0)
    except Exception as e:
        return None, f'Error while verifying the domain: {str(e)}'

def main(wordlist_path):
    try:
        with open(wordlist_path, 'r') as file:
            domains = file.readlines()
    except Exception as e:
        print(f'Error while opening the wordlist: {str(e)}')
        return

    print('Domain\t\tExpiration Date\t\tStatus'.upper())

    for domain in domains:
        domain = domain.strip()
        expiration_date, status = check_domain_status(domain)
        print(f'{domain}\t{expiration_date}\tStatus: {status}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check the expiration date of domains')
    parser.add_argument('wordlist', help='Path to domain wordlist')
    args = parser.parse_args()

    main(args.wordlist)
