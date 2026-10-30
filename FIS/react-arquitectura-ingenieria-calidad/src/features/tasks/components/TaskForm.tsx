import { useState, type FormEvent } from 'react';
import { Button } from '../../../components/Button/Button';
import { TextField } from '../../../components/TextField/TextField';
import styles from './TaskForm.module.css';

interface TaskFormProps {
  onSubmit: (title: string) => void | Promise<void>;
}

// Conserva solo el texto temporal del formulario.
export function TaskForm({ onSubmit }: TaskFormProps) {
  const [title, setTitle] = useState('');

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    if (title.trim() === '') return;
    onSubmit(title);
    setTitle('');
  }

  return (
    <form className={styles.form} onSubmit={handleSubmit}>
      <TextField
        label="Nueva tarea"
        placeholder="¿Qué hay que hacer?"
        value={title}
        onChange={(event) => setTitle(event.target.value)}
      />
      <Button type="submit">Agregar</Button>
    </form>
  );
}
