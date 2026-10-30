import { Button } from '../../../components/Button/Button';
import { filterLabels, filterOrder, type FilterName } from '../model/taskFilters';
import styles from './TaskFilterBar.module.css';

interface TaskFilterBarProps {
  current: FilterName;
  onChange: (filter: FilterName) => void;
}

// Recorre una estructura de datos en vez de repetir JSX por cada filtro.
export function TaskFilterBar({ current, onChange }: TaskFilterBarProps) {
  return (
    <div className={styles.bar} role="group" aria-label="Filtrar tareas">
      {filterOrder.map((name) => (
        <Button
          key={name}
          variant={name === current ? 'primary' : 'ghost'}
          aria-pressed={name === current}
          onClick={() => onChange(name)}
        >
          {filterLabels[name]}
        </Button>
      ))}
    </div>
  );
}
