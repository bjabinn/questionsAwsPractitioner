# 📚 Aplicación de Examen AWS Cloud Practitioner

Aplicación interactiva de Streamlit para realizar exámenes de preparación para la certificación AWS Cloud Practitioner.

## ✨ Características

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
   - Selecciona el número de preguntas que deseas (de 1 hasta 699 preguntas disponibles)
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

- Necesitas un 70% o más para aprobar
- Verás un desglose completo de:
  - Respuestas correctas vs incorrectas
  - Porcentaje de aciertos
  - Revisión detallada de cada pregunta con la respuesta correcta marcada

## 📁 Archivos del proyecto

- `app_examen.py`: Aplicación principal de Streamlit
- `preguntas_aws.json`: Base de datos con 699 preguntas de AWS Cloud Practitioner
- `README_EXAMEN.md`: Este archivo de documentación

## 🎯 Consejos para el examen

1. **Lee cuidadosamente**: Cada pregunta debe leerse completamente antes de responder
2. **Gestiona tu tiempo**: 
   - El tiempo se calcula automáticamente (~1min 23seg por pregunta)
   - Para 65 preguntas: 90 minutos totales
   - Para 90 preguntas: ~125 minutos totales
3. **Revisa antes de finalizar**: Usa el mapa de preguntas para revisar las que dejaste sin responder
4. **Aprende de los errores**: Después del examen, revisa detenidamente las respuestas incorrectas

## 🔧 Personalización

Puedes modificar la aplicación editando `app_examen.py`:
- Cambiar el umbral de aprobación (actualmente >70%)
- Modificar los colores y estilos
- Ajustar la fórmula de cálculo de tiempo (actualmente: preguntas/65 × 90 minutos)
- Personalizar los mensajes de retroalimentación

## 📝 Notas

- Las preguntas se seleccionan aleatoriamente de la base de datos cada vez que inicias un nuevo examen
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