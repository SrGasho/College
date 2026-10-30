import { act, renderHook, waitFor } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { createTask } from '../model/task';
import { createMemoryTaskGateway } from '../services/taskGateway';
import { useTasks } from './useTasks';

async function ready(gateway = createMemoryTaskGateway()) {
  const hook = renderHook(() => useTasks(gateway));
  await waitFor(() => expect(hook.result.current.isLoading).toBe(false));
  return hook;
}

describe('useTasks', () => {
  it('carga el estado inicial desde el gateway inyectado', async () => {
    const hook = await ready(createMemoryTaskGateway([createTask('Preparar demo')]));
    expect(hook.result.current.tasks).toHaveLength(1);
    expect(hook.result.current.tasks[0].title).toBe('Preparar demo');
  });

  it('addTask agrega una tarea y la conserva en el gateway', async () => {
    const gateway = createMemoryTaskGateway();
    const hook = await ready(gateway);
    await act(async () => hook.result.current.addTask('Escribir pruebas'));
    expect(hook.result.current.tasks).toHaveLength(1);
    expect(hook.result.current.tasks[0].title).toBe('Escribir pruebas');
  });

  it('toggleTask invierte el estado completado', async () => {
    const hook = await ready();
    await act(async () => hook.result.current.addTask('Tarea'));
    const id = hook.result.current.tasks[0].id;
    await act(async () => hook.result.current.toggleTask(id));
    expect(hook.result.current.tasks[0].completed).toBe(true);
  });

  it('removeTask elimina la tarea', async () => {
    const hook = await ready();
    await act(async () => hook.result.current.addTask('Tarea'));
    await act(async () => hook.result.current.removeTask(hook.result.current.tasks[0].id));
    expect(hook.result.current.tasks).toHaveLength(0);
  });

  it('clearCompleted elimina solo las completadas', async () => {
    const hook = await ready();
    await act(async () => {
      await hook.result.current.addTask('A');
      await hook.result.current.addTask('B');
    });
    await act(async () => hook.result.current.toggleTask(hook.result.current.tasks[0].id));
    await act(async () => hook.result.current.clearCompleted());
    expect(hook.result.current.tasks).toHaveLength(1);
    expect(hook.result.current.tasks[0].title).toBe('B');
  });

  it('setFilter cambia las tareas visibles y stats conserva el total', async () => {
    const hook = await ready();
    await act(async () => {
      await hook.result.current.addTask('A');
      await hook.result.current.addTask('B');
    });
    await act(async () => hook.result.current.toggleTask(hook.result.current.tasks[0].id));
    act(() => hook.result.current.setFilter('active'));
    expect(hook.result.current.tasks).toHaveLength(1);
    expect(hook.result.current.stats).toEqual({ total: 2, active: 1, completed: 1 });
  });
});
