# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2024 TU Wien.
#
# Invenio-Config-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module containing some customizations and configuration for TU Wien."""

from datetime import datetime

from invenio_i18n import gettext as _
from invenio_oauthclient.views.client import auto_redirect_login
from invenio_rdm_records.config import RDM_RECORDS_REVIEWS

from .auth import TUWSSOSettingsHelper
from .forms import tuw_registration_form
from .permissions import (
    TUWCommunityPermissionPolicy,
    TUWRecordPermissionPolicy,
    TUWRequestsPermissionPolicy,
)
from .schemas import TUWUserPreferencesSchema, TUWUserProfileSchema, TUWUserSchema
from .services import TUWRecordsComponents
from .utils import check_user_email_for_tuwien, current_user_as_creator

# Invenio-Config-TUW
# ==================

CONFIG_TUW_AUTO_TRUST_USERS = True
"""Whether or not to auto-assign the 'trusted-user' role to new users."""

CONFIG_TUW_AUTO_TRUST_CONDITION = check_user_email_for_tuwien
"""Function for checking if the user is eligible for auto-trust.

This must be a function that accepts a 'user' argument and returns a boolean value.
Alternatively, it can be set to None. This is the same as ``lambda u: True``.
"""

CONFIG_TUW_READ_ONLY_MODE = False
"""Disallow insert and update operations in the repository."""

CONFIG_TUW_DISABLE_ERROR_MAILS = False
"""Disable registration of the SMTP mail handler to suppress warnings."""

CONFIG_TUW_MINIFY_ENABLED = False
"""Enable or disable the Flask-Minify extension."""


# Invenio-Mail
# ============
# See https://invenio-mail.readthedocs.io/en/latest/configuration.html

MAIL_SERVER = "localhost"
"""Domain ip where mail server is running."""

SECURITY_EMAIL_SENDER = "no-reply@tuwien.ac.at"
"""Email address used as sender of account registration emails."""

MAIL_SUPPRESS_SEND = True
"""Disable email sending by default."""

SECURITY_SEND_REGISTER_EMAIL = True
"""Enable sending emails after user registration."""

SECURITY_EMAIL_SUBJECT_REGISTER = _("Welcome to TU Wien Research Data!")
"""Email subject for account registration emails."""

SECURITY_EMAIL_HTML = True
"""Send the HTML version of the email."""

# disable sending of emails related to local login
SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False
SECURITY_SEND_PASSWORD_RESET_EMAIL = False
SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL = False


# Invenio-Previewer
# =================

PREVIEWER_MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

PREVIEWER_MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


# Authentication
# ==============

SECURITY_CHANGEABLE = False
"""Allow password change by users."""

SECURITY_RECOVERABLE = False
"""Allow password recovery by users."""

SECURITY_REGISTERABLE = False
""""Allow users to register."""

SECURITY_CONFIRMABLE = False
"""Allow user to confirm their email address."""

ACCOUNTS = True
"""Tells if the templates should use the accounts module."""

ACCOUNTS_LOCAL_LOGIN_ENABLED = False
"""Disable local login (rely only on OAuth)."""

USERPROFILES_READ_ONLY = True
"""Prevent users from updating their profiles."""


# Invenio-OAuthClient
# ===================

ACCOUNTS_LOGIN_VIEW_FUNCTION = auto_redirect_login

OAUTHCLIENT_SIGNUP_FORM = tuw_registration_form

OAUTHCLIENT_AUTO_REDIRECT_TO_EXTERNAL_LOGIN = True

helper = TUWSSOSettingsHelper(
    title="TU Wien SSO",
    description="TU Wien Single Sign-On",
    base_url="https://s194.dl.hpc.tuwien.ac.at",
    realm="tu-data-test",
)

OAUTHCLIENT_KEYCLOAK_REALM_URL = helper.realm_url
OAUTHCLIENT_KEYCLOAK_USER_INFO_URL = helper.user_info_url
OAUTHCLIENT_KEYCLOAK_AUD = "tu-data-test"
OAUTHCLIENT_KEYCLOAK_VERIFY_AUD = True
OAUTHCLIENT_KEYCLOAK_USER_INFO_FROM_ENDPOINT = True
OAUTHCLIENT_REMOTE_APPS = {
    "keycloak": helper.remote_app,
}


# Invenio-App-RDM
# ================

APP_RDM_DEPOSIT_FORM_DEFAULTS = {
    "publication_date": lambda: datetime.now().strftime("%Y-%m-%d"),
    "creators": current_user_as_creator,
    "rights": [
        {
            "id": "cc-by-4.0",
            "title": "Creative Commons Attribution 4.0 International",
            "description": (
                "The Creative Commons Attribution license allows "
                "re-distribution and re-use of a licensed work "
                "on the condition that the creator is "
                "appropriately credited."
            ),
            "link": "https://creativecommons.org/licenses/by/4.0/legalcode",
        }
    ],
    "publisher": "TU Wien",
    "resource_type": {
        "id": "dataset",
    },
    "version": "1.0.0",
    "description": "<h2>A primer on your dataset's description (to be edited)</h2><p>The influence of proper documentation on the reusability for research data should not be underestimated!<br>In order to help others understand how to interpret and reuse your data, we provide you with a few questions to help you structure your dataset's description (though please don't feel obligated to stick to them):</p><h3>Context and methodology</h3><ul><li>What is the research domain or project in which this dataset was created?</li><li>Which purpose does this dataset serve?</li><li>How was this dataset created?</li></ul><h3>Technical details</h3><ul><li>What is the structure of this dataset? Do the folders and files follow a certain naming convention?</li><li>Is any specific software required to open and work with this dataset?</li><li>Are there any additional resources available regarding the dataset, e.g. documentation, source code, etc.?</li></ul><h3>Further details</h3><ul><li>Is there anything else that other people may need to know when they want to reuse the dataset?</li></ul>",  # noqa
}

RDM_RECORDS_SERVICE_COMPONENTS = TUWRecordsComponents
"""Override for the default record service components."""

RDM_CITATION_STYLES = [
    ("apa", _("APA")),
    ("bibtex", _("BibTeX")),
    ("ieee", _("IEEE")),
]

RDM_PERMISSION_POLICY = TUWRecordPermissionPolicy

OAISERVER_METADATA_FORMATS = {
    "oai_dc": {
        "serializer": "invenio_rdm_records.oai:dublincore_etree",
        "schema": "http://www.openarchives.org/OAI/2.0/oai_dc.xsd",
        "namespace": "http://www.openarchives.org/OAI/2.0/oai_dc/",
    },
    "datacite": {
        "serializer": "invenio_rdm_records.oai:datacite_etree",
        "schema": "http://schema.datacite.org/meta/nonexistant/nonexistant.xsd",
        "namespace": "http://datacite.org/schema/nonexistant",
    },
    "oai_datacite": {
        "serializer": "invenio_rdm_records.oai:oai_datacite_etree",
        "schema": "http://schema.datacite.org/oai/oai-1.1/oai.xsd",
        "namespace": "http://schema.datacite.org/oai/oai-1.1/",
    },
}

RDM_ARCHIVE_DOWNLOAD_ENABLED = False

RDM_RECORDS_REVIEWS = [rt for rt in RDM_RECORDS_REVIEWS if rt != "community-submission"]
"""Remove the ``community-submission`` from the list of supported review types.

We require mandatory record reviews before publication, but community-submission
requests could be used to evade them and publish records directly (when community
members accept the record in question).
As such, we remove the community-submission as a supported review type.
This config item is checked in the `records_service.review.create()` method.
"""


# Invenio-Requests
# ================

REQUESTS_PERMISSION_POLICY = TUWRequestsPermissionPolicy


# Invenio-Communities
# ================

COMMUNITIES_ALLOW_RESTRICTED = True

COMMUNITIES_PERMISSION_POLICY = TUWCommunityPermissionPolicy


# Limitations
# ===========

RATELIMIT_ENABLED = True

RATELIMIT_AUTHENTICATED_USER = "30000 per hour;3000 per minute"

RATELIMIT_GUEST_USER = "6000 per hour;600 per minute"

# Default file size limits for deposits: 75 GB
max_file_size = 75 * (1024**3)

# ... per file
FILES_REST_DEFAULT_MAX_FILE_SIZE = max_file_size

# ... for the entire bucket
FILES_REST_DEFAULT_QUOTA_SIZE = max_file_size

# ... and on the deposit form UI
APP_RDM_DEPOSIT_FORM_QUOTA = {
    "maxFiles": 100,
    "maxStorage": max_file_size,
}

# show the display in powers of 2 (KiB, MiB, GiB, ...) rather than 10 (KB, MB, GB, ...)
APP_RDM_DISPLAY_DECIMAL_FILE_SIZES = False

# for multipart form uploads, we'll use a max. content length of 100 MB
# (e.g. community logo upload, but not record/draft file deposits)
MAX_CONTENT_LENGTH = 100 * (1024**2)


# Misc. Configuration
# ===================

# Default locale (language)
BABEL_DEFAULT_LOCALE = "en"

# Default time zone
BABEL_DEFAULT_TIMEZONE = "Europe/Vienna"

# Recaptcha public key (change to enable).
RECAPTCHA_PUBLIC_KEY = None

# Recaptcha private key (change to enable).
RECAPTCHA_PRIVATE_KEY = None

# Preferred URL scheme to use
PREFERRED_URL_SCHEME = "https"

# Extended schema for user preferences
ACCOUNTS_USER_PREFERENCES_SCHEMA = TUWUserPreferencesSchema()

# Extended schema for user preferences
ACCOUNTS_USER_PROFILE_SCHEMA = TUWUserProfileSchema()

# Extended schema for users in the users service
USERS_RESOURCES_SERVICE_SCHEMA = TUWUserSchema
