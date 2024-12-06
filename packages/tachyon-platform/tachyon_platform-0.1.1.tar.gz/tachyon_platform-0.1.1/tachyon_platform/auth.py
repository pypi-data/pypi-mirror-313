# coding: utf-8

from __future__ import annotations

import hashlib
import json
import os
from hmac import compare_digest
from pathlib import Path
from typing import Optional

import jwt
import urllib3

from tachyon_platform.configuration import Configuration


class Credential:
    """Credential class to store the access token and expiration time.

    :param sp_email: The email address of the service principal.
    :param sp_password_hash: The hashed password of the service principal.
    :param access_token: The access token.
    :param expiration_time: The expiration time of the access token.
    """

    def __init__(
        self,
        *,
        sp_email: str,
        sp_password_hash: str,
        access_token: str,
        expiration_time: int,
    ) -> None:
        self.sp_email = sp_email
        self.sp_password_hash = sp_password_hash
        self.access_token = access_token
        self.expiration_time = expiration_time


class AuthClient:
    """AuthClient class to handle the authentication with the Auth0 server.

    :param client_id: The client ID.
    :param auth_server_url: The URL of the Auth0 server.
    :param token_cache_dir: The directory path to store the token cache.
    :param audience: The audience of the token.
    :param workspace_name: The workspace name to be accessed.
    :param email: The email address of the service principal.
    :param password: The password of the service principal.
    """

    def __init__(self, configuration: Configuration) -> None:
        """Initialize the AuthClient object.

        :param configuration: The configuration object.
        """

        self.client_id = configuration.client_id
        self.auth_server_url = configuration.auth_server_url
        self.audience = configuration.audience
        self.workspace_name = configuration.workspace_name
        self.token_cache_dir = Path(configuration.token_cache_dir / self.workspace_name)
        self.email = configuration.sp_email
        self.password = configuration.sp_password

        self._http = urllib3.PoolManager()

        # Create the token cache directory if it doesn't exist
        self.token_cache_dir.mkdir(parents=True, exist_ok=True)

    def get_credential(self) -> Credential:
        """Get the credential object.

        :return: The credential object.
        """

        # read the credential from local cache
        cred = self._read_credential_cache()

        if cred is not None:
            # check if the service principal email and password are correct
            if cred.sp_email == self.email and self._verify_password_hash(cred.sp_password_hash):
                # check if the access token is not expired
                if not check_jwt_expired(cred.access_token):
                    return cred

        # request a new credential
        cred = self._request_new_credential()

        # write the credential to the local cache
        self._write_credential_cache(cred)

        return cred

    def _request_new_credential(self) -> Credential:
        """Request a new credential using "Resource Owner Password Flow".

        ref: https://auth0.com/docs/get-started/authentication-and-authorization-flow/resource-owner-password-flow

        :return: The credential object.
        """

        req = json.dumps({
            "client_id": self.client_id,
            "audience": self.audience,
            "grant_type": "password",
            "username": self.email,
            "password": self.password,
        })

        resp = self._http.request(
            "POST",
            f"{self.auth_server_url}/oauth/token",
            body=req,
            headers={"Content-Type": "application/json"},
        )
        if resp.status >= 400:
            raise Exception(f"Failed to request a new credential. status: {resp.status} body: {resp.data!r}")

        # parse the response
        body = resp.json()

        password_hash = self._hash_password(password=self.password)

        return Credential(
            sp_email=self.email,
            sp_password_hash=password_hash,
            access_token=body["access_token"],
            expiration_time=body["expires_in"]
        )

    def _read_credential_cache(self) -> Optional[Credential]:
        """Get the cached credential from the local disk.

        :return: The credential object if it exists, None otherwise.
        """

        token_path = self.token_cache_dir / "access_token"

        if token_path.exists():
            try:
                with open(token_path, 'r') as f:
                    token_data = f.read()
            except Exception:
                # if the token file is corrupted, ignore the error and return None
                return None

            token = json.loads(token_data)
            return Credential(
                sp_email=token["sp_email"],
                sp_password_hash=token["sp_password_hash"],
                access_token=token["access_token"],
                expiration_time=token["expires_in"],
            )
        else:
            return None

    def _write_credential_cache(self, cred: Credential) -> None:
        """Write the credential to the local disk.

        :param cred: The credential object.
        """

        token_path = self.token_cache_dir / "access_token"

        with open(token_path, "w") as f:
            json.dump({
                "sp_email": cred.sp_email,
                "sp_password_hash": cred.sp_password_hash,
                "access_token": cred.access_token,
                "expires_in": cred.expiration_time,
            }, f)

    def _hash_password(self, *, password: str, salt: str | None = None) -> str:
        """Hash the password using PBKDF2.

        :param password: The password to be hashed.
        :param salt: The salt value. If None, generate a new salt.
        :return: The hashed password.
        """
        if salt is None:
            salt = os.urandom(32).hex()

        hash_value = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            100000,
        ).hex()

        return f"{salt}:{hash_value}"

    def _verify_password_hash(self, cached_password: str) -> bool:
        """Verify the hashed password is correct.

        :param cached_password: The cached password hash.
        :return: True if the password is correct, False otherwise.
        """
        salt, _ = cached_password.split(":")

        # hash the given password with the same salt value
        password_hash = self._hash_password(password=self.password, salt=salt)

        return compare_digest(password_hash, cached_password)


def check_jwt_expired(token: str) -> bool:
    """Check if the JWT token is expired.

    :param token: The JWT token.
    :return: True if the token is expired, False otherwise.
    """

    try:
        jwt.decode(
            token,
            algorithms=["RS256"],
            options={
                "verify_signature": False,
                "verify_exp": True,
            },
        )
        return False
    except jwt.ExpiredSignatureError:
        return True
