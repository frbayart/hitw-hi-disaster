export class Disaster {
    private doc: string;
    private dou: string;
    public type: string;
    public status: string;
    public severity: string;
    public xy_coordinates = [0, 0];
    public coordinates = [0, 0];
}

export class DisasterZone {
    public severity = '3';
    public coordinates = [[0, 0], [800, 600]];
    public doc = '2018-08-03T15:42:28.336Z';
    public type = '8';
    public id = 1;
    public image = '';
    public dou = '2018-08-03T15:42:28.336Z';
}

export class DisasterResult {
    public results = [] as Disaster[];
}

export class SuggestionResult {
    public zone_id = '1';
    public score = 0.28;
    public coordinates: [0, 0, 10, 10, 1];
    public disaster_type = 4;
}

export class Suggestion {
    public results = [] as SuggestionResult[];
}