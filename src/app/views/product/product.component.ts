import { Component } from '@angular/core';
import {Router} from '@angular/router';
import {ActivatedRoute} from '@angular/router';
import {CookieManagerService} from '../../../utilities/services/cookie-manager.service'
import UIkit from 'uikit';

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
    "DISCOUNT": false
  }
  sizeSelection = 'S' 
  recently_viewed = []
  colorSelection = ''

  constructor(
    private readonly router: Router, private readonly route: ActivatedRoute, private readonly cookieManagerService:CookieManagerService) { 
      this.product = this.route.snapshot.data["Product"];

  }

  addBag() {
    if(this.sizeSelection) {
      this.cookieManagerService.addToBag(this.product.ID, 
            this.product.NAME, 
            this.product.IMAGE_LINK, 
            this.product.PRICE, 
            this.product.SIZE, 
            this.product.COLOR,
            false,
            0,
            )
    }
    else {
        UIkit.notification(
            'Please select a size',
            {status: "danger"}
        )
    }
  }

}
