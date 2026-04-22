import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { TareaService } from '../../../core/services/tarea.service';

@Component({
  selector: 'app-tarea-list',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './tarea-list.component.html'
})
export class TareaListComponent implements OnInit {
  tareas: any[] = [];
  recomendaciones: any[] = [];
  loading = true;
  loadingRec = true;
  mensaje = '';
  tabActiva: 'tareas' | 'recomendaciones' = 'tareas';

  constructor(private svc: TareaService, private cdr: ChangeDetectorRef) {}

  ngOnInit() {
    this.cargar();
    this.cargarRecomendaciones();
  }

  cargar() {
    this.loading = true;
    this.svc.getAll().subscribe({
      next: r => { this.tareas = r.data; this.loading = false; this.cdr.detectChanges(); },
      error: () => { this.loading = false; this.cdr.detectChanges(); }
    });
  }

  cargarRecomendaciones() {
    this.loadingRec = true;
    this.svc.getRecomendaciones().subscribe({
      next: r => { this.recomendaciones = r.data; this.loadingRec = false; this.cdr.detectChanges(); },
      error: () => { this.loadingRec = false; this.cdr.detectChanges(); }
    });
  }

  cambiarEstado(id: number, estado: string) {
    this.svc.cambiarEstado(id, estado).subscribe(() => {
      this.cargar();
      this.mensaje = 'Estado actualizado.';
      setTimeout(() => { this.mensaje = ''; this.cdr.detectChanges(); }, 2000);
    });
  }

  crearDesdRecomendacion(rec: any) {
    const hoy = new Date();
    hoy.setDate(hoy.getDate() + 1);
    const fecha = hoy.toISOString().split('T')[0];
    const tarea = {
      cultivo_id: rec.cultivo_id,
      tipo_tarea: rec.tipo_tarea,
      descripcion: rec.descripcion,
      fecha_programada: fecha,
      estado: 'pendiente'
    };
    this.svc.create(tarea).subscribe(() => {
      this.mensaje = `Tarea "${rec.tipo_tarea}" creada para ${rec.cultivo_nombre}.`;
      this.cargar();
      setTimeout(() => { this.mensaje = ''; this.cdr.detectChanges(); }, 3000);
    });
  }

  eliminar(id: number) {
    if (!confirm('¿Eliminar esta tarea?')) return;
    this.svc.delete(id).subscribe(() => {
      this.mensaje = 'Tarea eliminada.';
      this.cargar();
      setTimeout(() => { this.mensaje = ''; this.cdr.detectChanges(); }, 2000);
    });
  }

  estadoClass(estado: string) {
    const map: any = {
      'pendiente': 'bg-yellow-100 text-yellow-800',
      'en proceso': 'bg-blue-100 text-blue-800',
      'completada': 'bg-green-100 text-green-800'
    };
    return map[estado] || 'bg-gray-100 text-gray-600';
  }

  iconoTarea(tipo: string) {
    const map: any = {
      'Riego': 'water_drop',
      'Fertilización': 'science',
      'Fumigación': 'pest_control',
      'Inspección': 'search',
      'Cosecha': 'agriculture'
    };
    return map[tipo] || 'task';
  }

  sigEstado(actual: string): string {
    if (actual === 'pendiente') return 'en proceso';
    if (actual === 'en proceso') return 'completada';
    return 'pendiente';
  }

  labelSigEstado(actual: string): string {
    if (actual === 'pendiente') return 'Iniciar';
    if (actual === 'en proceso') return 'Completar';
    return 'Reabrir';
  }
}