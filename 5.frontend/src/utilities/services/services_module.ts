import {NgModule} from '@angular/core';

import {StoreInfoService} from './store-info.service';
import {CookieManagerService} from './cookie-manager.service';

@NgModule({
    providers: [StoreInfoService, CookieManagerService]
})
export class ServicesModule{

}
