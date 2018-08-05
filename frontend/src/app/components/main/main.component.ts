import { Component, OnInit, ElementRef, ViewChild, AfterViewInit } from '@angular/core';
import { DisasterZone, Disaster, DisasterResult, Suggestion } from '../../classes/disaster';
import { BackendService } from '../../services/backend.service';
import { HTTPBackendService } from '../../services/HTTPbackend.service';
import { ComputeService } from '../../services/compute.service';
import { LatLngBoundsLiteral, LatLngBounds, AgmMap } from '@agm/core';
import { MockBackendService } from '../../services/mock-backend.service';
import { NgSwitchDefault } from '@angular/common';
import { ActivatedRoute, Params } from '@angular/router';
import { Observable, timer, interval } from 'rxjs';
import { ModalDirective } from 'angular-bootstrap-md';

declare var google: any;

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css'],
})
export class MainComponent implements OnInit, AfterViewInit {

  @ViewChild('div') div: ElementRef;
  @ViewChild('canvas') canvas: ElementRef;
  @ViewChild('agmMap') agmMap: AgmMap;
  public context: CanvasRenderingContext2D;

  @ViewChild('basicModal') basicModal: ElementRef;
  public ICONS = ['./assets/icons/broken_road.png',
    './assets/icons/damaged_building.png',
    './assets/icons/trapped_ppl.png',
    './assets/icons/mud.png',
    './assets/icons/gaz.png',
    './assets/icons/fire.png',
    './assets/icons/flood.png',
    './assets/icons/dieuzilla.png',
    './assets/icons/jb.png',
    './assets/icons/unknown.png'
  ];
  public latitude = 50.6018;
  public longitude = 3.5112;
  public image = '';

  public DISASTER_TYPES = ['Broken road',
    'Damage building',
    'Trapped people',
    'Mud',
    'Gas',
    'Fire',
    'Flood',
    'Godzilla',
    'Justin Bieber Concert',
    'Unknown'];
  public disasterType = '4';
  public suggestion = new Suggestion();
  public disasterZone = new DisasterZone();
  public disasters = [] as Disaster[];
  public disasterResults = [] as Disaster[];
  public bounds = { west: 3.2612, north: 50.8518, south: 50.3518, east: 3.7612 } as LatLngBoundsLiteral;
  public currentDisaster = new Disaster();
  public currentPicture = 2;
  public viewerMode = false;

  constructor(private backendService: HTTPBackendService, private computeService: ComputeService,
    private activatedRoute: ActivatedRoute) {
    this.activatedRoute.queryParams.subscribe((params: Params) => {
      if (params['type'] === 'viewer') {
        this.viewerMode = true;
        console.log('viewer mode enabled');
        interval(1000).subscribe(() => {
          this.getAggregateData();
        });
      }
    });
  }

  ngOnInit() {
  }

  ngAfterViewInit(): void {
    this.context = (<HTMLCanvasElement>this.canvas.nativeElement).getContext('2d');
    this.updateZone();
  }

  clear() {
    this.currentDisaster = new Disaster();
    this.currentDisaster.xy_coordinates = [];
    this.suggestion = new Suggestion();
    this.disasters = [] as Disaster[];
    this.disasterResults = [] as Disaster[];
    this.draw();
  }

  clickPicture(event: MouseEvent) {
    if (!this.viewerMode) {

      const dimension = (event.target as HTMLImageElement).getBoundingClientRect();
      const x = event.clientX - dimension.left;
      const y = event.clientY - dimension.top;

      this.currentDisaster = new Disaster();
      this.currentDisaster.xy_coordinates[0] = x;
      this.currentDisaster.xy_coordinates[1] = y;

      this.currentDisaster.severity = '1';
      this.currentDisaster.status = '2';
      this.currentDisaster.type = '3';

      this.basicModal['show']();
    }
  }

  saveCurrentDisaster() {
    console.log(this.currentDisaster);
    this.backendService.postDisasterPin(this.disasterZone, this.currentDisaster).subscribe(
      (data: Disaster) => {
        this.disasters = this.disasters.map(x => x).concat([data]);
        this.basicModal['hide']();
        this.draw();
      }
    );

  }

  getAggregateData() {
    this.backendService.getDisasters(this.disasterZone).subscribe(
      (data: DisasterResult) => {
        console.log(data);
        this.disasterResults = data.results;
        this.draw();
      }
    );
  }

  drawDisasters(disasters: Disaster[]) {
    disasters.forEach(disaster => {
      const drawing = new Image();
      drawing.src = this.ICONS[disaster.type]; // can also be a remote URL e.g. http://
      const context = this.context;
      const computeService = this.computeService;
      const canvas = this.canvas;
      const disasterZone = this.disasterZone;

      drawing.onload = function () {
        context.drawImage(drawing, disaster.xy_coordinates[0] - drawing.width / 2, disaster.xy_coordinates[1] - drawing.height / 2);
      };
    });
  }

  draw() {
    this.context.clearRect(0, 0, this.canvas.nativeElement.width, this.canvas.nativeElement.height);
    this.drawDisasters(this.disasters);
    this.drawDisasters(this.disasterResults);

    if (this.suggestion.results) {
      this.suggestion.results.forEach(
        suggestionResult => {
          if (suggestionResult) {
            this.drawSquare(suggestionResult.coordinates[0],
              suggestionResult.coordinates[1],
              suggestionResult.coordinates[2] - suggestionResult.coordinates[0],
              suggestionResult.coordinates[3] - suggestionResult.coordinates[1]);
          }
        }
      );
    }
  }

  getSuggestion() {
    console.log(this.disasterType);
    this.backendService.getSuggestions(this.disasterZone, this.disasterType).subscribe(
      (data: Suggestion) => {
        this.suggestion = data;
        console.log(data);

        this.draw();
      }
    );
  }

  drawSquare(x: number, y: number, width: number, height: number) {
    this.context.beginPath();
    this.context.rect(x, y, width, height);
    this.context.lineWidth = 5;
    this.context.strokeStyle = 'black';
    this.context.stroke();
  }

  getIconUrl(disasterType: number): string {
    return this.ICONS[disasterType];
  }

  back() {
    this.clear();
    this.currentPicture--;
    if (this.currentPicture === 0) {
      this.currentPicture = 17;
    }
    this.updateZone();
  }

  next() {
    this.clear();
    this.currentPicture++;
    if (this.currentPicture === 17) {
      this.currentPicture = 1;
    }
    this.updateZone();
  }

  updateZone() {
    this.clear();
    this.backendService.getDisasterZone(this.currentPicture).subscribe(
      (data: DisasterZone) => {
        console.log(data);
        this.disasterZone = data;
        const center = this.computeService.computeCenter(this.disasterZone);
        this.image = data.image;
        this.latitude = center[0];
        this.longitude = center[1];
        this.updateView();
      },
      error => console.log(error) // error path
    );
  }

  updateView() {
    console.log('map ready');
    const bounds: LatLngBounds = new google.maps.LatLngBounds();

    const offset = 0.000445;
    let lattitude = this.disasterZone.coordinates[0][0] - offset;
    let longitude = this.disasterZone.coordinates[0][1] + offset;

    bounds.extend(new google.maps.LatLng(lattitude, longitude));

    lattitude = this.disasterZone.coordinates[1][0] + offset;
    longitude = this.disasterZone.coordinates[1][1] - offset;
    bounds.extend(new google.maps.LatLng(lattitude, longitude));
    this.agmMap['_mapsWrapper'].fitBounds(bounds);
  }
}
