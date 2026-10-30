import { taskFilters } from './taskFilters';
import type { Task } from './task';

export interface TaskCounts {
  total: number;
  active: number;
  completed: number;
}

// Calcula contadores desde el estado completo.
// Reutiliza la regla de tarea completada.
export function countTasks(tasks: Task[]): TaskCounts {
  const completed = tasks.filter(taskFilters.completed).length;
  return { total: tasks.length, active: tasks.length - completed, completed };
}
