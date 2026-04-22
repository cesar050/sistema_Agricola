import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface Cultivo {
  id?: number;
  nombre: string;
  tipo: string;
  area_hectareas: number;
  fecha_siembra: string;
  estado?: string;
}

@Injectable({ providedIn: 'root' })
export class CultivoService {
  private url = `${environment.apiUrl}/cultivos`;
  constructor(private http: HttpClient) {}
  getAll(): Observable<any>                        { return this.http.get(`${this.url}/`); }
  getById(id: number): Observable<any>             { return this.http.get(`${this.url}/${id}`); }
  create(d: Cultivo): Observable<any>              { return this.http.post(`${this.url}/`, d); }
  update(id: number, d: Cultivo): Observable<any>  { return this.http.put(`${this.url}/${id}`, d); }
  delete(id: number): Observable<any>              { return this.http.delete(`${this.url}/${id}`); }
}