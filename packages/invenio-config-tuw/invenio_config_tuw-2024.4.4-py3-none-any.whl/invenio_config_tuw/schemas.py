# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 TU Wien.
#
# Invenio-Config-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Various schemas to use in InvenioRDM."""

from invenio_app_rdm.users.schemas import NotificationsUserSchema as UserSchema
from invenio_app_rdm.users.schemas import (
    UserPreferencesNotificationsSchema as UserPreferencesSchema,
)
from invenio_users_resources.services.schemas import UserProfileSchema
from marshmallow import fields


# profile
class TUWUserProfileSchema(UserProfileSchema):
    """User profile schema with TU Wien extensions."""

    given_name = fields.String()
    family_name = fields.String()
    tiss_id = fields.Integer()


# preferences
class TUWUserPreferencesSchema(UserPreferencesSchema):
    """User preferences schema with TU Wien extensions."""

    curation_consent = fields.Boolean(default=False)


# complete user schema
class TUWUserSchema(UserSchema):
    """User schema with TU Wien extensions."""

    preferences = fields.Nested(TUWUserPreferencesSchema)
