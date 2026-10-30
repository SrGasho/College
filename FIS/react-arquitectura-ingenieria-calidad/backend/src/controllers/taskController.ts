import type { Request, Response } from 'express';
import type { TaskService } from '../services/taskService.js';

function routeId(request: Request): string {
  const value = request.params.id;
  return Array.isArray(value) ? value[0] : value;
}

// El controlador traduce HTTP; no contiene consultas ni reglas de negocio.
export function createTaskController(service: TaskService) {
  return {
    list(_request: Request, response: Response) {
      response.json({ data: service.list() });
    },
    create(request: Request, response: Response) {
      response.status(201).json({ data: service.create(request.body) });
    },
    toggle(request: Request, response: Response) {
      response.json({ data: service.toggle(routeId(request)) });
    },
    remove(request: Request, response: Response) {
      service.remove(routeId(request));
      response.status(204).send();
    },
    clearCompleted(_request: Request, response: Response) {
      service.clearCompleted();
      response.status(204).send();
    },
  };
}
