# 🚀 Guía para Conectar con GitHub y Desplegar en Streamlit.io

## 📋 Pasos para conectar con el repositorio GitHub

### 1️⃣ Inicializar Git y conectar con GitHub

Ejecuta los siguientes comandos **en orden** en tu terminal desde la carpeta `c:\dev\ProjectsPython\examenAWS`:

```bash
# 1. Inicializar el repositorio git local
git init

# 2. Añadir el repositorio remoto de GitHub
git remote add origin https://github.com/bjabinn/questionsAwsPractitioner.git

# 3. Descargar el contenido del repositorio (especialmente el README.md)
git fetch origin

# 4. Crear una rama main local si no existe
git branch -M main

# 5. Hacer merge del contenido remoto con el local (esto fusionará el README.md existente)
git pull origin main --allow-unrelated-histories

# 6. Añadir todos tus archivos al staging area
git add .

# 7. Hacer commit de tus cambios
git commit -m "Añadir aplicación de examen AWS Streamlit"

# 8. Subir los cambios a GitHub
git push -u origin main
```

### ⚠️ Nota sobre conflictos

Si hay conflictos con el README.md existente, Git te pedirá que los resuelvas. Tienes dos opciones:

**Opción A: Mantener tu README y el del repositorio**
```bash
# Si hay conflictos, puedes renombrar tu README antes de hacer merge
git mv README_EXAMEN.md README.md
git add README.md
git commit -m "Actualizar README con información del examen"
git push origin main
```

**Opción B: Usar solo tu README (reemplazar el existente)**
```bash
# Durante el merge, si hay conflictos:
git checkout --ours README.md  # Usa tu versión
git add README.md
git commit -m "Actualizar README con información del examen"
git push origin main
```

---

## 🌐 Desplegar en Streamlit.io

### Preparación previa

1. **Crear archivo requirements.txt** (ya debería existir):
```txt
streamlit
```

2. **Asegurarse de que estos archivos estén en el repositorio**:
   - ✅ `app_examen.py` (aplicación principal)
   - ✅ `preguntas_aws.json` (base de datos de preguntas)
   - ✅ `requirements.txt` (dependencias)
   - ✅ `README.md` (documentación)

### Pasos en Streamlit.io

1. **Ir a** [https://share.streamlit.io](https://share.streamlit.io)

2. **Iniciar sesión** con tu cuenta de GitHub

3. **Hacer clic en "New app"**

4. **Configurar la aplicación**:
   - **Repository**: `bjabinn/questionsAwsPractitioner`
   - **Branch**: `main`
   - **Main file path**: `app_examen.py`
   - **App URL**: Elige un nombre único (ej: `aws-exam-practitioner`)

5. **Hacer clic en "Deploy"**

6. **Esperar** a que Streamlit compile y despliegue la aplicación (puede tomar 2-3 minutos)

### 🎉 ¡Listo!

Tu aplicación estará disponible en:
```
https://[tu-nombre-app].streamlit.app
```

---

## 🔄 Actualizar la aplicación desplegada

Cada vez que hagas cambios:

```bash
# 1. Añadir cambios
git add .

# 2. Hacer commit
git commit -m "Descripción de los cambios"

# 3. Subir a GitHub
git push origin main
```

Streamlit.io detectará automáticamente los cambios y redessplegará la aplicación.

---

## 📝 Archivos en el repositorio

Estos son los archivos que se subirán:

- `app_examen.py` - Aplicación principal de Streamlit
- `preguntas_aws.json` - Base de datos con 699 preguntas
- `README.md` - Documentación del proyecto
- `requirements.txt` - Dependencias de Python
- `README_EXAMEN.md` - Documentación detallada del examen (opcional)
- `.gitignore` - Archivos a ignorar por Git (recomendado)

---

## 🛡️ Crear archivo .gitignore (recomendado)

Antes de hacer el primer commit, es buena idea crear un `.gitignore`:

```bash
# Crear archivo .gitignore
echo __pycache__/ > .gitignore
echo *.pyc >> .gitignore
echo .streamlit/ >> .gitignore
echo .DS_Store >> .gitignore
echo *.bat >> .gitignore
```

O simplemente copia este contenido en un nuevo archivo llamado `.gitignore`:

```
__pycache__/
*.pyc
.streamlit/
.DS_Store
*.bat
.vscode/
```

---

## ⚡ Comando todo en uno (después de resolver README)

Si prefieres ejecutar todo de una vez después de la configuración inicial:

```bash
git init && git remote add origin https://github.com/bjabinn/questionsAwsPractitioner.git && git fetch origin && git branch -M main && git pull origin main --allow-unrelated-histories && git add . && git commit -m "Añadir aplicación de examen AWS Streamlit" && git push -u origin main
```

---

## 🆘 Solución de problemas

### Problema: "Authentication failed"
**Solución**: Necesitas configurar tus credenciales de GitHub
```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

### Problema: "Repository not found"
**Solución**: Verifica que la URL del repositorio sea correcta y que tengas permisos

### Problema: Conflictos de merge
**Solución**: Edita manualmente los archivos en conflicto, luego:
```bash
git add .
git commit -m "Resolver conflictos"
git push origin main
```

---

¡Buena suerte con tu despliegue! 🚀☁️