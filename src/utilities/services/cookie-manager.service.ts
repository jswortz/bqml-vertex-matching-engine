import { Injectable } from '@angular/core';
import {BehaviorSubject, Observable} from 'rxjs';
import { v4 as uuid } from 'uuid';

@Injectable({
  providedIn: 'root'
})
export class CookieManagerService {
  login$ = new BehaviorSubject<boolean>(false);
  bag$ = new BehaviorSubject<any>([]);
  _bag = [];
  bagTotal$ = new BehaviorSubject(0.0);
  bagSize$ = new BehaviorSubject(0);
  visitorId$ = new BehaviorSubject<string>('');

  getCookie(name: string) {
    const ca: string[] = document.cookie.split(';');
    const caLen: number = ca.length;
    const cookieName = `${name}=`;
    let c: string;

    for (let i: number = 0; i < caLen; i += 1) {
      c = ca[i].replace(/^\s+/g, '');
      if (c.indexOf(cookieName) === 0) {
        return c.substring(cookieName.length, c.length);
      }
    }
    return '';
  }

  setCookie(
    name: string, value: any, expireDays: number, path: string = '') {
    const d = new Date();
    d.setTime(d.getTime() + expireDays * 24 * 60 * 60 * 1000);
    const expires: string = `expires=${d.toUTCString()}`;
    const cpath: string = path ? `; path=${path}` : '';
    document.cookie = `${name}=${value}; ${expires}${cpath}`;
  }

  constructor() {
    this.bag = this.getCookie('bag') ? JSON.parse(this.getCookie('bag')) : [];
    this.login = this.getCookie('login') ? true : false;
    this.bagTotal = this.getCookie('bagTotal') ? typeof this.getCookie('bagTotal') === 'string' ? parseFloat(this.getCookie('bagTotal')) : this.getCookie('bagTotal') : 0.0;
    this.bagSize = this.getCookie('bagSize') ? typeof this.getCookie('bagSize') === 'string' ? parseInt(this.getCookie('bagSize')) : this.getCookie('bagSize') : 0;
    if(this.getCookie('visitorId')) {
      this.visitorId = this.getCookie('visitorId');
    }
    else {
      this.visitorId = uuid();
      this.setCookie('visitorId',this.visitorId$.value, 100, '/');
    }
  }

  set login(value: boolean) {
    this.login$.next(value);
  }

  set bag(value: any) {
    this.bag$.next(value);
  }

  get getBag() {
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

  set visitorId(value: string) {
    this.visitorId$.next(value);
  }

  get _visitorId() {
    return this.visitorId$.asObservable();
  }

  editBag(index: number, newQuantity: number) {
    let current_bag = this.getCookie('bag') ? JSON.parse(this.getCookie('bag')) : [];
    console.log(current_bag, index, newQuantity);
    let newSize = 0;
    if(newQuantity > current_bag[index]['quantity']) {
      current_bag[index]['quantity'] = newQuantity;
    }
    else {
      if(newQuantity > 0) {
        current_bag[index]['quantity'] = newQuantity;
      }
      else {
        current_bag.splice(index, 1);
      }
    }
    let total = 0.0;
    current_bag.map(item => {
      newSize += item['quantity']; 
      total += item.PRICE * item.quantity; 
    })
    this._bag = current_bag;
    this.bag = current_bag;
    this.bagSize = newSize;
    this.bagTotal = total.toFixed(2)
    this.setCookie('bag', JSON.stringify(current_bag), 100, '/')
  }

  addToBag = (product) => {
    let current_bag = this.bag$.value
    let bagSize = this.bagSize$.value
    let filtered_bag = current_bag.findIndex(e => e.ID === product.ID && e.SIZE === product.SIZE && e.COLOR === product.COLOR)
    if (filtered_bag > -1) {
      current_bag[filtered_bag]['quantity'] = typeof current_bag[filtered_bag]['quantity'] === typeof 1 ? current_bag[filtered_bag]['quantity']+1 : parseInt(current_bag[filtered_bag]['quantity'] as string) + 1
    }
    else {
      current_bag.push({
        ID: product.ID,
        NAME: product.NAME,
        SIZE: product.SIZE,
        COLOR: product.COLOR,
        IMAGE_LINK: product.IMAGE_LINK,
        PRICE: product.PRICE,
        quantity: 1
      })
    }
    let total = 0.0;
    current_bag.map(item => total += item.PRICE * item.quantity)
    this._bag = current_bag;
    this.bag = current_bag;
    this.bagSize = bagSize+1;
    this.bagTotal = total.toFixed(2)
    this.setCookie('bag', JSON.stringify(current_bag), 100, '/')
  }
}
