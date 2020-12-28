import { Component, Input, OnInit } from '@angular/core';

import {CookieManagerService} from '../../../utilities/services/cookie-manager.service'

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit {
  @Input() store_name = "";
  signed_in = false;
  bagSize = 0;
  @Input() categories = [];

  constructor(private readonly cookieManager: CookieManagerService) { 
    
  }

  ngOnInit(): void {
  }

  login() {
    this.signed_in = !this.signed_in;
  }

}
