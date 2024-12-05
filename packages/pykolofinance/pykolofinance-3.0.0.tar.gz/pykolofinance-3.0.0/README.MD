# Shared Python Utilities

== Custom Auth Service

In order to use the Custom Auth Middleware, kindly set the following

[source,bash]
---
poetry add pykolofinance
---

[source,bash]
---
pip install pykolofinance
---
[source,bash]
---
AUTH_SERVICE_BASE_URL=
---


## Usage
1. Install the package 

[source,bash]
---
poetry add pykolofinance
---

2. Add `pykolofinance` to installed apps in django
3. update `REST_FRAMEWORK` settings as showing below

[source,python]
---
REST_FRAMEWORK = {
    ...
    # 'DATE_INPUT_FORMATS': ["%d/%m/%Y", ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        "pykolofinance.authentication.CustomJWTAuthentication",
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    ...
}
---

=== Manage Migrations
Whenever you make changes to models, you need to generate migrations locally before pushing your code to the repo. In order to generate migrations, kindly run the following command in another terminal window while your main app is also running


== Logging

The service includes a middleware that logs both requests and responses to Elasticsearch (ELK). To enable logging, specify the `ELK_LOGGER_URL` in your environment variables.

=== Configuration

Ensure your `.env` file includes the following:

[source,bash]
----
ELK_LOGGER_URL=https://your-elasticsearch-url:9200
----

=== Middleware Integration

The logging middleware is already integrated into the application. It captures API interactions and stores them in Elasticsearch for monitoring and analysis.

=== Skip URL Name

You can skip logging for specific API endpoints by setting `API_LOGGER_SKIP_URL_NAME` in your `settings.py`. Example:

[source,python]
----
API_LOGGER_SKIP_URL_NAME = ['url_name1', 'url_name2']
----

=== Skip Namespace

Skip logging for entire apps by specifying their namespaces in `API_LOGGER_SKIP_NAMESPACE` in your `settings.py`. Example:

[source,python]
----
API_LOGGER_SKIP_NAMESPACE = ['APP_NAMESPACE1', 'APP_NAMESPACE2']
----

=== Exclude  http request methods from being logged ?(Optional)

You can exclude selected https methods by specifying `API_LOGGER_EXCLUDE_HTTP_METHODS` in settings.py. By default all GET request are excluded from being logged
[source,python]
----
API_LOGGER_EXCLUDE_HTTP_METHODS = ['GET', 'PATCH']
----

=== Hide Sensitive Data From Logs

To prevent sensitive information from appearing in the logs, configure `API_LOGGER_EXCLUDE_KEYS` in your `settings.py` with a list of sensitive keys. By default, the following keys are excluded:

[source,python]
----
API_LOGGER_EXCLUDE_KEYS = ['password', 'token', 'access', 'refresh']
# Sensitive data will be replaced with "***FILTERED***".
----

= KYC

== 1. Verification

The service includes a KYC verification service. There are three verification types:

. BVN
. NIN
. BVN_SELFIE

We currently have two providers:

. MOCK
. DOJAH

By default, the provider is set to MOCK. To override the default value, set `PYKOLO_DEFAULT_IDENTITY_SERVICE` in your settings file to your preferred provider:

[source,python]
----
PYKOLO_DEFAULT_IDENTITY_SERVICE = "DOJAH"
----

Please note that when you switch the provider to DOJAH, you are required to set `DOJAH_API_URL`, `DOJAH_APP_ID`, and `DOJAH_API_KEY` in your settings.py file. Please note that the DOJAH API URL must be without a trailing slash `/`.

[source,python]
----
from pykolofinance.kyc.verifier import get_identity_data

identity_data = get_identity_data(identity_type, identity_number, image=None, user_id=None)
----

Note that an image is required while verifying BVN_SELFIE.





.Table Contributors
|===
|Name |Role |Email
|Daniel Ale |SA |d.ale@capitalsage.ng
|Isaiah Aimiton |BE |i.aimiton@capitalsage.ng
|===
[quote]
____
Happy Coding
____
