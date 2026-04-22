import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface Lectura {
  id?: number;
  sensor_id: number;
  valor: number;
  fecha_hora?: string;
  estado_alerta?: string;
  tipo_sensor?: string;
  ubicacion?: string;
}

@Injectable({ providedIn: 'root' })
export class LecturaService {
  private url = `${environment.apiUrl}/lecturas`;
  constructor(private http: HttpClient) {}
  getAll(): Observable<any>                        { return this.http.get(`${this.url}/`); }
  getBySensor(id: number): Observable<any>         { return this.http.get(`${this.url}/sensor/${id}`); }
  create(d: Lectura): Observable<any>              { return this.http.post(`${this.url}/`, d); }
  delete(id: number): Observable<any>              { return this.http.delete(`${this.url}/${id}`); }
}