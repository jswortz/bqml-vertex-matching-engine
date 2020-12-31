import { Component } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { CookieManagerService } from '../../../utilities/services/cookie-manager.service'
import {GoogleTagManagerService} from 'angular-google-tag-manager';

@Component({
  selector: 'app-bag',
  templateUrl: './bag.component.html',
  styleUrls: ['./bag.component.scss']
})
export class BagComponent {
  _bag = []
  bagTotal = 0.0
  bagSize = 0
  editBag;
  products = [];
  test = '';
  getCookie;
  setCookie;

  constructor(private readonly cookieManagerService: CookieManagerService, private readonly router: Router, private readonly gtmService: GoogleTagManagerService) { 
    this.cookieManagerService.bag$.subscribe(val => {
      this._bag = val;
      this.products = [];
      val.forEach(item => {
        this.products.push({
          "id": item.ID,
          "originalPrice": item.PRICE,
          "displayPrice": item.PRICE,
        });
      });
      console.log(this._bag);
    })
    this.cookieManagerService.bagSize$.subscribe(val => {
      this.bagSize = val;
    })
    this.cookieManagerService.bagTotal$.subscribe(val => {
      this.bagTotal = val;
    })
    this.editBag = this.cookieManagerService.editBag;
    this.getCookie = this.cookieManagerService.getCookie;
    this.setCookie = this.cookieManagerService.setCookie;

    this.router.events.forEach(item => {
      if (item instanceof NavigationEnd) {
        const gtmTag = {
          "automl": {
            "eventType": 'detail-page-view',
            "userInfo": {
              "visitorId": cookieManagerService.visitorId$.value,
            },
            "productEventDetail": {
              "productDetails": this.products,
              "purchaseTransaction": {
                "revenue": this.bagTotal
              }
            }
          }
        };
        this.gtmService.pushTag(gtmTag);
      }
    });
  }
  help(item) {
    console.log(item);
  }
}
