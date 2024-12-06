# Hack4u Academy Courses Library

Una biblioteca de Python para consultar cursos de la academia Hack4u.
## Cursos disponibles

- Introducción a Linux [15 horas]
- Personalización de entorno en Linux [3 horas]
- Python ofensivo [35 horas]
- Introducción al Hacking [53 horas]

## Instalación

Instala el paquete utilizando `pip3`

```python3	
pip3 install hack4u
```

## Uso básico

### Listar todos los cursos

```python
from hack4u import list_courses

for course in list_courses():
	print(course)
```

### Obtener un curso por nombre

```python
from hack4u import search_course_by_name

course = search_course_by_name("Introducción a Linux")
print(course)
```


### Calcular la duración total de los cursos

```python
from hack4u import total_duration

print(f"Duración total: {total_duration()} horas")
```

