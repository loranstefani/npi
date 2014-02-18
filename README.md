NPPES Redux
===========

This is a redesign of the National Plan and Provider Enumeration System (NPPES).
NPPES is a system managed by the Cevters for Medicare and Medicaid Services
(CMS).See http://cms.hhs.gov for more information. NPPES is designed to
enumerate all providers in the United States.

The Google Group for this project is here: https://groups.google.com/d/forum/nppes


License and Contributions
=========================

This project is being developed by the federal government of the United States
and is public domain.  We invite any interested parties to help make this great.
We can accept pull requests. If you wish to contribute to this effort
please send an email to `alan.viars at cms.hhs.gov`. Please consider joining the
Google Group too.

About
=====

The project is written in Python and uses the Django web framework.  For more
information on Django see https://www.djangoproject.com/

Branches
========

This project is still in an early development phase and hence we are pushing to
the `master` branch for the time being.  We will soon be switching to working
from a branch called `develop`.


Installation Quick Start
========================

Here are short set of instructions for getting the project running in a local
environment. These instructions assume Python 2.7 and pip are already installed.

Dowload the source code:

    git clone git@github.com:HHSIDEAlab/npi.git

Change into the project directory:

    cd npi

Install all requierises using pip:

    pip install -r npi/requirements.txt


Build the database and install fixtures:

    python manage.py syncdb
    
Run the development server on http://127.0.0.1/8000.
    
    python manage.py runserver

Point your browser to http://127.0.0.1 to see the main page.


Other Important Notes:
======================

Currently, user creation occurs in the Django admin.  It is envisioned that
accounts will be created using CMS's current Identity and Access (I&A) system.
PECOS and EHRIncentives also use I&A for access.  A user is not the same thing
as an Enumeration.  


