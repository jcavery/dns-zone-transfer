#!/usr/bin/env python3
"""
Simple DNS Zone Transfer Checker
Replicates: for ns in $(dig +short NS example.com); do dig axfr @$ns example.com; done
"""

import subprocess
import sys
import os

def get_nameservers(domain):
    """Get name servers using dig"""
    result = subprocess.run(
        ["dig", "+short", "NS", domain],
        capture_output=True, text=True, timeout=10
    )
    return [line.strip().rstrip('.') for line in result.stdout.splitlines() if line.strip()]

def check_zone_transfer(domain, nameserver):
    print(f"\n[*] Checking {domain} against {nameserver}")
    print("-" * 60)
    
    result = subprocess.run(
        ["dig", "axfr", f"@{nameserver}", domain],
        capture_output=True, text=True, timeout=15
    )
    
    output = result.stdout
    print(output)
    
    if "Transfer failed" in output or "REFUSED" in output:
        print(f"[+] AXFR refused by {nameserver}\n")
    elif domain in output and "SOA" in output:
        print(f"[!!!] SUCCESS: Zone transfer allowed from {nameserver}\n")
    else:
        print(f"[+] No zone data returned from {nameserver}\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: python zone_transfer_checker_simple.py domains.txt")
        sys.exit(1)

    domains_file = sys.argv[1]

    if not os.path.isfile(domains_file):
        print(f"[!] File not found: {domains_file}")
        sys.exit(1)

    print("=" * 60)
    print("Simple DNS Zone Transfer Checker")
    print("=" * 60)
    print("[!] Only use on domains you are authorized to test!\n")

    with open(domains_file, 'r') as f:
        domains = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    for domain in domains:
        print(f"\n{'='*60}")
        print(f"Domain: {domain}")
        print('='*60)
        
        nameservers = get_nameservers(domain)
        if not nameservers:
            print(f"[!] No name servers found for {domain}")
            continue

        print(f"[i] Name servers: {', '.join(nameservers)}")
        
        for ns in nameservers:
            check_zone_transfer(domain, ns)

if __name__ == "__main__":
    main()