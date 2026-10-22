---
title: Spartakos — Seguridad durante la etapa de prototipo
lang: es-ES
license: CC-BY-SA-4.0
version: 0.1
date: 2026-10-22
status: Sin servicio de producción; canal privado pendiente de activación
---

# Seguridad durante la etapa de prototipo

Solo existe una maqueta local descartable con datos ficticios. No implementa identidad, autenticación, control real de acceso, cifrado, recuperación ni conexión a una red social. No introducir datos personales ni utilizarla para comunicaciones privadas.

No existen versiones de producción mantenidas ni compromisos de respuesta de un equipo de seguridad. Un control visible que simula permisos no es una barrera de seguridad; las acciones de varias personas están disponibles en una misma sesión deliberadamente para estudiar las reglas.

## Comunicar problemas

Antes de abrir la colaboración se activará un canal privado atendido, preferiblemente el mecanismo privado de vulnerabilidades del repositorio elegido cuando esté disponible. A fecha de este documento no hay dirección ni formulario privado operativo que se pueda recomendar. No publicar secretos, datos de terceros ni exportaciones reales en incidencias públicas.

Los defectos de la simulación que no requieran datos sensibles podrán documentarse con pasos reproducibles y contenido ficticio cuando exista el repositorio. Indicar versión, entorno, resultado esperado, resultado observado y alcance. No afirmar que una prueba local demuestra una vulnerabilidad de una red que todavía no se ha implementado.

## Condiciones antes de producción

La apertura de código no acredita seguridad. Identidad, recuperación, dispositivos, permisos distribuidos, restauraciones y cifrado requieren ensayos propios y revisión conforme al [protocolo de validación](VALIDACION-Y-PUERTAS-DE-AVANCE.md). No se ofrecen garantías para usos de alto riesgo basadas en esta maqueta.
