import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface Tarea {
  id?: number;
  cultivo_id: number;
  tipo_tarea: string;
  descripcion?: string;
  fecha_programada: string;
  estado?: string;
  cultivo_nombre?: string;
}

@Injectable({ providedIn: 'root' })
export class TareaService {
  private url = `${environment.apiUrl}/tareas`;
  constructor(private http: HttpClient) {}

  getAll(): Observable<any>                        { return this.http.get(`${this.url}/`); }
  getPendientes(): Observable<any>                 { return this.http.get(`${this.url}/pendientes`); }
  getRecomendaciones(): Observable<any>            { return this.http.get(`${this.url}/recomendaciones`); }
  getByCultivo(id: number): Observable<any>        { return this.http.get(`${this.url}/cultivo/${id}`); }
  getById(id: number): Observable<any>             { return this.http.get(`${this.url}/${id}`); }
  create(d: Tarea): Observable<any>                { return this.http.post(`${this.url}/`, d); }
  update(id: number, d: Tarea): Observable<any>    { return this.http.put(`${this.url}/${id}`, d); }
  cambiarEstado(id: number, estado: string): Observable<any> {
    return this.http.patch(`${this.url}/${id}/estado`, { estado });
  }
  delete(id: number): Observable<any>              { return this.http.delete(`${this.url}/${id}`); }
}