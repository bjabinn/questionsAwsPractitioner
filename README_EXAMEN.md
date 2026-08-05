# 📚 Aplicación de Examen de Certificaciones

Aplicación interactiva de Streamlit para realizar exámenes de preparación para certificaciones
técnicas (AWS y otras que se vayan añadiendo).

## ✨ Características

- **Múltiples certificaciones**: elige de un desplegable qué certificación quieres practicar
- **Personalización del examen**: Elige el número de preguntas y el tiempo por pregunta
- **Navegación intuitiva**: Botones para avanzar y retroceder entre preguntas
- **Mapa de preguntas**: Visualiza qué preguntas has respondido y navega directamente a cualquier pregunta
- **Temporizador**: Contador de tiempo por pregunta
- **Evaluación detallada**: Revisa tus respuestas con explicación de correctas e incorrectas
- **Interfaz moderna**: Diseño limpio y fácil de usar

## 🚀 Instalación

1. Asegúrate de tener Python 3.7+ instalado

2. Instala Streamlit si no lo tienes:
```bash
pip install streamlit
```

## 🎮 Cómo usar

1. Ejecuta la aplicación:
```bash
streamlit run app_examen.py
```

2. En la pantalla de configuración:
   - Elige la certificación en el desplegable
   - Selecciona el número de preguntas que deseas (según las disponibles para esa certificación)
   - El tiempo total se calculará automáticamente según la fórmula: (preguntas / 65) × 90 minutos
   - Por ejemplo: 65 preguntas = 90 minutos (~1min 23seg por pregunta)
   - Haz clic en "Comenzar Examen"

3. Durante el examen:
   - Lee cada pregunta cuidadosamente
   - Selecciona la respuesta haciendo clic en el botón correspondiente
   - Usa los botones "Anterior" y "Siguiente" para navegar entre preguntas
   - Monitorea el temporizador en la esquina superior derecha
   - Usa el "Mapa de Preguntas" para saltar a cualquier pregunta específica
   - Las preguntas respondidas se marcan con ✅
   - Las preguntas sin responder se marcan con ⭕

4. Finalizar el examen:
   - Haz clic en "Finalizar Examen" cuando hayas terminado
   - Revisa tus resultados
   - Analiza cada pregunta con las respuestas correctas e incorrectas

5. Después del examen:
   - Puedes realizar un nuevo examen con preguntas diferentes
   - O cambiar la configuración para ajustar el número de preguntas y tiempo

## 📊 Evaluación

- La nota de corte para aprobar depende de la certificación (definida en su fichero JSON, por
  defecto 70%)
- Verás un desglose completo de:
  - Respuestas correctas vs incorrectas
  - Porcentaje de aciertos
  - Revisión detallada de cada pregunta con la respuesta correcta marcada

## 📁 Archivos del proyecto

- `app_examen.py`: Aplicación principal de Streamlit
- `preguntas/`: Carpeta con un fichero JSON por certificación (ver "Añadir una certificación nueva")
- `convertir_a_json.py` / `limpiar_examen_aws.py`: Utilidades para generar un fichero de
  `preguntas/` a partir de un dump de texto
- `README_EXAMEN.md`: Este archivo de documentación

## ➕ Añadir una certificación nueva

No hace falta tocar el código de la app. Solo hay que crear un fichero JSON dentro de `preguntas/`
con este esquema:

```json
{
  "certificacion": {
    "id": "mi-cert",
    "nombre": "Nombre de la certificación",
    "codigo": "COD-01",
    "nota_corte": 70
  },
  "preguntas": [
    {
      "id": 1,
      "pregunta": "Texto de la pregunta",
      "opciones": {"A": "...", "B": "...", "C": "...", "D": "..."},
      "respuesta_correcta": "B",
      "explicacion": null,
      "referencia": null
    }
  ]
}
```

Para preguntas de respuesta múltiple, `respuesta_correcta` va con las letras separadas por coma
(ej. `"B,D"`).

Al reiniciar la app (o refrescar si el fichero se añadió con la app ya abierta), la nueva
certificación aparece automáticamente en el desplegable.

Si el origen de las preguntas es un dump de texto similar al de AWS, puedes reutilizar el pipeline:
1. `python limpiar_examen_aws.py` (ajustando el nombre de fichero de entrada dentro del script)
2. `python convertir_a_json.py entrada_limpio.txt preguntas/mi_cert.json --id mi-cert --nombre "Mi Certificación" --codigo COD-01 --nota-corte 70`

## 🎯 Consejos para el examen

1. **Lee cuidadosamente**: Cada pregunta debe leerse completamente antes de responder
2. **Gestiona tu tiempo**: 
   - El tiempo se calcula automáticamente (~1min 23seg por pregunta)
   - Para 65 preguntas: 90 minutos totales
   - Para 90 preguntas: ~125 minutos totales
3. **Revisa antes de finalizar**: Usa el mapa de preguntas para revisar las que dejaste sin responder
4. **Aprende de los errores**: Después del examen, revisa detenidamente las respuestas incorrectas

## 🔧 Personalización

- Cambiar el umbral de aprobación de una certificación: edita `nota_corte` en su fichero JSON
  dentro de `preguntas/` (no requiere tocar código)
- Modificar los colores y estilos, la fórmula de cálculo de tiempo (actualmente: preguntas/65 × 90
  minutos) o los mensajes de retroalimentación: edita `app_examen.py`

## 📝 Notas

- Las preguntas se seleccionan aleatoriamente de la certificación elegida cada vez que inicias un nuevo examen
- El tiempo total se calcula según: **(preguntas / 65) × 90 minutos**
- El temporizador por pregunta se calcula dividiendo el tiempo total entre el número de preguntas
- El temporizador se reinicia al navegar entre preguntas
- Tus respuestas se guardan automáticamente al hacer clic en una opción
- **Número de preguntas por defecto**: 65 preguntas = 90 minutos de examen

## 🆘 Soporte

Si encuentras algún problema o tienes sugerencias, por favor revisa el código en `app_examen.py` o consulta la documentación de Streamlit en https://docs.streamlit.io

## 📜 Licencia

Este proyecto es solo para fines educativos y de preparación para la certificación AWS Cloud Practitioner.

---

**¡Buena suerte con tu preparación para la certificación AWS Cloud Practitioner! ☁️🚀**