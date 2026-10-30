import math

class NodoArbolB:
    def __init__(self, t, esHoja=False):
        self.t = t
        self.esHoja = esHoja
        self.claves = []
        self.hijos = []

    def __str__(self):
        return str(self.claves)


class ArbolB:
    def __init__(self, t):
        self.t = t
        self.raiz = NodoArbolB(t, esHoja=True)

    def mostrarArbol(self):
        self._mostrarArbol(self.raiz, "", True)

    def _mostrarArbol(self, nodo, prefijo, esUltimo):
        if nodo is None:
            return

        conector = "└── " if esUltimo else "├── "
        print(prefijo + conector + str(nodo.claves))

        prefijo += "    " if esUltimo else "│   "

        for i, hijo in enumerate(nodo.hijos):
            self._mostrarArbol(hijo, prefijo, i == len(nodo.hijos) - 1)


    def insertar(self, clave):
        raiz = self.raiz

        if len(raiz.claves) == 2 * self.t - 1:
            nuevaRaiz = NodoArbolB(self.t, esHoja=False)
            nuevaRaiz.hijos.append(raiz)
            self.dividirHijo(nuevaRaiz, 0)
            self.raiz = nuevaRaiz
            self.insertarNoLleno(nuevaRaiz, clave)
        else:
            self.insertarNoLleno(raiz, clave)

    def insertarNoLleno(self, nodo, clave):
        i = len(nodo.claves) - 1

        if nodo.esHoja:
            nodo.claves.append(None)
            while i >= 0 and clave < nodo.claves[i]:
                nodo.claves[i + 1] = nodo.claves[i]
                i -= 1
            nodo.claves[i + 1] = clave
        else:
            while i >= 0 and clave < nodo.claves[i]:
                i -= 1
            i += 1

            if len(nodo.hijos[i].claves) == 2 * self.t - 1:
                self.dividirHijo(nodo, i)
                if clave > nodo.claves[i]:
                    i += 1

            self.insertarNoLleno(nodo.hijos[i], clave)

    def dividirHijo(self, padre, i):
        t = self.t
        hijoLleno = padre.hijos[i]
        nuevoHijo = NodoArbolB(t, esHoja=hijoLleno.esHoja)

        padre.claves.insert(i, hijoLleno.claves[t - 1])
        padre.hijos.insert(i + 1, nuevoHijo)

        nuevoHijo.claves = hijoLleno.claves[t:]
        hijoLleno.claves = hijoLleno.claves[:t - 1]

        if not hijoLleno.esHoja:
            nuevoHijo.hijos = hijoLleno.hijos[t:]
            hijoLleno.hijos = hijoLleno.hijos[:t]

    def eliminar(self, clave):
        self._eliminar(self.raiz, clave)

        if len(self.raiz.claves) == 0 and not self.raiz.esHoja:
            self.raiz = self.raiz.hijos[0]

    def _eliminar(self, nodo, clave):
        t = self.t
        i = 0

        while i < len(nodo.claves) and clave > nodo.claves[i]:
            i += 1

        if i < len(nodo.claves) and nodo.claves[i] == clave:
            if nodo.esHoja:
                nodo.claves.pop(i)
            else:
                self.eliminarNodoInterno(nodo, clave, i)
        else:
            if nodo.esHoja:
                print("Clave no encontrada")
                return

            if i < len(nodo.hijos) and len(nodo.hijos[i].claves) < t:
                self.llenar(nodo, i)
                if i > len(nodo.claves):
                    i -= 1

            if i < len(nodo.hijos):
                self._eliminar(nodo.hijos[i], clave)

    def eliminarNodoInterno(self, nodo, clave, i):
        t = self.t

        if len(nodo.hijos[i].claves) >= t:
            predecesor = self.obtenerPredecesor(nodo, i)
            nodo.claves[i] = predecesor
            self._eliminar(nodo.hijos[i], predecesor)

        elif len(nodo.hijos[i + 1].claves) >= t:
            sucesor = self.obtenerSucesor(nodo, i)
            nodo.claves[i] = sucesor
            self._eliminar(nodo.hijos[i + 1], sucesor)

        else:
            self.fusionar(nodo, i)
            self._eliminar(nodo.hijos[i], clave)

    def obtenerPredecesor(self, nodo, i):
        actual = nodo.hijos[i]
        while not actual.esHoja:
            actual = actual.hijos[-1]
        return actual.claves[-1]

    def obtenerSucesor(self, nodo, i):
        actual = nodo.hijos[i + 1]
        while not actual.esHoja:
            actual = actual.hijos[0]
        return actual.claves[0]

    def llenar(self, nodo, i):
        if i != 0 and len(nodo.hijos[i - 1].claves) >= self.t:
            self.tomarDelAnterior(nodo, i)
        elif i != len(nodo.hijos) - 1 and len(nodo.hijos[i + 1].claves) >= self.t:
            self.tomarDelSiguiente(nodo, i)
        else:
            if i != len(nodo.hijos) - 1:
                self.fusionar(nodo, i)
            else:
                self.fusionar(nodo, i - 1)

    def tomarDelAnterior(self, nodo, i):
        hijo = nodo.hijos[i]
        hermano = nodo.hijos[i - 1]

        hijo.claves.insert(0, nodo.claves[i - 1])
        nodo.claves[i - 1] = hermano.claves.pop()

        if not hermano.esHoja:
            hijo.hijos.insert(0, hermano.hijos.pop())

    def tomarDelSiguiente(self, nodo, i):
        hijo = nodo.hijos[i]
        hermano = nodo.hijos[i + 1]

        hijo.claves.append(nodo.claves[i])
        nodo.claves[i] = hermano.claves.pop(0)

        if not hermano.esHoja:
            hijo.hijos.append(hermano.hijos.pop(0))

    def fusionar(self, nodo, i):
        hijo = nodo.hijos[i]
        hermano = nodo.hijos[i + 1]

        hijo.claves.append(nodo.claves.pop(i))
        hijo.claves.extend(hermano.claves)

        if not hijo.esHoja:
            hijo.hijos.extend(hermano.hijos)

        nodo.hijos.pop(i + 1)


def principal():
    m = int(input("Ingrese el orden del Árbol B (máximo número de hijos m): "))
    t = math.ceil(m / 2)

    print("\nConfiguración del árbol:")
    print("Máx hijos:", m)
    print("Máx claves:", m - 1)
    print("Mín hijos:", math.ceil(m / 2))
    print("Mín claves:", math.ceil(m / 2) - 1)
    print("Grado mínimo interno usado por el algoritmo (t):", t)

    arbol = ArbolB(t)


    while True:
        print("\n1 Insertar")
        print("2 Eliminar")
        print("4 Salir")

        opcion = input("Opción: ")

        if opcion == "1":
            clave = int(input("Clave a insertar: "))
            arbol.insertar(clave)
            arbol.mostrarArbol()

        elif opcion == "2":
            clave = int(input("Clave a eliminar: "))
            arbol.eliminar(clave)
            arbol.mostrarArbol()

        elif opcion == "4":
            break

        else:
            print("Opción inválida")


if __name__ == "__main__":
    principal()