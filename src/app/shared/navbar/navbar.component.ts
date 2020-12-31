import { Component, Input } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Router } from '@angular/router';

import {CookieManagerService} from '../../../utilities/services/cookie-manager.service'

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent {
  @Input() store_name = "";
  signed_in = false;
  bagSize = 0;
  @Input() categories = [];
  myControl = new FormControl();

  constructor(private readonly cookieManagerService: CookieManagerService, private readonly router: Router) { 
    this.cookieManagerService._bagSize.subscribe(val => this.bagSize = val)
  }

  goToSearch(event: KeyboardEvent) {
    event.preventDefault();
    this.router.navigate(
        ['product'], {queryParams: {q: (event.target as HTMLInputElement).value}});
  }

  login() {
    this.signed_in = !this.signed_in;
  }

}
