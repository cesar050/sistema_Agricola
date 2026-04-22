import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, ActivatedRoute, RouterLink } from '@angular/router';
import { CultivoService, Cultivo } from '../../../core/services/cultivo.service';

@Component({
  selector: 'app-cultivo-form',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './cultivo-form.component.html'
})
export class CultivoFormComponent implements OnInit {
  esEdicion = false;
  id: number | null = null;
  error = '';
  loading = false;

  cultivo: Cultivo = {
    nombre: '', tipo: '', area_hectareas: 0, fecha_siembra: '', estado: 'activo'
  };

  constructor(
    private svc: CultivoService,
    private router: Router,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {
    this.id = this.route.snapshot.params['id'] ? +this.route.snapshot.params['id'] : null;
    if (this.id) {
      this.esEdicion = true;
      this.svc.getById(this.id).subscribe(r => this.cultivo = r.data);
    }
  }

  guardar() {
    this.loading = true;
    const op = this.esEdicion
      ? this.svc.update(this.id!, this.cultivo)
      : this.svc.create(this.cultivo);

    op.subscribe({
      next: () => this.router.navigate(['/cultivos']),
      error: () => { this.error = 'Error al guardar. Verifica los datos.'; this.loading = false; }
    });
  }
}