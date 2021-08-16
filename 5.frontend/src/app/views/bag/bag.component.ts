import { Component } from '@angular/core';
import { Router, NavigationEnd, ActivatedRoute } from '@angular/router';
import { CookieManagerService } from '../../../utilities/services/cookie-manager.service';
import {GoogleTagManagerService} from 'angular-google-tag-manager';
import {getRandomValues} from '../../../utilities/helpers/getRandomValues';

@Component({
  selector: 'app-bag',
  templateUrl: './bag.component.html',
  styleUrls: ['./bag.component.scss']
})
export class BagComponent {
  bag = [];
  bagTotal = '0.00';
  editBag;
  products = [];
  test = '';
  getCookie;
  setCookie;
  recentlyViewed = [];
  recommended = [];
  getRandomValues = getRandomValues;


  constructor(private readonly cookieManagerService: CookieManagerService,
              private readonly route: ActivatedRoute,
              private readonly router: Router,
              private readonly gtmService: GoogleTagManagerService) {
    this.recommended = this.route.snapshot.data['FeaturedProducts'];
    this.recommended = this.getRandomValues(this.recommended, 5);
    this.recentlyViewed = this.route.snapshot.data['RecentlyViewed'];
    try {
      if (Object.keys(this.recentlyViewed).includes('recommendationToken')) {
        this.recentlyViewed = [];
      }
    } catch (error) {
      console.log(error);
    }
    this.cookieManagerService.bag$.subscribe(val => {
      this.bag = val;
      this.products = [];
      val.forEach(item => {
        this.products.push({
          id: String(item.ID),
          quantity: item.quantity,
          originalPrice: item.PRICE,
          displayPrice: item.PRICE,
          currencyCode: 'USD',
        });
      });
    });
    this.cookieManagerService.bag$.subscribe(val => {
      let total = 0.0;
      val.forEach(i => total += i.quantity * i.PRICE);
      this.bagTotal = total.toFixed(2);
    });
    this.editBag = (index: number, newQuantity: number) => {
      this.cookieManagerService.editBag(index, newQuantity);
      this.cookieManagerService.bag = this.bag;
    };
    this.getCookie = this.cookieManagerService.getCookie;
    this.setCookie = this.cookieManagerService.setCookie;

    this.router.events.forEach(item => {
      if (item instanceof NavigationEnd) {
        const gtmTag = {
          automl: {
            eventType: 'checkout-start',
            userInfo: {
              visitorId: cookieManagerService.visitorId$.value,
              userId: this.cookieManagerService.visitorId$.value
            },
            productEventDetail: {
              productDetails: this.products,
            }
          }
        };
        this.gtmService.pushTag(gtmTag);
      }
    });
  }
  help(item): void {
    console.log(item);
  }
}
