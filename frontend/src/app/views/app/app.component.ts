import {AfterViewInit, Component} from '@angular/core';
import {Event, NavigationCancel, NavigationEnd, NavigationError, Router} from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements AfterViewInit {
  isLoading = true;

  constructor(private readonly router: Router) {
  }

  ngAfterViewInit() {
    this.router.events.subscribe((event: Event) => {
      switch (true) {
        case event instanceof NavigationEnd:
        case event instanceof NavigationCancel:
        case event instanceof NavigationError: {
          this.isLoading = false;
          break;
        }
        default:
          break;
      }
    });
  }
}
