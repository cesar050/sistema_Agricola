import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { CultivoService } from '../../core/services/cultivo.service';
import { SensorService } from '../../core/services/sensor.service';
import { LecturaService } from '../../core/services/lectura.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './dashboard.component.html'
})
export class DashboardComponent implements OnInit {
  cultivos: any[] = [];
  sensores: any[] = [];
  lecturas: any[] = [];
  totalArea = 0;
  alertas = 0;
  criticos = 0;

  constructor(
    private cultivoSvc: CultivoService,
    private sensorSvc: SensorService,
    private lecturaSvc: LecturaService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.cultivoSvc.getAll().subscribe(r => {
      this.cultivos = r.data;
      this.totalArea = r.data.reduce((s: number, c: any) => s + parseFloat(c.area_hectareas), 0);
      this.cdr.detectChanges();
    });
    this.sensorSvc.getAll().subscribe(r => {
      this.sensores = r.data;
      this.cdr.detectChanges();
    });
    this.lecturaSvc.getAll().subscribe(r => {
      this.lecturas = r.data;
      this.alertas = r.data.filter((l: any) => l.estado_alerta === 'alerta').length;
      this.criticos = r.data.filter((l: any) => l.estado_alerta === 'critico' || l.estado_alerta === 'crítico').length;
      this.cdr.detectChanges();
    });
  }

  estadoBadge(estado: string) {
    const map: any = {
      'activo': 'bg-green-100 text-green-800',
      'cosechado': 'bg-stone-100 text-stone-600',
      'en_riesgo': 'bg-red-100 text-red-700',
      'en riesgo': 'bg-red-100 text-red-700',
    };
    return map[estado] || 'bg-gray-100 text-gray-600';
  }
}