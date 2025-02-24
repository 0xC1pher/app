# Proyecto: Sistema de Gestión Académica
## Changelog

**[Fecha Actual] - Funcionalidad de Reporte de Asistencia**

*   **Módulo de Reporte de Asistencia para Profesores:**
    *   Se implementó la funcionalidad para que los profesores generen reportes de asistencia.
    *   Se creó la ruta `/asistencia/reporte` y la vista `reporte_asistencia` en `app.py` para gestionar la generación de reportes.
    *   Se diseñó el template `reporte_asistencia.html` para el formulario de generación y visualización de reportes.
    *   Se agregó un enlace "Reporte de Asistencia" en la barra de navegación, visible solo para usuarios con rol de "Profesor".
    *   El reporte permite filtrar por curso y rango de fechas (opcional).

**[Fecha Anterior] - Funcionalidad de Registro de Asistencia y Mejoras en Modelos**

*   **Funcionalidad de Registro de Asistencia:**
    *   Se implementó la funcionalidad para que los profesores registren la asistencia de los estudiantes a través de un formulario web.
    *   Se creó la ruta `/asistencia/registrar` y la vista `registrar_asistencia` en `app.py` para gestionar el registro de asistencia.
    *   Se diseñó el template `registrar_asistencia.html` para el formulario de registro de asistencia.
    *   Se agregó un enlace "Registrar Asistencia" en la barra de navegación, visible solo para usuarios con rol de "Profesor".
*   **Mejoras en Modelos y Base de Datos:**
    *   **Modelo `Usuario`:**
        *   Se actualizó la columna `rol` para utilizar un tipo `ENUM` de PostgreSQL (`tipo_rol`), mejorando la validación de roles a nivel de base de datos.
        *   Se alinearon los nombres de los campos (`correo_email`, `contraseña`, `rol`) del modelo `Usuario` con los nombres de las columnas en el esquema SQL para mayor coherencia.
    *   **Modelo `Profesor`:**
        *   Se restauró el modelo `Profesor` y se estableció una relación One-to-One con el modelo `Usuario`.
        *   Se definió la relación para representar a los profesores como perfiles extendidos de usuarios.
    *   **Base de Datos:**
        *   Se creó el tipo `ENUM` `tipo_rol` en PostgreSQL.
        *   Se aplicaron migraciones para reflejar los cambios en los modelos, incluyendo el uso del `ENUM` para roles y la relación One-to-One Usuario-Profesor.

**[Fecha Anterior] - ... (Historial de cambios previos)**
*   ... (Registros de cambios anteriores)

---

**Próximos Pasos:**

1.  **Gestión de Cursos (Módulo de Administrador):**  Implementar completamente la creación, edición y eliminación de cursos y la gestión de la relación Many-to-Many entre Cursos y Materias.
    *   ✅ **Creación de Cursos:**  Implementado formulario y ruta para crear nuevos cursos, incluyendo nombre, descripción y selección de materias.
    *   ✅ **Listado de Cursos:** Implementada página de gestión de cursos con tabla para listar cursos existentes y enlace para crear nuevos cursos.
    *   ✅ **Edición de Cursos:** Implementado formulario y ruta para editar cursos existentes, permitiendo modificar nombre, descripción y materias asociadas.
    *   ✅ **Eliminación de Cursos:** Implementada funcionalidad para eliminar cursos existentes, con confirmación de seguridad.
2.  **Edición y Eliminación de Materias y Usuarios:**  Implementar la edición y eliminación de materias y usuarios. (Pendiente)
3.  **Validaciones Robustas:**  Agregar validaciones más robustas en formularios de creación y edición. (Pendiente - Validaciones básicas implementadas en formularios de Cursos)
4.  **Mejoras UI/UX:**  Refinar la interfaz de usuario. (Pendiente)

```
flask db migrate -m "Corrección de relaciones y modelos"
flask db upgrade
```
