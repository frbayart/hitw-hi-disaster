import { TestBed, inject } from '@angular/core/testing';

import { ComputeService } from './compute.service';

describe('ComputeService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ComputeService]
    });
  });

  it('should be created', inject([ComputeService], (service: ComputeService) => {
    expect(service).toBeTruthy();
  }));
});
