import { Injectable } from '@angular/core';
import { DisasterZone } from '../classes/disaster';

@Injectable({
  providedIn: 'root'
})
export class ComputeService {

  constructor() { }

  public getLattitudeOffset(disasterZone: DisasterZone): number {
    return disasterZone.coordinates[1][0] - disasterZone.coordinates[0][0];
  }

  public getLongitudeOffset(disasterZone: DisasterZone): number {
    return disasterZone.coordinates[1][1] - disasterZone.coordinates[0][1];
  }

  public computeCenter(disasterZone: DisasterZone): number[] {
    return [disasterZone.coordinates[0][0] + this.getLattitudeOffset(disasterZone) / 2.0,
    disasterZone.coordinates[0][1] + this.getLongitudeOffset(disasterZone) / 2.0];

  }

  public computePixels(disasterZone: DisasterZone, longitude: number, lattitude: number, width: number, height: number) {
    const x = (longitude - disasterZone.coordinates[0][1]) / this.getLongitudeOffset(disasterZone) * width;
    const y = (lattitude - disasterZone.coordinates[0][0]) / this.getLattitudeOffset(disasterZone) * width;

    return [x, y];
  }

  public computeCoordinates(disasterZone: DisasterZone, x: number, y: number, width: number, height: number): number[] {
    const ratio_h = y / height;
    const ratio_w = x / width;

    return [disasterZone.coordinates[0][0] + this.getLattitudeOffset(disasterZone) * ratio_h,
    disasterZone.coordinates[0][1] + this.getLongitudeOffset(disasterZone) * ratio_w];
  }
}
