# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

import httpx
import jwt

external_token = "..."
access_token = "..."
token = access_token

if __name__ == "__main__":
    r = httpx.get("https://id.anaconda.cloud/.well-known/openid-configuration")
    if r.status_code < 300:
        data = r.json()
        jwks_uri = data.get("jwks_uri", "")
        s = httpx.get(jwks_uri)
        if jwks_uri:
            alg, client = (
                data.get("id_token_signing_alg_values_supported", []),
                jwt.PyJWKClient(jwks_uri, headers={"User-agent": "datalayer-iam"}),
            )

            headers = jwt.get_unverified_header(token)
            if headers.get("kid") == "default":
                jwt_token = None
                last_error = ValueError("No signing key found")
                for signing_key in client.get_signing_keys():
                    try:
                        jwt_token = jwt.decode(token, key=signing_key.key, algorithms=alg)
                    except jwt.InvalidTokenError as e:
                        last_error = e
                        continue
                if jwt_token is None:
                    raise last_error
            else:
                signing_key = client.get_signing_key_from_jwt(token)
                jwt_token = jwt.decode(token, key=signing_key.key, algorithms=alg)
            print(jwt_token)