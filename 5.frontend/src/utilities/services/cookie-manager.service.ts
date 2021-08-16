import { Injectable } from '@angular/core';
import {BehaviorSubject, Observable} from 'rxjs';
import { v4 as uuid } from 'uuid';

@Injectable({
  providedIn: 'root'
})
export class CookieManagerService {
  login$ = new BehaviorSubject<boolean>(false);
  bag$ = new BehaviorSubject<any>([]);
  bagTotal$ = new BehaviorSubject(0.0);
  bagSize$ = new BehaviorSubject(0);
  visitorId$ = new BehaviorSubject<string>('');

  getCookie(name: string): string {
    const ca: string[] = document.cookie.split(';');
    const caLen: number = ca.length;
    const cookieName = `${name}=`;
    let c: string;

    for (let i = 0; i < caLen; i += 1) {
      c = ca[i].replace(/^\s+/g, '');
      if (c.indexOf(cookieName) === 0) {
        return c.substring(cookieName.length, c.length);
      }
    }
    return '';
  }

  setCookie(name: string, value: any, expireDays: number, path: string = ''): void {
    const d = new Date();
    d.setTime(d.getTime() + expireDays * 24 * 60 * 60 * 1000);
    const expires = `expires=${d.toUTCString()}`;
    const cpath: string = path ? `; path=${path}` : '';
    document.cookie = `${name}=${value}; ${expires}${cpath}`;
  }

  constructor() {
    this.bag = this.getCookie('bag') ?
      JSON.parse(this.getCookie('bag')) :
      [];
    this.login = this.getCookie('login') ? true : false;
    this.bagTotal = this.getCookie('bagTotal') ?
      typeof this.getCookie('bagTotal') === 'string' ?
        parseFloat(this.getCookie('bagTotal')) :
        this.getCookie('bagTotal')
      : 0.0;
    this.bagSize = this.getCookie('bagSize') ?
      typeof this.getCookie('bagSize') === 'string' ?
        parseInt(this.getCookie('bagSize')) :
        this.getCookie('bagSize') :
      0;
    if (this.getCookie('visitorId')) {
      this.visitorId = this.getCookie('visitorId');
    }
    else {
      this.visitorId = uuid();
      this.setCookie('visitorId',
        this.visitorId$.value,
        100,
        '/');
    }
  }

  set login(value: boolean) {
    this.login$.next(value);
  }

  set bag(value: any) {
    this.bag$.next(value);
  }

  get getBag(): Observable<any> {
    return this.bag$.asObservable();
  }

  set bagTotal(value: any) {
    this.bagTotal$.next(value);
  }

  get getBagTotal(): Observable<any> {
    return this.bagTotal$.asObservable();
  }

  set bagSize(value: any) {
    this.bagSize$.next(value);
  }

  get getBagSize(): Observable<any> {
    return this.bagSize$.asObservable();
  }

  set visitorId(value: string) {
    this.visitorId$.next(value);
  }

  get getVisitorId(): Observable<any> {
    return this.visitorId$.asObservable();
  }

  editBag(index: number, newQuantity: number): void {
    const currentBag = this.getCookie('bag') ?
      JSON.parse(this.getCookie('bag')) :
      [];
    console.log(currentBag, index, newQuantity);
    let newSize = 0;
    if (newQuantity > currentBag[index]['quantity']) {
      currentBag[index]['quantity'] = newQuantity;
    }
    else {
      if (newQuantity > 0) {
        currentBag[index]['quantity'] = newQuantity;
      }
      else {
        currentBag.splice(index, 1);
      }
    }
    let total = 0.0;
    currentBag.map(item => {
      newSize += item['quantity'];
      total += item.PRICE * item.quantity;
    });
    this.bag = currentBag;
    this.bagSize = newSize;
    this.bagTotal = total.toFixed(2);
    this.setCookie('bag',
      JSON.stringify(currentBag),
      100,
      '/');
  }

  addToBag = (product) => {
    const currentBag = this.bag$.value;
    const bagSize = this.bagSize$.value;
    const filteredBag = currentBag.findIndex(e =>
      e.ID === product.ID &&
      e.SIZE === product.SIZE &&
      e.COLOR === product.COLOR);
    if (filteredBag > -1) {
      currentBag[filteredBag]['quantity'] =
        typeof currentBag[filteredBag]['quantity'] === typeof 1 ?
          currentBag[filteredBag]['quantity'] + 1 :
          parseInt(currentBag[filteredBag]['quantity'] as string) + 1;
    } else {
      currentBag.push({
        ID: product.ID,
        NAME: product.NAME,
        SIZE: product.SIZE,
        COLOR: product.COLOR,
        IMAGE_LINK: product.IMAGE_LINK,
        PRICE: product.PRICE,
        quantity: 1
      });
    }
    let total = 0.0;
    currentBag.map(item => total += item.PRICE * item.quantity);
    this.bag = currentBag;
    this.bagSize = bagSize + 1;
    this.bagTotal = total.toFixed(2);
    this.setCookie('bag', JSON.stringify(currentBag), 100, '/');
  }
}
