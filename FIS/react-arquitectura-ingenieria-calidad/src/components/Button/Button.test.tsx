import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import { Button } from './Button';

describe('Button', () => {
  it('renderiza el contenido', () => {
    render(<Button>Guardar</Button>);
    expect(screen.getByRole('button', { name: 'Guardar' })).toBeInTheDocument();
  });

  it('reenvía el onClick', async () => {
    const onClick = vi.fn();
    render(<Button onClick={onClick}>Guardar</Button>);
    await userEvent.click(screen.getByRole('button'));
    expect(onClick).toHaveBeenCalledOnce();
  });

  it('aplica la clase de la variante', () => {
    render(<Button variant="danger">Borrar</Button>);
    expect(screen.getByRole('button').className).toMatch(/danger/);
  });

  it('reenvía atributos nativos como disabled', () => {
    render(<Button disabled>Nop</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
