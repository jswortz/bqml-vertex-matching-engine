import { Component } from '@angular/core';
import { CookieManagerService } from '../../../utilities/services/cookie-manager.service'

@Component({
  selector: 'app-bag',
  templateUrl: './bag.component.html',
  styleUrls: ['./bag.component.scss']
})
export class BagComponent {
  bag = []
  bagTotal = 0.0
  bagSize = 0
  editBag;

  constructor(private readonly cookieManagerService: CookieManagerService) { 
    cookieManagerService.bag$.subscribe(val => {
      this.bag = val;
    })
    cookieManagerService.bagSize$.subscribe(val => {
      this.bagSize = val;
    })
    cookieManagerService.bagTotal$.subscribe(val => {
      this.bagTotal = val;
    })
    this.editBag = cookieManagerService.editBag;
  }

  

}
