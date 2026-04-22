import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { LecturaService } from '../../../core/services/lectura.service';

@Component({
  selector: 'app-lectura-list',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './lectura-list.component.html'
})
export class LecturaListComponent implements OnInit {
  lecturas: any[] = [];
  loading = true;
  mensaje = '';

  constructor(private svc: LecturaService, private cdr: ChangeDetectorRef) {}

  ngOnInit() { this.cargar(); }

  cargar() {
    this.loading = true;
    this.svc.getAll().subscribe({
      next: r => {
        this.lecturas = r.data;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: () => { this.loading = false; this.cdr.detectChanges(); }
    });
  }

  eliminar(id: number) {
    if (!confirm('¿Eliminar esta lectura?')) return;
    this.svc.delete(id).subscribe(() => {
      this.mensaje = 'Lectura eliminada.';
      this.cargar();
      setTimeout(() => { this.mensaje = ''; this.cdr.detectChanges(); }, 3000);
    });
  }

  alertaClass(estado: string) {
    const map: any = {
      'normal': 'bg-green-100 text-green-800',
      'alerta': 'bg-yellow-100 text-yellow-800',
      'critico': 'bg-red-100 text-red-700',
      'crítico': 'bg-red-100 text-red-700'
    };
    return map[estado] || 'bg-gray-100 text-gray-600';
  }
}