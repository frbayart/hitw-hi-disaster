import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-startup',
  templateUrl: './startup.component.html',
  styleUrls: ['./startup.component.css']
})
export class StartupComponent implements OnInit {

  constructor(private router: Router) { }

  ngOnInit() {
  }

  public openMainApp() {
    return this.router.navigate(['/main']);
  }
}
