---
title: Spartakos — Preparación del desarrollo abierto
lang: es-ES
license: CC-BY-SA-4.0
version: 0.1
date: 2026-10-22
status: Licencias y destino público adoptados; canal privado atendido pendiente
---

# Preparación del desarrollo abierto

## 1. Apertura inicial

Publicar especificaciones y maqueta descartable junto a una declaración de etapa: investigación y prototipo, sin servicio operativo ni garantías de privacidad. Mantener el desarrollo de producción abierto desde su primer trabajo compartido. No esperar a completar una red utilizable.

Repositorio de referencia: [JLPalmes/spartakos](https://github.com/JLPalmes/spartakos). El titular inicial custodia la publicación, sin adquirir propiedad del proyecto social. GitHub es el proveedor inicial; no es requisito de arquitectura. Un espejo sigue pendiente de despliegue.

## 2. Licencias adoptadas

| Material | Licencia adoptada | Razón y límite |
| --- | --- | --- |
| Servicio y maqueta de experiencia | AGPL-3.0-or-later | Favorecer disponibilidad de modificaciones en usos de red conforme a la licencia; no obliga a financiar servidores |
| SDK y bibliotecas independientes para integración | Apache-2.0 | Facilitar clientes y servicios diversos; delimitar componentes y compatibilidad antes de extraer código |
| Documentación original | CC-BY-SA-4.0 | Permitir adaptación con atribución y condiciones de compartir igual; no relicencia materiales ajenos enlazados |

Las licencias fueron adoptadas el 22 de octubre de 2026. El [mapa de licencias](LICENCIAS.md), los textos completos y los avisos de archivo establecen su aplicación. No hay una licencia propia ni una restricción comercial añadida.

La AGPL contiene obligaciones específicas sobre versiones modificadas usadas a través de una red, pero no regula la reciprocidad de infraestructura de Spartakos. Apache-2.0 incluye permisos y condiciones propios, entre ellos disposiciones de patentes. CC BY-SA permite reutilización comercial y exige sus condiciones de atribución y compartir igual. Fuentes: [AGPL publicada por OSI](https://opensource.org/license/agpl-3.0), [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

Se incorporan textos canónicos completos, mapa por rutas e identificadores SPDX. Los avisos de terceros deben conservarse cuando corresponda. No modificar las licencias para imponer financiación, aprobación de clientes o cesión exclusiva al promotor. La elección no decide marcas, contratos de servicio ni derechos sobre publicaciones de participantes.

## 3. Contribución preparada

Primeras tareas que no requieren acceder a datos personales: revisión de recorridos, accesibilidad de la maqueta, pruebas del censo, revisión del contrato de autoridad, formatos de exportación sintéticos y documentación de instalación. No presentar «construir la descentralización» como una tarea inicial pequeña.

Cada propuesta debe explicar problema, comportamiento esperado, prueba y límites. Identificar requisito confirmado o decisión afectada. Los cambios de interfaz no pueden introducir por comodidad métricas de presión, ampliación de audiencias ni exigencia de pago para derechos básicos.

Las aportaciones se reciben bajo la licencia del material al que contribuyen, según LICENCIAS.md y CONTRIBUTING.md. No exigir cesión exclusiva por defecto. Revisar procedencia de dependencias y no aceptar secretos, exportaciones personales ni capturas de comunidades reales como pruebas públicas.

## 4. Seguridad y conducta

El primer repositorio necesita indicar claramente que no existe servicio de producción y que la maqueta no protege datos reales. Antes de ofrecer reporte privado de vulnerabilidades hay que configurar un canal atendido y sus responsables; no inventar una dirección de correo ni prometer plazos sin capacidad.

En la colaboración: crítica a propuestas permitida, acoso y publicación de datos privados no; investigación por responsables sin conflicto y recurso cuando exista capacidad. Antes de invitar participantes, identificar quién atiende incidentes. Este borrador no afirma que ya exista equipo de seguridad ni moderación.

## 5. Preparado y pendiente

Preparado: especificación, registro de decisiones, aceptación, guiones de validación, contrato de datos, maqueta con pruebas, reporte de comprobaciones, [guía de contribución](CONTRIBUTING.md) y [política de seguridad de esta etapa](SECURITY.md). Adoptados: destino público y licencias iniciales. Pendiente: configurar un canal privado atendido, incorporar mantenedores y desplegar espejos. Estos datos no pueden inferirse de una simulación local ni atribuirse al conjunto de la futura red.
