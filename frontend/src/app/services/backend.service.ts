import { Injectable } from '@angular/core';
import { DisasterResult, DisasterZone, Disaster, Suggestion, Win } from '../classes/disaster';
import { Observable } from 'rxjs';

export abstract class BackendService {
  public abstract getDisasterZone(zoneId: number): Observable<DisasterZone>;
  public abstract getDisasters(disasterZone: DisasterZone): Observable<DisasterResult>;
  public abstract getSuggestions(disasterZone: DisasterZone, disasterType: string): Observable<Suggestion>;
  public abstract postDisasterPin(disasterZone: DisasterZone, disaster: Disaster): Observable<Disaster>;
  public abstract getWin(): Observable<Win>;
}
