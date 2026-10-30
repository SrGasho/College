import { describe, expect, it } from 'vitest';
import { tasksReducer } from './tasksReducer';
import { createTask } from './task';

describe('tasksReducer', () => {
  it('added agrega una tarea nueva al final', () => {
    const next = tasksReducer([], { type: 'added', title: 'Preparar demo' });
    expect(next).toHaveLength(1);
    expect(next[0]).toMatchObject({ title: 'Preparar demo', completed: false });
    expect(typeof next[0].id).toBe('string');
    expect(typeof next[0].createdAt).toBe('number');
  });

  it('added ignora un título vacío o solo espacios', () => {
    expect(tasksReducer([], { type: 'added', title: '   ' })).toEqual([]);
  });

  it('added no muta el estado anterior', () => {
    const state = [createTask('Existente')];
    const next = tasksReducer(state, { type: 'added', title: 'Nueva' });
    expect(next).not.toBe(state);
    expect(state).toHaveLength(1);
  });

  it('toggled invierte completed solo en la tarea indicada', () => {
    const state = [createTask('A'), createTask('B')];
    const next = tasksReducer(state, { type: 'toggled', id: state[0].id });
    expect(next[0].completed).toBe(true);
    expect(next[1].completed).toBe(false);
    expect(next[0]).not.toBe(state[0]);
  });

  it('removed quita la tarea indicada', () => {
    const state = [createTask('A'), createTask('B')];
    const next = tasksReducer(state, { type: 'removed', id: state[0].id });
    expect(next).toHaveLength(1);
    expect(next[0].title).toBe('B');
  });

  it('clearedCompleted deja solo las tareas activas', () => {
    const a = { ...createTask('A'), completed: true };
    const b = createTask('B');
    const next = tasksReducer([a, b], { type: 'clearedCompleted' });
    expect(next).toEqual([b]);
  });

  it('hydrated reemplaza el estado completo', () => {
    const incoming = [createTask('Desde almacenamiento')];
    expect(tasksReducer([createTask('Vieja')], { type: 'hydrated', tasks: incoming })).toBe(
      incoming,
    );
  });
});
