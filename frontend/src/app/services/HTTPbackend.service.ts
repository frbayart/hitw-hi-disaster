import { Injectable } from '@angular/core';
import { BackendService } from './backend.service';
import { Disaster, DisasterResult, DisasterZone, Suggestion, Win } from '../classes/disaster';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class HTTPBackendService extends BackendService {
    private disastersUrl = 'http://10.20.0.52:5000/hd/disaster-zone/<zid>/disaster';
    private disasterZoneUrl = 'http://10.20.0.52:5000/hd/disaster-zone/<zid>';
    private disasterPinPostUrl = 'http://10.20.0.52:5000/hd/disaster-zone/<zid>/disaster';
    private suggestionUrl = 'http://10.20.0.52:5000/hd/disaster-zone/<zid>/<disasterType>';

    constructor(private http: HttpClient) {
        super();
    }

    public getDisasterZone(zoneId: number): Observable<DisasterZone> {
        const regex = /<zid>/gi;
        const route = this.disasterZoneUrl.replace(regex, zoneId.toString());
        return this.http.get(route) as Observable<DisasterZone>;
    }

    public getDisasters(disasterZone: DisasterZone): Observable<DisasterResult> {
        const regex = /<zid>/gi;
        const route = this.disastersUrl.replace(regex, disasterZone.id.toString());
        return this.http.get(route) as Observable<DisasterResult>;
    }

    public getSuggestions(disasterZone: DisasterZone, disasterType: string): Observable<Suggestion> {
        let regex = /<zid>/gi;
        let route = this.suggestionUrl.replace(regex, disasterZone.id.toString());
        regex = /<disasterType>/gi;
        route = route.replace(regex, disasterType);

        return this.http.get(route) as Observable<Suggestion>;
    }

    public getWin(): Observable<Win> {
        return this.http.get('http://10.20.0.52:5000/hd/biere') as Observable<Win>;
    }

    public postDisasterPin(disasterZone: DisasterZone, disaster: Disaster): Observable<Disaster> {
        const regex = /<zid>/gi;
        const route = this.disasterPinPostUrl.replace(regex, disasterZone.id.toString());
        console.log(route);
        return this.http.post(route, disaster) as Observable<Disaster>;
    }
}
