import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { App } from './App';
import { createMemoryTaskGateway } from './features/tasks/services/taskGateway';

describe('App', () => {
  it('muestra el encabezado y el formulario de tareas', () => {
    render(<App gateway={createMemoryTaskGateway()} />);
    expect(screen.getByRole('heading', { name: 'Dashboard de Tareas' })).toBeInTheDocument();
    expect(screen.getByLabelText('Nueva tarea')).toBeInTheDocument();
  });
});
