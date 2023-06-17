import geoip2.database

def get_asn_info(ip_address):
    reader = geoip2.database.Reader('GeoLite2-ASN.mmdb')  # Replace with the actual path to your GeoLite2-ASN database file
    try:
        response = reader.asn(ip_address)
        asn = response.autonomous_system_organization
        return asn
    except geoip2.errors.AddressNotFoundError:
        return "Not found"

# Usage
ip_address = "239.255.255.250" # Replace with the IP address you want to lookup
asn = get_asn_info(ip_address)
print(f"ASN associated with IP address {ip_address}: {asn}")
