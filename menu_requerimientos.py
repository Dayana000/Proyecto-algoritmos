#!/usr/bin/env python3
"""
Menú interactivo para ejecutar los requerimientos disponibles.

Opciones actuales:
1. Requerimiento 4 (clustering jerárquico y dendrogramas)
2. Requerimiento 5 (visualizaciones bibliométricas + PDF)
3. Salir
"""

from __future__ import annotations

import subprocess
import sys


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


def run_command(cmd: list[str]) -> None:
    print(f"\nEjecutando: {' '.join(cmd)}\n")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        print("\n⚠️  El comando finalizó con errores.")
        print(exc)
    else:
        print("\n✅ Proceso completado.\n")


def pedir_max_articulos() -> list[str]:
    value = input("¿Deseas limitar la cantidad de artículos? (dejar vacío para usar todos): ").strip()
    if value.isdigit():
        return ["--max-articulos", value]
    return []


def menu() -> None:
    while True:
        print("\n=== MENÚ DE REQUERIMIENTOS ===")
        print("1. Requerimiento 4 (Clustering jerárquico)")
        print("2. Requerimiento 5 (Visualizaciones bibliométricas)")
        print("3. Salir")
        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            extra = pedir_max_articulos()
            run_command(REQ4_CMD + extra)
        elif opcion == "2":
            extra = pedir_max_articulos()
            run_command(REQ5_CMD + extra)
        elif opcion == "3":
            print("Hasta pronto 👋")
            break
        else:
            print("Opción inválida, intenta nuevamente.")


if __name__ == "__main__":
    menu()

