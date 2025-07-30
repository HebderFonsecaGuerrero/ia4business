import os
from typing import Dict

# Este script permite modificar un glosario almacenado en un PDF.
# Se necesitan las librerías PyPDF2 para leer el documento y fpdf para escribirlo.

try:
    from PyPDF2 import PdfReader
    from fpdf import FPDF
except ImportError as e:
    print("Faltan dependencias para ejecutar este programa:", e)
    print("Instale PyPDF2 y fpdf para poder continuar.")
    raise


def cargar_glosario(ruta_pdf: str) -> Dict[str, str]:
    """Extrae el glosario de un PDF en un diccionario."""
    glosario = {}
    with open(ruta_pdf, "rb") as f:
        reader = PdfReader(f)
        texto = "\n".join(page.extract_text() or "" for page in reader.pages)
    for linea in texto.splitlines():
        if ':' in linea:
            concepto, definicion = linea.split(':', 1)
            glosario[concepto.strip()] = definicion.strip()
        elif '-' in linea:
            concepto, definicion = linea.split('-', 1)
            glosario[concepto.strip()] = definicion.strip()
    return glosario


def guardar_glosario(glosario: Dict[str, str], ruta_pdf: str) -> None:
    """Guarda el glosario ordenado alfabéticamente en un PDF."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for concepto, definicion in sorted(glosario.items()):
        linea = f"{concepto}: {definicion}"
        pdf.multi_cell(0, 10, linea)
    pdf.output(ruta_pdf)


def main():
    ruta_original = input("Ruta del PDF original: ").strip()
    if not os.path.exists(ruta_original):
        print("No se encontró el archivo especificado.")
        return
    glosario = cargar_glosario(ruta_original)

    accion = input("¿Desea incluir, modificar o borrar un concepto? ").strip().lower()
    if accion.startswith("inclu"):
        concepto = input("Concepto nuevo: ").strip()
        definicion = input("Definición: ").strip()
        glosario[concepto] = definicion
    elif accion.startswith("bor"):
        concepto = input("¿Qué concepto desea borrar?: ").strip()
        if concepto in glosario:
            confirm = input(f"¿Está seguro de borrar '{concepto}'? (s/n): ").lower()
            if confirm == 's':
                del glosario[concepto]
        else:
            print("Concepto no encontrado.")
    elif accion.startswith("modifi"):
        concepto = input("¿Qué concepto desea modificar?: ").strip()
        if concepto in glosario:
            print(f"Definición actual: {glosario[concepto]}")
            definicion = input("Nueva definición: ").strip()
            glosario[concepto] = definicion
        else:
            print("Concepto no encontrado.")
    else:
        print("Acción no reconocida.")
        return

    ruta_nuevo_pdf = input("Ruta para guardar el nuevo PDF: ").strip()
    guardar_glosario(glosario, ruta_nuevo_pdf)
    print("Glosario guardado correctamente.")


if __name__ == "__main__":
    main()
