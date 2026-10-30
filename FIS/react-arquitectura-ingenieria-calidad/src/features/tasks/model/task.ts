export interface Task {
  id: string;
  title: string;
  completed: boolean;
  createdAt: number; // Marca temporal de creación.
}

// Normaliza el título; el reducer valida que no esté vacío.
export function createTask(title: string): Task {
  return {
    id: crypto.randomUUID(),
    title: title.trim(),
    completed: false,
    createdAt: Date.now(),
  };
}

// Valida la forma mínima de una tarea. El JSON.parse de localStorage no da
// garantías en runtime, así que se comprueba antes de tratar el dato como Task.
export function isTask(value: unknown): value is Task {
  if (typeof value !== 'object' || value === null) return false;
  const candidate = value as Record<string, unknown>;
  return (
    typeof candidate.id === 'string' &&
    typeof candidate.title === 'string' &&
    typeof candidate.completed === 'boolean' &&
    typeof candidate.createdAt === 'number'
  );
}
