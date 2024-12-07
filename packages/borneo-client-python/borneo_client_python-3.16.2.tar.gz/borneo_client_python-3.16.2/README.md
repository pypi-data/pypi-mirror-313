# borneo-client-python

Borneo Client Python SDK

## Installing

To install the this package, simply add or install using your favorite package manager and dependent packages:

- `pip install borneo-client-python`
- `pip install boto3`
- `pip install PyJWT`

### Usage

To send a request using `borneo-client-python` and an example command:

```python
import asyncio
from borneo_client_python.client import Borneo
from borneo_client_python.config import Config, IdentityResolver, ApiKeyIdentity, IdentityProperties, ApiKeyIdentity
from borneo_client_python.models import ListLogsInput, ListLogsFilter
from borneo_auth_provider import borneo_auth_provider
from smithy_http.aio.aiohttp import AIOHTTPClient

# Replace the service account key file location
auth_provider = borneo_auth_provider.BorneoAuthProviderConfig.fromConfigFile('../Borneo-Service-Account-Token.json')

class ApiKeyIdentityResolver(IdentityResolver[ApiKeyIdentity, IdentityProperties]):
    async def get_identity(self, identity_properties) -> ApiKeyIdentity:
        token = auth_provider.get_api_key()
        return ApiKeyIdentity(api_key=token)
        
async def main() -> None:
    http_client = AIOHTTPClient()
    endpoint_uri = auth_provider.get_api_endpoint()
    client = Borneo(Config(endpoint_uri=endpoint_uri, api_key_identity_resolver=ApiKeyIdentityResolver(), retry_strategy=None, http_client=http_client))

    # Payload inputs
    input = ListLogsInput(filter=ListLogsFilter(search='<text>'))
    data = await client.list_logs(input)

    # Data output here
    print(data)

    await http_client._session.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### Config
```
const config = {
  clientId: 'STRING_VALUE', /* required */
  region: 'STRING_VALUE', /* required */
  token: 'STRING_VALUE', /* required */
  apiEndpoint: 'STRING_VALUE', /* required */
  secret: 'STRING_VALUE'
}
```

## API Documentation

More API documentation is here at `https://<my-stack>/docs/api`

## License

This SDK is distributed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0)
