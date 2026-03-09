#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para convertir el archivo de preguntas AWS del formato TXT al formato JSON
"""

import re
import json

def limpiar_texto(texto):
    """Limpia el texto eliminando espacios extra y saltos de línea innecesarios"""
    return ' '.join(texto.split()).strip()

def parsear_preguntas(archivo_entrada):
    """
    Lee y parsea el archivo de preguntas, extrayendo cada pregunta con sus componentes
    """
    with open(archivo_entrada, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    preguntas = []
    
    # Dividir el contenido por el patrón de pregunta
    patron_pregunta = r'PREGUNTA N\.o:?\s*(\d+)'
    partes = re.split(patron_pregunta, contenido)
    
    # La primera parte antes del primer split no contiene pregunta útil
    for i in range(1, len(partes), 2):
        if i + 1 >= len(partes):
            break
            
        id_pregunta = int(partes[i])
        texto_pregunta = partes[i + 1]
        
        # Parsear esta pregunta
        pregunta_obj = parsear_pregunta_individual(id_pregunta, texto_pregunta)
        if pregunta_obj:
            preguntas.append(pregunta_obj)
    
    return preguntas

def parsear_pregunta_individual(id_pregunta, texto):
    """
    Parsea una pregunta individual extrayendo todos sus componentes
    """
    lineas = texto.split('\n')
    
    pregunta_texto = []
    opciones = {}
    respuesta = None
    explicacion = None
    referencia = None
    
    estado = 'pregunta'  # Estados: pregunta, opciones, respuesta, explicacion, referencia
    opcion_actual = None
    opcion_texto = []
    
    for linea in lineas:
        linea = linea.strip()
        
        # Ignorar líneas vacías y líneas de encabezado/pie
        if not linea or 'Liderando el camino' in linea or 'www.testking.com' in linea:
            continue
        if 'Amazon AWS Certified Cloud Practitioner' in linea or 'CLF-C02 Exam' in linea:
            continue
        
        # Detectar inicio de opciones
        if re.match(r'^[A-E]\.$', linea.strip()):
            # Guardar opción anterior si existe
            if opcion_actual and opcion_texto:
                opciones[opcion_actual] = limpiar_texto(' '.join(opcion_texto))
            
            opcion_actual = linea.strip()[0]  # A, B, C, D o E
            opcion_texto = []
            estado = 'opciones'
            continue
        
        # Detectar respuesta
        if linea.startswith('Respuesta:'):
            # Guardar última opción
            if opcion_actual and opcion_texto:
                opciones[opcion_actual] = limpiar_texto(' '.join(opcion_texto))
                opcion_actual = None
                opcion_texto = []
            
            respuesta = linea.replace('Respuesta:', '').strip()
            estado = 'respuesta'
            continue
        
        # Detectar explicación
        if linea.startswith('Explicación:'):
            explicacion = linea.replace('Explicación:', '').strip()
            estado = 'explicacion'
            continue
        
        # Detectar referencia
        if linea.startswith('Referencia:') or re.match(r'^https?://', linea):
            if linea.startswith('Referencia:'):
                referencia = linea.replace('Referencia:', '').strip()
            else:
                referencia = linea.strip()
            estado = 'referencia'
            continue
        
        # Agregar contenido según el estado actual
        if estado == 'pregunta':
            pregunta_texto.append(linea)
        elif estado == 'opciones' and opcion_actual:
            opcion_texto.append(linea)
        elif estado == 'explicacion':
            if explicacion:
                explicacion += ' ' + linea
            else:
                explicacion = linea
        elif estado == 'referencia':
            if referencia:
                referencia += ' ' + linea
            else:
                referencia = linea
    
    # Guardar última opción si existe
    if opcion_actual and opcion_texto:
        opciones[opcion_actual] = limpiar_texto(' '.join(opcion_texto))
    
    # Construir el objeto de pregunta
    if pregunta_texto and opciones and respuesta:
        pregunta_obj = {
            'id': id_pregunta,
            'pregunta': limpiar_texto(' '.join(pregunta_texto)),
            'opciones': opciones,
            'respuesta_correcta': respuesta,
            'explicacion': limpiar_texto(explicacion) if explicacion else None,
            'referencia': limpiar_texto(referencia) if referencia else None
        }
        return pregunta_obj
    
    return None

def convertir_a_json(archivo_entrada, archivo_salida):
    """
    Función principal que convierte el archivo TXT a JSON
    """
    print(f"Leyendo archivo: {archivo_entrada}")
    preguntas = parsear_preguntas(archivo_entrada)
    
    print(f"Se encontraron {len(preguntas)} preguntas")
    
    # Guardar en JSON
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        json.dump(preguntas, f, ensure_ascii=False, indent=2)
    
    print(f"Archivo JSON guardado en: {archivo_salida}")
    
    # Mostrar estadísticas
    con_explicacion = sum(1 for p in preguntas if p['explicacion'])
    con_referencia = sum(1 for p in preguntas if p['referencia'])
    
    print(f"\nEstadisticas:")
    print(f"  - Total de preguntas: {len(preguntas)}")
    print(f"  - Con explicacion: {con_explicacion}")
    print(f"  - Con referencia: {con_referencia}")

if __name__ == '__main__':
    archivo_entrada = 'AWSCertifiedCloudPractitionerCLF-C02___699preguntas_limpio.txt'
    archivo_salida = 'preguntas_aws.json'
    
    try:
        convertir_a_json(archivo_entrada, archivo_salida)
        print("\n[OK] Conversion completada exitosamente!")
    except Exception as e:
        print(f"\n[ERROR] Error durante la conversion: {e}")
        import traceback
        traceback.print_exc()