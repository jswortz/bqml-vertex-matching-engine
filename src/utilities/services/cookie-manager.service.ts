import { Injectable } from '@angular/core';
import {BehaviorSubject} from 'rxjs';
import Cookies from 'universal-cookie';

const cookies = new Cookies();

@Injectable({
  providedIn: 'root'
})
export class CookieManagerService {
  login$ = new BehaviorSubject<boolean>(false);
  bag$ = new BehaviorSubject<any>([]);
  bagTotal$ = new BehaviorSubject(0.0);
  bagSize$ = new BehaviorSubject(0);

  constructor() {
    this.bag = cookies.get('bag') ? cookies.get('bag') : [];
    this.login = cookies.get('login') ? true : false;
    this.bagTotal = cookies.get('bagTotal') ? cookies.get('bagTotal') : 0.0;
    this.bagSize = cookies.get('bagSize') ? cookies.get('bagSize') : 0
  }

  set login(value: boolean) {
    this.login$.next(value);
  }

  set bag(value: any) {
    this.bag$.next(value);
  }

  get _bag() {
    return this.bag$.asObservable();
  }

  set bagTotal(value: any) {
    this.bagTotal$.next(value);
  }

  get _bagTotal() {
    return this.bagTotal$.asObservable();
  }

  set bagSize(value: any) {
    this.bagSize$.next(value);
  }

  get _bagSize() {
    return this.bagSize$.asObservable();
  }

  editBag(index, newQuantity) {
    let current_bag = this.bag$.value
    let newSize = 0;
    if(newQuantity > current_bag[index]['quantity']) {
      current_bag[index]['quantity'] = newQuantity;
      cookies.set('bag', current_bag, {path: '/'})
    }
    else {
      if(newQuantity) {
        current_bag[index]['quantity'] = newQuantity;
        cookies.set('bag', current_bag, {path: '/'})
      }
      else {
        current_bag.splice(index, 1);
        cookies.set('bag', current_bag, {path: '/'})
      }
    }
    let total = 0.0;
    current_bag.map(item => {newSize += item['quantity']; total += item.price * item.quantity; return '';})
    this.bag = current_bag;
    this.bagSize = newSize;
    this.bagTotal = total.toFixed(2)
    cookies.set('bagSize', newSize, {path: '/'})
  }

  addToBag = (sku,name,image,price,size,color, discount, additional_price=0) => {
    let current_bag = this.bag$.value
    let bagSize = this.bagSize$.value
    let filtered_bag = current_bag.findIndex(e => e.sku === sku && e.size === size && e.color === color)
    if (filtered_bag > -1) {
      current_bag[filtered_bag]['quantity'] += 1
    }
    else {
      current_bag.push({
        sku: sku,
        name: name,
        size: size,
        color: color,
        image: image,
        price: price,
        discount: discount,
        additional_price: additional_price,
        quantity: 1
      })
    }
    let total = 0.0;
    current_bag.map(item => total += item.price * item.quantity)
    this.bag = current_bag;
    this.bagSize = bagSize+1;
    this.bagTotal = total.toFixed(2)
    cookies.set('bag', current_bag, {path: '/'})
    cookies.set('bagSize', this.bagSize$, {path: '/'})
    cookies.set('bagTotal', this.bagTotal$, {path: '/'})
  }
}
