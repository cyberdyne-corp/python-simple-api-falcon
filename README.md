# Falcon API

Simple demo of a Python REST API using Falcon.

## About

Falcon: a very fast Python framework for building cloud APIs, app backends, and WSGI middleware.

http://falconframework.org/

# Use it

## Setup

Install falcon (assuming you got a Python devel environment ready):

````
$ pip install falcon
````

## Play

Run it:

````
$ python myrestapi.py
````

Query it:

````
$ curl http://localhost:8080/containers/
```` 

````
$ curl -H 'Content-Type: application/json' -X PUT -d '{"image": "organization/image", "service": "myService"}' http://localhost:8080/containers/
```` 

````
$ curl -X DELETE http://localhost:8080/containers/stomped_archibald
```` 
