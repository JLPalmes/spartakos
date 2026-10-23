---
title: Spartakos — Revisión de continuidad para el lunes 26 de octubre
lang: es-ES
license: CC-BY-SA-4.0
date: 2026-10-23
status: Registro de trabajo en curso; no aprobación ni versión de producción
---

# Revisión de continuidad

La revisión prevista es el lunes 26 de octubre de 2026. Este registro reúne resultados, límites y propuestas para facilitar la revisión conjunta. No sustituye la especificación ni la matriz de aceptación.

## Estado de partida

- Rama de trabajo: `prototipo-segunda-revision`; propuesta pública [#2](https://github.com/JLPalmes/spartakos/pull/2), sin integrar en main.
- Laboratorio local: `http://127.0.0.1:8787`; acceso libre con cuentas ficticias, no autenticación de producción.
- Última batería ejecutada al inicio de este bloque: 75 pruebas automáticas superadas; la matriz completa de producto sigue sin ejecutarse.
- Borradores recuperables implementados para publicaciones iniciales, con guardado explícito, versiones y copias ante conflictos.
- Estadísticas personales, comunitarias y globales documentadas como propuesta N11; sin captación nueva ni implementación.

## Orden de trabajo

1. Completar la gestión reversible de borradores y comprobar persistencia, privacidad y conflictos.
2. Desarrollar edición y retirada de publicaciones, preservando autoría, contexto de respuestas y restricciones de audiencia. Distinguir la retirada del cuerpo de una garantía de borrado de copias externas.
3. Revisar consistencia de editor, citas, avisos, programaciones y borradores después de los cambios.
4. Concretar el catálogo y permisos de estadísticas sin inventar seguimiento de lecturas, métricas globales exhaustivas ni clasificaciones de personas.
5. Consolidar resultados, límites, comprobaciones y propuestas pendientes para revisión.

## Límites de este trabajo

Conservar los datos locales existentes y separar los escenarios sintéticos. No publicar datos de ensayo del usuario. No integrar la rama principal, desplegar un servicio público ni contactar con terceros. No dar por aprobadas alternativas pendientes. Cualquier continuación debe inspeccionar los cambios presentes antes de editar y preservar el trabajo previo.

## Resultados acumulados

### Bloque 1 — 23 de octubre: gestión reversible de borradores

Implementada papelera privada y persistente, con restauración de contenido y estado anterior. Mover una referencia no retira publicaciones ni cancela programaciones; restaurarla no ejecuta de nuevo el envío. Se comprueban propiedad y versión. No hay borrado definitivo ni vaciado automático.

Comprobaciones: 78 pruebas automáticas superadas y recorrido de navegador con datos sintéticos. Se conservaron los datos locales del laboratorio. Se incorporan también las notas de estadísticas N11 y su desarrollo funcional, todavía sin implementación.

### Siguiente bloque

Edición y retirada de publicaciones. Partir de la sección 6 y 7 de FUNCIONAL-03-PUBLICACIONES-Y-CONVERSACIONES.md. Antes de modificar código, fijar la semántica mínima de edición, versión a la que responden otros y marcador de retirada. Preservar respuestas independientes y no prometer borrado de copias ajenas. Las citas deben dejar de mostrar el cuerpo retirado y la exportación, los avisos y las programaciones deben revisarse como posibles vías de filtración.

### Disciplina de continuidad

Inspeccionar rama, cambios locales y propuesta de revisión antes de continuar. La automatización no confirma por sí misma nuevas decisiones de producto. No empezar otro bloque tras el lunes 26; consolidar los resultados y límites. Registrar aquí las pruebas reales y el estado de publicación de cada bloque.
