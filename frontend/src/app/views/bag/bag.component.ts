import { Component } from '@angular/core';
import { Router, NavigationEnd, ActivatedRoute } from '@angular/router';
import { CookieManagerService } from '../../../utilities/services/cookie-manager.service'
import {GoogleTagManagerService} from 'angular-google-tag-manager';

@Component({
  selector: 'app-bag',
  templateUrl: './bag.component.html',
  styleUrls: ['./bag.component.scss']
})
export class BagComponent {
  _bag = [{"ID":102,"NAME":"US Polo Assn. Juniors Solid Polo With Small Pony","SIZE":"XXL","COLOR":"RED","IMAGE_LINK":"https://storage.cloud.google.com/css-retail-images/subcat_tops_tees.png","PRICE":25,"quantity":1},{"ID":158,"NAME":"Plain Long Spaghetti Strap Tank Top Camis Basic Camisole Cotton","SIZE":"XXL","COLOR":"RED","IMAGE_LINK":"https://storage.cloud.google.com/css-retail-images/subcat_tops_tees.png","PRICE":8.35,"quantity":1}]
  bagTotal = '0.00'
  editBag;
  products = [];
  test = '';
  getCookie;
  setCookie;
  recently_viewed = [];
  recommended = [];

  constructor(private readonly cookieManagerService: CookieManagerService, private readonly route: ActivatedRoute, private readonly router: Router, private readonly gtmService: GoogleTagManagerService) { 
    this.recommended = this.route.snapshot.data["FeaturedProducts"];
    this.recently_viewed = this.route.snapshot.data["RecentlyViewed"];
    try {
      if(Object.keys(this.recently_viewed).includes('recommendationToken')) this.recently_viewed = []
    } catch (error) {
      console.log(error)
    }
    this.cookieManagerService.bag$.subscribe(val => {
      this._bag = val;
      this.products = [];
      val.forEach(item => {
        this.products.push({
          "id": String(item.ID),
          "quantity": item.quantity,
          "originalPrice": item.PRICE,
          "displayPrice": item.PRICE,
          "currencyCode":"USD",
        });
      });
    })
    this.cookieManagerService.bag$.subscribe(val => {
      let total = 0.0;
      val.forEach(i => total += i.quantity*i.PRICE);
      this.bagTotal = total.toFixed(2);
    })
    this.editBag = (index: number, newQuantity: number) => {
      this.cookieManagerService.editBag(index, newQuantity);  
      this.cookieManagerService._bag = this._bag;
      this.cookieManagerService.bag = this._bag;
    }
    this.getCookie = this.cookieManagerService.getCookie;
    this.setCookie = this.cookieManagerService.setCookie;

    this.router.events.forEach(item => {
      if (item instanceof NavigationEnd) {
        const gtmTag = {
          "automl": {
            "eventType": 'checkout-start',
            "userInfo": {
              "visitorId": cookieManagerService.visitorId$.value,
              "userId": this.cookieManagerService.visitorId$.value
            },
            "productEventDetail": {
              "productDetails": this.products,
            }
          }
        };
        this.gtmService.pushTag(gtmTag);
      }
    });
    this._bag = [{"ID":102,"NAME":"US Polo Assn. Juniors Solid Polo With Small Pony","SIZE":"XXL","COLOR":"RED","IMAGE_LINK":"https://storage.cloud.google.com/css-retail-images/subcat_tops_tees.png","PRICE":25,"quantity":1},{"ID":158,"NAME":"Plain Long Spaghetti Strap Tank Top Camis Basic Camisole Cotton","SIZE":"XXL","COLOR":"RED","IMAGE_LINK":"https://storage.cloud.google.com/css-retail-images/subcat_tops_tees.png","PRICE":8.35,"quantity":1}];
  }
  help(item) {
    console.log(item);
  }
}
