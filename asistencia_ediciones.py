import csv
from horarios_profesores import horarios_profesores, carreras, materias, grupos

# Nombre del archivo de asistencia
archivo_asistencia = 'data/asistencia.csv'

# Registrar asistencia
def registrar_asistencia(profesor, materia, carrera, grupo, fecha, asistencia=True):
    """
    Registra la asistencia de un profesor en una materia específica.
    
    :param profesor: Nombre del profesor
    :param materia: Nombre de la materia
    :param carrera: Nombre de la carrera
    :param grupo: Nombre del grupo
    :param fecha: Fecha de la asistencia
    :param asistencia: Estado de la asistencia (True para asistencia, False para falta)
    """
    estado = 'Asistencia' if asistencia else 'Falta'
    with open(archivo_asistencia, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([profesor, materia, carrera, grupo, fecha, estado])

# Función para leer asistencia
def leer_asistencia():
    """
    Lee los registros de asistencia desde el archivo de asistencia.
    
    :return: Lista de registros de asistencia
    """
    registros = []
    try:
        with open(archivo_asistencia, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Saltar encabezado
            for row in reader:
                registros.append(row)
    except FileNotFoundError:
        print("Archivo de asistencia no encontrado.")
    return registros

# Función para actualizar asistencia
def actualizar_asistencia(profesor, materia, carrera, grupo, nueva_asistencia):
    """
    Actualiza el estado de asistencia de un profesor en una materia específica.
    
    :param profesor: Nombre del profesor
    :param materia: Nombre de la materia
    :param carrera: Nombre de la carrera
    :param grupo: Nombre del grupo
    :param nueva_asistencia: Nuevo estado de asistencia (True para asistencia, False para falta)
    """
    registros_actualizados = []
    try:
        with open(archivo_asistencia, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == profesor and row[1] == materia and row[2] == carrera and row[3] == grupo:
                    row[4] = 'Asistencia' if nueva_asistencia else 'Falta'
                registros_actualizados.append(row)
    
        with open(archivo_asistencia, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(registros_actualizados)
    except Exception as e:
        print(f"Error al actualizar asistencia: {e}")

# Función para eliminar asistencia
def eliminar_asistencia(profesor, materia, carrera, grupo):
    """
    Elimina el registro de asistencia de un profesor en una materia específica.
    
    :param profesor: Nombre del profesor
    :param materia: Nombre de la materia
    :param carrera: Nombre de la carrera
    :param grupo: Nombre del grupo
    """
    registros_actualizados = []
    try:
        with open(archivo_asistencia, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and not (row[0] == profesor and row[1] == materia and row[2] == carrera and row[3] == grupo):
                    registros_actualizados.append(row)
        
        with open(archivo_asistencia, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(registros_actualizados)
    except Exception as e:
        print(f"Error al eliminar asistencia: {e}")

# Obtener profesores disponibles
def obtener_profesores_disponibles(carrera, grupo, materia_seleccionada):
    """
    Obtiene la lista de profesores disponibles para una materia específica en una carrera y grupo determinados.
    
    :param carrera: Nombre de la carrera
    :param grupo: Nombre del grupo
    :param materia_seleccionada: Nombre de la materia
    :return: Lista de profesores disponibles
    """
    profesores_disponibles = set()  # Cambiado a set para evitar duplicados
    for profesor, materias_dict in horarios_profesores.items():
        for materia, horarios in materias_dict.items():
            if materia == materia_seleccionada and materia in materias[carrera]:
                for horario in horarios:
                    if grupo == horario[-1]:  # Verificar si el grupo es el último valor en el horario
                        profesores_disponibles.add(profesor)
                        break
    return list(profesores_disponibles)  # Convertimos set a lista

# Agregar profesor
def agregar_profesor(nombre_profesor, carrera, materia, horarios):
    """
    Agrega un nuevo profesor con su materia y horarios.
    
    :param nombre_profesor: Nombre del profesor
    :param carrera: Nombre de la carrera
    :param materia: Nombre de la materia
    :param horarios: Lista de horarios del profesor
    """
    if not nombre_profesor.strip():
        raise ValueError("El nombre del profesor no puede estar vacío.")
    
    # Validar que cada horario esté en el formato correcto
    horarios_lista = []
    for horario in horarios:
        if len(horario) == 4 or len(horario) == 5:
            horarios_lista.append(horario)
        else:
            raise ValueError("Cada horario debe incluir Día, Hora Inicio, Hora Fin y Grupo.")

    # Agregar el profesor al diccionario de horarios
    if nombre_profesor not in horarios_profesores:
        horarios_profesores[nombre_profesor] = {materia: horarios_lista}
    else:
        if materia not in horarios_profesores[nombre_profesor]:
            horarios_profesores[nombre_profesor][materia] = horarios_lista
        else:
            horarios_profesores[nombre_profesor][materia].extend(horarios_lista)  # Agregar horarios si ya existe

def eliminar_profesor(nombre_profesor, carrera):
    """
    Elimina un profesor de la carrera especificada.
    
    :param nombre_profesor: Nombre del profesor
    :param carrera: Nombre de la carrera
    """
    if nombre_profesor in horarios_profesores:
        del horarios_profesores[nombre_profesor]
    else:
        raise ValueError(f"No se encontró al profesor {nombre_profesor} en la carrera {carrera}.")

# Función para agregar una nueva carrera
def agregar_carrera(carrera):
    """
    Agrega una nueva carrera a la lista de carreras.
    
    :param carrera: Nombre de la carrera
    """
    if carrera not in carreras:
        carreras.append(carrera)

# Función para eliminar una carrera
def eliminar_carrera(carrera):
    """
    Elimina una carrera de la lista de carreras.
    
    :param carrera: Nombre de la carrera
    """
    if carrera in carreras:
        carreras.remove(carrera)

# Función para agregar una nueva materia
def agregar_materia(carrera, materia):
    """
    Agrega una nueva materia a la lista de materias de una carrera.
    
    :param carrera: Nombre de la carrera
    :param materia: Nombre de la materia
    """
    if carrera in materias:
        if materia not in materias[carrera]:
            materias[carrera].append(materia)

# Función para eliminar una materia
def eliminar_materia(carrera, materia):
    """
    Elimina una materia de la lista de materias de una carrera.
    
    :param carrera: Nombre de la carrera
    :param materia: Nombre de la materia
    """
    if carrera in materias and materia in materias[carrera]:
        materias[carrera].remove(materia)

# Función para agregar un nuevo grupo
def agregar_grupo(grupo):
    """
    Agrega un nuevo grupo a la lista de grupos.
    
    :param grupo: Nombre del grupo
 """
    if grupo not in grupos:
        grupos.append(grupo)

# Función para eliminar un grupo
def eliminar_grupo(grupo):
    """
    Elimina un grupo de la lista de grupos.
    
    :param grupo: Nombre del grupo
    """
    if grupo in grupos:
        grupos.remove(grupo)