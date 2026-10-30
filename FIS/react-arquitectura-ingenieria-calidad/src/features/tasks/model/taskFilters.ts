import type { Task } from './task';

export type FilterName = 'all' | 'active' | 'completed';

// OCP: para agregar un filtro nuevo se añade una entrada aquí; filterTasks no cambia.
export const taskFilters: Record<FilterName, (task: Task) => boolean> = {
  all: () => true,
  active: (task) => !task.completed,
  completed: (task) => task.completed,
};

export const filterOrder: FilterName[] = ['all', 'active', 'completed'];

export const filterLabels: Record<FilterName, string> = {
  all: 'Todas',
  active: 'Activas',
  completed: 'Completadas',
};

export function filterTasks(tasks: Task[], filter: FilterName): Task[] {
  return tasks.filter(taskFilters[filter]);
}
