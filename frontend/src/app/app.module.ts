import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './views/base/app-routing.module';
import { AppComponent } from './views/app/app.component';
import { BaseComponent } from './views/base/base.component';
import { ProductComponent } from './views/product/product.component';
import { HomeComponent } from './views/home/home.component';
import { BagComponent } from './views/bag/bag.component';
import { FooterComponent } from './shared/footer/footer.component';
import { NavbarComponent } from './shared/navbar/navbar.component';
import { ProductCardComponent } from './shared/product-card/product-card.component';
import { ServicesModule } from '../utilities/services/services_module';
import { SearchComponent } from './views/search/search.component'

@NgModule({
  declarations: [
    AppComponent,
    BaseComponent,
    ProductComponent,
    HomeComponent,
    BagComponent,
    FooterComponent,
    NavbarComponent,
    ProductCardComponent,
    SearchComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ServicesModule
  ],
  providers: [  
    {provide: 'googleTagManagerId', useValue: 'GTM-5328V3D'} //update tag manager container id
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }