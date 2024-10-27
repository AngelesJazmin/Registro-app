
# 📘 Sistema de Registro de Clases para Control de Asistencia Docente

### 🖥️ Descripción

Este proyecto es una aplicación en Python y Streamlit diseñada para registrar y gestionar la asistencia de profesores en distintas carreras de ingeniería, como **Ingeniería en Computación Inteligente** e **Ingeniería Mecánica y Electrónica**. Su interfaz es intuitiva y facilita el control de asistencias, ofreciendo reportes detallados para el análisis de cumplimiento de clases.

---

## ✨ Funcionalidades Principales

- **✅ Registro de Asistencia**: Registro y consulta de asistencia de profesores, validando horarios y asignaturas asignadas.
- **📝 Gestión de Profesores, Materias y Horarios**: Opciones para agregar, editar y eliminar profesores, materias y horarios.
- **📊 Generación de Reportes y Estadísticas**: Reportes filtrados por profesor, materia y carrera, y estadísticas de asistencia en periodos semanales, mensuales, trimestrales y semestrales.
- **🚀 Escalabilidad**: Fácil integración de nuevas carreras y actualización dinámica de datos.

---

## 🚀 Instalación

### Requisitos Previos

- 🐍 Python 3.8 o superior
- 🎈 Streamlit
- 🐼 Pandas

### Pasos de Instalación

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/TU_USUARIO/Sistema-de-Control-de-Asistencia.git
   cd Sistema-de-Control-de-Asistencia
   ```

2. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecuta la aplicación**:
   ```bash
   streamlit run app.py
   ```

---

## 🛠️ Uso de la Aplicación

1. **Agregar Profesores y Horarios**: Ingresa los datos de nuevos profesores y asigna su horario y carrera correspondiente.

2. **Registro de Asistencia**: Selecciona el profesor, materia, carrera y fecha para registrar la asistencia.

3. **Consultas y Reportes**:
   - **Por Profesor**: Muestra las clases impartidas o faltantes en el periodo seleccionado.
   - **Por Materia**: Compara la asistencia entre materias de un mismo grupo y carrera.
   - **Estadísticas Globales**: Calcula el porcentaje de cumplimiento de clases por carrera.

---

## 📁 Archivos Principales

| Archivo                  | Descripción                                   |
|--------------------------|-----------------------------------------------|
| `app.py`                 | Interfaz principal con Streamlit              |
| `horarios_profesores.py` | Configuración de los horarios de los profesores |
| `asistencia.csv`         | Archivo de almacenamiento de registros de asistencia |
| `asistencia_funciones.py`| Funciones de registro y validación de asistencias |
| `asistencia_ediciones.py`| Módulo para editar registros de asistencia    |

