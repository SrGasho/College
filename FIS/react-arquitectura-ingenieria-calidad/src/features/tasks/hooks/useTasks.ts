import { useCallback, useEffect, useMemo, useReducer, useState } from 'react';
import type { Task } from '../model/task';
import { countTasks, type TaskCounts } from '../model/taskCounts';
import { filterTasks, type FilterName } from '../model/taskFilters';
import { tasksReducer } from '../model/tasksReducer';
import { apiTaskGateway, type TaskGateway } from '../services/taskGateway';

export interface UseTasksResult {
  tasks: Task[];
  filter: FilterName;
  stats: TaskCounts;
  isLoading: boolean;
  error: string | null;
  addTask: (title: string) => Promise<void>;
  toggleTask: (id: string) => Promise<void>;
  removeTask: (id: string) => Promise<void>;
  clearCompleted: () => Promise<void>;
  setFilter: (filter: FilterName) => void;
}

function errorMessage(error: unknown): string {
  return error instanceof Error ? error.message : 'No se pudo completar la operación.';
}

// Coordina la API, el reducer y las vistas; no contiene consultas SQL.
export function useTasks(gateway: TaskGateway = apiTaskGateway): UseTasksResult {
  const [allTasks, dispatch] = useReducer(tasksReducer, []);
  const [filter, setFilter] = useState<FilterName>('all');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // La carga inicial hidrata el estado desde el tier de aplicación.
  useEffect(() => {
    let cancelled = false;
    setIsLoading(true);
    gateway
      .list()
      .then((tasks) => {
        if (!cancelled) dispatch({ type: 'hydrated', tasks });
      })
      .catch((reason: unknown) => {
        if (!cancelled) setError(errorMessage(reason));
      })
      .finally(() => {
        if (!cancelled) setIsLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [gateway]);

  const addTask = useCallback(
    async (title: string) => {
      if (title.trim() === '') return;
      try {
        setError(null);
        const task = await gateway.create(title);
        dispatch({ type: 'addedTask', task });
      } catch (reason: unknown) {
        setError(errorMessage(reason));
      }
    },
    [gateway],
  );

  const toggleTask = useCallback(
    async (id: string) => {
      try {
        setError(null);
        const task = await gateway.toggle(id);
        dispatch({ type: 'updated', task });
      } catch (reason: unknown) {
        setError(errorMessage(reason));
      }
    },
    [gateway],
  );

  const removeTask = useCallback(
    async (id: string) => {
      try {
        setError(null);
        await gateway.remove(id);
        dispatch({ type: 'removed', id });
      } catch (reason: unknown) {
        setError(errorMessage(reason));
      }
    },
    [gateway],
  );

  const clearCompleted = useCallback(async () => {
    try {
      setError(null);
      await gateway.clearCompleted();
      dispatch({ type: 'clearedCompleted' });
    } catch (reason: unknown) {
      setError(errorMessage(reason));
    }
  }, [gateway]);

  const tasks = useMemo(() => filterTasks(allTasks, filter), [allTasks, filter]);
  const stats = useMemo(() => countTasks(allTasks), [allTasks]);

  return {
    tasks,
    filter,
    stats,
    isLoading,
    error,
    addTask,
    toggleTask,
    removeTask,
    clearCompleted,
    setFilter,
  };
}
