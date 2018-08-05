import { TestBed, inject } from '@angular/core/testing';

import { HTTPBackendService } from './HTTPbackend.service';

describe('BackendService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [HTTPBackendService]
    });
  });

  it('should be created', inject([HTTPBackendService], (service: HTTPBackendService) => {
    expect(service).toBeTruthy();
  }));
});
