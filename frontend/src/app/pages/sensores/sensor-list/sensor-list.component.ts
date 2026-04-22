import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { SensorService } from '../../../core/services/sensor.service';

@Component({
  selector: 'app-sensor-list',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './sensor-list.component.html'
})
export class SensorListComponent implements OnInit {
  sensores: any[] = [];
  loading = true;
  mensaje = '';

  constructor(private svc: SensorService, private cdr: ChangeDetectorRef) {}

  ngOnInit() { this.cargar(); }

  cargar() {
    this.loading = true;
    this.svc.getAll().subscribe({
      next: r => {
        this.sensores = r.data;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: () => { this.loading = false; this.cdr.detectChanges(); }
    });
  }

  eliminar(id: number) {
    if (!confirm('¿Eliminar este sensor?')) return;
    this.svc.delete(id).subscribe(() => {
      this.mensaje = 'Sensor eliminado.';
      this.cargar();
      setTimeout(() => { this.mensaje = ''; this.cdr.detectChanges(); }, 3000);
    });
  }

  iconoSensor(tipo: string) {
    if (!tipo) return 'sensors';
    const t = tipo.toLowerCase();
    if (t.includes('humedad')) return 'water_drop';
    if (t.includes('temperatura')) return 'thermostat';
    if (t.includes('ph')) return 'science';
    if (t.includes('agua')) return 'water';
    return 'sensors';
  }
}