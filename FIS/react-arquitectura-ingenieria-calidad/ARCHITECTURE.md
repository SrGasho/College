# Arquitectura del Dashboard de Tareas

## 1. Objetivo

Este proyecto es un CRUD didáctico de tareas. Su objetivo es mostrar cómo una aplicación React puede evolucionar desde una persistencia local hacia una arquitectura de tres tiers sin perder la claridad del frontend.

## 2. Tres tiers

Los tiers son partes independientes del sistema que se comunican mediante contratos:

```text
Tier 1: Presentación       React en el navegador
          │ HTTP/JSON
Tier 2: Aplicación         Node.js + Express
          │ SQL
Tier 3: Datos              SQLite
```

### Tier 1: presentación

Está en `src/`. Renderiza la interfaz, administra el estado de la vista y usa `taskGateway.ts` para comunicarse con el backend. No conoce SQL ni importa Express.

### Tier 2: aplicación

Está en `backend/src/`. Expone la API REST, valida las entradas y aplica las reglas de negocio. Sus capas internas son rutas, controladores, servicios y repositorios; todas pertenecen al tier de aplicación.

### Tier 3: datos

Está representado por SQLite en `backend/data/tasks.db`. La base se crea al iniciar el backend y conserva las tareas fuera del navegador.

> Una capa y un tier no son exactamente lo mismo: las capas organizan responsabilidades dentro del código; los tiers separan partes ejecutables del sistema.

## 3. Flujo de una operación

Al completar una tarea:

```text
Checkbox
  → TaskItem
  → TasksDashboard
  → useTasks
  → taskGateway
  → PATCH /api/tasks/:id/toggle
  → controller
  → service
  → repository
  → SQLite
```

La respuesta vuelve por la misma frontera HTTP y el reducer actualiza la vista con la tarea confirmada por el servidor.

## 4. API REST

| Método   | Ruta                    | Responsabilidad          |
| -------- | ----------------------- | ------------------------ |
| `GET`    | `/api/tasks`            | Listar tareas            |
| `POST`   | `/api/tasks`            | Crear una tarea          |
| `PATCH`  | `/api/tasks/:id/toggle` | Cambiar el estado        |
| `DELETE` | `/api/tasks/:id`        | Eliminar una tarea       |
| `DELETE` | `/api/tasks/completed`  | Limpiar completadas      |
| `GET`    | `/health`               | Comprobar disponibilidad |

## 5. Estructura

```text
src/                              # Tier 1: presentación
├── components/                   # Primitivos reutilizables
└── features/tasks/
    ├── components/               # Componentes del dominio
    ├── hooks/useTasks.ts          # Coordinación del estado
    ├── model/                    # Reducer y funciones puras
    └── services/taskGateway.ts   # Frontera HTTP

backend/                          # Tier 2: aplicación
├── src/
│   ├── routes/                   # Rutas REST
│   ├── controllers/              # Adaptación HTTP
│   ├── services/                 # Reglas de negocio
│   ├── repositories/             # Acceso abstracto a datos
│   └── database/                 # Conexión y esquema SQLite
└── data/tasks.db                 # Tier 3: datos generados
```

## 6. Patrones que se pueden explicar

- **Componentes reutilizables:** `Button`, `TextField` y `Checkbox` no dependen del dominio.
- **Flujo unidireccional:** los datos bajan por props y los eventos suben por callbacks.
- **Reducer:** `tasksReducer` transforma el estado de forma pura e inmutable.
- **Gateway/Adapter:** `taskGateway.ts` oculta el protocolo HTTP al resto del frontend.
- **Service Layer:** `TaskService` concentra validaciones y casos de uso.
- **Repository:** `TaskRepository` permite cambiar SQLite por otra fuente.
- **Dependency Inversion:** `TaskService` recibe una interfaz de repositorio.
- **Inyección para pruebas:** el frontend usa `createMemoryTaskGateway` y el backend prueba el servicio con un repositorio en memoria.

## 7. Decisiones didácticas

- SQLite evita configurar un servidor de base de datos durante la exposición.
- El frontend conserva `useReducer` para mostrar el estado como una máquina de acciones.
- La API valida aunque el formulario ya valide, porque el backend es la frontera de confianza.
- `taskStorage.ts` se conserva como adaptador local de contraste y sus pruebas; el flujo principal usa la API.
- No se incluyen autenticación, usuarios, routing ni microservicios para mantener el ejemplo explicable.

## 8. Ejecución

En una terminal:

```bash
npm install
npm run dev
```

En otra terminal:

```bash
cd backend
npm install
npm run dev
```

La interfaz queda en `http://localhost:5173` y la API en `http://localhost:3001`.

## 9. Validación

```bash
npm test
npm run lint
npm run build
cd backend && npm test && npm run build
```
