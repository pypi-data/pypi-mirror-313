
### Sample Code

``` python
from desync_search import DesyncSearch

# Initialize the client
client = DesyncSearch(api_key="Your-API-Key")

# Perform a search
response = client.search("https://www.137ventures.com/", stealth_level=1)

# Access results
print(response.text_content)
print(response.internal_links)
print(response.external_links)

```