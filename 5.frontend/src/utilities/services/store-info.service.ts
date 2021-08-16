import { Injectable } from '@angular/core';
import {BehaviorSubject} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class StoreInfoService {
  storeName$ = new BehaviorSubject<string>('store');
  primaryColor$ = new BehaviorSubject<string>('');
  secondaryColor$ = new BehaviorSubject<string>('');

  set storeName(value: string){
    this.storeName$.next(value);
  }

  set primaryColor(value: string){
    this.primaryColor$.next(value);
  }

  set secondaryColor(value: string){
    this.secondaryColor$.next(value);
  }
}
