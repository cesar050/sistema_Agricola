import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface Sensor {
  id?: number;
  cultivo_id: number;
  tipo_sensor: string;
  ubicacion?: string;
  cultivo_nombre?: string;
}

@Injectable({ providedIn: 'root' })
export class SensorService {
  private url = `${environment.apiUrl}/sensores`;
  constructor(private http: HttpClient) {}
  getAll(): Observable<any>                        { return this.http.get(`${this.url}/`); }
  getById(id: number): Observable<any>             { return this.http.get(`${this.url}/${id}`); }
  getByCultivo(id: number): Observable<any>        { return this.http.get(`${this.url}/cultivo/${id}`); }
  create(d: Sensor): Observable<any>               { return this.http.post(`${this.url}/`, d); }
  update(id: number, d: Sensor): Observable<any>   { return this.http.put(`${this.url}/${id}`, d); }
  delete(id: number): Observable<any>              { return this.http.delete(`${this.url}/${id}`); }
}