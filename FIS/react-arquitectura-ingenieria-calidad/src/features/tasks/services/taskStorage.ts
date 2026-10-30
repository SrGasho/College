import { isTask, type Task } from '../model/task';

// Contrato de persistencia intercambiable.
export interface TaskStorage {
  load(): Task[];
  save(tasks: Task[]): void;
}

export const STORAGE_KEY = 'task-dashboard.tasks';

export function createLocalStorageTaskStorage(): TaskStorage {
  return {
    load() {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw === null) return [];
      try {
        const parsed: unknown = JSON.parse(raw);
        // Descarta datos que no cumplen el contrato.
        if (Array.isArray(parsed) && parsed.every(isTask)) return parsed;
        console.warn('Las tareas guardadas no tienen el formato esperado, se empieza vacío.');
        return [];
      } catch (error) {
        console.warn('No se pudieron leer las tareas guardadas, se empieza vacío.', error);
        return [];
      }
    },
    save(tasks) {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
      } catch (error) {
        // La app continúa aunque falle la persistencia.
        console.warn(
          'No se pudieron guardar las tareas (almacenamiento lleno o no disponible).',
          error,
        );
      }
    },
  };
}

// Doble en memoria para pruebas sin navegador.
export function createMemoryTaskStorage(initial: Task[] = []): TaskStorage {
  let tasks = [...initial];
  return {
    load() {
      return [...tasks];
    },
    save(next) {
      tasks = [...next];
    },
  };
}
