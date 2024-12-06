#--------------------------------------------------
# FLAGS
#--------------------------------------------------
USE_GRAPH_INDEX = True

#--------------------------------------------------
# Constants
#--------------------------------------------------

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

class GlobalProfileSetting:
    def __init__(self):
        self.profile = None

    def set(self, profile):
        self.profile = profile

    def get(self):
        return self.profile

GlobalProfile = GlobalProfileSetting()

SNOWFLAKE = "Snowflake"
AZURE = "Azure (Beta)"

SNOWFLAKE_AUTHENTICATOR = {
    "USERNAME & PASSWORD": "snowflake",
    "USERNAME & PASSWORD (MFA ENABLED)": "username_password_mfa",
    "SINGLE SIGN-ON (SSO)": "externalbrowser",
}

FIELD_PLACEHOLDER = ""

SNOWFLAKE_PROFILE_DEFAULTS = {
    "platform": "snowflake",
    "user": FIELD_PLACEHOLDER,
    "account": FIELD_PLACEHOLDER,
    "role": "PUBLIC",
    "warehouse": FIELD_PLACEHOLDER,
    "rai_app_name": FIELD_PLACEHOLDER,
    "engine": FIELD_PLACEHOLDER,
    "engine_size": "HIGHMEM_X64_S"
}

SNOWFLAKE_AUTHS = {
    "snowflake": {
        "authenticator": "snowflake",
        "password": FIELD_PLACEHOLDER,
        **SNOWFLAKE_PROFILE_DEFAULTS,
    },
    "username_password_mfa": {
        "authenticator": "username_password_mfa",
        "password": FIELD_PLACEHOLDER,
        "passcode": FIELD_PLACEHOLDER,
        **SNOWFLAKE_PROFILE_DEFAULTS,
    },
    "externalbrowser": {
        "authenticator": "externalbrowser",
        **SNOWFLAKE_PROFILE_DEFAULTS,
    },
}

AZURE_ENVS = {
    "Production": {
        "host": "azure.relationalai.com",
        "client_credentials_url": "https://login.relationalai.com/oauth/token"
    },
    "Early Access": {
        "host": "azure-ea.relationalai.com",
        "client_credentials_url": "https://login-ea.relationalai.com/oauth/token"
    },
    "Staging": {
        "host": "azure-staging.relationalai.com",
        "client_credentials_url": "https://login-staging.relationalai.com/oauth/token"
    },
    "Latest": {
        "host": "azure-latest.relationalai.com",
        "client_credentials_url": "https://login-latest.relationalai.com/oauth/token"
    },
}
