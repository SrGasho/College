# Calculadora con árbol binario

Calculadora web en Python que construye un árbol binario de expresión y evalúa sus operaciones mediante recorrido postorden.

## Ejecución

```bash
python3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv/bin/python app.py
```

Después abre `http://127.0.0.1:5000` en el navegador.

También se puede probar el núcleo desde la terminal:

```bash
python3 main.py "8 + 3 * (4 - 1)"
```

La aplicación soporta `+`, `-`, `*`, `/`, paréntesis y números decimales. No utiliza `eval()` y rechaza la división entre cero.
