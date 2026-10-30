import { TaskFilterBar } from './components/TaskFilterBar';
import { TaskForm } from './components/TaskForm';
import { TaskList } from './components/TaskList';
import { TaskStats } from './components/TaskStats';
import { apiTaskGateway, type TaskGateway } from './services/taskGateway';
import { useTasks } from './hooks/useTasks';
import styles from './TasksDashboard.module.css';

interface TasksDashboardProps {
  gateway?: TaskGateway;
}

// Orquesta la vista y recibe la fuente de datos por inyección.
export function TasksDashboard({ gateway = apiTaskGateway }: TasksDashboardProps) {
  const {
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
  } = useTasks(gateway);

  return (
    <section className={styles.dashboard}>
      <TaskForm onSubmit={addTask} />
      <TaskFilterBar current={filter} onChange={setFilter} />
      {isLoading && (
        <p className={styles.status} role="status">
          Cargando tareas...
        </p>
      )}
      {error && (
        <p className={styles.error} role="alert">
          {error}
        </p>
      )}
      <TaskList tasks={tasks} onToggle={toggleTask} onRemove={removeTask} />
      <TaskStats stats={stats} onClearCompleted={clearCompleted} />
    </section>
  );
}
