NPPES Testing & Gap  Example:
=============================

This document contains 2 sets of tests. The first set passes and the second
set does not because it is not yet implemented (i.e. "a Gap"). The diagram outlines the basic 
process flow.

![alt text](http://nppes.s3.amazonaws.com/test-process.png "Testing Flow")


Example 1. - Self-Takeover
==========================

1.1 The Use Case:
-----------------
A user shall be able to take control (i.e. manage) of his or her own Type-1 NPI by providing the NPI number, last four SSN (or ITI), year of birth, and attesting by clicking a check box that it is indeed thier information (via a check-box). A user cannot supply both an SSN and ITIN.



1.2 Determine the Key Infromation Needed to Perform the Test
------------------------------------------------------------

The test identifies (as necessary):

* the URL `/enumerations/self-take-over`
* the user logged in
* the data that must already exist in the database to perform the work/test (as a fixture).
* The data that is submitted to the application (in this case as as a web form).

1.3 Define Several Tests
-------------------------

These tests are individual requirements of the Use Case.  We have defined 7.  We could come up with more but this is a reasonable amount of code coverage for this function IMHO.


1. Successfully suppying all information with last four of SSN will allow a user to manage the specified record.
2. Successfully suppying all information with last four of ITIN will allow a user to manage the specified record.
3. Suppying an incorrect SSN will not result in management of the record.
4. Suppying an incorrect ITIN will not result in management of the record.
5. Suppplying both SSN and ITIN will not result in management of the record.
6. Suppying an incorrect year of birth will not result in management of the record.
7. Not checking the "I attest" checkbox will not result in management of the record.


Example 2. - Print a Historical Enumeration Report
==================================================

2.1 The Use Case:
-----------------
A staff user can provide a valid enumeration record ID and get an HTML report of all changes to the enumeration record including who changed what when.

2.2 Determine the Key Infromation Needed to Perform the Test
------------------------------------------------------------

The test identifies (as necessary):

* the URL `/enumerations/self-take-over/[enmeration_id]`
* the user logged in (staff user 'alan' ) and a non staff member 'not-staff' for negative testing.
* the data that must already exist in the database to perform the work/test (as a fixture).
* The data that is submitted to the application (in this case an `enumeration_id` provided as part of the URL.

2.3 Define Several Tests
-------------------------


1. Going to the URL generates a report with a history of the enumeration record.
2. If a user is not a staff user he or she should not get the report and are instead redirected to provide staff credentials.




3. Running Tests
================

This is quite easy to run and re-run test once written.  Each of these use cases are defined in their own file within `apps/enumerations/tests`.

    python manage.py test apps.enumerations.
    Creating test database for alias 'default'...
    .
    .
    ERROR: test_a_user_historical_report_is_generated (apps.enumerations.tests.test_print_historical_enumerator_report.PrintHistoricalReport_TestCase
    ,
    ,
    ValueError: The view apps.enumerations.views.create_historical_report didn't return an HttpResponse object.
    Ran 9 tests in 1.014s
    FAILED (errors=1)
    Destroying test database

The first 7 from Use Case 1 ran no problem, but one failed in the "Print a Historical Enumeration Report" Use Case. This is what we would expect since it is not yet implemented.  In this way, running the tests actually produce the gap.



