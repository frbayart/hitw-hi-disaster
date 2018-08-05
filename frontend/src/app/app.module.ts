import { BrowserModule } from '@angular/platform-browser';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { MDBBootstrapModule } from 'angular-bootstrap-md';

import { Route, RouterModule, ActivatedRoute } from '@angular/router';
import { AppComponent } from './app.component';
import { MainComponent } from './components/main/main.component';
import { CommonModule } from '@angular/common';
import { StartupComponent } from './components/startup/startup.component';

import { AgmCoreModule } from '@agm/core';
import { HttpClientModule } from '@angular/common/http';

import { HTTPBackendService } from './services/HTTPbackend.service';
import { BackendService } from './services/backend.service';
import { MockBackendService } from './services/mock-backend.service';

import { NgSelectModule } from '@ng-select/ng-select';
import { FormsModule } from '@angular/forms';
import { AboutComponent } from './components/about/about.component';

export const ROUTES: Route[] = [
  {
    path: '',

    component: MainComponent
  }, {
    path: 'main',

    component: MainComponent
  }, {
    path: 'about',

    component: AboutComponent
  }
];


@NgModule({
  declarations: [
    AppComponent,
    MainComponent,
    StartupComponent,
    AboutComponent
  ],
  imports: [
    MDBBootstrapModule.forRoot(),
    NgSelectModule,
    FormsModule,
    BrowserModule,
    RouterModule.forRoot(ROUTES),
    AgmCoreModule.forRoot({
      apiKey: 'AIzaSyAGYUGG1GNsfr818v66O6gfRvyLgFnm2eQ',
      libraries: ['places']
    }),
    HttpClientModule
  ],
  schemas: [NO_ERRORS_SCHEMA],
  providers: [
    { provide: BackendService, useValue: HTTPBackendService }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
