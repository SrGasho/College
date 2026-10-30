import { Button } from '../../../components/Button/Button';
import type { TaskCounts } from '../model/taskCounts';
import styles from './TaskStats.module.css';

interface TaskStatsProps {
  stats: TaskCounts;
  onClearCompleted: () => void;
}

export function TaskStats({ stats, onClearCompleted }: TaskStatsProps) {
  // Un solo nodo de texto: se lee fácil y la prueba puede buscarlo entero.
  const summary = `${stats.active} activas, ${stats.completed} completadas, ${stats.total} en total`;
  return (
    <footer className={styles.stats}>
      <span>{summary}</span>
      <Button variant="ghost" onClick={onClearCompleted} disabled={stats.completed === 0}>
        Limpiar completadas
      </Button>
    </footer>
  );
}
