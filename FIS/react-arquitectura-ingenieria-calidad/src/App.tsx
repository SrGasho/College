import { TasksDashboard } from './features/tasks/TasksDashboard';
import type { TaskGateway } from './features/tasks/services/taskGateway';
import styles from './App.module.css';

interface AppProps {
  gateway?: TaskGateway;
}

export function App({ gateway }: AppProps) {
  return (
    <main className={styles.app}>
      <header className={styles.header}>
        <h1>Dashboard de Tareas</h1>
        <p className={styles.subtitle}>
          Caso de estudio: componentes reutilizables, API REST, estado inmutable y arquitectura de
          tres tiers.
        </p>
      </header>
      <TasksDashboard gateway={gateway} />
    </main>
  );
}
