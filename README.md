# LMCache
[![License](https://img.shields.io/badge/License-GPL%203.0%20with%20AGPL%203.0-blue.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/Th3Tr1ckst3r/LMCache)](https://github.com/Th3Tr1ckst3r/LMCache/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/Th3Tr1ckst3r/LMCache)](https://github.com/Th3Tr1ckst3r/LMCache/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/Th3Tr1ckst3r/LMCache)](https://github.com/Th3Tr1ckst3r/LMCache/issues)

# About
Lightning memory-mapped cache(LMCache) is a integration for OpenThreatMap using LMDB that allows us to easily utilize any DNS server, &amp; cache/store our results locally in a scalable fashion so that we dont overwhelm DNS servers as much with too many requests.

# Install
In order to start using this integration separately yourself, you simply use pip with your Python3 virtual environment:
```
pip install dnspython lmdb
```
Then, you can start immdiately by using the following example:
```
from lmcache import *

# Usage example
cache = LMCache(ttl=10)  # Set the TTL to 10 seconds
domains = ['example.com', 'google.com', 'openai.com']
for domain in domains:
    ip = cache.resolve_domain(domain)
    if ip:
        print(f"{domain} resolved to {ip}")
    else:
        print(f"Failed to resolve {domain}")

# Close the database environment when done
cache.env.close()
```
<a name="Contributors"></a>
## Contributors

<p align="center">
    <a href="https://github.com/Th3Tr1ckst3r"><img src="https://avatars.githubusercontent.com/u/21149460?v=4" width=75 height=75></a>
</p>


I welcome you to contribute code to LMCache, and thank you for your contributions, feedback, and support.
