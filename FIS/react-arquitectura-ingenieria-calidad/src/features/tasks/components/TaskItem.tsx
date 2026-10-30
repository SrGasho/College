import { Button } from '../../../components/Button/Button';
import { Checkbox } from '../../../components/Checkbox/Checkbox';
import type { Task } from '../model/task';
import styles from './TaskItem.module.css';

// Recibe solo las props que necesita.
interface TaskItemProps {
  task: Task;
  onToggle: (id: string) => void;
  onRemove: (id: string) => void;
}

// Presenta una fila sin estado propio.
export function TaskItem({ task, onToggle, onRemove }: TaskItemProps) {
  return (
    <li className={styles.item} data-completed={task.completed}>
      <Checkbox label={task.title} checked={task.completed} onChange={() => onToggle(task.id)} />
      <Button
        variant="danger"
        onClick={() => onRemove(task.id)}
        aria-label={`Eliminar ${task.title}`}
      >
        Eliminar
      </Button>
    </li>
  );
}
