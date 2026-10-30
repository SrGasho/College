import { Router } from 'express';
import type { TaskService } from '../services/taskService.js';
import { createTaskController } from '../controllers/taskController.js';

// Las rutas exponen casos de uso como recursos HTTP.
export function createTaskRoutes(service: TaskService): Router {
  const router = Router();
  const controller = createTaskController(service);

  router.get('/', controller.list);
  router.post('/', controller.create);
  router.patch('/:id/toggle', controller.toggle);
  router.delete('/completed', controller.clearCompleted);
  router.delete('/:id', controller.remove);

  return router;
}
