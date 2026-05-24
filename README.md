# dns-zone-transfer
Attempt to perform an unauthorized DNS Zone Transfer

DNS Zone Transfer (also called AXFR — Authoritative Zone Transfer) is a legitimate DNS mechanism that becomes a serious information disclosure vulnerability when misconfigured.
What is a DNS Zone Transfer?
DNS Zone Transfer is a feature in the DNS protocol that allows one DNS server to request a full copy of all DNS records for a domain (the entire "zone") from another DNS server.
It was originally designed for replication:
A primary (master) DNS server holds the authoritative records.
Secondary (slave) DNS servers request a full zone transfer from the primary so they stay in sync.
This is done using the AXFR query type.
Normal/secure behavior:
The primary DNS server is configured to only allow zone transfers from specific authorized secondary servers (usually via IP address ACLs or TSIG cryptographic keys).
Vulnerable behavior:
The DNS server allows anyone on the internet to request a full zone transfer with no authentication or restrictions.
--=-=-=-=-=-=-==-=-==-=-=-=-=-=-=-=-=-=-=.............____________________

1. Place zone_transfer_checker_simple.py in the same folder as your domain list (domainlist.txt)

2. Run the following in your command prompt:
python3 zone_transfer_checker_simple.py domainlist.txt

3. It will run through your list and output the results. Make sure the list only comtains the top level domains (example: google.com) it will break if there are subdomains (example: maps.google.com)
