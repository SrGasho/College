import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { TaskList } from './TaskList';
import type { Task } from '../model/task';

const tasks: Task[] = [
  { id: 't1', title: 'Preparar la demo', completed: false, createdAt: 0 },
  { id: 't2', title: 'Revisar el guion', completed: true, createdAt: 1 },
];

describe('TaskList', () => {
  it('muestra el mensaje de estado vacío cuando no hay tareas', () => {
    render(<TaskList tasks={[]} onToggle={vi.fn()} onRemove={vi.fn()} />);
    expect(screen.getByText('No hay tareas para este filtro.')).toBeInTheDocument();
    expect(screen.queryAllByRole('listitem')).toHaveLength(0);
  });

  it('pinta una fila por tarea cuando la lista tiene elementos', () => {
    render(<TaskList tasks={tasks} onToggle={vi.fn()} onRemove={vi.fn()} />);
    expect(screen.getAllByRole('listitem')).toHaveLength(2);
    expect(screen.getByText('Preparar la demo')).toBeInTheDocument();
  });
});
