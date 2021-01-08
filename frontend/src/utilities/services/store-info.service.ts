import { Injectable } from '@angular/core';
import {BehaviorSubject} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class StoreInfoService {
  store_name$ = new BehaviorSubject<string>('store');
  primary_color$ = new BehaviorSubject<string>('');
  secondary_color$ = new BehaviorSubject<string>('');

  set store_name(value: string){
    this.store_name$.next(value)
  }

  set primary_color(value: string){
    this.primary_color$.next(value)
  }

  set secondary_color(value: string){
    this.secondary_color$.next(value)
  }
}
