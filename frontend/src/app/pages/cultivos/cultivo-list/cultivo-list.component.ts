import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { CultivoService } from '../../../core/services/cultivo.service';

@Component({
  selector: 'app-cultivo-list',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './cultivo-list.component.html'
})
export class CultivoListComponent implements OnInit {
  cultivos: any[] = [];
  loading = true;
  mensaje = '';

  constructor(private svc: CultivoService, private cdr: ChangeDetectorRef) {}

  ngOnInit() { this.cargar(); }

  cargar() {
    this.loading = true;
    this.svc.getAll().subscribe({
      next: r => {
        this.cultivos = r.data;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: () => { this.loading = false; this.cdr.detectChanges(); }
    });
  }

  eliminar(id: number) {
    if (!confirm('¿Eliminar este cultivo?')) return;
    this.svc.delete(id).subscribe(() => {
      this.mensaje = 'Cultivo eliminado correctamente.';
      this.cargar();
      setTimeout(() => { this.mensaje = ''; this.cdr.detectChanges(); }, 3000);
    });
  }

  estadoClass(estado: string) {
    const map: any = {
      'activo': 'bg-green-100 text-green-800',
      'cosechado': 'bg-stone-100 text-stone-600',
      'en_riesgo': 'bg-red-100 text-red-700',
      'en riesgo': 'bg-red-100 text-red-700'
    };
    return map[estado] || 'bg-gray-100 text-gray-600';
  }
}