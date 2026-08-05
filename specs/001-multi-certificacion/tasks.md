# Tasks: Feature 001 - Soporte multi-certificación

- [x] T1. Crear carpeta `preguntas/` y fijar el esquema (metadata + preguntas) — ver `spec.md`
- [x] T2. Migrar `preguntas_aws.json` → `preguntas/aws_clf_c02.json` (copia literal envuelta en el
      nuevo esquema, sin transformar texto)
- [x] T3. Refactorizar `app_examen.py`: `descubrir_certificaciones()` + `st.selectbox` en la
      pantalla de configuración
- [x] T4. Parametrizar `cargar_preguntas(ruta)` por fichero/ruta seleccionada (cache por ruta)
- [x] T5. Nota de corte dinámica (`st.session_state.nota_corte`) en vez de `70` hardcodeado
- [x] T6. Generalizar textos/títulos de la UI para que no sean específicos de AWS
- [x] T7. Generalizar `convertir_a_json.py` (parámetros CLI + escritura del nuevo esquema)
- [x] T8. Actualizar `README_EXAMEN.md` (estructura `preguntas/` + cómo añadir una certificación)
- [x] T9. Eliminar `preguntas_aws.json` suelto del repo tras validar la migración
- [x] T10. Prueba manual end-to-end: lanzado `streamlit run app_examen.py` con Streamlit
      (Python 3.11) y pilotado con Chrome. Verificado: selectbox con AWS CLF-C02, examen completo,
      resultados con 100% de nota, título dinámico en examen/resultados. Añadida una segunda
      certificación de prueba (`nota_corte: 50`) en `preguntas/`: apareció en el selectbox, se
      pudo completar un examen y la pantalla de resultados aplicó correctamente el 50% de corte
      ("No Aprobado - 50.0%" / "Necesitas superar el 50%").

## Hallazgos durante la validación (no en el alcance original, pendientes de decisión)

- **Bug de descubrimiento con caché**: `descubrir_certificaciones()` estaba cacheada con
  `@st.cache_data` sin TTL, por lo que una certificación añadida en caliente no aparecía sin
  reiniciar el servidor. Corregido añadiendo `ttl=30` para que se refresque sola.
- **Datos con doble codificación UTF-8 preexistente**: ya presente en el `preguntas_aws.json`
  original (no introducido por esta migración). Se corrigió con un script puntual (`ftfy.fix_encoding`,
  ejecutado y luego eliminado) el caso mecánico de doble-codificación UTF-8 en 34 campos
  (ej. "automÃ¡ticamente" -> "automática mente") de `preguntas/aws_clf_c02.json`.
  Quedan **31 preguntas con un patrón de corrupción distinto y no mecánico** (ej. "múltiples" ->
  "mÃoltiples": la "ú" fue sustituida por "Ã"+"o", no es un simple problema de encoding) que no es
  seguro corregir automáticamente sin arriesgar introducir texto incorrecto en preguntas de examen
  real. Requeriría revisión manual contra el PDF/DOCX original si se quiere resolver del todo.
