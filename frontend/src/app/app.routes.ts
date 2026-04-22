import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  { path: 'dashboard', loadComponent: () => import('./pages/dashboard/dashboard.component').then(m => m.DashboardComponent) },
  { path: 'cultivos', loadComponent: () => import('./pages/cultivos/cultivo-list/cultivo-list.component').then(m => m.CultivoListComponent) },
  { path: 'cultivos/nuevo', loadComponent: () => import('./pages/cultivos/cultivo-form/cultivo-form.component').then(m => m.CultivoFormComponent) },
  { path: 'cultivos/editar/:id', loadComponent: () => import('./pages/cultivos/cultivo-form/cultivo-form.component').then(m => m.CultivoFormComponent) },
  { path: 'sensores', loadComponent: () => import('./pages/sensores/sensor-list/sensor-list.component').then(m => m.SensorListComponent) },
  { path: 'sensores/nuevo', loadComponent: () => import('./pages/sensores/sensor-form/sensor-form.component').then(m => m.SensorFormComponent) },
  { path: 'lecturas', loadComponent: () => import('./pages/lecturas/lectura-list/lectura-list.component').then(m => m.LecturaListComponent) },
  { path: 'lecturas/nueva', loadComponent: () => import('./pages/lecturas/lectura-form/lectura-form.component').then(m => m.LecturaFormComponent) },
  { path: 'tareas', loadComponent: () => import('./pages/tareas/tarea-list/tarea-list.component').then(m => m.TareaListComponent) },
  { path: 'tareas/nueva', loadComponent: () => import('./pages/tareas/tarea-form/tarea-form.component').then(m => m.TareaFormComponent) },
];