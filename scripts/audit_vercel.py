import os
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print('=== VERCEL DEPLOYMENT READINESS CHECK ===')
print('1. File size:', len(html), 'bytes')
print('2. Has DOCTYPE:', '<!DOCTYPE html>' in html)
print('3. Has meta viewport:', 'name="viewport"' in html)

# Check insecure links
http_links = re.findall(r'http://[^\s"\'<>]+', html)
print('4. Insecure HTTP links:', http_links)

# Check all external links
ext_links = re.findall(r'https://[^\s"\'<>]+', html)
print('5. External HTTPS link domains:')
domains = set()
for l in ext_links:
    m = re.match(r'https://([^/]+)', l)
    if m:
        domains.add(m.group(1))
for d in sorted(domains):
    print('   -', d)

# Check local asset references
srcs = re.findall(r'(?:src|href)=["\']([^"\'<>]+)["\']', html)
local_assets = [s for s in srcs if not s.startswith('http') and not s.startswith('data:') and not s.startswith('#') and not s.startswith('mailto:')]
print('6. Local asset references:', local_assets)
for a in local_assets:
    print('   -', a, 'exists:', os.path.exists(a))

print('=== AUDIT COMPLETE ===')
