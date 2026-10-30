import { createTask, type Task, type CreateTaskInput } from '../domain/task.js';
import type { TaskRepository } from '../repositories/taskRepository.js';

export class TaskServiceError extends Error {
  public constructor(
    message: string,
    public readonly statusCode: number,
  ) {
    super(message);
    this.name = 'TaskServiceError';
  }
}

export class TaskService {
  // El servicio recibe una abstracción y no crea su propio repositorio.
  public constructor(private readonly repository: TaskRepository) {}

  public list(): Task[] {
    return this.repository.findAll();
  }

  public create(input: CreateTaskInput): Task {
    if (typeof input?.title !== 'string' || input.title.trim() === '') {
      throw new TaskServiceError('El título de la tarea es obligatorio.', 400);
    }
    return this.repository.create(createTask(input.title));
  }

  public toggle(id: string): Task {
    const task = this.repository.toggle(id);
    if (!task) throw new TaskServiceError('La tarea no existe.', 404);
    return task;
  }

  public remove(id: string): void {
    if (!this.repository.remove(id)) {
      throw new TaskServiceError('La tarea no existe.', 404);
    }
  }

  public clearCompleted(): void {
    this.repository.clearCompleted();
  }
}
