#!/usr/bin/env python3
"""
Menú interactivo para ejecutar los requerimientos funcionales (2 a 5).

Opciones:
1. Requerimiento 2 (Similitud textual)
2. Requerimiento 3 (Frecuencias y palabras asociadas)
3. Requerimiento 4 (Clustering jerárquico y dendrogramas)
4. Requerimiento 5 (Visualizaciones bibliométricas + PDF)
5. Salir
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

# Asegura que el directorio raíz del proyecto esté disponible en sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from req2 import req2 as req2_cli
from req3 import req3 as req3_cli


REQ4_CMD = [
    sys.executable,
    "req4/req4.py",
    "--entrada",
    "Data/unificados.bib",
    "--salida",
    "Data/visualizations/req4",
]

REQ5_CMD = [
    sys.executable,
    "req5/generate_visualizations.py",
    "--entrada",
    "Data/unificados.bib",
    "--salida",
    "Data/visualizations/req5",
]


def run_req2() -> None:
    """Ejecuta el menú del Requerimiento 2 (similitud textual)."""
    try:
        req2_cli.iniciar_menu()
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.")


def run_req3() -> None:
    """Ejecuta el menú del Requerimiento 3 (frecuencias y palabras asociadas)."""
    try:
        req3_cli.iniciar_menu()
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.")


def run_command(cmd: list[str]) -> None:
    """Ejecuta un comando externo e informa el resultado."""
    print(f"\nEjecutando: {' '.join(cmd)}\n")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        print("\n⚠️  El comando finalizó con errores.")
        print(exc)
    else:
        print("\n✅ Proceso completado.\n")


def pedir_max_articulos() -> list[str]:
    """Pregunta al usuario si desea limitar la cantidad de artículos."""
    value = input("¿Deseas limitar la cantidad de artículos? (dejar vacío para usar todos): ").strip()
    if value.isdigit():
        return ["--max-articulos", value]
    return []


def menu() -> None:
    """Bucle principal del menú."""
    opciones = {
        "1": ("Requerimiento 2 (Similitud textual)", "func", run_req2),
        "2": ("Requerimiento 3 (Frecuencias y palabras asociadas)", "func", run_req3),
        "3": ("Requerimiento 4 (Clustering jerárquico)", "cmd", REQ4_CMD, True),
        "4": ("Requerimiento 5 (Visualizaciones bibliométricas)", "cmd", REQ5_CMD, True),
        "5": ("Salir", "exit"),
    }

    while True:
        print("\n=== MENÚ DE REQUERIMIENTOS ===")
        for clave, (descripcion, *_) in opciones.items():
            print(f"{clave}. {descripcion}")

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion not in opciones:
            print("Opción inválida, intenta nuevamente.")
            continue

        descripcion, tipo, *datos = opciones[opcion]

        if tipo == "exit":
            print("Hasta pronto 👋")
            break

        if tipo == "func":
            funcion = datos[0]
            funcion()
        elif tipo == "cmd":
            cmd_base = datos[0]
            admite_max = datos[1]
            extra = pedir_max_articulos() if admite_max else []
            run_command(cmd_base + extra)


if __name__ == "__main__":
    menu()

