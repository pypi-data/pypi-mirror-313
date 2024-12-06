import os, msal, atexit, keyring
from cryptography.fernet import Fernet
from getpass import getuser
import eigeningenuity.settings as settings

cache = msal.SerializableTokenCache()
url = None

def encrypt(data,key):
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

def decrypt(data,key):
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(data).decode()
    return decrypted_data

def _authenticate_azure_user(baseurl):
    global url
    url = baseurl

    if settings._token_cache_enabled_:
        global cache
        try:
            encryptionKey = keyring.get_password("eigeningenuity","python")
        except:
            pass

        if not os.path.exists(os.path.dirname(__file__) + '/.azure'):
            os.mkdir(os.path.dirname(__file__) + "/.azure")

        if os.path.exists(os.path.dirname(__file__) + f"/.azure/{getuser()}_cache.bin"):
            encryptedToken = open(os.path.dirname(__file__) + f"/.azure/{getuser()}_cache.bin", "rb").read()
            if encryptedToken != b'':
                cache.deserialize(decrypt(encryptedToken,encryptionKey))
        
        encryptionKey = Fernet.generate_key().decode('utf-8')

        atexit.register(lambda:
            open(os.path.dirname(__file__) + f"/.azure/{getuser()}_cache.bin", "wb").write(encrypt(cache.serialize(),encryptionKey)) and keyring.set_password("eigeningenuity","python",encryptionKey)
            if cache.has_state_changed else None
            )

    tenant_id = settings._azure_tenant_id_
    client_id = settings._azure_client_id_
    client_secret = settings._azure_client_secret_
    authority = f'https://login.microsoftonline.com/{tenant_id}'

    if client_secret: # USE CLIENT_CREDENTIALS FLOW
        scope=[f"{baseurl}/.default"]
        # Create a confidential client application
        app = msal.ConfidentialClientApplication(
            client_id,
            authority=authority,
            client_credential=client_secret
        )

        # Acquire a token
        result = app.acquire_token_for_client(scopes=scope)

        if "access_token" in result:
            access_token = (result["access_token"])
        else:
            print("Error acquiring token:")
            print(result.get("error"))
            print(result.get("error_description"))
            print(result.get("correlation_id"))  # You might want to save this in case of reporting a bug

    else: # USE INTERACTIVE FLOW

        scope=[f"{baseurl}/{settings._auth_scope_}"]

        app = msal.PublicClientApplication(
            client_id=client_id,
            authority=authority,
            token_cache=cache
        )

        # We now check the cache to see
        # whether we already have some accounts that the end user already used to sign in before.
        accounts = app.get_accounts()
        if accounts:
            account = 0
            # If so, you could then somehow display these accounts and let end user choose
            if len(accounts) >= 2:
                print("Found Multiple Users in Cache")
                while True:
                    for idx,a in enumerate(accounts):
                        print(f'{idx}: {a["username"]}')
                    try:
                        account = int(input("Enter the number of the account you want to use:\n"))
                        if account not in list(range(len(accounts))):
                            print("That is not a valid option!")
                        else:
                            break
                    except:
                        print("That is not a valid option!")

            # Assuming the end user chose this one
            chosen = accounts[account]
            # Now let's try to find a token in cache for this account
            result = app.acquire_token_silent(scope, account=chosen)


        if not result:
            # So no suitable token exists in cache. Let's get a new one from Azure AD.
            settings.clear_auth_token_cache()
            result = app.acquire_token_interactive(scope,auth_uri_callback=_backup_auth_azure_user)

        if "access_token" in result:
            access_token = (result["access_token"])  # Yay!
        else:
            print("Error acquiring token:")
            print(result.get("error"))
            print(result.get("error_description"))
            print(result.get("correlation_id"))  # You may need this when reporting a bug

    # Make requests to the Java API using the obtained access token
    return {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }


def _backup_auth_azure_user(_uri):
    global url
    baseurl = url
    if settings._token_cache_enabled_:
        global cache
        try:
            encryptionKey = keyring.get_password("eigeningenuity","python")
        except:
            pass

        if not os.path.exists(os.path.dirname(__file__) + '/.azure'):
            os.mkdir(os.path.dirname(__file__) + "/.azure")

        if os.path.exists(os.path.dirname(__file__) + f"/.azure/{getuser()}_cache.bin"):
            encryptedToken = open(os.path.dirname(__file__) + f"/.azure/{getuser()}_cache.bin", "rb").read()
            if encryptedToken != b'':
                cache.deserialize(decrypt(encryptedToken,encryptionKey))
        
        encryptionKey = Fernet.generate_key().decode('utf-8')

        atexit.register(lambda:
            open(os.path.dirname(__file__) + f"/.azure/{getuser()}_cache.bin", "wb").write(encrypt(cache.serialize(),encryptionKey)) and keyring.set_password("eigeningenuity","python",encryptionKey)
            if cache.has_state_changed else None
            )


    authority = f'https://login.microsoftonline.com/{settings._azure_tenant_id_}'
    scope=[f"{baseurl}/{settings._auth_scope_}"]
    client_id = settings._azure_client_id_


    app = msal.PublicClientApplication(
        client_id=client_id,
        authority=authority,
        token_cache=cache
    )

    result=None

    # We now check the cache to see
    # whether we already have some accounts that the end user already used to sign in before.
    accounts = app.get_accounts()
    if accounts:
        account = 0
        # If so, you could then somehow display these accounts and let end user choose
        if len(accounts) >= 2:
            print("Found Multiple Users in Cache")
            while True:
                for idx,a in enumerate(accounts):
                    print(f'{idx}: {a["username"]}')
                try:
                    account = int(input("Enter the number of the account you want to use:\n"))
                    if account not in list(range(len(accounts))):
                        print("That is not a valid option!")
                    else:
                        break
                except:
                    print("That is not a valid option!")

        # Assuming the end user chose this one
        chosen = accounts[account]
        # Now let's try to find a token in cache for this account
        result = app.acquire_token_silent(scope, account=chosen)


    if not result:
        # So no suitable token exists in cache. Let's get a new one from Azure AD.
        flow = app.initiate_device_flow(scopes=scope)
        print(flow["message"])
        print("Please navigate to:", flow["verification_uri"])

        result = app.acquire_token_by_device_flow(flow)

    # Make requests to the Java API using the obtained access token
    return result

