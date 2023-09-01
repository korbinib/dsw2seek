# DSW2Seek

## Project overview

dsw2seek is a python web application that transfers Data Management Plans (DMPs) from DSW to FAIRDOM-SEEK.

## Important resources

DSW test environment: https://dsw-test.elixir.no/
DSW SDK: https://github.com/ds-wizard/dsw-sdk

Seek API documentation: https://docs.seek4science.org/tech/api/
Examples using the Seek API: https://docs.seek4science.org/help/user-guide/api.html
Seek for Docker: https://docs.seek4science.org/tech/docker

## Seek API

Example request to the Seek API:

```
GET http://localhost:3000/projects/1 HTTP/1.1
Accept: application/vnd.api+json
Accept-Charset: ISO-8859-1
Authorization: Basic <credentials>
Content-Type: application/vnd.api+json
```

The authorization credentials are the base64-encoding of the string "<username>:<password>".
