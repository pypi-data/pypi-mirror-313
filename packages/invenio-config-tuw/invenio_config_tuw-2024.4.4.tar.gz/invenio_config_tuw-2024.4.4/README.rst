..
    Copyright (C) 2020-2024 TU Wien.

    Invenio-Config-TUW is free software; you can redistribute it and/or
    modify it under the terms of the MIT License; see LICENSE file for more
    details.

====================
 Invenio-Config-TUW
====================

Invenio package for tweaking InvenioRDM to the needs of TU Wien.

The following list is a quick overview of the most relevant customizations happening in this package:

* Configuration values
* Permission policies
* OIDC authentication handling
* E-Mail notification on errors
* User profile extension
* Integration with other TU Wien services


Details
=======

Configuration values
--------------------

The primary purpose of this Invenio package is to provide some baseline configuration for InvenioRDM to suit deployment at TU Wien.
These updated configurations include (but are not limited to) setting default values for record metadata and enabling access requests for restricted records per default.


Permission policies
-------------------

InvenioRDM is not just some sort of cheap storage platform where users can upload their data and update it at any time.
Instead, it is a platform intended to host digital objects that get [DOIs](https://www.doi.org/) assigned.
Since the idea behind DOIs (and persistent identifiers in general) is to point at the same content over time, it does not allow users to change the files after publication.

This is one of the unique features that the system offers that may not be immediately obvious to users.
To make sure that users understand the implications of using the system, we require a brief communication between the users and operators.

In contrast to vanilla InvenioRDM, having an account is not enough to create uploads in our system.
Instead, the creation of records requires the ``trusted-user`` role, which typically has to be given out by administrators.

Also, communities can be quite confusing in the beginning.
Thus, we restrict the creation of new communities for non-administrators.


OIDC authentication handling
----------------------------

We do not want to handle certain aspects like password management of user management in our system.
Instead, we offload authentication to a separate service, with which InvenioRDM communicates via OIDC.
Sometimes we have slightly non-standard requirements, which are satisfied by the authentication handler logic in this package.


E-Mail notification on errors
-----------------------------

This module defines a custom log handler for error-level logs which sends out notifications as e-mail to a set of configured recipient addresses.


User profile extension
----------------------

We forgot to secure the rights to curate metadata for uploads in our system in the first version of the terms of use.
So instead, we extended the user profiles to collect consent for curation individually per user.


Integration with other TU Wien services
---------------------------------------

One of the benefits of hosting InvenioRDM as an institutional repository is that it enables some conveniences by integrating with the local environment more.
For example, we integrate with [TISS](https://tiss.tuwien.ac.at/) by periodically querying it for TU Wien employees and adding their names to the controlled vocabulary of known ``names``.
