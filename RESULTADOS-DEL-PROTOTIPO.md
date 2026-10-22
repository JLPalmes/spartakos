---
title: Spartakos — Resultados de la primera comprobación del prototipo
lang: es-ES
license: CC-BY-SA-4.0
version: 0.1
date: 2026-10-22
status: Diez pruebas locales del modelo superadas; sin validación con participantes
---

# Primera comprobación del prototipo

## 1. Artefacto y alcance

La [maqueta local](prototipo/README.md) permite recorrer Inicio, Explorar, Mi interés, Mi comunidad, Mi archivo y Mi cuenta y salida. No es una aplicación de red: usa contenido ficticio, memoria local y simulación de decisiones de varias personas. No demuestra autenticación, autorización real, portabilidad, cifrado ni capacidad.

## 2. Comprobaciones automáticas ejecutadas

Entorno: Node.js v22.23.4; sin dependencias externas. Ejecutado `node --test prototipo/modelo.test.mjs`: **10 pruebas superadas, 0 fallos**. Se han comprobado separación entre guardar y seguir, validación mínima de publicaciones, importación ficticia repetible, ausencia de apertura sin unanimidad, negativa, cambios de propuesta, expulsión elusiva y conservación de audiencia del historial.

Un defecto detectado durante revisión del modelo permitía perder protección si se cerraba la propuesta por una negativa y se expulsaba después a quien se había opuesto. Se corrigió conservando en la simulación la protección de las personas que causan baja. Se añadió una prueba específica. El modelo es deliberadamente conservador y no sustituye una política real de censo, memoria de membresía ni tratamiento de sus datos.

## 3. Comprobaciones en navegador ejecutadas

En navegador local de escritorio se observó:

- Escribir un borrador y guardar un interés conserva el texto sin publicar ni cambiar seguimiento.
- Una publicación marcada «Solo integrantes» aparece en la comunidad con indicación de acceso del operador.
- Intentar abrir sin consentimientos se bloquea.
- Dos consentimientos de tres siguen bloqueando la apertura.
- Tres consentimientos permiten la apertura simulada; la publicación anterior conserva su indicación de audiencia restringida.
- Importar el ejemplo y repetirlo mantiene una sola entrada ficticia y no crea un contacto activo.

La inspección reveló que una actualización de pantalla podía perder el borrador; se corrigió manteniéndolo durante la sesión. No se guarda al recargar. La [captura de la comunidad](prototipo/comunidad-verificada.png) documenta un estado observado; no prueba que un servidor real proteja contenido.

## 4. Revisión de autoridad

El [contrato preliminar](CONTRATO-DE-DATOS-Y-AUTORIDAD.md) separa titularidad, alojamiento, permisos, publicaciones, importación y acreditación. No se ha implementado. Su principal restricción es impedir que una función visible en la maqueta se convierta en una garantía falsa sobre infraestructura.

## 5. Límites y siguiente evidencia

Los guiones V01–V09 siguen sin ejecutarse con participantes. No se ha medido comprensión, utilidad al volver, presión social, experiencia móvil, accesibilidad completa, recursos voluntarios ni comparación operativa. Los 148 criterios de la matriz de producto permanecen **sin ejecutar**; no se contabilizan estas diez pruebas como cumplimiento de esos criterios.

Antes de laboratorio de producción y contribuciones externas, concretar la [apertura del desarrollo](PREPARACION-DE-APERTURA.md). Las licencias y el destino público iniciales están adoptados; no modifican los resultados ni convierten las comprobaciones locales en garantías de red.
