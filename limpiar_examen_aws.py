#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para limpiar el archivo de preguntas del examen AWS
Realiza las siguientes operaciones:
1. Elimina líneas vacías
2. Elimina líneas que contengan únicamente un número
3. Añade un salto de línea antes de "PREGUNTA N.o XX"
"""

import re
import sys


def detectar_codificacion(archivo):
    """
    Detecta la codificación del archivo probando varias codificaciones comunes.
    
    Args:
        archivo (str): Ruta del archivo
        
    Returns:
        str: La codificación detectada
    """
    codificaciones = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'utf-16']
    
    for encoding in codificaciones:
        try:
            with open(archivo, 'r', encoding=encoding) as f:
                f.read()
            return encoding
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    # Si ninguna funciona, usar latin-1 que acepta cualquier byte
    return 'latin-1'


def es_linea_solo_numero(linea):
    """
    Verifica si una línea contiene únicamente un número.
    
    Args:
        linea (str): La línea a verificar
        
    Returns:
        bool: True si la línea solo contiene un número, False en caso contrario
    """
    linea_limpia = linea.strip()
    # Verifica si la línea solo contiene dígitos y no está vacía
    return linea_limpia.isdigit() and len(linea_limpia) > 0


def es_pregunta(linea):
    """
    Verifica si una línea es una línea de pregunta (PREGUNTA N.o XX).
    
    Args:
        linea (str): La línea a verificar
        
    Returns:
        bool: True si la línea comienza con "PREGUNTA N.o", False en caso contrario
    """
    return linea.strip().startswith("PREGUNTA N.o") or linea.strip().startswith("PREGUNTA N.º")


def limpiar_archivo(archivo_entrada, archivo_salida=None):
    """
    Limpia el archivo de preguntas según las reglas especificadas.
    
    Args:
        archivo_entrada (str): Ruta del archivo a limpiar
        archivo_salida (str): Ruta del archivo de salida (opcional)
        
    Returns:
        dict: Estadísticas de la limpieza
    """
    if archivo_salida is None:
        # Si no se especifica archivo de salida, añadir "_limpio" antes de la extensión
        if archivo_entrada.endswith('.txt'):
            archivo_salida = archivo_entrada.replace('.txt', '_limpio.txt')
        else:
            archivo_salida = archivo_entrada + '_limpio.txt'
    
    # Detectar la codificación del archivo
    encoding = detectar_codificacion(archivo_entrada)
    print(f"Codificacion detectada: {encoding}")
    
    # Estadísticas
    stats = {
        'lineas_totales': 0,
        'lineas_vacias_eliminadas': 0,
        'numeros_eliminados': 0,
        'saltos_añadidos': 0,
        'lineas_finales': 0
    }
    
    try:
        # Leer el archivo con la codificación detectada
        with open(archivo_entrada, 'r', encoding=encoding) as f:
            lineas = f.readlines()
        
        stats['lineas_totales'] = len(lineas)
        
        # Procesar las líneas
        lineas_limpias = []
        linea_anterior_vacia = False
        
        for i, linea in enumerate(lineas):
            # Regla 1: Eliminar líneas vacías
            if linea.strip() == '':
                stats['lineas_vacias_eliminadas'] += 1
                linea_anterior_vacia = True
                continue
            
            # Regla 2: Eliminar líneas que solo contengan un número
            if es_linea_solo_numero(linea):
                stats['numeros_eliminados'] += 1
                continue
            
            # Regla 3: Añadir salto de línea antes de "PREGUNTA N.o XX"
            if es_pregunta(linea):
                # Solo añadir salto si la línea anterior no estaba vacía
                if lineas_limpias and not linea_anterior_vacia:
                    lineas_limpias.append('\n')
                    stats['saltos_añadidos'] += 1
            
            # Añadir la línea limpia
            lineas_limpias.append(linea)
            linea_anterior_vacia = False
        
        stats['lineas_finales'] = len(lineas_limpias)
        
        # Escribir el archivo limpio en UTF-8
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            f.writelines(lineas_limpias)
        
        return stats, archivo_salida
    
    except FileNotFoundError:
        print(f"ERROR: No se encontro el archivo '{archivo_entrada}'")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Error al procesar el archivo: {str(e)}")
        sys.exit(1)


def mostrar_estadisticas(stats, archivo_salida):
    """
    Muestra las estadísticas de la limpieza.
    
    Args:
        stats (dict): Diccionario con las estadísticas
        archivo_salida (str): Ruta del archivo de salida
    """
    print("\n" + "="*60)
    print("ESTADISTICAS DE LIMPIEZA")
    print("="*60)
    print(f"Lineas originales:           {stats['lineas_totales']:,}")
    print(f"Lineas vacias eliminadas:    {stats['lineas_vacias_eliminadas']:,}")
    print(f"Numeros eliminados:          {stats['numeros_eliminados']:,}")
    print(f"Saltos de linea añadidos:    {stats['saltos_añadidos']:,}")
    print(f"Lineas finales:              {stats['lineas_finales']:,}")
    print("="*60)
    print(f"Archivo guardado: {archivo_salida}")
    print("="*60 + "\n")


def main():
    """Función principal del script."""
    # Nombre del archivo a limpiar
    archivo_entrada = "AWSCertifiedCloudPractitionerCLF-C02___699preguntas.txt"
    
    print("\nIniciando limpieza del archivo de preguntas AWS...")
    print(f"Archivo de entrada: {archivo_entrada}")
    
    # Limpiar el archivo
    stats, archivo_salida = limpiar_archivo(archivo_entrada)
    
    # Mostrar estadísticas
    mostrar_estadisticas(stats, archivo_salida)
    
    print("Limpieza completada exitosamente!")


if __name__ == "__main__":
    main()