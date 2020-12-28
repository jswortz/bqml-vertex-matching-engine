import { TestBed } from '@angular/core/testing';

import { StoreInfoService } from './store-info.service';

describe('StoreInfoService', () => {
  let service: StoreInfoService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(StoreInfoService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
