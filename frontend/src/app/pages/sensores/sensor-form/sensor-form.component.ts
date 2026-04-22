import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { SensorService, Sensor } from '../../../core/services/sensor.service';
import { CultivoService } from '../../../core/services/cultivo.service';

@Component({
  selector: 'app-sensor-form',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './sensor-form.component.html'
})
export class SensorFormComponent implements OnInit {
  cultivos: any[] = [];
  error = '';
  loading = false;

  sensor: Sensor = { cultivo_id: 0, tipo_sensor: '', ubicacion: '' };

  constructor(
    private svc: SensorService,
    private cultivoSvc: CultivoService,
    private router: Router
  ) {}

  ngOnInit() {
    this.cultivoSvc.getAll().subscribe(r => this.cultivos = r.data);
  }

  guardar() {
    this.loading = true;
    this.svc.create(this.sensor).subscribe({
      next: () => this.router.navigate(['/sensores']),
      error: () => { this.error = 'Error al guardar.'; this.loading = false; }
    });
  }
}