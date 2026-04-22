import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { LecturaService, Lectura } from '../../../core/services/lectura.service';
import { SensorService } from '../../../core/services/sensor.service';

@Component({
  selector: 'app-lectura-form',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './lectura-form.component.html'
})
export class LecturaFormComponent implements OnInit {
  sensores: any[] = [];
  error = '';
  loading = false;

  lectura: Lectura = { sensor_id: 0, valor: 0, estado_alerta: 'normal' };

  constructor(
    private svc: LecturaService,
    private sensorSvc: SensorService,
    private router: Router
  ) {}

  ngOnInit() {
    this.sensorSvc.getAll().subscribe(r => this.sensores = r.data);
  }

  guardar() {
    this.loading = true;
    this.svc.create(this.lectura).subscribe({
      next: () => this.router.navigate(['/lecturas']),
      error: () => { this.error = 'Error al guardar.'; this.loading = false; }
    });
  }
}