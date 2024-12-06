# Authese

### Authenticate through OpenID Connect and cache your JWT token in a file.

## Example
```
from authese import get_token, EnvConfig, Environment

token = get_token(EnvConfig.from_env(Environment.STAGING))
```

## Install
`pip install authese`

## Info
There are 3 possible environments.
- LOCAL
- STAGING
- PROD
#### Assuming STAGING
Create an EnvConfig object.
Call get_token() and provide it with the EnvConfig object.  
### EnvConfig
#### - Personal access token  
  `grant_type: ''`  *Identical to `grant_type: 'authorization_code'`*  
  This is the **default** authorization flow.  
  This will open a browser window where you can authenticate to the requested keycloak_url.  
  
#### - Server to server  
  Depending if you set the `grant_type: 'client_credentials'`.  
This will authenticate to the requested keycloak_url using the client credentials.  

### Cache

Once authenticated, your token will be cached at /tmp/authese-cache.dat  
Subsequent calls to get_token() will use the cached token.  
When the token expires it will be deleted and you must authenticate again.

To force reauthentication just remove the /tmp/authese-cache.dat file.

## Config
```
local:
staging:
  keycloak_url: 'https://<openid-host>/realms/<realm>/protocol/openid-connect'
  grant_type: '<authorization_code | client_credentials>'
  client_id: '<client_id>'
  client_secret: '<client_secret>'
  redirect_host: 'http://127.0.0.1'
  redirect_port: 9981
  scopes:
    - 'email'
    - 'profile'
prod:
  keycloak_url: 'https://<openid-host>/realms/<realm>/protocol/openid-connect'
  grant_type: '<authorization_code | client_credentials>'
  client_id: '<client_id>'
  client_secret: '<client_secret>'
  redirect_host: 'http://127.0.0.1'
  redirect_port: 9981
  scopes:
    - 'email'
    - 'profile'
```
