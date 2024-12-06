# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 TU Wien.
#
# Invenio-Config-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Custom view functions for TU Wien."""

from flask import Blueprint, current_app, flash, render_template, request
from flask_login import current_user, login_required
from invenio_db import db

from .curation import CurationForm

blueprint = Blueprint(
    "invenio_config_tuw_settings",
    __name__,
    url_prefix="/account/settings/curation",
)


@blueprint.route("/", methods=["GET", "POST"])
@login_required
def curation_settings_view():
    """Page for the curation consent setting in user profiles."""
    preferences_curation_form = CurationForm(
        formdata=None, obj=current_user, prefix="preferences-curation"
    )

    form_name = request.form.get("submit", None)
    form = preferences_curation_form if form_name else None

    if form:
        form.process(formdata=request.form)
        if form.validate_on_submit():
            form.populate_obj(current_user)
            db.session.add(current_user)
            current_app.extensions["security"].datastore.commit()
            flash(("Curation settings were updated."), category="success")

    return render_template(
        "invenio_theme_tuw/settings/curation.html",
        preferences_curation_form=preferences_curation_form,
    )
