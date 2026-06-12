import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ChatResponse } from '../models/audit.models';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private http = inject(HttpClient);
  private baseUrl = 'http://localhost:8000/api';

  getSyntheticData(count = 20): Observable<{ items: any[] }> {
    return this.http.get<{ items: any[] }>(`${this.baseUrl}/synthetic-data?count=${count}`);
  }

  askQuestion(question: string): Observable<ChatResponse> {
    return this.http.post<ChatResponse>(`${this.baseUrl}/chat`, { question });
  }
}