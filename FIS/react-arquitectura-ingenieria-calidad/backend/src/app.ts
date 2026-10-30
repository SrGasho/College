import cors from 'cors';
import express, { type ErrorRequestHandler } from 'express';
import { database } from './database/database.js';
import { SqliteTaskRepository } from './repositories/sqliteTaskRepository.js';
import { createTaskRoutes } from './routes/taskRoutes.js';
import { TaskService, TaskServiceError } from './services/taskService.js';

// La composición conecta repositorio, servicio y rutas.
const repository = new SqliteTaskRepository(database);
const service = new TaskService(repository);

export function createApp() {
  const app = express();
  app.use(cors());
  app.use(express.json());

  app.get('/health', (_request, response) => {
    response.json({ status: 'ok' });
  });
  app.use('/api/tasks', createTaskRoutes(service));

  const errorHandler: ErrorRequestHandler = (error, _request, response, next) => {
    void next;
    if (error instanceof TaskServiceError) {
      response.status(error.statusCode).json({ error: error.message });
      return;
    }
    response.status(500).json({ error: 'Error interno del servidor.' });
  };
  app.use(errorHandler);

  return app;
}

export const app = createApp();
