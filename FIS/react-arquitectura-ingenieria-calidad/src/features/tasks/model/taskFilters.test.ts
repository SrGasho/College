import { describe, expect, it } from 'vitest';
import { filterLabels, filterOrder, filterTasks, taskFilters } from './taskFilters';
import { createTask } from './task';

const active = createTask('Activa');
const done = { ...createTask('Completada'), completed: true };
const list = [active, done];

describe('taskFilters', () => {
  it('all deja pasar cualquier tarea', () => {
    expect(list.filter(taskFilters.all)).toEqual(list);
  });

  it('active deja solo las no completadas', () => {
    expect(list.filter(taskFilters.active)).toEqual([active]);
  });

  it('completed deja solo las completadas', () => {
    expect(list.filter(taskFilters.completed)).toEqual([done]);
  });

  it('filterTasks aplica el filtro por nombre', () => {
    expect(filterTasks(list, 'active')).toEqual([active]);
    expect(filterTasks(list, 'completed')).toEqual([done]);
    expect(filterTasks(list, 'all')).toEqual(list);
  });

  it('filterOrder y filterLabels cubren los tres filtros', () => {
    expect(filterOrder).toEqual(['all', 'active', 'completed']);
    expect(Object.keys(filterLabels).sort()).toEqual(['active', 'all', 'completed']);
  });
});
