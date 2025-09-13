#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instalador Automático de Dependencias
Para el Analizador OCR Universal
"""

import subprocess
import sys
import os
import tkinter as tk
from tkinter import messagebox
import importlib.util
import urllib.request
import tempfile

class InstaladorDependencias:
    def __init__(self):
        self.dependencias_python = [
            ('PyPDF2', 'PyPDF2'),
            ('openpyxl', 'openpyxl'), 
            ('pytesseract', 'pytesseract'),
            ('pdf2image', 'pdf2image'),
            ('Pillow', 'PIL'),
            ('pandas', 'pandas')
        ]
        
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Rutas para herramientas incluidas en el proyecto (autónomas)
        self.tesseract_portable = os.path.join(self.script_dir, 'tesseract', 'tesseract.exe')
        self.tessdata_path = os.path.join(self.script_dir, 'tessdata')
        self.poppler_path = os.path.join(self.script_dir, 'poppler', 'Library', 'bin')
        
        # Rutas de sistema como fallback
        self.rutas_tesseract_sistema = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            r"C:\Tesseract-OCR\tesseract.exe"
        ]

    def instalar_tesseract_automatico(self):
        """Descarga e instala Tesseract OCR automáticamente"""
        print("🔄 Descargando Tesseract OCR...")
        
        # URL del instalador oficial de Tesseract
        tesseract_url = "https://github.com/UB-Mannheim/tesseract/releases/download/v5.4.0.20240606/tesseract-ocr-w64-setup-5.4.0.20240606.exe"
        
        try:
            # Crear directorio temporal
            with tempfile.TemporaryDirectory() as temp_dir:
                installer_path = os.path.join(temp_dir, "tesseract_installer.exe")
                
                # Descargar instalador
                print("📥 Descargando instalador desde GitHub...")
                urllib.request.urlretrieve(tesseract_url, installer_path)
                
                if not os.path.exists(installer_path):
                    print("❌ Error: No se pudo descargar el instalador")
                    return False
                
                print("✅ Instalador descargado correctamente")
                
                # Mostrar diálogo de confirmación
                root = tk.Tk()
                root.withdraw()
                
                respuesta = messagebox.askyesno(
                    "Instalar Tesseract OCR",
                    "Se ha descargado el instalador oficial de Tesseract OCR.\n\n" +
                    "¿Desea ejecutar la instalación?\n\n" +
                    "IMPORTANTE: Se requerirán permisos de administrador.",
                    icon='question'
                )
                
                root.destroy()
                
                if not respuesta:
                    print("❌ Instalación cancelada por el usuario")
                    return False
                
                # Ejecutar instalador
                print("🔧 Ejecutando instalador de Tesseract...")
                print("   (Se abrirá ventana de instalación)")
                
                resultado = subprocess.run([
                    installer_path,
                    "/S",  # Instalación silenciosa
                    "/D=C:\\Program Files\\Tesseract-OCR"  # Directorio de instalación
                ], capture_output=False)
                
                if resultado.returncode == 0:
                    print("✅ Tesseract OCR instalado correctamente")
                    
                    # Verificar instalación
                    if self.verificar_tesseract()[0]:
                        print("✅ Instalación verificada exitosamente")
                        return True
                    else:
                        print("⚠️ Instalación completada pero no se puede verificar")
                        return False
                else:
                    print(f"❌ Error en instalación (código: {resultado.returncode})")
                    return False
                    
        except Exception as e:
            print(f"❌ Error instalando Tesseract: {e}")
            return False

    def verificar_python_packages(self):
        """Verifica qué paquetes de Python están instalados"""
        faltantes = []
        instalados = []
        
        for nombre_pip, nombre_import in self.dependencias_python:
            try:
                spec = importlib.util.find_spec(nombre_import)
                if spec is not None:
                    instalados.append(nombre_pip)
                else:
                    faltantes.append(nombre_pip)
            except ImportError:
                faltantes.append(nombre_pip)
        
        return instalados, faltantes

    def verificar_tesseract(self):
        """Verifica si Tesseract está disponible (portable o sistema)"""
        
        # Primero verificar la versión portable incluida en el proyecto
        if os.path.exists(self.tesseract_portable):
            return True, self.tesseract_portable
        
        # Si no existe la portable, buscar en el sistema
        for ruta in self.rutas_tesseract_sistema:
            if os.path.exists(ruta):
                return True, ruta
                
        return False, None

    def verificar_tessdata(self):
        """Verifica si están los archivos de idioma español"""
        spa_file = os.path.join(self.tessdata_path, 'spa.traineddata')
        eng_file = os.path.join(self.tessdata_path, 'eng.traineddata')
        
        return {
            'spa': os.path.exists(spa_file),
            'eng': os.path.exists(eng_file),
            'tessdata_exists': os.path.exists(self.tessdata_path)
        }

    def verificar_poppler(self):
        """Verifica si Poppler está disponible"""
        return os.path.exists(self.poppler_path)

    def instalar_packages_python(self, packages):
        """Instala paquetes de Python usando pip"""
        resultados = []
        
        for package in packages:
            try:
                print(f"🔄 Instalando {package}...")
                resultado = subprocess.run([
                    sys.executable, "-m", "pip", "install", package
                ], capture_output=True, text=True, check=True)
                
                resultados.append((package, True, "Instalado correctamente"))
                print(f"✅ {package} instalado correctamente")
                
            except subprocess.CalledProcessError as e:
                resultados.append((package, False, f"Error: {e.stderr}"))
                print(f"❌ Error instalando {package}: {e.stderr}")
        
        return resultados

    def verificacion_completa(self):
        """Realiza verificación completa del sistema"""
        print("🔍 VERIFICACIÓN COMPLETA DEL SISTEMA")
        print("=" * 50)
        
        # Python packages
        instalados, faltantes = self.verificar_python_packages()
        print(f"\n📦 PAQUETES PYTHON:")
        for pkg in instalados:
            print(f"  ✅ {pkg}")
        for pkg in faltantes:
            print(f"  ❌ {pkg} (FALTANTE)")
        
        # Tesseract
        tesseract_ok, tesseract_path = self.verificar_tesseract()
        print(f"\n🔧 TESSERACT OCR:")
        if tesseract_ok:
            print(f"  ✅ Encontrado en: {tesseract_path}")
        else:
            print(f"  ❌ NO ENCONTRADO")
        
        # Tessdata
        tessdata_info = self.verificar_tessdata()
        print(f"\n📚 ARCHIVOS DE IDIOMA:")
        print(f"  {'✅' if tessdata_info['tessdata_exists'] else '❌'} Carpeta tessdata")
        print(f"  {'✅' if tessdata_info['spa'] else '❌'} Español (spa.traineddata)")
        print(f"  {'✅' if tessdata_info['eng'] else '❌'} Inglés (eng.traineddata)")
        
        # Poppler
        poppler_ok = self.verificar_poppler()
        print(f"\n🖼️ POPPLER (PDF a imagen):")
        print(f"  {'✅' if poppler_ok else '❌'} {'Disponible' if poppler_ok else 'NO ENCONTRADO'}")
        
        return {
            'python_faltantes': faltantes,
            'tesseract_ok': tesseract_ok,
            'tesseract_path': tesseract_path,
            'tessdata_info': tessdata_info,
            'poppler_ok': poppler_ok
        }

    def mostrar_dialogo_instalacion(self, verificacion):
        """Muestra diálogo para confirmar instalación"""
        if not verificacion['python_faltantes'] and verificacion['tesseract_ok'] and verificacion['tessdata_info']['spa'] and verificacion['tessdata_info']['eng']:
            return True  # Todo está bien
        
        # Crear ventana de diálogo
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana principal
        
        mensaje = "🔧 INSTALACIÓN REQUERIDA\n\n"
        mensaje += "Se detectaron dependencias faltantes:\n\n"
        
        if verificacion['python_faltantes']:
            mensaje += f"📦 Paquetes Python faltantes:\n"
            for pkg in verificacion['python_faltantes']:
                mensaje += f"   • {pkg}\n"
            mensaje += "\n"
        
        if not verificacion['tesseract_ok']:
            mensaje += "🔧 Tesseract OCR no encontrado\n"
            mensaje += "   (Se descargará e instalará automáticamente)\n\n"
        
        if not verificacion['tessdata_info']['spa']:
            mensaje += "📚 Archivo de idioma español faltante\n\n"
        
        mensaje += "¿Desea proceder con la instalación automática?"
        
        respuesta = messagebox.askyesno(
            "Instalación Requerida", 
            mensaje,
            icon='question'
        )
        
        root.destroy()
        return respuesta

    def instalar_automatico(self, modo_auto=False):
        """Proceso completo de instalación automática"""
        print("🚀 INICIANDO INSTALACIÓN AUTOMÁTICA")
        print("=" * 50)
        
        verificacion = self.verificacion_completa()
        
        # Solo instalar paquetes Python faltantes y Tesseract si es necesario
        instalacion_exitosa = True
        
        if verificacion['python_faltantes'] or not verificacion['tesseract_ok']:
            if modo_auto:
                # Instalación automática sin diálogos
                print("🔄 Modo automático activado - procediendo sin confirmación...")
                confirmar = True
            else:
                confirmar = self.mostrar_dialogo_instalacion(verificacion)
                
            if not confirmar:
                print("❌ Instalación cancelada por el usuario")
                return False
            
            # Instalar paquetes Python faltantes
            if verificacion['python_faltantes']:
                print(f"\n🔄 Instalando {len(verificacion['python_faltantes'])} paquetes Python...")
                resultados = self.instalar_packages_python(verificacion['python_faltantes'])
                
                exitosos = sum(1 for _, exito, _ in resultados if exito)
                print(f"\n📊 RESULTADOS PYTHON: {exitosos}/{len(resultados)} paquetes instalados")
                
                if exitosos != len(resultados):
                    instalacion_exitosa = False
            
            # Instalar Tesseract si falta
            if not verificacion['tesseract_ok']:
                print(f"\n🔧 Instalando Tesseract OCR...")
                if self.instalar_tesseract_automatico():
                    print("✅ Tesseract OCR instalado correctamente")
                else:
                    print("❌ Error instalando Tesseract OCR")
                    instalacion_exitosa = False
        
        if instalacion_exitosa:
            print("✅ ¡Instalación completada exitosamente!")
        else:
            print("⚠️ Algunas instalaciones no se completaron correctamente")
        
        return instalacion_exitosa

def main():
    """Función principal"""
    instalador = InstaladorDependencias()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--verificar':
        # Solo verificar
        instalador.verificacion_completa()
    elif len(sys.argv) > 1 and sys.argv[1] == '--auto':
        # Instalación automática sin diálogos
        instalador.instalar_automatico(modo_auto=True)
    else:
        # Instalación automática con diálogos
        instalador.instalar_automatico(modo_auto=False)

if __name__ == "__main__":
    main()