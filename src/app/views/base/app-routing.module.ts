import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { BaseComponent } from './base.component';
import { FeaturedProductsResolver, CategoriesResolver, BrandsResolver, ProductsResolver, ProductResolver } from '../../../utilities/resolvers/list_resolvers'
import { HomeComponent } from '../home/home.component';
import { ProductComponent } from '../product/product.component';
import { SearchComponent } from '../search/search.component';
import { BagComponent } from '../bag/bag.component';

const routes: Routes = [
  {
    path: '',
    component: BaseComponent,
    resolve: {
      Products: ProductsResolver,
      Categories: CategoriesResolver
    },
    children: [
      {
        path: '',
        component: HomeComponent,
        resolve: {
          FeaturedProducts: FeaturedProductsResolver,
        }
      },
      {
        path: 'product/:productId',
        component: ProductComponent,
        resolve: {
          Product: ProductResolver
        }
      },
      {
        path: 'product',
        component: SearchComponent,
        resolve: {
          Products: ProductsResolver,
          Brands: BrandsResolver,
          Categories: CategoriesResolver
        },
        runGuardsAndResolvers: 'paramsOrQueryParamsChange',
      },
      {
        path: 'bag',
        component: BagComponent,
        resolve: {
          Product: ProductResolver
        }
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
