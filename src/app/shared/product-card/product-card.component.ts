import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-product-card',
  templateUrl: './product-card.component.html',
  styleUrls: ['./product-card.component.scss']
})
export class ProductCardComponent implements OnInit {
  @Input() product;
  
  ngOnInit() {
    if(Object.keys(this.product).includes('IMAGE LINK')){
      this.product['IMAGE_LINK'] = this.product['IMAGE LINK'];
    }
  }
}
