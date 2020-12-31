import { Component, ViewChild, Input } from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent {
  productList = [];
  brands = [];
  categories = [];
  brand = "";
  parent_category = "";
  sub_category = "";
  query = "";
  page = 1;
  entire_category = {category: {name: '', subcategories: []}};
  rowHeight:number = 50;
  itemsInView: any[];
  startIndex:number = 0;
  endIndex:number = 0;
  numPages = 1;
  onlyPage = false;
  loading = false;

  constructor(
    private readonly router: Router, private readonly route: ActivatedRoute) { 
      this.router.routeReuseStrategy.shouldReuseRoute = () => false;
      this.brands = this.route.snapshot.data['Brands'];
      this.categories = this.route.snapshot.data['Categories'];
      this.route.data.subscribe(val => {
        if(this.onlyPage){
          this.onlyPage = false;
          return;
        }
        this.productList = val['Products'];
      })
      // disable router reuse on param change
      this.route.queryParams.subscribe(params => {
        if(this.parent_category === params['category'] && this.sub_category === params['subcategory'] && this.query === params['q']) {
          this.onlyPage = true;
        }
        this.parent_category = params['category'] ?? params['category'];
        this.sub_category = params['subcategory'] ?? params['subcategory'];
        this.query = params['q'] ?? params['q'];
        this.page = params['page'] ? parseInt(params['page']) : 1;
        this.numPages = Math.floor(this.productList.length/this.rowHeight);
        this.itemsInView = this.productList.slice(this.page*this.rowHeight, this.page*this.rowHeight+this.rowHeight);
        this.categories.some(category => {
          if(category.category.name === this.parent_category) {
            this.entire_category = category;
            return true;
          }
        });
      });
    }

    scrollToTop() {
      this.loading = true;
      window.scrollTo(0, 0);
    }

    selectBrand() {

    }

}
