import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-product-card',
  templateUrl: './product-card.component.html',
  styleUrls: ['./product-card.component.scss']
})
export class ProductCardComponent {
  @Input() product = {
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
    "DISCOUNT": false
  }

}
