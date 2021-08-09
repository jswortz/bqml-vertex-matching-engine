import { AfterViewInit, Component } from '@angular/core';
import {Event, NavigationCancel, NavigationEnd, NavigationError, NavigationStart, Router} from '@angular/router';
import {ActivatedRoute} from '@angular/router';
import { StoreInfoService } from '../../../utilities/services/store-info.service';
import { CookieManagerService } from '../../../utilities/services/cookie-manager.service';

@Component({
  selector: 'app-base',
  templateUrl: './base.component.html',
  styleUrls: ['./base.component.scss']
})
export class BaseComponent implements AfterViewInit {
  isLoading = true;
  categories = [];
  store_name = "";
  bag_size = 0;
  login;

  constructor(
    private readonly router: Router, private readonly route: ActivatedRoute, private readonly storeInfoService: StoreInfoService, private readonly cookieManagerService: CookieManagerService) {
      this.categories = this.route.snapshot.data["Categories"];
      storeInfoService.store_name$.subscribe(val => {
        this.store_name = val;
      });
      cookieManagerService.bagSize$.subscribe(val => {
        this.bag_size = val;
      })
      cookieManagerService.login$.subscribe(val => {
        this.login = val;
      })
    }

  ngAfterViewInit() {
    this.router.events.subscribe((event: Event) => {
      switch (true) {
        case event instanceof NavigationStart: {
          this.isLoading = true;
          break;
        }
        case event instanceof NavigationEnd:
        case event instanceof NavigationCancel:
        case event instanceof NavigationError: {
          this.isLoading = false;
          break;
        }
        default:
          break;
      }
    });
  }

}