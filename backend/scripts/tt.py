import jsonschema

create_disaster_schema = {
        "$schema": "http://json-schema.org/schema#",

        "type": "object",
        "properties": {
            "doc": {"type": "string"},
            "dou": {"type": "string"},
            "coordinates": {
                "type": "array",
                "minItems": 2,
                "maxItems": 2,
                "items": { "type": "number"}
            },  
            "type": { "type": "integer", "enum": [0, 1, 2, 3, 4, 5, 6, 7, 8] },
            "status": { "type": "integer", "enum": [0, 1, 2]},
            "severity": { "type": "integer", "enum": [0, 1, 2, 3, 4]},
            "zone_id": { "type": "integer" },
            "id": { "type": "string" },
        }
    }



sample = { "status" : 2, "severity" : 1, "coordinates" : [ -38.26258213816534, 144.5778443645971 ], "type" : 3, "id" : "b91955786abc4009b85a033bd24fc55f", "zone_id" : 666}

try:
    jsonschema.validate(sample, create_disaster_schema)
except jsonschema.exceptions.ValidationError, e:
    print str(e).split('\n')[0]
