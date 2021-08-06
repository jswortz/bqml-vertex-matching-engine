import {Injectable} from '@angular/core';
import {ActivatedRouteSnapshot, ActivatedRoute, Resolve, RouterStateSnapshot} from '@angular/router';
import { product, products } from '../../assets/sample/product';
import { categories } from '../../assets/sample/categories';
import { brands } from '../../assets/sample/brands'
import {Observable, of} from 'rxjs';
import { CookieManagerService } from '../services/cookie-manager.service';

let homeRoute = 'https://backend-q-dot-babrams-recai-demo.uc.r.appspot.com' // update the backend app engine site you just deployed

@Injectable({providedIn: 'root'})
export class ProductResolver implements Resolve<any> {
  async getList(productId: number): Promise<any> {
    return fetch(`${homeRoute}/getproduct/${productId}`, {headers: {'Access-Control-Allow-Origin': 'no-cors'}})
        .then((response => {
          if (!response.ok) {
            throw new Error(response.statusText);
          }
          return response.json();
        }))
        .then(d => {
          return d;
        })
        .catch(err => {
          console.log(err);
          return products[productId - 1];
        });
  }

  resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot):
      Promise<any> {
    const row: string[] = [];
    let id: string = '';

    Object.keys(route.data).forEach(e => {
      row.push(route.data[e]);
    });

    const path: string = row[0];
    delete row[0];

    route.data = row;

    if (path && path.lastIndexOf('/') === path.length - 1) {
      id = route.params['productId'];
    }
    return this.getList(Number(route.params['productId']));
  }
}


@Injectable({providedIn: 'root'})
export class ProductsResolver implements Resolve<any> {
  async getList(category: string, subcategory: string, q: string): Promise<any> {
    return fetch(`${homeRoute}/productbyfilter`, {
        method: 'POST',
        body: JSON.stringify({
            "filters": {
                "name": q ? q : "",
                "company": "",
                "sizes": "",
                "colors": "",
                "price": "",
                "category": category ?  [category] : [],
                "subcategory": subcategory ? [subcategory] : []
                }
            }),
        headers: {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': 'no-cors'}
      }).then(response => {
            if (!response.ok) {
            throw new Error(response.statusText);
            }
            return response.json();
        })
              .then(products => {
              return products;
              })
              .catch(err => {
              console.log(err);
              return products;
            });
  }

  resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot):
      Promise<any> {
    const row: string[] = [];
    let category: string = '';
    let subcategory: string = '';
    let q: string = '';
    category = route.queryParamMap.get('category') ? route.queryParamMap.get('category').trim() : '';
    subcategory = route.queryParamMap.get('subcategory') ? route.queryParamMap.get('subcategory').trim() : '';
    q = route.queryParamMap.get('q') ? route.queryParamMap.get('q').trim() : '';
    console.log(category, subcategory, q)
    return this.getList(category, subcategory, q);
  }
}


@Injectable({providedIn: 'root'})
export class RecentlyViewedResolver implements Resolve<any> {
    async getList(): Promise<any> {
      let cookieManagerService = new CookieManagerService();
        return fetch(`${homeRoute}/getfeaturedproduct`, {
            method: 'POST',
            body: JSON.stringify({
                "placement_name":"recently_viewed_default",  // Update to your recently viewed placement name
                "params":{
                          "dryRun": false,
                          "userEvent": {
                              "eventType": "home-page-view",
                              "userInfo": {
                                  "visitorId": cookieManagerService.getCookie('_ga'),
                                  "userId": cookieManagerService.visitorId$.value
                              }
                        }
                    }
                }
            ),
            headers: {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': 'no-cors'}
          }).then(response => {
                if (!response.ok) {
                throw new Error(response.statusText);
                }
                return response.json();
            })
                .then(products => {
                  if(Array.isArray(products)) {
                    return products;
                  }
                  else {
                    return [];
                  }
                })
                .catch(err => {
                console.log(err);
                return products;
                });

      }

      resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot):
          Promise<any> {
        return this.getList();
      }
}


@Injectable({providedIn: 'root'})
export class FeaturedProductsResolver implements Resolve<any> {
    async getList(): Promise<any> {
      let cookieManagerService = new CookieManagerService();
        return fetch(`${homeRoute}/getfeaturedproduct`, {
            method: 'POST',
            body: JSON.stringify({
                "placement_name":"homepage",  // Update to your recommended placement name
                "params":{
                          "dryRun": false,
                          "userEvent": {
                              "eventType": "home-page-view",
                              "userInfo": {
                                  "visitorId": cookieManagerService.getCookie('_ga'),
                                  "userId": cookieManagerService.visitorId$.value
                              }
                        }
                    }
                }
            ),
            headers: {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': 'no-cors'}
          }).then(response => {
                if (!response.ok) {
                throw new Error(response.statusText);
                }
                return response.json();
            })
                .then(products => {
                return products;
                })
                .catch(err => {
                console.log(err);
                return products;
                });

      }

      resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot):
          Promise<any> {
        return this.getList();
      }
}

@Injectable({providedIn: 'root'})
export class CategoriesResolver implements Resolve<any> {
    async getList(): Promise<any> {
        return fetch(`${homeRoute}/getcategory`, {headers: {'Access-Control-Allow-Origin': 'no-cors'}}).then(response => {
                if (!response.ok) {
                throw new Error(response.statusText);
                }
                return response.json();
            })
                .then(categories => {
                return categories;
                })
                .catch(err => {
                console.log(err);
                return categories;
                });
      }

      resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot):
          Promise<any> {
        return this.getList();
      }
}

@Injectable({providedIn: 'root'})
export class BrandsResolver implements Resolve<any> {
    async getList(): Promise<any> {
        return fetch(`${homeRoute}/getbrand`, {headers: {'Access-Control-Allow-Origin': 'no-cors'}}).then(response => {
                if (!response.ok) {
                throw new Error(response.statusText);
                }
                return response.json();
            })
                .then(brand => {
                return brand;
                })
                .catch(err => {
                console.log(err);
                return brands;
                });
      }

      resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot):
          Promise<any> {
        return this.getList();
      }
}
