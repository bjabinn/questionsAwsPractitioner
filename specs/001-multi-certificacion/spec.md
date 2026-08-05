# Feature 001: Soporte multi-certificación

## Contexto

La app (`app_examen.py`) solo soporta AWS Cloud Practitioner: carga `preguntas_aws.json` con una
ruta fija, y tiene hardcodeados el título, la nota de corte (70%) y los textos de la UI. Queremos
poder añadir preguntas de otras certificaciones (ej. AWS Solutions Architect, Azure, GCP...) sin
tocar código, con un desplegable para elegir la certificación antes de configurar el examen.

## Requisitos

1. **Almacenamiento por certificación**: cada certificación vive en su propio fichero JSON dentro
   de `preguntas/`, autodescriptivo (incluye su propia metadata). Añadir una certificación nueva es
   soltar un fichero con el esquema correcto en esa carpeta — no requiere editar ningún registro
   central ni el código de la app.

   Esquema:
   ```json
   {
     "certificacion": {
       "id": "aws-clf-c02",
       "nombre": "AWS Certified Cloud Practitioner",
       "codigo": "CLF-C02",
       "nota_corte": 70
     },
     "preguntas": [
       {"id": 1, "pregunta": "...", "opciones": {"A": "...", "B": "..."}, "respuesta_correcta": "B", "explicacion": null, "referencia": null}
     ]
   }
   ```

2. **Descubrimiento automático**: la app escanea `preguntas/*.json` al arrancar y construye la
   lista de certificaciones disponibles a partir de la clave `certificacion` de cada fichero.

3. **Selector**: pantalla de configuración muestra un `st.selectbox` con las certificaciones
   descubiertas (ordenadas por nombre), antes de elegir el número de preguntas. El límite máximo
   de preguntas y el tiempo estimado se recalculan según la certificación elegida.

4. **Nota de corte dinámica**: el % necesario para aprobar viene de `certificacion.nota_corte` del
   fichero elegido (ya no un `70` fijo en el código).

5. **UI genérica**: título de página, cabeceras y textos dejan de referirse solo a "AWS" y pasan a
   mostrar el nombre de la certificación activa.

6. **Migración de datos**: `preguntas_aws.json` se traslada a `preguntas/aws_clf_c02.json` con el
   nuevo esquema, copiando el array de preguntas tal cual (ya está en UTF-8 correcto en disco, no
   requiere ninguna transformación de texto). El fichero suelto original se elimina tras validar.

7. **Pipeline de generación reutilizable**: `convertir_a_json.py` (que convierte un dump de texto a
   JSON) se generaliza para aceptar parámetros por CLI (fichero de entrada, fichero de salida en
   `preguntas/`, metadata de la certificación) y escribir directamente el nuevo esquema, para poder
   reutilizarse con futuras certificaciones que vengan de un dump de texto similar.

## Fuera de alcance

- No se corrige ningún problema de codificación real (no lo había: era solo la consola de Windows
  mostrando mal los acentos al depurar).
- No se implementa un registro central de certificaciones — el descubrimiento es siempre por
  escaneo de carpeta.
- No se migra el pipeline de limpieza (`limpiar_examen_aws.py`) — sigue siendo un paso manual previo
  específico del formato de origen de cada certificación.

## Criterios de aceptación

- Con solo `preguntas/aws_clf_c02.json` presente, la app funciona exactamente igual que antes
  (mismo comportamiento, mismo 70% de corte), pero mostrando el nombre de la certificación en la UI.
- Al añadir un segundo fichero JSON válido en `preguntas/`, aparece automáticamente como opción en
  el desplegable sin reiniciar código ni tocar `app_examen.py`.
- Si esa segunda certificación tiene una `nota_corte` distinta de 70, la pantalla de resultados usa
  esa nota, no 70.
