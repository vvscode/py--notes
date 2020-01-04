import requests

url = 'http://proxy.seoshnik.top/working?key=asjdhasod9asd9as8d9asdhaidnoklvm'

resp = requests.get(url)

print(resp.status_code)
print(resp.text.split()[:30])
