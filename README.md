Sistema de Registro de Clases para Control de Asistencia Docente
Descripción
Este proyecto es una aplicación en Python y Streamlit diseñada para registrar y gestionar la asistencia de profesores en distintas carreras de ingeniería, como Ingeniería en Computación Inteligente e Ingeniería Mecánica y Electrónica. Ofrece una interfaz intuitiva para facilitar el control de asistencias y proporciona reportes detallados para el análisis de cumplimiento de clases.

Funcionalidades Principales
Registro de Asistencia: Permite registrar y consultar la asistencia de los profesores, validando horarios y asignaturas asignadas.
Gestión de Profesores, Materias, y Horarios: Incluye opciones para agregar, editar y eliminar profesores, asignaturas y horarios, configurando tanto los horarios regulares como las horas de trabajo independiente.
Generación de Reportes y Estadísticas: Genera reportes por profesor, materia y carrera, con opciones de filtrado por periodos (semanal, mensual, trimestral, semestral).
Escalabilidad: Posibilidad de agregar nuevas carreras y actualizar los datos de forma dinámica.
Instalación
Requisitos Previos
Python 3.8 o superior
Streamlit
Pandas
Pasos de Instalación
Clona el repositorio:

bash
Copiar código
git clone https://github.com/TU_USUARIO/Sistema-de-Control-de-Asistencia.git
cd Sistema-de-Control-de-Asistencia
Instala las dependencias:

bash
Copiar código
pip install -r requirements.txt
Ejecuta la aplicación:

bash
Copiar código
streamlit run app.py
Uso de la Aplicación
Agregar Profesores y Horarios: Permite ingresar los datos de nuevos profesores, asignando su horario y carrera correspondiente.
Registro de Asistencia: En la sección de registro, selecciona el profesor, materia, carrera y fecha. El sistema valida la asignación antes de guardar la asistencia.
Consultas y Reportes:
Por Profesor: Muestra las clases impartidas o faltantes en el periodo seleccionado.
Por Materia: Permite comparar la asistencia entre materias dentro de un mismo grupo y carrera.
Estadísticas Globales: Calcula el porcentaje de cumplimiento de clases para cada carrera.
Archivos Principales
app.py: Interfaz principal con Streamlit.
horarios_profesores.py: Configuración de los horarios de los profesores.
asistencia.csv: Archivo de almacenamiento de registros de asistencia.
asistencia_funciones.py: Funciones de registro y validación de asistencias.
asistencia_ediciones.py: Módulo de edición para agregar, modificar y eliminar registros de asistencia.
