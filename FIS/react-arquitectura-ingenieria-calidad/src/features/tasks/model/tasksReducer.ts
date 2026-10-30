import { createTask, type Task } from './task';

export type TaskAction =
  | { type: 'added'; title: string }
  | { type: 'addedTask'; task: Task }
  | { type: 'updated'; task: Task }
  | { type: 'toggled'; id: string }
  | { type: 'removed'; id: string }
  | { type: 'clearedCompleted' }
  | { type: 'hydrated'; tasks: Task[] };

// Obliga a tratar cada acción antes de compilar.
function assertNever(action: never): never {
  throw new Error(`Acción desconocida: ${JSON.stringify(action)}`);
}

// El reducer solo transforma estado; no conoce HTTP ni almacenamiento.
export function tasksReducer(state: Task[], action: TaskAction): Task[] {
  switch (action.type) {
    case 'added':
      if (action.title.trim() === '') return state;
      return [...state, createTask(action.title)];
    case 'addedTask':
      return [...state, action.task];
    case 'updated':
      return state.map((task) => (task.id === action.task.id ? action.task : task));
    case 'toggled':
      return state.map((task) =>
        task.id === action.id ? { ...task, completed: !task.completed } : task,
      );
    case 'removed':
      return state.filter((task) => task.id !== action.id);
    case 'clearedCompleted':
      return state.filter((task) => !task.completed);
    case 'hydrated':
      return action.tasks;
    default:
      return assertNever(action);
  }
}
