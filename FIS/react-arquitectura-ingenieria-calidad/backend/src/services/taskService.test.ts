import { describe, expect, it } from 'vitest';
import type { Task } from '../domain/task.js';
import type { TaskRepository } from '../repositories/taskRepository.js';
import { TaskService, TaskServiceError } from './taskService.js';

function createMemoryRepository(): TaskRepository {
  let tasks: Task[] = [];
  return {
    findAll: () => [...tasks],
    create: (task) => {
      tasks = [...tasks, task];
      return task;
    },
    toggle: (id) => {
      const task = tasks.find((candidate) => candidate.id === id);
      if (!task) return null;
      const updated = { ...task, completed: !task.completed };
      tasks = tasks.map((candidate) => (candidate.id === id ? updated : candidate));
      return updated;
    },
    remove: (id) => {
      const next = tasks.filter((task) => task.id !== id);
      const changed = next.length !== tasks.length;
      tasks = next;
      return changed;
    },
    clearCompleted: () => {
      const before = tasks.length;
      tasks = tasks.filter((task) => !task.completed);
      return before - tasks.length;
    },
  };
}

describe('TaskService', () => {
  it('valida y crea una tarea', () => {
    const service = new TaskService(createMemoryRepository());
    expect(service.create({ title: '  Preparar demo  ' })).toMatchObject({
      title: 'Preparar demo',
      completed: false,
    });
  });

  it('rechaza títulos vacíos', () => {
    const service = new TaskService(createMemoryRepository());
    expect(() => service.create({ title: '  ' })).toThrow(TaskServiceError);
  });

  it('informa cuando se intenta cambiar una tarea inexistente', () => {
    const service = new TaskService(createMemoryRepository());
    expect(() => service.toggle('missing')).toThrow('La tarea no existe.');
  });
});
