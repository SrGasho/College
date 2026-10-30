class RedGrafos:
    """
    Clase RedGrafos: Gestiona la estructura y conectividad de un grafo.
    Sustenta 4 modelos: Matriz Adyacencia, Lista Adyacencia, Matriz Incidencia y Lista Enlaces.
    """
    def __init__(self, tipo_representacion):
        # Atributos de control
        self.tipo_representacion = tipo_representacion
        self.conteo_nodos = 0
        self.conteo_aristas = 0
        self.contenedor_datos = None  # Aquí se guarda la matriz o el diccionario

    def inicializar_grafo(self):
        """
        Actúa como un selector. Dependiendo del tipo elegido al crear el objeto,
        llama a la función de carga correspondiente.
        """
        if self.tipo_representacion == 1:
            self._cargar_matriz_adyacencia()
        elif self.tipo_representacion == 2:
            self._cargar_lista_adyacencia()
        elif self.tipo_representacion == 3:
            self._cargar_matriz_incidencia()
        elif self.tipo_representacion == 4:
            self._cargar_lista_enlaces()

    # --- MÉTODOS DE CONFIGURACIÓN (INTERNOS) ---

    def _cargar_matriz_adyacencia(self):
        """
        Crea una matriz cuadrada de N x N. 
        Útil para saber instantáneamente si el nodo A llega al B.
        """
        self.conteo_nodos = int(input("Número de nodos totales: "))
        self.contenedor_datos = []
        for i in range(self.conteo_nodos):
            # Se ingresa la fila completa (ej: 0 1 0 1)
            fila = list(map(int, input(f"Conexiones del nodo {i}: ").split()))
            self.contenedor_datos.append(fila)

    def _cargar_lista_adyacencia(self):
        """
        Crea un diccionario donde cada clave es un nodo y su valor es 
        una lista de sus vecinos directos. Ahorra mucho espacio.
        """
        
        self.conteo_nodos = int(input("Número de nodos totales: "))
        self.contenedor_datos = {}
        for i in range(self.conteo_nodos):
            vecinos = input(f"Nodos conectados al nodo {i} (espacios entre ellos): ").split()
            self.contenedor_datos[i] = [int(v) for v in vecinos]

    def _cargar_matriz_incidencia(self):
        """
        Relaciona Nodos (filas) con Aristas (columnas).
        Cada columna suele tener dos '1' que indican qué nodos une esa arista.
        """
        
        self.conteo_nodos = int(input("Número de nodos: "))
        self.conteo_aristas = int(input("Número de aristas: "))
        self.contenedor_datos = []
        for i in range(self.conteo_nodos):
            fila = list(map(int, input(f"Fila nodo {i} ({self.conteo_aristas} valores): ").split()))
            self.contenedor_datos.append(fila)

    def _cargar_lista_enlaces(self):
        """
        Almacena el grafo como una colección de aristas (origen, destino, peso).
        """
        self.conteo_nodos = int(input("Número de nodos: "))
        n_aristas = int(input("¿Cuántas aristas va a ingresar?: "))
        self.contenedor_datos = {}
        for i in range(n_aristas):
            u, v, peso = map(float, input(f"Arista {i} (inicio fin peso): ").split())
            self.contenedor_datos[i] = [int(u), int(v), peso]

    # --- MÉTODOS DE MANIPULACIÓN ---

    def añadir_nuevo_nodo(self):
        """
        Inserta un nodo vacío a la estructura actual.
        Si es matriz, añade una fila y una columna de ceros.
        """
        if self.tipo_representacion == 1:
            # Añadir columna a filas existentes
            for fila in self.contenedor_datos:
                fila.append(0)
            # Añadir la nueva fila de la base
            self.contenedor_datos.append([0] * (self.conteo_nodos + 1))
            
        elif self.tipo_representacion == 2:
            # Simplemente se añade una nueva entrada al diccionario
            self.contenedor_datos[self.conteo_nodos] = []

        self.conteo_nodos += 1
        print(f"--> Nodo {self.conteo_nodos - 1} integrado correctamente.")

    def remover_nodo(self, id_objetivo):
        """
        Busca un nodo por su ID y lo elimina, limpiando cualquier 
        referencia hacia él en otros nodos.
        """
        if id_objetivo >= self.conteo_nodos or id_objetivo < 0:
            print("Error: El nodo no existe.")
            return

        if self.tipo_representacion == 1:
            self.contenedor_datos.pop(id_objetivo) # Quitar fila
            for fila in self.contenedor_datos:
                fila.pop(id_objetivo) # Quitar columna
        
        elif self.tipo_representacion == 2:
            self.contenedor_datos.pop(id_objetivo)
            # Eliminar el rastro del nodo en las listas de vecinos de los demás
            for nodo in self.contenedor_datos:
                self.contenedor_datos[nodo] = [v for v in self.contenedor_datos[nodo] if v != id_objetivo]
        
        self.conteo_nodos -= 1
        print(f"--> Nodo {id_objetivo} y sus conexiones han sido eliminados.")

    def visualizar_estado(self):
        """Muestra por consola la estructura de datos según el modelo."""
        print(f"\n[Visualización: Modelo {self.tipo_representacion}]")
        if isinstance(self.contenedor_datos, list):
            for linea in self.contenedor_datos: print(linea)
        else:
            for clave, valor in self.contenedor_datos.items(): print(f"{clave} -> {valor}")

# --- BLOQUE PRINCIPAL ---

def menu_principal():
    print("--- GESTIÓN DE RED DE GRAFOS ---")
    print("1. Matriz Adyacencia | 2. Lista Adyacencia | 3. Matriz Incidencia | 4. Lista Enlaces")
    opcion = int(input("Elija la representación: "))
    
    grafo_actual = RedGrafos(opcion)
    grafo_actual.inicializar_grafo()

    while True:
        print("\nACCIONES: [1] Añadir Nodo | [2] Eliminar Nodo | [3] Mostrar | [4] Salir")
        accion = input("Seleccione: ")
        if accion == "1":
            grafo_actual.añadir_nuevo_nodo()
        elif accion == "2":
            target = int(input("ID del nodo a remover: "))
            grafo_actual.remover_nodo(target)
        elif accion == "3":
            grafo_actual.visualizar_estado()
        elif accion == "4":
            print("Cerrando sistema...")
            break

if __name__ == "__main__":
    menu_principal()