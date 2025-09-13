#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VERIFICADOR DE INSTALACIÓN - GUI ANALIZADOR OCR
Verifica que todas las dependencias estén correctamente instaladas
"""

import sys
import subprocess

def verificar_dependencia(nombre_modulo, nombre_display=None):
    """Verifica si un módulo de Python está instalado"""
    if nombre_display is None:
        nombre_display = nombre_modulo
    
    try:
        __import__(nombre_modulo)
        print(f"✅ {nombre_display}: INSTALADO")
        return True
    except ImportError:
        print(f"❌ {nombre_display}: NO INSTALADO")
        return False

def verificar_ejecutable(comando, nombre_display):
    """Verifica si un ejecutable está disponible en el PATH"""
    try:
        result = subprocess.run(comando, capture_output=True, text=True)
        print(f"✅ {nombre_display}: DISPONIBLE")
        return True
    except FileNotFoundError:
        print(f"❌ {nombre_display}: NO DISPONIBLE")
        return False

def main():
    print("="*50)
    print("🔍 VERIFICADOR DE INSTALACIÓN")
    print("GUI Analizador OCR - Memorias Legislatura Porteña")
    print("="*50)
    print()
    
    errores = 0
    
    print("📦 VERIFICANDO DEPENDENCIAS DE PYTHON:")
    print("-" * 40)
    
    dependencias = [
        ("tkinter", "Tkinter (GUI)"),
        ("PyPDF2", "PyPDF2"),
        ("openpyxl", "OpenPyXL"),
        ("PIL", "Pillow (PIL)"),
        ("pdf2image", "PDF2Image"),
        ("pytesseract", "PyTesseract"),
        ("pandas", "Pandas")
    ]
    
    for modulo, display in dependencias:
        if not verificar_dependencia(modulo, display):
            errores += 1
    
    print()
    print("🔧 VERIFICANDO HERRAMIENTAS EXTERNAS:")
    print("-" * 40)
    
    herramientas = [
        (["tesseract", "--version"], "Tesseract OCR"),
        (["pdftoppm", "-h"], "Poppler (PDF to Image)")
    ]
    
    for comando, display in herramientas:
        if not verificar_ejecutable(comando, display):
            errores += 1
    
    print()
    print("="*50)
    if errores == 0:
        print("🎉 TODAS LAS DEPENDENCIAS ESTÁN INSTALADAS CORRECTAMENTE")
        print("✅ El sistema está listo para ejecutar la GUI")
    else:
        print(f"⚠️  SE ENCONTRARON {errores} PROBLEMAS")
        print("❌ Algunas dependencias no están instaladas")
    print("="*50)
    print()
    
    # Configurar pytesseract si está disponible
    try:
        import pytesseract
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        print("🔧 Pytesseract configurado con la ruta de Tesseract")
    except ImportError:
        pass
    
    return errores == 0

if __name__ == "__main__":
    success = main()
    input("\nPresione Enter para continuar...")
    sys.exit(0 if success else 1)
