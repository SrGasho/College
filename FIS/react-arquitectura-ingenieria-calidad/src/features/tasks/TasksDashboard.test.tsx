import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it } from 'vitest';
import { TasksDashboard } from './TasksDashboard';
import { createMemoryTaskGateway } from './services/taskGateway';

function renderDashboard() {
  return render(<TasksDashboard gateway={createMemoryTaskGateway()} />);
}

async function addTask(title: string) {
  await userEvent.type(screen.getByLabelText('Nueva tarea'), title);
  await userEvent.click(screen.getByRole('button', { name: 'Agregar' }));
}

describe('TasksDashboard', () => {
  it('agrega una tarea desde el formulario', async () => {
    renderDashboard();
    await addTask('Escribir el guion');
    expect(await screen.findByText('Escribir el guion')).toBeInTheDocument();
  });

  it('actualiza los contadores al completar', async () => {
    renderDashboard();
    await addTask('Tarea uno');
    await userEvent.click(await screen.findByRole('checkbox', { name: 'Tarea uno' }));
    expect(await screen.findByText('0 activas, 1 completadas, 1 en total')).toBeInTheDocument();
  });

  it('el filtro Activas oculta las completadas', async () => {
    renderDashboard();
    await addTask('Visible');
    await addTask('Oculta');
    await userEvent.click(await screen.findByRole('checkbox', { name: 'Oculta' }));
    await userEvent.click(screen.getByRole('button', { name: 'Activas' }));
    expect(screen.getByText('Visible')).toBeInTheDocument();
    expect(screen.queryByText('Oculta')).not.toBeInTheDocument();
  });
});
