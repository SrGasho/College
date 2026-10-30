import type { Task } from '../domain/task.js';

export interface TaskRepository {
  findAll(): Task[];
  create(task: Task): Task;
  toggle(id: string): Task | null;
  remove(id: string): boolean;
  clearCompleted(): number;
}
