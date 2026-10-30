import type { Task } from '../model/task';

// El frontend depende de este contrato, no de Express ni de SQLite.
export interface TaskGateway {
  list(): Promise<Task[]>;
  create(title: string): Promise<Task>;
  toggle(id: string): Promise<Task>;
  remove(id: string): Promise<void>;
  clearCompleted(): Promise<void>;
}

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:3001';

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  });
  if (!response.ok) {
    const body = (await response.json().catch(() => null)) as { error?: string } | null;
    throw new Error(body?.error ?? 'No se pudo completar la operación.');
  }
  if (response.status === 204) return undefined as T;
  const body = (await response.json()) as { data: T };
  return body.data;
}

export const apiTaskGateway: TaskGateway = {
  list: () => request<Task[]>('/api/tasks'),
  create: (title) =>
    request<Task>('/api/tasks', { method: 'POST', body: JSON.stringify({ title }) }),
  toggle: (id) => request<Task>(`/api/tasks/${id}/toggle`, { method: 'PATCH' }),
  remove: (id) => request<void>(`/api/tasks/${id}`, { method: 'DELETE' }),
  clearCompleted: () => request<void>('/api/tasks/completed', { method: 'DELETE' }),
};

export function createMemoryTaskGateway(initial: Task[] = []): TaskGateway {
  let tasks = [...initial];
  return {
    async list() {
      return [...tasks];
    },
    async create(title) {
      const task = {
        id: crypto.randomUUID(),
        title: title.trim(),
        completed: false,
        createdAt: Date.now(),
      };
      tasks = [...tasks, task];
      return task;
    },
    async toggle(id) {
      const task = tasks.find((candidate) => candidate.id === id);
      if (!task) throw new Error('La tarea no existe.');
      const updated = { ...task, completed: !task.completed };
      tasks = tasks.map((candidate) => (candidate.id === id ? updated : candidate));
      return updated;
    },
    async remove(id) {
      tasks = tasks.filter((task) => task.id !== id);
    },
    async clearCompleted() {
      tasks = tasks.filter((task) => !task.completed);
    },
  };
}
