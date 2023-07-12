import geoip2.database


def get_ip_company(ip):
    # Replace with the actual path to your GeoLite2-ASN database file
    reader = geoip2.database.Reader('GeoLite2-ASN.mmdb')
    try:
        response = reader.asn(ip)
        asn = response.autonomous_system_organization
        return asn
    except geoip2.errors.AddressNotFoundError:
        return "Not found"
    
def get_company_ip(company):
    # Replace with the actual path to your GeoLite2-ASN database file
    reader = geoip2.database.Reader('GeoLite2-ASN.mmdb')
    try:
        response = reader.enterprise(company)
        ip_addresses = response.network
        return ip_addresses
    except geoip2.errors.AddressNotFoundError:
        return "Not found"
        
if __name__ == '__main__':
    ip = "149.137.83.30"
    print(get_ip_company(ip))
    company = "ZOOM-VIDEO-COMM-AS"
    print(get_company_ip(company))