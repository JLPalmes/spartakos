---
title: Spartakos — Revisión de continuidad para el lunes 26 de octubre
lang: es-ES
license: CC-BY-SA-4.0
date: 2026-10-24
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

### Bloque 2 — 24 de octubre: edición propia y retirada del cuerpo

Implementada edición con versión, autoría y permisos, sin cambio de audiencia o contexto. Respuestas, citas y Me gusta anteriores conservan su referencia; se advierte sobre versiones anteriores y no se renueva automáticamente la aprobación. La retirada vacía el cuerpo activo, deja marcador y conserva respuestas ajenas. Las citas no muestran el cuerpo retirado y las programaciones que lo necesitan quedan bloqueadas. El autor puede retirar su propio texto tras perder acceso, sin recibir historial ajeno.

Comprobaciones: 88 pruebas automáticas superadas; edición y referencias anteriores comprobadas con dos clientes; vista sintética de marcador y cita retirada comprobada en navegador. No se modificaron publicaciones del laboratorio del usuario durante esas pruebas. Límites: sin borrado garantizado de copias/respaldos, historial público de cuerpos anteriores o moderación por terceros.

### Bloque 3 — 24 de octubre: consistencia de operaciones

Añadidos tres escenarios sintéticos de regresión: un borrador conserva estado y privacidad cuando se retira su fuente citada; una retirada obsoleta no borra una edición vigente; restaurar una referencia privada ya utilizada no reactiva el cuerpo retirado. Recuperar el estado serializado mantiene estos resultados. Batería completa: **91 pruebas superadas**, incluidos los 33 ensayos HTTP anteriores. Verificación documental y diferencias sin errores.

No se han modificado datos del laboratorio, comportamiento de producción ni configuración del servidor. Los controles de accesibilidad y el rescate persistente de ediciones siguen pendientes; no se presentan como verificados en este bloque. Los cambios se conservan en la rama de la propuesta #2, sin integrar en main.

### Bloque 4 — 24 de octubre: catálogo propuesto de estadísticas

El [diseño de estadísticas](DISENO-ESTADISTICAS.md) concreta fuentes, audiencias, actualización y conservación de una primera fase de gestión de recursos y pendientes. Propone excluir recuentos de comportamiento en grupos, sin atribuir anonimato a un umbral numérico. El panel público se limita como candidato a declaraciones voluntarias y fechadas de servicios, con cobertura y caducidad explícitas; no mide por sí mismo disponibilidad ni capacidad global.

Diez casos de aceptación documentales quedan pendientes de ejecución si se aprueba desarrollar el catálogo. No se ha añadido captación, implementación ni acceso a datos del laboratorio. Verificación editorial de 48 documentos y diferencias sin errores; la batería funcional vigente sigue siendo de 91 pruebas, sin repetirla por este cambio exclusivamente documental. Catálogo enlazado en la documentación de la rama de #2 para revisión, no decisión ratificada.

### Siguiente bloque

Revisar accesibilidad de controles del editor y conflictos visibles entre pestañas con escenarios sintéticos. No convertir texto rescatado en publicación ni borrador sin acción explícita. La implementación de estadísticas queda pendiente de revisión del catálogo; la automatización no lo aprueba.

### Disciplina de continuidad

Inspeccionar rama, cambios locales y propuesta de revisión antes de continuar. La automatización no confirma por sí misma nuevas decisiones de producto. No empezar otro bloque tras el lunes 26; consolidar los resultados y límites. Registrar aquí las pruebas reales y el estado de publicación de cada bloque.
