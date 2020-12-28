import {Injectable} from '@angular/core';
import {ActivatedRouteSnapshot, Resolve, RouterStateSnapshot} from '@angular/router';
import { product, products } from '../../assets/sample/product';
import { categories } from '../../assets/sample/categories';
import { brands } from '../../assets/sample/brands'
import {Observable, of} from 'rxjs';


@Injectable({providedIn: 'root'})
export class ProductResolver implements Resolve<any> {
  async getList(productId: number): Promise<any> {
    return fetch(`/getproduct/${productId}`)
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
  async getList(): Promise<any> {
    return fetch('/productbyfilter', {
        method: 'POST',
        body: JSON.stringify({
            "filters": {
                "company": "MG",
                "sizes": "XXL",
                "colors": "",
                "price": "",
                "category":["Clothing"],
                "subcategory":["Plus"]
                }
            }),
        headers: {'Content-Type': 'application/json'}
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
export class FeaturedProductsResolver implements Resolve<any> {
    async getList(): Promise<any> {
        return fetch('/getfeaturedproduct', {
            method: 'POST',
            body: JSON.stringify({
                "placement_name":"recommendedforyou-ctr",
                "product_id": "28174",
                "params":{
                                "dryRun": false,
                                "userEvent": {
                                    "eventType": "detail-page-view",
                                    "userInfo": {
                                        "visitorId": "32.215.17.15"
                                    },
                                    "productEventDetail": {
                                        "productDetails": [
                                            {
                                                "id": "28174"
                                            }
                                        ]
                                    }
                        }
                    }
                }
            ),
            headers: {'Content-Type': 'application/json'}
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
        return fetch('/getcategory').then(response => {
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
        return fetch('/getbrand').then(response => {
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