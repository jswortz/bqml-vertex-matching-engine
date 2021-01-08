import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router, NavigationEnd} from '@angular/router';

import {CookieManagerService} from '../../../utilities/services/cookie-manager.service'
import {GoogleTagManagerService} from 'angular-google-tag-manager';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  login = false;
  products:any = [];
  recently_viewed:any = [];

  constructor(private gtmService: GoogleTagManagerService, private readonly router: Router, private readonly route: ActivatedRoute, private readonly cookieManagerService: CookieManagerService) { 
    this.router.events.forEach(item => {
      if (item instanceof NavigationEnd) {
        const gtmTag = {
          "automl": {
            "eventType": 'home-page-view',
            "userInfo": {
              "visitorId": cookieManagerService.visitorId$.value,
              "userId": cookieManagerService.visitorId$.value
            }
          }
        };
        this.gtmService.pushTag(gtmTag);
      }
    });
    this.products = this.route.snapshot.data["FeaturedProducts"];
    this.recently_viewed = this.route.snapshot.data["RecentlyViewed"];

  }

  ngOnInit(): void {
  }

}
