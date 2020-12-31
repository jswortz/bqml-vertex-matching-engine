import { Component } from '@angular/core';
import {ActivatedRoute, Router, NavigationEnd} from '@angular/router';
import {CookieManagerService} from '../../../utilities/services/cookie-manager.service';
import UIkit from 'uikit';
import {getRandomValues} from '../../../utilities/helpers/getRandomValues';
import {GoogleTagManagerService} from 'angular-google-tag-manager';

@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrls: ['./product.component.scss']
})
export class ProductComponent {
  product = {
    "ID": 0,
    "NAME": "",
    "SIZE": "",
    "COLOR": "",
    "COMPANY": "",
    "CATEGORY": "",
    "SUB_CATEGORY": "",
    "IMAGE_LINK": "",
    "REVIEW": null,
    "AVAILABILITY": 0,
    "ESTIMATE_DELIVERY_AT": 0,
    "PRICE": 0.0,
    "RECOMMENDATIONS": [],
    "DISCOUNT": false,
    "bought_together": [],
    "recommended": []
  }
  sizeSelection = '' 
  recently_viewed = []
  colorSelection = ''
  getRandomValues = getRandomValues;

  constructor( private gtmService: GoogleTagManagerService,
    private readonly router: Router, private readonly route: ActivatedRoute, private readonly cookieManagerService:CookieManagerService) { 
      this.product = this.route.snapshot.data["Product"];
      try {
        console.log(this.product);
        this.product = this.product[0];
        this.product.bought_together = getRandomValues(this.product.RECOMMENDATIONS, 3);
        this.product.recommended = getRandomValues(this.product.RECOMMENDATIONS, 3);
        this.colorSelection = this.product.COLOR
        
      } catch (error) {
        console.log(error);
        console.log(this.product);
        this.product = {
          "ID": 0,
          "NAME": "",
          "SIZE": "",
          "COLOR": "",
          "COMPANY": "",
          "CATEGORY": "",
          "SUB_CATEGORY": "",
          "IMAGE_LINK": "",
          "REVIEW": null,
          "AVAILABILITY": 0,
          "ESTIMATE_DELIVERY_AT": 0,
          "PRICE": 0.0,
          "RECOMMENDATIONS": [],
          "DISCOUNT": false,
          "bought_together": [],
          "recommended": []
        }
      }
      this.router.events.forEach(item => {
        if (item instanceof NavigationEnd) {
          const gtmTag = {
            "automl": {
              "eventType": 'detail-page-view',
              "userInfo": {
                "visitorId": cookieManagerService.visitorId$.value
              },
              "productEventDetail": {
                "productDetails": [
                  {
                    "id": this.product.ID,
                    "originalPrice": this.product.PRICE,
                    "displayPrice": this.product.PRICE,
                  }
                ]
              }
            }
          };
          this.gtmService.pushTag(gtmTag);
        }
      });
  }

  setSize(size) {
    this.sizeSelection = size;
  }

  setColor(color) {
    this.colorSelection = color;
  }

  addBag() {
    if(this.sizeSelection) {
      this.cookieManagerService.addToBag(this.product);
    }
    else {
        UIkit.notification(
            'Please select a size',
            {status: "danger"}
        )
    }
  }

}
