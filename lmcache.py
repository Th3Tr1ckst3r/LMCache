import dns.resolver
import lmdb
import datetime
import json
import re
import itertools


class LMCache:
    def __init__(self, path='lm_cache.lmdb', ttl=10):
        self.env = lmdb.open(path, map_size=15 * 1024 ** 3)  # Set map_size to 15 GB
        self.ttl = ttl
        self.nameservers = itertools.cycle(['1.0.0.1', '1.1.1.1', '8.8.8.8', '208.67.222.222', '208.67.220.220'])
        self.resolver = dns.resolver.Resolver()
        self.update_nameserver()

    def update_nameserver(self):
        """Update the resolver with the next nameserver in the cycle."""
        self.resolver.nameservers = [next(self.nameservers)]

    def get(self, domain):
        with self.env.begin() as txn:
            value = txn.get(domain.encode('utf-8'))
            if value:
                data = json.loads(value.decode('utf-8'))
                timestamp = datetime.datetime.fromisoformat(data['timestamp'])
                if (datetime.datetime.now(datetime.timezone.utc) - timestamp).total_seconds() < self.ttl:
                    return data['ip'], data['nameserver']
                else:
                    self.delete(domain)  # Cache expired, delete entry
        return None

    def set(self, domain, ip, nameserver):
        with self.env.begin(write=True) as txn:
            data = {
                'ip': ip,
                'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'nameserver': nameserver
            }
            txn.put(domain.encode('utf-8'), json.dumps(data).encode('utf-8'))

    def delete(self, domain):
        with self.env.begin(write=True) as txn:
            txn.delete(domain.encode('utf-8'))

    def resolve_domain(self, domain):
        # Sanitize the domain
        domain = re.sub(r'[\'"\\]', '', domain)
        
        # Check the cache first
        cached_data = self.get(domain)
        if cached_data:
            ip, nameserver = cached_data
            print(f'Used Cache with nameserver {nameserver}')
            return ip, nameserver
        
        # Update nameserver to the next one in the cycle
        self.update_nameserver()
        
        # Resolve the domain if not in cache
        try:
            # Use the current nameserver
            nameserver = str(self.resolver.nameservers[0])
            
            # Resolve 'A' (IPv4) records
            answers_v4 = self.resolver.resolve(domain, 'A')
            for ipval in answers_v4:
                ip = str(ipval)
                self.set(domain, ip, nameserver)
                return ip, nameserver
            
            # If no IPv4 records found, attempt to resolve 'AAAA' (IPv6) records
            answers_v6 = self.resolver.resolve(domain, 'AAAA')
            for ipval in answers_v6:
                ip = str(ipval)
                self.set(domain, ip, nameserver)
                return ip, nameserver
            
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.Timeout):
            pass
        except Exception as e:
            print(f'Error resolving domain: {e}')
        
        return None, None
