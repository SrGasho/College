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
        self.contenedor_datos = None  # Aquí se guarda la matriz 

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

    # métodos de configuración (internos) :DDD

    def _cargar_matriz_adyacencia(self):
        self.conteo_nodos = int(input("Numero de nodos totales: "))
        self.contenedor_datos = []

        for i in range(self.conteo_nodos):
            while True:
                fila = list(map(int, input(f"Conexiones del nodo {i} (espacios entre ellos): ").split()))

                if len(fila) == self.conteo_nodos:
                    self.contenedor_datos.append(fila)
                    break
                else:
                    print(f"Error: debe ingresar exactamente {self.conteo_nodos} valores.")


    def _cargar_lista_adyacencia(self):
        """
        Crea un diccionario donde cada clave es un nodo y su valor es 
        una lista de sus vecinos directos. Ahorra mucho espacio.
        """
        
        self.conteo_nodos = int(input("Numero de nodos totales: "))
        self.contenedor_datos = {}
        for i in range(self.conteo_nodos):
            vecinos = input(f"Nodos conectados al nodo {i} (espacios entre ellos): ").split()
            self.contenedor_datos[i] = [int(v) for v in vecinos]

    def _cargar_matriz_incidencia(self):
        """
        Relaciona Nodos (filas) con Aristas (columnas).
        Cada columna suele tener dos '1' que indican qué nodos une esa arista.
        """
        
        self.conteo_nodos = int(input("Numero de nodos: "))
        self.conteo_aristas = int(input("Numero de aristas: "))
        self.contenedor_datos = []
        for i in range(self.conteo_nodos):
            fila = list(map(int, input(f"Fila nodo {i} (espacios entre ellos) ({self.conteo_aristas} valores): ").split()))
            self.contenedor_datos.append(fila)

    def _cargar_lista_enlaces(self):
        self.conteo_nodos = int(input("Numero de nodos: "))
        n_aristas = int(input("¿Cuantas aristas va a ingresar?: "))
        self.conteo_aristas = n_aristas
        self.contenedor_datos = {}

        for i in range(n_aristas):
            u, v, peso = map(float, input(f"Arista {i} (inicio fin peso): ").split())
            self.contenedor_datos[i] = [int(u), int(v), peso]


    # Métodos de manipulación :3333

    def añadir_nuevo_nodo(self):
        """
        Inserta un nodo vacío a la estructura actual.
        Si es matriz, anade una fila y una columna de ceros.
        """
        if self.tipo_representacion == 1:
            
            for fila in self.contenedor_datos:
                fila.append(0)
            
            self.contenedor_datos.append([0] * (self.conteo_nodos + 1))
            
        elif self.tipo_representacion == 2:
            
            self.contenedor_datos[self.conteo_nodos] = []

        self.conteo_nodos += 1
        print(f"--> Nodo {self.conteo_nodos - 1} integrado correctamente.")

    def remover_nodo(self, id_objetivo):
        """
        Busca un nodo por su ID y lo elimina, limpian cualquier 
        referencia hacia el en otros nodos.
        """
        if id_objetivo >= self.conteo_nodos or id_objetivo < 0:
            print("Error: El nodo no existe.")
            return

        if self.tipo_representacion == 1:
            self.contenedor_datos.pop(id_objetivo) # Quita fila
            for fila in self.contenedor_datos:
                fila.pop(id_objetivo) # Quita columna
        
        elif self.tipo_representacion == 2:
            self.contenedor_datos.pop(id_objetivo)
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

    def obtener_lista_adyacencia(self):
        lista = {i: set() for i in range(self.conteo_nodos)}

        if self.tipo_representacion == 1:
            for i in range(self.conteo_nodos):
                for j in range(self.conteo_nodos):
                    if self.contenedor_datos[i][j] != 0 and i != j:
                        lista[i].add(j)
                        lista[j].add(i)

        elif self.tipo_representacion == 2:
            for nodo, vecinos in self.contenedor_datos.items():
                for vecino in vecinos:
                    if nodo != vecino:
                        lista[nodo].add(vecino)
                        lista[vecino].add(nodo)

        elif self.tipo_representacion == 3:
            for arista in range(self.conteo_aristas):
                nodos_conectados = []

                for nodo in range(self.conteo_nodos):
                    if self.contenedor_datos[nodo][arista] != 0:
                        nodos_conectados.append(nodo)

                if len(nodos_conectados) == 2:
                    u = nodos_conectados[0]
                    v = nodos_conectados[1]
                    lista[u].add(v)
                    lista[v].add(u)

        elif self.tipo_representacion == 4:
            for enlace in self.contenedor_datos.values():
                u = enlace[0]
                v = enlace[1]

                if u != v:
                    lista[u].add(v)
                    lista[v].add(u)

        return {nodo: list(vecinos) for nodo, vecinos in lista.items()}

    def color_disponible(self, nodo, colores, lista_adyacencia):
        colores_vecinos = []

        for vecino in lista_adyacencia[nodo]:
            if vecino in colores:
                colores_vecinos.append(colores[vecino])

        color = 1
        while color in colores_vecinos:
            color += 1

        return color

    def mostrar_coloreo(self, nombre_algoritmo, colores):
        numero_cromatico = max(colores.values()) if colores else 0

        print(f"\n--- Resultado con {nombre_algoritmo} ---")
        print(f"Numero cromatico encontrado: {numero_cromatico}")

        for nodo in sorted(colores):
            print(f"Nodo {nodo} -> Color {colores[nodo]}")

    def colorear_voraz(self):
        lista_adyacencia = self.obtener_lista_adyacencia()
        colores = {}

        for nodo in sorted(lista_adyacencia):
            colores[nodo] = self.color_disponible(nodo, colores, lista_adyacencia)

        self.mostrar_coloreo("Voraz", colores)

    def colorear_welsh_powell(self):
        lista_adyacencia = self.obtener_lista_adyacencia()
        colores = {}

        nodos_ordenados = sorted(
            lista_adyacencia,
            key=lambda nodo: len(lista_adyacencia[nodo]),
            reverse=True
        )

        for nodo in nodos_ordenados:
            colores[nodo] = self.color_disponible(nodo, colores, lista_adyacencia)

        self.mostrar_coloreo("Welsh Powell", colores)

    def grado_saturacion(self, nodo, colores, lista_adyacencia):
        colores_vecinos = set()

        for vecino in lista_adyacencia[nodo]:
            if vecino in colores:
                colores_vecinos.add(colores[vecino])

        return len(colores_vecinos)

    def colorear_dsatur(self):
        lista_adyacencia = self.obtener_lista_adyacencia()
        colores = {}
        nodos_sin_colorear = set(lista_adyacencia.keys())

        while nodos_sin_colorear:
            nodo_elegido = max(
                nodos_sin_colorear,
                key=lambda nodo: (
                    self.grado_saturacion(nodo, colores, lista_adyacencia),
                    len(lista_adyacencia[nodo])
                )
            )

            colores[nodo_elegido] = self.color_disponible(
                nodo_elegido,
                colores,
                lista_adyacencia
            )

            nodos_sin_colorear.remove(nodo_elegido)

        self.mostrar_coloreo("D-Satur", colores)


# Bloque principal :)))

def menu_principal():
    print("--- GESTION DE RED DE GRAFOS ---")
    print("1. Matriz Adyacencia | 2. Lista Adyacencia | 3. Matriz Incidencia | 4. Lista Enlaces")
    opcion = int(input("Elija la representacion: "))
    
    grafo_actual = RedGrafos(opcion)
    grafo_actual.inicializar_grafo()

    while True:
        print("\nACCIONES:")
        print("[1] Anadir Nodo")
        print("[2] Eliminar Nodo")
        print("[3] Mostrar")
        print("[4] Colorear Voraz")
        print("[5] Colorear Welsh Powell")
        print("[6] Colorear D-Satur")
        print("[7] Salir")

        accion = input("Seleccione: ")
        if accion == "1":
            grafo_actual.añadir_nuevo_nodo()

        elif accion == "2":
            target = int(input("ID del nodo a remover: "))
            grafo_actual.remover_nodo(target)

        elif accion == "3":
            grafo_actual.visualizar_estado()

        elif accion == "4":
            grafo_actual.colorear_voraz()

        elif accion == "5":
            grafo_actual.colorear_welsh_powell()

        elif accion == "6":
            grafo_actual.colorear_dsatur()

        elif accion == "7":
            print("Cerrando sistema...")
            break


if __name__ == "__main__":
    menu_principal()