import { Component} from '@angular/core';
import {Router} from '@angular/router';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent {
  productList = []
  brands = []
  categories = {}
  brand = ""
  parent_category = ""
  sub_category = ""

  constructor(
    private readonly router: Router, private readonly route: ActivatedRoute) { 
      this.productList = this.route.snapshot.data['Products']
      this.brands = this.route.snapshot.data['Brands']
      this.categories = this.route.snapshot.data['Categories']
      this.route.queryParams.subscribe(params => {
        this.parent_category = params['category'] ? params['category'] : null;
        this.sub_category = params['subcategory'] ? params['subcategory'] : null;
      });
    }

    selectBrand() {

    }

}
