import { Component, ViewChild, Input } from '@angular/core';
import {ActivatedRoute, Router, NavigationEnd} from '@angular/router';
import { CookieManagerService } from '../../../utilities/services/cookie-manager.service'
import {GoogleTagManagerService} from 'angular-google-tag-manager';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent {
  allProducts = [];
  productList = [];
  brands = [];
  categories = [];
  brand = "";
  parent_category = "";
  sub_category = "";
  query = "";
  page = 0;
  entire_category = {category: {name: '', subcategories: []}};
  rowHeight:number = 50;
  itemsInView: any[];
  startIndex:number = 0;
  endIndex:number = 0;
  numPages = 1;
  onlyPage = false;
  loading = false;

  constructor( private readonly cookieManagerService: CookieManagerService, 
    private readonly router: Router, private readonly route: ActivatedRoute, private readonly gtmService: GoogleTagManagerService) {

      this.router.routeReuseStrategy.shouldReuseRoute = () => false;
      this.brands = this.route.snapshot.data['Brands'].sort();
      this.categories = this.route.snapshot.data['Categories'];
      this.route.data.subscribe(val => {
        if(this.onlyPage){
          this.onlyPage = false;
          return;
        }
        this.allProducts = val['Products'];
        this.productList = this.allProducts;
      })
      // disable router reuse on param change
      this.route.queryParams.subscribe(params => {
        if(this.parent_category === params['category'] && this.sub_category === params['subcategory'] && this.query === params['q']) {
          this.onlyPage = true;
        }
        this.parent_category = params['category'] ?? params['category'];
        this.sub_category = params['subcategory'] ?? params['subcategory'];
        this.query = params['q'] ?? params['q'];
        this.brand = params['brand'] ?? params['brand'];
        this.page = params['page'] ? parseInt(params['page']) : 0;
        this.productList = this.brand ? this.allProducts.filter(product => product.COMPANY === this.brand) : this.allProducts
        this.numPages = Math.floor(this.productList.length/this.rowHeight);
        this.itemsInView = this.productList.slice(this.page*this.rowHeight, this.page*this.rowHeight+this.rowHeight);
        this.categories.some(category => {
          if(category.category.name === this.parent_category) {
            this.entire_category = category;
            return true;
          }
        });
        this.router.events.forEach(item => {
          if (item instanceof NavigationEnd) {
            const gtmTag = {
              "automl": {
                "eventType": 'search',
                "userInfo": {
                  "visitorId": cookieManagerService.visitorId$.value,
                  "userId": this.cookieManagerService.visitorId$.value
                },
                "productEventDetail": {
                  "searchQuery": this.query + " " + this.parent_category + " " + this.sub_category,
                }
              }
            };
            this.gtmService.pushTag(gtmTag);
          }
        }); 
      });
    }

    scrollToTop() {
      this.loading = true;
      window.scrollTo(0, 0);
    }

    selectBrand(event: any) {
      event.preventDefault()
      this.brand = event.target.value;  
      this.productList = this.allProducts.filter(product => {
        return product.COMPANY.trim().toLowerCase() === this.brand.trim().toLowerCase();
      });
      this.numPages = Math.floor(this.productList.length/this.rowHeight);
      this.itemsInView = this.productList.slice(this.page*this.rowHeight, this.page*this.rowHeight+this.rowHeight);
    }

}
