---
title: Spartakos — Propuesta de resolución de pendientes
lang: es-ES
license: CC-BY-SA-4.0
version: 0.1
date: 2026-10-22
status: Recomendaciones de diseño; no ratificación ni validación experimental
---

# Propuesta de resolución de pendientes

## 1. Resultado y límite

Se recomienda construir una red de alojamientos sustituibles, con identidad separada, clientes compatibles y una base gratuita limitada por recursos comprometidos. La reciprocidad debe ensayarse como condición de acceso a prestaciones comunes adicionales, antes de considerar obligaciones generales. La acreditación debe verificar afirmaciones concretas y permitir impugnaciones; no constituir una autoridad universal sobre la veracidad de las personas.

Este documento concreta las 29 cuestiones del registro. Una recomendación permite avanzar en el diseño, pero no sustituye pruebas, adhesión de operadores, revisión jurídica ni adopción del gobierno. Los requisitos confirmados prevalecen. Las alternativas funcionales siguen disponibles para comparación.

## 2. Identidad y autoridad: Q01–Q03

**Recomendación:** separar tres controles: firmar actividad cotidiana, cambiar alojamiento y recuperar el control perdido. El alojamiento no debe disponer por sí solo de las tres facultades. Ningún dominio comprado por el usuario será requisito para conservar identidad.

Comparar en laboratorio dos vías: reutilizar un sistema existente de identidad portable y desplegar una autoridad de continuidad independiente con controles plurales. La segunda describe un requisito de organización, no un protocolo criptográfico ya diseñado. No se propone inventar firmas, consenso ni recuperación propios.

AT Protocol aporta mecanismos documentados de identidad y traslado que merecen ensayo. Su alternativa `did:web` depende del dominio y no resuelve perderlo; la guía de migración distingue cambio de identidad, datos y servicios. Por tanto, adoptar una referencia persistente no basta para garantizar continuidad completa. Fuentes: [identidad](https://atproto.com/specs/did) y [migración](https://atproto.com/guides/account-migration).

**Puerta de decisión:** el candidato debe conservar la misma identidad ante un alojamiento hostil, sustituir al servicio de resolución conforme a un procedimiento verificable y evitar que recuperar identidad publique contenido cifrado. Si el mecanismo concreto no cumple, no anunciar independencia completa. No fijar un umbral como «dos de tres» hasta identificar fallos tolerados, colusión y operadores realmente independientes.

Durante un ensayo local pueden simularse custodios; en un piloto real deben declararse las dependencias existentes. Réplicas administradas por una sola organización no satisfacen independencia institucional.

## 3. Privacidad y resistencia: Q04, Q14 y Q15

**Recomendación:** tres modos explícitos: público, restringido accesible al operador y cifrado de extremo a extremo. No presentar el segundo como solución suficiente para conversaciones cuyo riesgo requiere el tercero. El piloto sin E2EE debe limitar su alcance y advertirlo antes de crear espacios privados.

Para E2EE, ensayar entrada y expulsión de miembros, dispositivos perdidos, búsqueda local, recuperación y denuncias parciales. Definir qué historial puede descifrar cada incorporación; recuperar la cuenta no garantiza recuperar las claves del historial. La protección frente a vigilancia incluye metadatos, distribución del cliente y resolución de identidad, además del contenido.

La apertura pública exige revisar el [modelo de amenazas](VIGILANCIA-Y-CENSURA.md). Los usos de alto riesgo quedan fuera de las garantías hasta disponer de pruebas y revisión independiente; no basta con añadir una conexión alternativa.

## 4. Operación, recursos y responsabilidad: Q05–Q08

**Recomendación:** admitir cuentas según capacidad comprometida y comprobada, sin prometer una cuota universal todavía. El [programa de operadores](OPERACION-Y-VOLUNTARIADO.md) define inventario, carga, reserva y salida. La lista de espera es preferible a convertir funciones básicas en servicios exclusivamente de pago.

El piloto requiere identificar al responsable de cada servicio y de la atención de incidentes. Antes de apertura pública, revisar jurisdicción, responsabilidades, conservación, protección de datos y procedimiento ante requerimientos con asesoramiento competente. No atribuir personalidad jurídica a «la red» ni suponer que descentralizar elimina obligaciones.

Para el gobierno, recomendar poderes limitados por ámbito y mandatos temporales. Ni aportaciones económicas ni reputación otorgan votos adicionales. No iniciar una votación constitucional abierta sin resolver duplicación de identidades, elegibilidad, impugnaciones y representación de usuarios ausentes. El [borrador de acreditación](GOBIERNO-DE-LA-ACREDITACION.md) ofrece un procedimiento provisional acotado, no un sistema electoral definitivo.

## 5. Cuenta huérfana: Q09

Propuesta de procedimiento: solicitud fundada; comprobación de que los canales de recuperación previstos se han agotado; aviso por canales previamente registrados; revisión por persona distinta de quien propone la marca; resolución motivada e impugnable. El silencio o la inactividad, por sí solos, nunca bastan. Una denuncia externa puede abrir una revisión, pero no legitima declarar la pérdida de control.

La marca pública solo indicará «Control no recuperado según revisión de [fecha]», sin revelar pruebas privadas, ni afirmar fallecimiento, abandono voluntario o apropiación por terceros. Si no hay evidencia suficiente, el expediente queda sin conclusión y no se publica la marca. Una prueba posterior válida de control permite retirarla y deja constancia restringida de la rectificación. El estado no transfiere cuenta, publicaciones ni membresías a nadie.

## 6. Código abierto e importación: Q10–Q13 y Q29

Actualización de apertura: adoptadas AGPL-3.0-or-later para servicio/prototipo, Apache-2.0 para futuras bibliotecas independientes con aviso y CC-BY-SA-4.0 para documentación original. Alcance y textos completos en [LICENCIAS.md](LICENCIAS.md). Se mantiene revisión de derechos y compatibilidad para incorporaciones. Antes de aceptar contribuciones debe existir licencia efectiva y una política de aportaciones coherente; no exigir cesión exclusiva al promotor como condición general.

La reciprocidad no debe añadirse como prohibición comercial a la licencia del código. La definición de open source permite uso comercial y redistribución; las condiciones de prestaciones concretas deben estudiarse por separado. [Definición de la OSI](https://opensource.org/osd).

Preparación local: alcance, guía de contribución, registro de decisiones y criterios de aceptación ya disponibles. La apertura efectiva necesita titular del repositorio, licencia elegida y canal de incidencias de seguridad atendido. No publicar datos de participantes ni fingir un canal operativo sin responsables.

Para cada importador: conservar el archivo de origen bajo control del usuario, generar inventario previo, explicar exclusiones y procesar con reintentos sin duplicar. Separar fecha original y fecha de importación. No convertir conversaciones privadas en publicaciones públicas. Contactos importados son referencias de origen hasta vinculación confirmada, nunca cuentas activas fabricadas. No se promete importación directa por API sin comprobar acceso y permisos vigentes.

## 7. Referencias, interacciones e historial: Q16–Q19

**Q16:** nombre mostrado no exclusivo; identidad técnica persistente; enlace compartible que resuelva mediante servicios sustituibles. Los alias legibles son auxiliares y recuperables conforme a su ámbito, no la raíz de propiedad. Las menciones se vinculan a identidad, no a texto reutilizable por otra persona. El formato final del enlace depende de Q01. Perfil no listado por defecto para quien solo participa en privadas; una intervención pública muestra la identidad necesaria para entenderla, sin abrir el resto del perfil.

**Q17:** probar primero responder, guardar en privado y seguir como base. Comparar una variante con «coincido» graduado y otra sin reacción rápida. No vincular acuerdo a reputación ni ordenar por su volumen. Los reconocimientos temáticos deben competir en la prueba con una alternativa sencilla: aportaciones seleccionadas por su autor, identificadas como tales.

**Q18:** fijar la audiencia al publicar. Ampliarla requiere una acción separada, advertencia y revisión de permisos; nunca arrastrar respuestas ajenas. Conservar contexto de edición sin ofrecer acceso indiscriminado a datos sensibles retirados. La regla de historial de una comunidad debe ser visible antes de entrar. Si cambia para futuros miembros, no ampliar acceso a contenido anterior sin autorización de quienes corresponda. El detalle de retención de copias y pruebas de abuso exige política propia, no una promesa de borrado instantáneo universal.

**Q19:** al proponer apertura, congelar el censo y la versión exacta de la propuesta. Todos los integrantes deben consentir expresamente; ausencias e identidades irrecuperables bloquean la apertura. Altas, bajas o expulsiones suspenden el procedimiento y obligan a revisar el censo. Reiniciarlo no elimina derechos de las personas excluidas para eludir su negativa: la auditoría debe mantenerlas como afectadas por la transformación. Una negativa cierra la propuesta; no reintentar automáticamente ni presionar con avisos. La alternativa es crear otra comunidad pública, sin trasladar miembros ni contenido sin permiso. Incluso con unanimidad, proteger el historial requiere permisos separados de sus autores, incluidos antiguos integrantes.

## 8. Adopción y comparación: Q20–Q22

Recomendar una primera sesión que permita leer una comunidad útil, conservar algo de interés y volver a una conversación, sin importar nada ni encontrar contactos existentes. La importación es una ayuda de continuidad, no una fuente suficiente de actividad.

Antes de declarar ventajas, ejecutar tareas equivalentes frente a soluciones existentes: entrada individual, comprensión de privacidad, traslado con origen caído y mantenimiento de un servicio pequeño. Medir fallos, intervención de ayuda, tiempo, carga operativa y comprensión; no limitarse a preferencias estéticas. El [protocolo de validación](VALIDACION-Y-PUERTAS-DE-AVANCE.md) establece resultados que pueden descartar el diseño.

## 9. Reciprocidad y acreditación: Q23–Q28

**Q23:** comenzar con un programa voluntario de prestaciones adicionales comunes: distribución publicitaria identificada, directorio de servicios y capacidades adicionales acordadas. El acceso ordinario a identidades y publicaciones autorizadas debe seguir disponible a clientes compatibles, con límites técnicos neutrales. No recomendar bloquear toda una aplicación por desacuerdo comercial.

**Q24:** calcular contribución sobre demanda atribuible y capacidad neta utilizable. Separar reservas para sus propios clientes, redundancia comprometida y oferta libre. La condición institucional o el número de seguidores no bastan para exigir una aportación: deben estudiarse por separado uso de recursos y oferta organizada de servicios. No equiparar opinión política, prensa pequeña o una asociación sin recursos a una gran operación publicitaria.

**Q25–Q27:** varios comprobadores bajo un marco público, con declaración de conflictos, revisión independiente y financiación separada del resultado. No basta con que cada proveedor elija al auditor más permisivo. El [borrador de gobierno](GOBIERNO-DE-LA-ACREDITACION.md) desarrolla selección y recursos. Sigue siendo necesaria una autoridad legítima para adoptar el marco: la firma de una credencial no la crea. El modelo W3C estructura afirmaciones de emisores y su verificación técnica; no decide qué emisores debe aceptar Spartakos. [W3C VC 2.0](https://www.w3.org/TR/vc-data-model-2.0/).

**Q26:** distinguir remuneración o contraprestación por difusión, patrocinio, promoción propia identificada y opinión personal. Un enlace favorable o una discrepancia no son prueba de pago. Las consecuencias requieren evidencia de la conducta y posibilidad de respuesta, evitando recopilar comunicaciones privadas indiscriminadamente.

**Q28:** una credencial caducada no equivale a fraude. Diferenciar disputa, indisponibilidad del emisor y revocación fundada. La revisión afecta primero a la prestación condicionada, con conservación de lectura, exportación y traslado. Los plazos propuestos constan en el borrador; deben probarse contra capacidad real de atención antes de comprometerlos.

## 10. Qué queda pendiente y por qué

| Dependencia | Resultado necesario | Estado |
| --- | --- | --- |
| Decisiones de diseño | Revisar estas recomendaciones frente a los requisitos | Propuesta preparada |
| Participantes | Sesiones observadas con consentimiento | Protocolo preparado; no realizadas |
| Operadores | Capacidad, responsables y compromisos verificables | Ficha preparada; sin adhesiones |
| Identidad y E2EE | Ensayos y revisión de seguridad | Casos definidos; sin ejecución |
| Importación | Archivos consentidos y formatos comprobados | Sin corpus real |
| Gobierno y licencias | Licencias adoptadas; gobierno de la red y compatibilidad de incorporaciones requieren revisión propia | Licencias aplicadas; gobierno sin ratificación |
| Apertura pública | Repositorio de referencia JLPalmes/spartakos; canal privado atendido y pluralidad operativa pendientes | Apertura inicial; no servicio operativo |

No se exige resolver de antemano todos los futuros servicios comerciales. Sí se exige resolver los derechos y dependencias que la primera versión ya introduciría.
