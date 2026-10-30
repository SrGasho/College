# Dashboard de Tareas

Caso de estudio de la charla **React: Arquitectura, Ingeniería y Calidad**. Es un CRUD pequeño para explicar una arquitectura web de tres tiers, patrones de diseño y buenas prácticas sin ocultar el flujo.

## Arquitectura

```text
React / navegador  →  API Express  →  SQLite
 Tier 1               Tier 2          Tier 3
```

- **Tier 1:** `src/` presenta la interfaz y coordina el estado visual.
- **Tier 2:** `backend/src/` expone la API y contiene rutas, controladores, servicios y repositorios.
- **Tier 3:** `backend/data/tasks.db` conserva los datos en SQLite.

Las rutas, controladores, servicios y repositorios son capas internas del tier de aplicación; no son tiers separados. El detalle completo está en [`ARCHITECTURE.md`](./ARCHITECTURE.md).

## Requisitos

- Node 22
- npm 10

## Cómo ejecutar

Terminal 1, frontend:

```bash
npm install
npm run dev
```

Terminal 2, backend:

```bash
cd backend
npm install
npm run dev
```

Abrir `http://localhost:5173`. La API responde en `http://localhost:3001` y su comprobación rápida está en `http://localhost:3001/health`.

## Operaciones del dashboard

- Crear tareas.
- Listar tareas.
- Completar y descompletar tareas.
- Filtrar por todas, activas o completadas.
- Eliminar tareas.
- Limpiar tareas completadas.

## Árbol principal del frontend

```text
App
└── TasksDashboard        # Orquesta estado y presentación
    ├── TaskForm          # Entrada controlada
    ├── TaskFilterBar     # Filtros desde datos
    ├── TaskList          # Recorre la colección
    │   └── TaskItem      # Checkbox + Button
    └── TaskStats          # Contadores y limpieza
```

## Mapa de exposición a código

| Tema                      | Archivo                                                       | Qué observar                               |
| ------------------------- | ------------------------------------------------------------- | ------------------------------------------ |
| Tres tiers                | `src/features/tasks/services/taskGateway.ts` y `backend/src/` | Frontera HTTP entre React, API y SQLite    |
| Flujo unidireccional      | `TasksDashboard.tsx`                                          | Props hacia abajo y callbacks hacia arriba |
| Componentes reutilizables | `src/components/`                                             | Primitivos sin conocimiento del dominio    |
| Estado inmutable          | `model/tasksReducer.ts`                                       | Acciones y nuevos arreglos                 |
| Modelo puro               | `features/tasks/model/`                                       | Reglas sin React ni HTTP                   |
| Service Layer             | `backend/src/services/taskService.ts`                         | Validaciones y casos de uso                |
| Repository Pattern        | `backend/src/repositories/`                                   | SQL aislado detrás de una interfaz         |
| Dependency Inversion      | `TaskService` y `TaskRepository`                              | El servicio recibe su dependencia          |
| Pruebas                   | `*.test.ts` y `*.test.tsx`                                    | Modelo, hook, componentes y servicio       |

## Guion breve de demostración

1. Iniciar backend y frontend en dos terminales.
2. Crear una tarea y mostrar que React actualiza la interfaz.
3. Abrir las herramientas de red y observar `POST /api/tasks`.
4. Completar la tarea y seguir `PATCH → controller → service → repository → SQLite`.
5. Mostrar `tasksReducer.ts` para explicar la actualización inmutable.
6. Mostrar `backend/src/services/taskService.test.ts` para explicar la inyección de dependencias.
7. Detener el backend y mostrar el mensaje de error del frontend.

## Pruebas y calidad

```bash
npm test
npm run lint
npm run build
cd backend && npm test && npm run build
```

El frontend usa `createMemoryTaskGateway` en sus pruebas para no depender de un servidor. El backend prueba el servicio con un repositorio en memoria.
