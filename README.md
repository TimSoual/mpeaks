# Mpeaks Project

## Description

This is a project allowing to store and retrieve data concerning mountain peaks.
It was created in a weekend as a technical test before an interview.
The project uses Django Rest Framework with PostGIS and is deployed with docker and docker-compose.

## Installation

In order to use the project, you need docker and docker-compose.

Then to launch the server:

```sh
docker-compose up --build
```

And to stop it:

```sh
docker-down
```

## Usage

After launch, the api is visible at http://localhost:8000/
This redirects to http://localhost:8000/doc/ which shows the api usage.

The project urls are as follow:

* http://localhost:8000/peaks

Callable with get and post. Get takes no parameter and returns the list of peaks.
The post request takes a new peak as a body parameter and creates and returns a new peak.
The following can be given as a parameter:

```json
{
"name": "Mont blanc",
"location": {
        "type": "Point",
        "coordinates": [45.8326, 6.8652]
    },
"altitude": 4810
}
```

* http://localhost:8000/peaks/id

Callable with get, put and delete. Get takes an id as parameter and returns the peak.
Put takes an id and a peak as json and returns the modified peak. (the same json as above can be given)
Delete takes an id and returns a status of 204.

* http://localhost:8000/peaks/filter

Callable with get. Returns a list of peaks in an area.
Takes 4 query string parameters : minlon, maxlon, minlat and maxlat for minimum and maximum latitude and longitude.
For example: http://localhost:8000/peaks/filter/?minlon=1&maxlon=1000&minlat=1&maxlat=1000

* http://localhost:8000/doc

Swagger documentation of the API.

## Possible improvements

* Add unit testing
* Add production deployment options
* Improve the swagger documentation
