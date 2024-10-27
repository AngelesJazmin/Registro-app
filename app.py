import os
import csv
import streamlit as st
from datetime import datetime
from asistencia_ediciones import (
    registrar_asistencia, leer_asistencia, actualizar_asistencia, eliminar_asistencia,
    obtener_profesores_disponibles, agregar_carrera, eliminar_carrera, agregar_grupo, eliminar_grupo,
    agregar_profesor, eliminar_profesor
)
from asistencia_estadisticas import generar_reporte_por_profesor, generar_reporte_por_materia, generar_estadisticas_globales
from horarios_profesores import materias, carreras, grupos, horarios_profesores

# Verificar si la carpeta 'data' existe, y si no, crearla
if not os.path.exists('data'):
    os.makedirs('data')

# Verificar si el archivo 'asistencia.csv' existe y crearlo si no existe
if not os.path.exists('data/asistencia.csv'):
    with open('data/asistencia.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Profesor', 'Materia', 'Carrera', 'Grupo', 'Fecha', 'Estado de Asistencia'])

# Función de inicio de sesión
def login():
    """
    Función que maneja el inicio de sesión del usuario.
    Se requiere que el usuario ingrese un nombre de usuario y una contraseña.
    """
    st.title("Inicio de Sesión")
    st.info("Para acceder a la aplicación de registro, por favor haz clic en 'Iniciar Sesión' dos veces. Esto es necesario para confirmar tu intención de iniciar sesión.")
    username = st.text_input("Nombre de usuario")
    password = st.text_input("Contraseña", type="password")
    
    if st.button("Iniciar Sesión"):
        if username == "CodigoMaestro" and password == "HelloWorld":
            st.session_state['logged_in'] = True
            st.success("Inicio de sesión exitoso.")
        else:
            st.error("Nombre de usuario o contraseña incorrectos.")

# Verificar si el usuario está autenticado
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    login()
else:
    # Función para generar la lista de datos de profesores
    def generar_datos_profesores():
        """
        Genera una lista de datos de profesores con su respectiva carrera, materia, grupo y horario.
        """
        datos_profesores = []
        carrera_default = 'Ingeniería en Computación Inteligente (ICI)'  # Carrera por defecto

        for profesor, materias_horarios in horarios_profesores.items():
            for materia, horarios in materias_horarios.items():
                for horario in horarios:
                    if len(horario) == 4:
                        dia, hora_inicio, hora_fin, grupo = horario
                        datos_profesores.append({
                            'Nombre del Profesor': profesor,
                            'Carrera': carrera_default,
                            'Materia': materia,
                            'Grupo': grupo,
                            'Horario': f"{dia} {hora_inicio} - {hora_fin}"
                        })
                    elif len(horario) == 5:  # Para horarios de Trabajo Independiente
                        dia, hora_inicio, hora_fin, tipo, grupo = horario
                        datos_profesores.append({
                            'Nombre del Profesor': profesor,
                            'Carrera': carrera_default,
                            'Materia': materia,
                            'Grupo': grupo,
                            'Horario': f"{dia} {hora_inicio} - {hora_fin} (Trabajo Independiente)"
                        })
        return datos_profesores

    # Menú lateral
    menu = st.sidebar.selectbox('Menú', ['Registrar Asistencia', 'Actualizar/Eliminar Asistencia', 'Estadísticas', 'Administrar Materias, Grupos y Carreras', 'Listar Datos de Profesores'])

    # Opción: Registrar Asistencia
    if menu == 'Registrar Asistencia':
        st.title('Registrar Asistencia')
        
        # Selección de Carrera y Grupo
        carrera = st.selectbox('Seleccionar Carrera', carreras)
        grupo = st.selectbox('Seleccionar Grupo', grupos)
        
        # Selección de materia
        materia_seleccionada = st.selectbox('Seleccionar Materia', materias[carrera])
        
        # Obtener profesores disponibles según la carrera, grupo y materia seleccionada
        profesor = None  # Inicializar la variable profesor
        profesores_disponibles = obtener_profesores_disponibles(carrera, grupo, materia_seleccionada)

        # Verificar si hay profesores disponibles
        if profesores_disponibles:
            profesor = st.selectbox('Seleccionar Profesor', profesores_disponibles)
        else :
            st.error(f'No hay profesores disponibles para {materia_seleccionada} en la carrera {carrera} y el grupo {grupo}.')
        
        # Selección de fecha
        fecha = st.date_input ('Fecha', datetime.today())
        
        # Validar que la fecha no sea futura
        if fecha > datetime.today().date():
            st.error("La fecha no puede ser futura.")
        
        # Selección de asistencia
        asistencia = st.radio('¿Asistencia?', ['Sí', 'No'])
        
        # Validaciones
        errores = []
        if not carrera:
            errores.append("No seleccionaste una carrera.")
        if not grupo:
            errores.append("No seleccionaste un grupo.")
        if not materia_seleccionada:
            errores.append("No seleccionaste una materia.")
        if not profesores_disponibles:
            errores.append("No hay profesores disponibles para la selección actual.")
        if not profesor:
            errores.append("No seleccionaste un profesor.")
        
        # Botón para registrar asistencia
        if st.button('Registrar'):
            if errores:
                for error in errores:
                    st.error(error)
            else:
                registrar_asistencia(profesor, materia_seleccionada, carrera, grupo, fecha, asistencia == 'Sí')
                st.success('Asistencia registrada correctamente.')
                                    
    # Opción: Actualizar/Eliminar Asistencia
    elif menu == 'Actualizar/Eliminar Asistencia':
        st.title('Actualizar o Eliminar Asistencia')
        
        registros = leer_asistencia()
        
        if registros:
            st.write('Registros de Asistencia:')
            for i, registro in enumerate(registros):
                st.write(f'{i+1}. {registro}')
            
            # Selección del registro a modificar
            registro_idx = st.number_input('Seleccione el número de registro a modificar/eliminar', min_value=1, max_value=len(registros), step=1) - 1
            accion = st.selectbox('Seleccionar Acción', ['Actualizar Asistencia', 'Eliminar Asistencia'])
            
            if accion == 'Actualizar Asistencia':
                nueva_asistencia = st.radio('¿Asistencia?', ['Sí', 'No'])
                if st.button('Actualizar'):
                    if registro_idx < 0 or registro_idx >= len(registros):
                        st.error("Índice de registro no válido.")
                    else:
                        try:
                            actualizar_asistencia(
                                registros[registro_idx][0],  # Profesor
                                registros[registro_idx][1],  # Materia
                                registros[registro_idx][2],  # Carrera
                                registros[registro_idx][3],  # Grupo
                                nueva_asistencia == 'Sí'
                            )
                            st.success('Asistencia actualizada correctamente.')
                        except Exception as e:
                            st.error(f"Ocurrió un error al actualizar: {str(e)}")
            
            elif accion == 'Eliminar Asistencia':
                if st.button('Eliminar'):
                    confirmacion = st.radio('¿Está seguro de que desea eliminar este registro?', ['Sí', 'No'])
                    if confirmacion == 'Sí':
                        try:
                            eliminar_asistencia(
                                registros[registro_idx][0],  # Profesor
                                registros[registro_idx][1],  # Materia
                                registros[registro_idx][2],  # Carrera
                                registros[registro_idx][3]   # Grupo
                            )
                            st.success('Asistencia eliminada correctamente.')
                        except Exception as e:
                            st.error(f"Ocurrió un error al eliminar: {str(e)}")
                    else:
                        st.info("Eliminación cancelada.")
        else:
            st.warning('No hay registros de asistencia disponibles.')

    # Opción: Estadísticas
    elif menu == 'Estadísticas':
        st.title('Estadísticas')
        
        tipo_estadistica = st.selectbox('Seleccionar tipo de estadísticas', ['Por Profesor', 'Por Materia', 'Globales'])
        
        if tipo_estadistica == 'Por Profesor':
            carrera = st.selectbox('Seleccionar Carrera', carreras)
            grupo = st.selectbox('Seleccionar Grupo', grupos)
            
            # Llamar a obtener_profesores_disponibles sin materia
            profesores_disponibles = [prof for prof in horarios_profesores.keys()]
            
            if profesores_disponibles:
                profesor = st.selectbox('Seleccionar Profesor', profesores_disponibles)
                periodo = st.selectbox('Seleccionar Periodo', ['semana', 'mes', '3 meses', 'semestre'])
                
                # Validaciones antes de generar estadísticas
                if st.button('Generar Estadísticas por Profesor'):
                    if not carrera or not grupo or not profesor:
                        st.error("Por favor, asegúrate de seleccionar una carrera, un grupo y un profesor.")
                    else :
                        try:
                            reporte_profesor = generar_reporte_por_profesor(profesor, periodo)
                            st.write(reporte_profesor)
                        except Exception as e:
                            st.error(f"Ocurrió un error al generar el reporte: {str(e)}")
            else:
                st.error('No hay profesores registrados.')

        elif tipo_estadistica == 'Por Materia':
            carrera = st.selectbox('Seleccionar Carrera', carreras)
            grupo = st.selectbox('Seleccionar Grupo', grupos)
            
            # Validaciones antes de generar estadísticas
            if st.button('Generar Estadísticas por Materia'):
                if not carrera or not grupo:
                    st.error("Por favor, asegúrate de seleccionar una carrera y un grupo.")
                else:
                    try:
                        reporte_materia = generar_reporte_por_materia(carrera, grupo)
                        st.write(reporte_materia)
                    except Exception as e:
                        st.error(f"Ocurrió un error al generar el reporte: {str(e)}")

        elif tipo_estadistica == 'Globales':
            st.title("Estadísticas Globales")

            # Validaciones antes de generar estadísticas
            if st.button('Generar Estadísticas Globales'):
                try:
                    estadisticas = generar_estadisticas_globales()  # Llamada sin argumento
                    st.write(estadisticas)
                except Exception as e:
                    st.error(f"Ocurrió un error al generar las estadísticas: {str(e)}")

    # Opción: Administrar Materias, Grupos y Carreras
    elif menu == 'Administrar Materias, Grupos y Carreras':
        st.title('Administrar Profesores, Materias, Grupos y Horarios')

        # Instrucciones de entrada
        st.info("""
        **Instrucciones para ingresar datos:**
        - **Nombre del Profesor**: Ingresa comenzando con los apellidos (Ejemplo: "López Hernández Juan").
        - **Carrera**: Selecciona una carrera existente o añade una nueva (Ejemplo: "Ingeniería en Computación Inteligente (ICI)").
        - **Materia**: Selecciona una materia de la lista o agrega una nueva si no existe (Ejemplo: "Cálculo diferencial").
        - **Grupo**: Selecciona un grupo de la lista o escribe un nuevo grupo (Ejemplo: "1A").
        - **Horario**: 
            - Para **Clase Regular**: Ingresa cada horario en el formato "Día, Hora Inicio, Hora Fin" (Ejemplo: "Lunes, 14:00, 15:00").
            - Para **Trabajo Independiente**: Utiliza el mismo formato de horario (Ejemplo: "Miércoles, 12:00, 13:00").
        """)

        # Seleccionar operación
        opcion = st.selectbox('Seleccionar Operación', [
            'Agregar Profesor', 'Eliminar Profesor', 'Agregar Carrera', 'Eliminar Carrera', 'Agregar Grupo', 'Eliminar Grupo'
        ])

        if opcion == 'Agregar Profesor':
            # Campos para agregar un conjunto de profesor, materia, grupo y horario
            nombre_profesor = st.text_input(
                'Nombre del Profesor',
                placeholder="Ejemplo: López Hernández Juan"
            )

            # Selección de carrera existente o nueva carrera
            nueva_carrera = st.checkbox("Agregar nueva Carrera")
            if nueva_carrera:
                carrera_profesor = st.text_input(
                    'Nueva Carrera',
                    placeholder="Ejemplo: Ingeniería en Computación"
                )
            else:
                carrera_profesor = st.selectbox('Seleccionar Carrera', carreras)

            # Selección de materia existente o nueva materia
            nueva_materia = st.checkbox("Agregar nueva Materia")
            if nueva_materia:
                materia_profesor = st.text_input(
                    'Nueva Materia',
                    placeholder="Ejemplo: Cálculo Vectorial"
                )
            else:
                # La lista de materias cambia según la carrera seleccionada
                materias_carrera = materias.get(carrera_profesor, []) if not nueva_carrera else []
                materia_profesor = st.selectbox('Seleccionar Materia', materias_carrera)

            # Selección de grupo existente o nuevo grupo
            nuevo_grupo = st.checkbox("Agregar nuevo Grupo")
            if nuevo_grupo:
                grupo_profesor = st.text_input(
                    'Nuevo Grupo',
                    placeholder="Ejemplo: 3A"
                )
            else:
                grupo_profesor = st.selectbox('Seleccionar Grupo', grupos)

            # Seleccionar si es una clase regular o una hora de trabajo independ iente
            tipo_horario = st.selectbox('Tipo de Horario', ['Clase Regular', 'Trabajo Independiente'])
            
            # Entrada de horario sin incluir el grupo en el ejemplo
            if tipo_horario == 'Clase Regular':
                horarios_profesor = st.text_area(
                    'Horarios (formato : Día, Hora Inicio, Hora Fin)', 
                    placeholder='Ejemplo: Lunes, 14:00, 15:00'
                )
            else:
                horarios_profesor = st.text_area(
                    'Horarios de Trabajo Independiente (formato: Día, Hora Inicio, Hora Fin)', 
                    placeholder='Ejemplo: Miércoles, 12:00, 13:00'
                )

            # Botón para agregar el conjunto completo
            if st.button('Agregar Profesor con Materia, Grupo y Horario'):
                # Formatear el nombre con la primera letra en mayúscula para cada palabra
                nombre_profesor = nombre_profesor.title().strip()

                if not (nombre_profesor and carrera_profesor and materia_profesor and horarios_profesor):
                    st.error("Debes completar todos los campos: profesor, materia, carrera, grupo y horario.")
                else:
                    try:
                        # Agregar la nueva carrera o grupo si se seleccionó esa opción
                        if nueva_carrera and carrera_profesor not in carreras:
                            carreras.append(carrera_profesor)
                        if nueva_materia and materia_profesor not in materias.get(carrera_profesor, []):
                            materias.setdefault(carrera_profesor, []).append(materia_profesor)
                        if nuevo_grupo and grupo_profesor not in grupos:
                            grupos.append(grupo_profesor)

                        # Procesar horarios según el tipo seleccionado
                        horarios_formateados = []
                        for horario in horarios_profesor.splitlines():
                            partes = horario.split(',')
                            if len(partes) == 2:
                                dia, hora_inicio, hora_fin = partes
                                if tipo_horario == 'Clase Regular':
                                    horarios_formateados.append((dia.strip(), hora_inicio.strip(), hora_fin.strip(), grupo_profesor))
                                else:
                                    horarios_formateados.append((dia.strip(), hora_inicio.strip(), hora_fin.strip(), "Trabajo Independiente", grupo_profesor))

                        agregar_profesor(nombre_profesor, carrera_profesor, materia_profesor, horarios_formateados)
                        st.success(f'Profesor {nombre_profesor} agregado a la materia {materia_profesor} en la carrera {carrera_profesor}.')
                    except ValueError as e:
                        st.error(str(e))

        elif opcion == 'Eliminar Profesor':
            st.info("Para eliminar un profesor, selecciona la carrera y proporciona el nombre completo.")
            
            # Seleccionar profesor y datos relacionados para eliminar
            nombre_profesor = st.text_input('Nombre del Profesor (comenzando por apellidos)')
            carrera_profesor = st.selectbox('Seleccionar Carrera', carreras)
            
            if st.button('Eliminar Profesor con Materia, Grupo y Horario'):
                if not nombre_profesor:
                    st.error("Debes ingresar el nombre del profesor para eliminar.")
                else:
                    try:
                        eliminar_profesor(nombre_profesor, carrera_profesor)
                        st.success(f'Profesor {nombre_profesor} eliminado de la carrera {carrera_profesor}.')
                    except ValueError as e:
                        st.error(str(e))

        elif opcion == 'Agregar Carrera':
            ejemplo_formato = carreras[0] if carreras else "Ejemplo: Ingeniería en Computación Inteligente (ICI)"
            carrera = st.text_input('Nueva Carrera', placeholder=f"Ejemplo: {ejemplo_formato} (incluye abreviatura entre paréntesis)")
            if st.button('Agregar Carrera'):


                if not carrera.strip():
                    st.error("El nombre de la carrera no puede estar vacío.")
                elif carrera in carreras:
                    st.error("La carrera ya existe.")
                else:
                    agregar_carrera(carrera)
                    st.success(f'Carrera {carrera} agregada.')

        elif opcion == 'Eliminar Carrera':
            carrera = st.selectbox('Seleccionar Carrera para Eliminar', carreras)
            if st.button('Eliminar Carrera'):
                if carrera not in carreras:
                    st.error("La carrera no existe.")
                else:
                    eliminar_carrera(carrera)
                    st.success(f'Carrera {carrera} eliminada.')

        elif opcion == 'Agregar Grupo':
            # Formato de ejemplo del primer grupo, o un ejemplo genérico si no hay grupos
            ejemplo_grupo = grupos[0] if grupos else "Ejemplo: 3B"
    
            # Input para ingresar el nuevo grupo con un placeholder que sugiera el formato
            grupo = st.text_input('Nuevo Grupo', placeholder=f"Ejemplo: {ejemplo_grupo}")

            if st.button('Agregar Grupo'):
                if not grupo.strip():
                    st.error("El nombre del grupo no puede estar vacío.")
                elif grupo in grupos:
                    st.error(" El grupo ya existe.")
                else:
                    agregar_grupo(grupo)
                    st.success(f'Grupo {grupo} agregado.')

        elif opcion == 'Eliminar Grupo':
            grupo = st.selectbox('Seleccionar Grupo para Eliminar', grupos)
            if st.button('Eliminar Grupo'):
                if grupo not in grupos:
                    st.error("El grupo no existe.")
                else:
                    eliminar_grupo(grupo)
                    st.success(f'Grupo {grupo} eliminado.')

    # Opción: Listar Datos de Profesores
    elif menu == 'Listar Datos de Profesores':
        st.title('Datos de Profesores')
        datos_profesores = generar_datos_profesores()  # Llamar a la función para obtener los datos
        if datos_profesores:
            for dato in datos_profesores:
                st.write(dato)
        else:
            st.warning('No hay datos de profesores disponibles.')