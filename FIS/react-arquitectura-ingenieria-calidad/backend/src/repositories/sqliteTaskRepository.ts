import type Database from 'better-sqlite3';
import type { Task } from '../domain/task.js';
import type { TaskRepository } from './taskRepository.js';

type TaskRow = {
  id: string;
  title: string;
  completed: number;
  created_at: number;
};

// Traduce filas SQL al modelo que entiende la aplicación.
function mapRow(row: TaskRow): Task {
  return {
    id: row.id,
    title: row.title,
    completed: row.completed === 1,
    createdAt: row.created_at,
  };
}

export class SqliteTaskRepository implements TaskRepository {
  public constructor(private readonly database: Database.Database) {}

  public findAll(): Task[] {
    const rows = this.database
      .prepare('SELECT id, title, completed, created_at FROM tasks ORDER BY created_at ASC')
      .all() as TaskRow[];
    return rows.map(mapRow);
  }

  public create(task: Task): Task {
    this.database
      .prepare(
        'INSERT INTO tasks (id, title, completed, created_at) VALUES (@id, @title, @completed, @createdAt)',
      )
      .run({ ...task, completed: task.completed ? 1 : 0 });
    return task;
  }

  public toggle(id: string): Task | null {
    const task = this.findById(id);
    if (!task) return null;

    this.database.prepare('UPDATE tasks SET completed = @completed WHERE id = @id').run({
      id,
      completed: task.completed ? 0 : 1,
    });
    return { ...task, completed: !task.completed };
  }

  public remove(id: string): boolean {
    return this.database.prepare('DELETE FROM tasks WHERE id = ?').run(id).changes > 0;
  }

  public clearCompleted(): number {
    return this.database.prepare('DELETE FROM tasks WHERE completed = 1').run().changes;
  }

  private findById(id: string): Task | null {
    const row = this.database
      .prepare('SELECT id, title, completed, created_at FROM tasks WHERE id = ?')
      .get(id) as TaskRow | undefined;
    return row ? mapRow(row) : null;
  }
}
