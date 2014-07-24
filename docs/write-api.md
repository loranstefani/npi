NPPES Write API (Draft)
=======================

The NPPES Write API facilitates creation and updates of NPI-1 and NPI-2
enumeration records via a RESTful API.


The URL
=======

The URL is `/api/write`.  Currently, the full URL is
`https://nppes.npi.io/api/write`. This is not an official CMS resource and is for
development and testing purposes only.  Do not submit real personaly identifiiable
information (PII) such as social security number to this system. 


Authentication
==============

Authentication for the API uses HTTP Auth.  This means that the username and
password must be passed in the request header. You will need a working username
and password for `https://nppes.npi.io` in order to use the API. 


The HTTP Request Format
=======================

The request body is JSON and follows the ProviderJSON format defined here.
https://github.com/HHSIDEAlab/pjson . This format is based on the NPI final rule.

The request `Content-Type` shall be `application/json`.  The HTTP method for
submission is POST.

When ProviderJSON is submitted to the API it is first validated using a library
that can be found in the aforementioned Github repository.  This
library can be used in your own code or you can use the corresponding command
line utility that performs the same validation.  Since the same validation can be
accessed on both sides of the transaction, you can have a reasonable level of
confidence that your submissions will be accepted before sending them through
the API.  There are however some additional validation performed by the API that
cannon be included in the ProviderJSON validation tool.  For example, if you
attempted to update a non-existent NPI, the API will reply with an error and
not allow the transaction. 

The HTTP Response Format
========================

The response body shall be a JSON object with a `Content-Type` of
`application/json`.  If the record is created, the JSON object shall contain a
`"status": "CREATED"`.If the record is updated, the JSON object shall contain a
`"status": "UPDATED"`. If the record was not created or updated, then the JSON
object shall contain a `"status": "UPDATED"`.  When errors are present, these
shall be listed in an array field `[]` called `errors`. 



An Example in Curl
==================

In this example we use `-u` to provide the HTTP Auth credentials, `-H` to specify
the `Content-Type` as `application/json`, and `--data @test.json` to read the
json from a file called `test.json` into the request body.


    curl -u your-username:your-password -H "Content-Type: application/json" --data @test.json https://nppes.npi.io/api/write

