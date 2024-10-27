import csv
from datetime import datetime, timedelta

# Función para generar reporte por profesor
def generar_reporte_por_profesor(profesor, periodo='semestre'):
    """
    Genera un reporte de asistencia por profesor para un período determinado.
    
    :param profesor: Nombre del profesor
    :param periodo: Período de tiempo para el reporte (semana, mes, 3 meses, semestre)
    :return: Diccionario con los datos del reporte
    """
    periodos = {
        'semana': timedelta(weeks=1),
        'mes': timedelta(days=30),
        '3 meses': timedelta(days=90),
        'semestre': timedelta(days=180)
    }

    fecha_actual = datetime.today()
    fecha_inicio = fecha_actual - periodos.get(periodo, timedelta(days=180))

    asistencias_totales = 0
    faltas_totales = 0

    try:
        with open('data/asistencia.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Saltar encabezado
            for row in reader:
                profesor_csv, materia, carrera, fecha_str, estado_asistencia, grupo = row
                try:
                    fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
                except ValueError:
                    print(f"Formato de fecha inválido para el registro: {row}")
                    continue
                
                if profesor_csv == profesor and fecha >= fecha_inicio:
                    if estado_asistencia == 'Asistencia':
                        asistencias_totales += 1
                    else:
                        faltas_totales += 1
    except FileNotFoundError:
        print("Archivo de asistencia no encontrado.")

    total_clases = asistencias_totales + faltas_totales
    tasa_cumplimiento = (asistencias_totales / total_clases) * 100 if total_clases > 0 else 0

    return {
        'Profesor': profesor,
        'Asistencias': asistencias_totales,
        'Faltas': faltas_totales,
        'Cumplimiento (%)': round(tasa_cumplimiento, 2)
    }


# Función para generar reporte por materia
def generar_reporte_por_materia(carrera, grupo):
    """
    Genera un reporte de asistencia por materia para una carrera y grupo determinados.
    
    :param carrera: Nombre de la carrera
    :param grupo: Nombre del grupo
    :return: Diccionario con los datos del reporte
    """
    materias_asistencias = {}

    try:
        with open('data/asistencia.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Saltar encabezado
            for row in reader:
                profesor, materia, carrera_csv, fecha, estado_asistencia, grupo_csv = row

                if carrera_csv == carrera and grupo_csv == grupo:
                    if materia not in materias_asistencias:
                        materias_asistencias[materia] = {'Asistencias': 0, 'Faltas': 0}

                    if estado_asistencia == 'Asistencia':
                        materias_asistencias[materia]['Asistencias'] += 1
                    else:
                        materias_asistencias[materia]['Faltas'] += 1
    except FileNotFoundError:
        print("Archivo de asistencia no encontrado.")

    # Calcular el porcentaje de cumplimiento para cada materia
    for materia, conteos in materias_asistencias.items():
        total_clases = conteos['Asistencias'] + conteos['Faltas']
        tasa_cumplimiento = (conteos['Asistencias'] / total_clases) * 100 if total_clases > 0 else 0
        materias_asistencias[materia]['Cumplimiento (%)'] = round(tasa_cumplimiento, 2)
    
    return materias_asistencias

# Función para generar estadísticas globales por carrera
def generar_estadisticas_globales():
    """
    Genera estadísticas globales de asistencia por carrera y compara el cumplimiento entre ellas.
    
    :return: Diccionario con los datos de las estadísticas globales
    """
    carreras_asistencias = {}
    
    # Definir las carr eras que deseamos analizar
    carreras = ['Ingeniería en Computación Inteligente (ICI)', 'Ingeniería Mecánica y Eléctrica (IME)']
    
    # Inicializar contadores para cada carrera
    for carrera in carreras:
        carreras_asistencias[carrera] = {'Asistencias': 0, 'Faltas': 0}
    
    # Leer el archivo de asistencias y contar asistencias y faltas por carrera
    try:
        with open('data/asistencia.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Saltar encabezado
            for row in reader:
                if len(row) < 5:  # Verificar que la fila tenga los elementos esperados
                    continue
                _, _, carrera, _, estado_asistencia, _ = row
                if carrera in carreras_asistencias:
                    if estado_asistencia == 'Asistencia':
                        carreras_asistencias[carrera]['Asistencias'] += 1
                    elif estado_asistencia == 'Falta':
                        carreras_asistencias[carrera]['Faltas'] += 1
    except FileNotFoundError:
        print("Archivo de asistencia no encontrado.")
        return {}
    except Exception as e:
        print(f"Error al leer el archivo de asistencia: {e}")
        return {}

    # Calcular el porcentaje de cumplimiento para cada carrera
    resultados = {}
    for carrera, conteos in carreras_asistencias.items():
        total_clases = conteos['Asistencias'] + conteos['Faltas']
        tasa_cumplimiento = (conteos['Asistencias'] / total_clases) * 100 if total_clases > 0 else 0
        resultados[carrera] = {
            'Asistencias': conteos['Asistencias'],
            'Faltas': conteos['Faltas'],
            'Cumplimiento (%)': round(tasa_cumplimiento, 2)
        }
    
    # Comparación entre carreras
    if len(resultados) == 2:
        carrera_1, carrera_2 = carreras
        diferencia = abs(resultados[carrera_1]['Cumplimiento (%)'] - resultados[carrera_2]['Cumplimiento (%)'])
        print(f"Diferencia de cumplimiento entre {carrera_1} y {carrera_2}: {diferencia:.2f}%")
    
    return resultados