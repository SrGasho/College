import { describe, expect, it } from 'vitest';
import { countTasks } from './taskCounts';
import { createTask, type Task } from './task';

describe('countTasks', () => {
  it('cuenta en cero cuando no hay tareas', () => {
    expect(countTasks([])).toEqual({ total: 0, active: 0, completed: 0 });
  });

  it('separa activas de completadas y la suma cuadra con el total', () => {
    const tasks: Task[] = [
      createTask('Redactar guion'),
      { ...createTask('Preparar slides'), completed: true },
      createTask('Ensayar demo'),
    ];
    expect(countTasks(tasks)).toEqual({ total: 3, active: 2, completed: 1 });
  });

  it('no deja activas cuando todas están completadas', () => {
    const tasks: Task[] = [
      { ...createTask('A'), completed: true },
      { ...createTask('B'), completed: true },
    ];
    expect(countTasks(tasks)).toEqual({ total: 2, active: 0, completed: 2 });
  });
});
