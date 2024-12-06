# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 TU Wien.
#
# Invenio-Config-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Celery tasks running in the background."""

import copy
from typing import List, Optional

import requests
from celery import shared_task
from flask import current_app, render_template
from invenio_access.permissions import system_identity
from invenio_accounts.proxies import current_datastore
from invenio_db import db
from invenio_mail.tasks import send_email
from invenio_rdm_records.proxies import current_rdm_records_service as records_service
from invenio_records_resources.services.uow import UnitOfWork
from invenio_vocabularies.contrib.names.api import Name

from .tiss import Employee, fetch_tiss_data


def get_tuw_ror_aliases():
    """Fetch the aliases of TU Wien known to ROR."""
    try:
        response = requests.get("https://api.ror.org/organizations/04d836q62")
        if response == 200:
            tuw_ror = response.json()
            tuw_ror_names = [tuw_ror["name"], *tuw_ror["acronyms"], *tuw_ror["aliases"]]
            return tuw_ror_names

    except Exception as e:
        current_app.logger.warn(
            f"Error while fetching TU Wien information from ROR: {e}"
        )

    return [
        "TU Wien",
        "TUW",
        "Technische Universität Wien",
        "Vienna University of Technology",
    ]


def find_orcid_match(employee: Employee, names: List[Name]) -> Optional[Name]:
    """Find the name entry with the same ORCID as the given employee."""
    if not employee.orcid:
        return None

    for name in names:
        if {"scheme": "orcid", "identifier": employee.orcid} in name.get(
            "identifiers", []
        ):
            return name

    return None


def update_name_data(
    name: dict, employee: Employee, tuw_aliases: Optional[List[str]] = None
) -> dict:
    """Update the given name entry data with the information from the employee."""
    tuw_aliases = tuw_aliases or ["TU Wien"]
    name = copy.deepcopy(name)
    name["given_name"] = employee.first_name
    name["family_name"] = employee.last_name

    # normalize & deduplicate affilations, and make sure that TU Wien is one of them
    # NOTE: sorting is done to remove indeterminism and prevent unnecessary updates
    affiliations = {
        aff["name"] for aff in name["affiliations"] if aff["name"] not in tuw_aliases
    }
    affiliations.add("TU Wien")
    name["affiliations"] = sorted(
        [{"name": aff} for aff in affiliations], key=lambda aff: aff["name"]
    )

    # similar to above, add the ORCID mentioned in TISS and deduplicate
    identifiers = {(id_["scheme"], id_["identifier"]) for id_ in name["identifiers"]}
    if employee.orcid:
        identifiers.add(("orcid", employee.orcid))

    name["identifiers"] = sorted(
        [{"scheme": scheme, "identifier": id_} for scheme, id_ in identifiers],
        key=lambda id_: f'{id_["scheme"]}:{id_["identifier"]}',
    )

    return name


@shared_task(ignore_result=True)
def sync_names_from_tiss():
    """Look up TU Wien employees via TISS and update the names vocabulary."""
    results = {"created": 0, "updated": 0}
    tuw_ror_aliases = get_tuw_ror_aliases()
    svc = current_app.extensions["invenio-vocabularies"].names_service

    all_names = [
        svc.record_cls.get_record(model.id)
        for model in svc.record_cls.model_cls.query.all()
        if not model.is_deleted and model.data
    ]

    _, employees = fetch_tiss_data()
    employees_with_orcid = [e for e in employees if not e.pseudoperson and e.orcid]

    with UnitOfWork(db.session) as uow:
        for employee in employees_with_orcid:
            matching_name = find_orcid_match(employee, all_names)

            if matching_name:
                # if we found a match via ORCID, we update it according to the TISS data
                name = svc.read(identity=system_identity, id_=matching_name["id"])
                new_name_data = update_name_data(name.data, employee, tuw_ror_aliases)

                # only update the entry if it actually differs somehow
                if name.data != new_name_data:
                    svc.update(
                        identity=system_identity,
                        id_=name.id,
                        data=new_name_data,
                        uow=uow,
                    )
                    results["updated"] += 1

            else:
                # if we couldn't find a match via ORCID, that's a new entry
                svc.create(
                    identity=system_identity, data=employee.to_name_entry(), uow=uow
                )
                results["created"] += 1

        uow.commit()

    return results


@shared_task(ignore_result=True)
def send_publication_notification_email(recid: str, user_id: Optional[str] = None):
    """Send the record uploader an email about the publication of their record."""
    record = records_service.read(identity=system_identity, id_=recid)
    if user_id is not None:
        user = current_datastore.get_user(user_id)
    else:
        owner = record._obj.parent.access.owner
        if owner is not None and owner.owner_type == "user":
            user = owner.resolve()

    html_message = render_template(
        "invenio_theme_tuw/mails/record_published.html",
        uploader=user,
        record=record,
        app=current_app,
    )
    message = render_template(
        "invenio_theme_tuw/mails/record_published.txt",
        uploader=user,
        record=record,
        app=current_app,
    )

    record_title = record["metadata"]["title"]
    send_email(
        {
            "subject": f'Your record "{record_title}" was published',
            "html": html_message,
            "body": message,
            "recipients": [user.email],
        }
    )
