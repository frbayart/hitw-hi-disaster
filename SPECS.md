# BACKEND FEATURES

## Main loop
- take a picture of a disaster as input
- find the corresponding location on google maps
- queue/store a disaster object

## API
- Context path: /hd
- GET /disaster-zone (returns the next disaster to analyse)
- GET /disaster-zone/{id}/{disasterType} (autodetect disasterType in the given zone)                     8====3
- GET /disaster-zone/{id}/disaster      > get all disasters for a zone
- POST /disaster-zone/{id}/disaster (add an annotation)
- PUT /disaster-zone/{id}/disaster/{id} (update annotation, its status)
- GET /disaster-zone/biere (random FAILED or WIN pour gagner une bière

## OBJECT MODEL

```
POST /hd/disaster-zone/<zid>/disaster
{
        "doc": xx,
        "dou": None,
        "coordinates": [(x, y), (x,y)],
        "type": 8,
        "status": 0,
        "severity": 3,
        }
```



### Disaster:
- doc
- dou
- zone id
- geo coordinates point
- disaster type
- disaster status
- disaster severity

```
{
        "doc": ISODate("2018-08-03T15:42:28.336Z"),
        "coordinates": [
                [0, 0],
                [800, 600]
        ],
        "id": 666,
        "dou": null
}
```

```
% curl http://10.20.0.52:5000/hd/disaster-zone
"{\"severity\": 3, \"doc\": \"2018-08-03T15:58:35.299068\", \"coordinates\": [[0, 0], [800, 600]], \"type\": 8, \"id\": 666, \"dou\": null}"%
```


### DisasterZone:
- doc
- dou
- disaster zone photo bytes (or link ?)
- geo coordinates of the zone

### Suggestion:
- zone id
- disaster type
- squares (array de rectangles de xavier)

## TYPES

### DisasterStatus (enum):
* 0 active (default)
* 1 fixed

### DisasterType (enum):
* 0 broken road
* 1 damaged building
* 2 trapped people
* 3 mud
* 4 gaz
* 5 fire
* 6 flood
* 7 godzilla
* 8 justin bieber concert

### DisasterSeverity (enum):
* 0 Low
* 1 Medium
* 2 High
* 3 Very high
* 4 OMGWTF!!!1!

