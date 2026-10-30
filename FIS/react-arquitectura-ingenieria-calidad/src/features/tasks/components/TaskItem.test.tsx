import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import { TaskItem } from './TaskItem';
import type { Task } from '../model/task';

const baseTask: Task = { id: 't1', title: 'Preparar la demo', completed: false, createdAt: 0 };

describe('TaskItem', () => {
  it('muestra el título de la tarea', () => {
    render(<TaskItem task={baseTask} onToggle={vi.fn()} onRemove={vi.fn()} />);
    expect(screen.getByText('Preparar la demo')).toBeInTheDocument();
  });

  it('refleja el estado completado en el checkbox', () => {
    render(
      <TaskItem task={{ ...baseTask, completed: true }} onToggle={vi.fn()} onRemove={vi.fn()} />,
    );
    expect(screen.getByRole('checkbox')).toBeChecked();
  });

  it('llama onToggle con el id al marcar', async () => {
    const onToggle = vi.fn();
    render(<TaskItem task={baseTask} onToggle={onToggle} onRemove={vi.fn()} />);
    await userEvent.click(screen.getByRole('checkbox'));
    expect(onToggle).toHaveBeenCalledWith('t1');
  });

  it('llama onRemove con el id al eliminar', async () => {
    const onRemove = vi.fn();
    render(<TaskItem task={baseTask} onToggle={vi.fn()} onRemove={onRemove} />);
    await userEvent.click(screen.getByRole('button', { name: /eliminar/i }));
    expect(onRemove).toHaveBeenCalledWith('t1');
  });
});
