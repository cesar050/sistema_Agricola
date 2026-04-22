import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { TareaService, Tarea } from '../../../core/services/tarea.service';
import { CultivoService } from '../../../core/services/cultivo.service';

@Component({
  selector: 'app-tarea-form',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './tarea-form.component.html'
})
export class TareaFormComponent implements OnInit {
  cultivos: any[] = [];
  error = '';
  loading = false;

  tarea: Tarea = {
    cultivo_id: 0,
    tipo_tarea: '',
    descripcion: '',
    fecha_programada: '',
    estado: 'pendiente'
  };

  tiposTarea = ['Riego', 'Fertilización', 'Fumigación', 'Inspección', 'Cosecha', 'Poda'];

  constructor(
    private svc: TareaService,
    private cultivoSvc: CultivoService,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.cultivoSvc.getAll().subscribe(r => {
      this.cultivos = r.data;
      this.cdr.detectChanges();
    });
  }

  guardar() {
    this.loading = true;
    this.svc.create(this.tarea).subscribe({
      next: () => this.router.navigate(['/tareas']),
      error: () => {
        this.error = 'Error al guardar la tarea.';
        this.loading = false;
        this.cdr.detectChanges();
      }
    });
  }
}