#!/bin/bash
# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 TU Wien.
#
# Invenio-Config-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

if [[ $# -lt 1 ]]; then
    echo >&2 "error: expected at least one argument"
fi

case "${1}" in
    init)
        pybabel init \
            --input-file "invenio_config_tuw/translations/messages.pot" \
            --output-dir "invenio_config_tuw/translations/"
        ;;
    compile)
        pybabel compile \
            --directory "invenio_config_tuw/translations/"
        ;;
    extract)
        pybabel extract \
            --copyright-holder "TU Wien" \
            --msgid-bugs-address "tudata@tuwien.ac.at" \
            --mapping-file "babel.ini" \
            --output-file "invenio_config_tuw/translations/messages.pot" \
            --add-comments "NOTE"
        ;;
    update)
        pybabel update \
            --input-file "invenio_config_tuw/translations/messages.pot" \
            --output-dir "invenio_config_tuw/translations/"
        ;;
    *)
        echo >&2 "unknown command: ${1}"
        exit 1
        ;;
esac
