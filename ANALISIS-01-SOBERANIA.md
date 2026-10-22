---
title: Análisis 01 — Soberanía sobre identidad y publicaciones
lang: es-ES
license: CC-BY-SA-4.0
date: 2026-10-21
status: Investigación documental inicial; propuestas pendientes de deliberación y pruebas
---

# Soberanía sobre identidad y publicaciones

> Alcance: la interoperabilidad entre redes no es un requisito. Sí lo son la migración desde las redes populares hacia esta red, superando la pérdida de historial y contactos, y el derecho posterior a irse. Las comparaciones de compatibilidad de este documento son antecedentes técnicos; no justifican exigir federación, puentes ni comunicación permanente con redes externas. Véase REQUISITOS-MIGRACION.md.

## 1. Alcance y método

Este bloque examina la continuidad de la identidad y de las publicaciones al cambiar o perder un proveedor. Incluye Hubzilla, la línea Streams/Nomad, extensiones de portabilidad de ActivityPub, AT Protocol, Nostr, Solid, Diaspora*, Friendica, SSB/Manyverse e IndieWeb. Mastodon se utiliza como referencia de migración parcial. No constituye todavía el estudio completo de comunidades, algoritmos, reputación, economía o gobernanza.

Se distinguen cuatro niveles de evidencia: especificación, documentación de una implementación, incidencias de usuarios y comprobación mediante pruebas. Esta entrega alcanza los tres primeros, con distinta cobertura según proyecto. No se han realizado migraciones reales ni pruebas de usabilidad. Una función documentada no se considera por ello universalmente desplegada, segura o sencilla.

No se atribuyen causas de crecimiento o abandono sin evidencia específica. La documentación de un proyecto sirve para examinar sus mecanismos, pero no para demostrar por sí sola sus resultados sociales. Las conclusiones de diseño de este documento son razonamientos propios y se presentan como propuestas.

## 2. Descomposición del requisito

| Código | Garantía que hay que evaluar | Falso equivalente que debe evitarse |
| --- | --- | --- |
| S01 | Mantener la identidad reconocida al trasladarse | Crear otra cuenta con el mismo nombre visible |
| S02 | Mantener un nombre público o disponer de una transición verificable | Confundir el nombre con el identificador persistente |
| S03 | Continuar publicando tras perder al proveedor | Conservar solo una copia consultable |
| S04 | Restaurar publicaciones y adjuntos | Exportar texto con imágenes que siguen dependiendo del servidor antiguo |
| S05 | Mantener referencias a publicaciones, respuestas y menciones | Volver a publicar el historial con identificadores nuevos |
| S06 | Mantener relaciones compatibles y preferencias de seguridad | Llevarse una lista de nombres sin continuidad efectiva |
| S07 | Recuperar el control tras pérdida de acceso | Suponer que tener una clave elimina el problema de recuperación |
| S08 | Revocar dispositivos y credenciales comprometidas | Cambiar una contraseña que no invalida otros accesos |
| S09 | Corregir y retirar contenido en servicios participantes | Garantizar la eliminación de cualquier copia externa |
| S10 | Mantener la privacidad durante exportación y migración | Convertir datos privados en un archivo sin protección |
| S11 | Poder elegir servicios independientes | Tener distintos nombres comerciales bajo la misma dependencia |
| S12 | Poder separar identidades y abandonar una de ellas | Imponer un identificador personal correlacionable en toda actividad |

Estas garantías pueden entrar en conflicto. La persistencia pública facilita el reconocimiento, pero también el seguimiento entre contextos. La replicación aumenta disponibilidad, pero multiplica custodios y superficies de exposición. La recuperación asistida facilita el uso, pero concede poder a quienes pueden autorizarla.

## 3. Antecedentes y límites documentados

### Hubzilla y la línea Streams/Nomad

Hubzilla documenta canales como identidades, traslado y clonación entre hubs. La clonación mantiene identidad y datos en más de una ubicación. Es un antecedente directo de continuidad, no una simple exportación. Su documentación distingue capacidades nativas de las conexiones con otras redes, donde puede haber pérdida de funciones. [Conceptos](https://help.hubzilla.hu/en/basicconcepts.html), [compatibilidad](https://hub.hubzilla.hu/help/member/connections).

**Lectura para el proyecto:** una copia operativa previa puede proteger mejor frente a un cierre repentino que una migración iniciada después. Sin embargo, hay que comprobar cobertura de archivos, sincronización, revocación de un clon comprometido y comportamiento con contactos externos. No está demostrado aquí que un clon incluya todo tipo de dato ni que la interfaz sea adecuada para el público deseado.

Streams/Nomad pertenece a esta línea, pero no debe darse por idéntico a Hubzilla ni deben trasladarse afirmaciones entre versiones y derivados. El repositorio intentado no resultó accesible en esta revisión. La referencia histórica se ha contrastado mediante FEP-ef61; falta una ficha por implementación con versión, mantenimiento y pruebas.

### ActivityPub y objetos portables

ActivityPub define intercambios entre clientes y servidores y entre servidores. No debe confundirse ese alcance con una garantía uniforme de migración. FEP-ef61 propone objetos e identidades con identificadores independientes del servidor; la página consultada lo clasifica como borrador y enumera implementaciones. [ActivityPub](https://www.w3.org/TR/activitypub/), [FEP-ef61](https://fediverse.codeberg.page/fep/fep/ef61/).

**Lectura para el proyecto:** no sería correcto descartar todo el ecosistema por las limitaciones de una aplicación. Tampoco sería correcto asumir compatibilidad general por existir una extensión. Hay que comprobar negociación de capacidades, comportamiento con sistemas que no la entienden y manejo de referencias y archivos.

### AT Protocol / Bluesky

AT Protocol distingue el nombre legible de un identificador persistente. Su guía contempla trasladar repositorio, archivos y ciertas preferencias. La recuperación con un proveedor inaccesible exige condiciones de control de identidad y disponibilidad de copias: puede conservarse la identidad sin recuperar el contenido. Parte del estado de servicios externos queda fuera del traslado del alojamiento. La propia guía advierte que sus mecanismos concretos de migración no constituyen una parte formal del protocolo. [Identidad](https://atproto.com/guides/identity), [migración](https://atproto.com/guides/account-migration).

**Lectura para el proyecto:** distinguir nombre, identidad, alojamiento y aplicaciones es una base conceptual útil. Deben evaluarse separadamente recuperación, distribución, datos privados y permisos comunitarios; una guía de migración de alojamiento no los resuelve todos. Hay que medir también cuánto control independiente se entrega realmente durante el alta ordinaria.

### Nostr

El protocolo básico vincula eventos firmados a una clave pública y utiliza relays. Esto permite reconocer autoría independientemente de un relay concreto. NIP-09 describe solicitudes de borrado, sin garantía de eliminar todas las copias. La extensión opcional NIP-B7 contempla localizar archivos por su huella en servidores Blossom alternativos. [NIP-01](https://raw.githubusercontent.com/nostr-protocol/nips/master/01.md), [NIP-09](https://raw.githubusercontent.com/nostr-protocol/nips/master/09.md), [NIP-B7](https://raw.githubusercontent.com/nostr-protocol/nips/master/B7.md).

**Lectura para el proyecto:** autonomía de autoría no equivale a custodia suficiente de archivos, recuperación ni distribución garantizada. Debe evaluarse qué ocurre con una clave perdida o robada y qué extensiones entienden los clientes elegidos. No se afirma que todo el ecosistema carezca de soluciones de recuperación; no están acreditadas aquí como garantía común.

### Solid

Solid separa aplicaciones y datos almacenados en Pods, con acceso autorizado. Su especificación regula recursos, identidad y autorización, pero no acredita por sí sola una migración social completa que conserve todas las referencias. La edición consultada es un informe de grupo comunitario, no una Recomendación W3C. [Proyecto](https://solidproject.org/about), [protocolo](https://solidproject.org/TR/protocol).

**Lectura para el proyecto:** resulta especialmente relevante para elegir proveedores de funciones sobre datos controlados por el usuario. Hay que probar qué ocurre al cambiar dominios, identidad y almacenamiento, y cómo varias aplicaciones interpretan el mismo modelo social. Compartir un formato no garantiza compartir su significado.

### Diaspora*

Las notas oficiales incluyen importación de cuentas y tratamiento de mensajes de migración; sería incorrecto repetir sin revisión que el proyecto nunca desarrolló mecanismos de traslado. Esas notas no permiten certificar su cobertura actual de historial, adjuntos y relaciones. Las páginas de ayuda intentadas no fueron accesibles. [Versiones oficiales](https://github.com/diaspora/diaspora/releases).

**Lectura para el proyecto:** queda pendiente comprobar el flujo en una versión concreta. Exportación, recepción de avisos de migración e importación de cuenta son capacidades diferentes. No se asigna una puntuación de portabilidad basándose únicamente en el registro de cambios.

### Friendica

La ayuda de una instancia describe un traslado experimental mediante exportación/importación que incluye datos de cuenta, contactos, círculos, preferencias y claves secretas, con diferencias según la red de los contactos. Una petición abierta de 2026 reclama una migración completa y sencilla; es evidencia de una dificultad comunicada, no una medición representativa. [Ayuda de traslado](https://friendica.michael-mints.ru/help/Move-Account), [incidencia 15627](https://github.com/friendica/friendica/issues/15627).

**Lectura para el proyecto:** conviene evaluar por separado cobertura técnica, seguridad del archivo exportado y facilidad del proceso. La interoperabilidad multiprotocolo no debe presentarse como conservación automática de todas las relaciones y funciones.

### Secure Scuttlebutt / Manyverse

Manyverse documenta almacenamiento local y sincronización entre dispositivos de participantes. Su FAQ señala que no es posible borrar las publicaciones de la red; eliminar la cuenta local no equivale a retirar las copias distribuidas. Se trata de un compromiso de diseño directamente relevante para nuestro concepto de control del autor. [Modelo](https://www.manyver.se/), [permanencia](https://www.manyver.se/faq/permanence/), [eliminación de cuenta](https://www.manyver.se/faq/account-deletion/).

**Lectura para el proyecto:** funcionar sin un alojamiento central y funcionar sin conexión aportan autonomía, pero no bastan para cumplir nuestros requisitos. Antes de adoptar esta línea serían necesarias pruebas de recuperación, uso desde varios dispositivos y retirada de contenido. No se debe generalizar esta limitación a cualquier sistema entre pares.

### IndieWeb / POSSE

POSSE propone publicar primero en un sitio propio y distribuir copias o enlaces a otros servicios, manteniendo un camino hacia el original. Es una estrategia de publicación y convivencia, no un protocolo completo de identidad o comunidades. [POSSE](https://indieweb.org/POSSE).

**Lectura para el proyecto:** permite pensar una transición sin exigir que todos los contactos se muden a la vez. El control del original no concede control sobre respuestas o copias externas. Además, un dominio propio continúa teniendo costes, renovación, seguridad y dependencia de registro.

### Mastodon como referencia de cobertura parcial

Su documentación permite trasladar seguidores y exportar listas, pero no importar publicaciones y archivos en la nueva cuenta. Este límite no se atribuye por extensión a ActivityPub ni a todas sus aplicaciones. [Migración](https://docs.joinmastodon.org/user/moving/).

**Lectura para el proyecto:** hay que definir la unidad de continuidad: identidad, relaciones, publicaciones o vida social completa. Una función denominada «migrar» puede cubrir solo parte de ella.

## 4. Comparación de enfoques

La tabla resume mecanismos descritos arriba; no certifica prestaciones universales.

| Enfoque | Principal aportación | Dependencia que exige investigar |
| --- | --- | --- |
| Identidad con copias operativas — Hubzilla/línea Nomad | Continuidad mediante más de una ubicación | Clones, sincronización, custodia y compatibilidad externa |
| Identificador separado del alojamiento — AT Protocol | Traslado sin sustituir la identidad canónica | Control de actualización, copias y servicios externos |
| Eventos firmados y relays — Nostr | Autoría independiente del relay | Credenciales, retención de eventos y archivos |
| Aplicaciones sobre almacenamiento autorizado — Solid | Separación entre datos y servicios | Direcciones, identidad y modelos de datos compatibles |
| Exportación/importación — Diaspora*/Friendica | Mecanismos de traslado dentro de sus condiciones | Cobertura actual y participación de cada sistema remoto |
| Réplica local entre pares — SSB/Manyverse | Uso local y menor dependencia de alojamiento | Dispositivos, recuperación, almacenamiento y permanencia |
| Sitio propio con distribución — IndieWeb/POSSE | Control del original y convivencia | Dominio, alojamiento e integración con servicios externos |
| Traslado parcial — Mastodon | Continuidad de seguidores bajo condiciones | Historial no reimportable y dependencia del origen |

No hay base para declarar un ganador. El requisito de comunidades privadas puede alterar la preferencia que resultase de evaluar únicamente publicaciones públicas.

## 5. Problemas que nuestro diseño debe resolver

### Identidad y nombre no son lo mismo

Una identidad persistente puede continuar aunque cambie su nombre. Si el nombre pertenece al dominio de un proveedor, conservarlo dependerá también de ese dominio. Propuesta: distinguir claramente identidad interna, nombre público y credenciales. No exigir comprar un dominio para acceder a derechos fundamentales.

### La copia debe existir antes del desastre

La firma prueba procedencia, no reconstruye un archivo perdido. Propuesta: ofrecer copia independiente programada, con estado visible y una prueba de restauración. Hay que definir quién la paga, quién puede leerla y cuánto historial puede perderse entre copias. Una réplica que obedece inmediatamente un borrado malicioso tampoco basta como respaldo de recuperación.

### Recuperar sin crear una autoridad omnipotente

Opciones a comparar: secreto de recuperación, segundo dispositivo, personas de confianza, custodio independiente o una combinación. Cada una introduce costes de uso y ataques diferentes. Propuesta: credenciales de publicación separadas de la autorización de cambios críticos, revocación y avisos por vías independientes. Los mecanismos exactos quedan abiertos a modelado de amenazas.

### Marcharse no garantiza audiencia

El usuario puede mantener identidad y contenido sin que un buscador, recomendador o comunidad los muestre. Propuesta: distinguir portabilidad de cuenta y acceso a distribución. No prometer audiencia garantizada ni permitir que un único distribuidor se convierta en vía exclusiva de participación.

### Datos propios y conversaciones compartidas

Una respuesta tiene autor y permisos propios. Su inclusión en una exportación no implica permiso para republicarla en otra audiencia. Propuesta: conservar referencias y procedencia; no transformar respuestas ajenas en contenido propio ni hacer públicos intercambios privados al migrar.

### Retirar no equivale a reescribir la historia ajena

Propuesta: distinguir borrado del original, propagación de solicitudes a servicios participantes, desindexación y caducidad de copias de seguridad. Los plazos se tendrán que definir. Las respuestas pueden conservar una referencia a contenido retirado sin reproducirlo. Las capturas y los servicios ajenos quedan fuera de una garantía absoluta.

### La salida también es colectiva

Además del usuario, una comunidad puede quedar cautiva de su alojamiento. Su traslado requiere reglas sobre quién lo autoriza, miembros, roles, historial y copias. Propuesta: tratar la portabilidad comunitaria como requisito separado, sin que un administrador pueda apropiarse de las identidades personales ni ampliar la audiencia del historial.

## 6. Escenarios de aceptación propuestos

Son requisitos para evaluar y deliberar, no pruebas ya superadas.

| Escenario | Resultado que debería verificarse | Fallo que no debe ocultarse |
| --- | --- | --- |
| Cambio voluntario de proveedor | Identidad y referencias estables; inventario de datos trasladados | Adjuntos perdidos o preferencias reiniciadas sin aviso |
| Cierre sin aviso | Recuperación desde medios independientes del origen | Recuperar el nombre pero perder silenciosamente el historial |
| Proveedor que no coopera | Poder autorizar continuidad sin su permiso, si se conserva la autoridad de recuperación | Depender de un correo o una clave que solo posee el origen |
| Teléfono perdido | Recuperar acceso y revocar el dispositivo | Permitir que el dispositivo perdido siga actuando |
| Credencial robada | Contener el incidente y demostrar la transición válida | Confundir acciones del atacante con voluntad del titular |
| Error durante el traslado | Reanudar o volver a un estado conocido, sin doble autoría contradictoria | Dos ubicaciones activas con estados incompatibles |
| Exportación privada | Archivo protegido, inventario y restauración verificable | Filtrar contactos, intereses privados o claves |
| Cambiar o retirar una publicación | Procesamiento por participantes con estado comprensible | Presentar como confirmado lo que solo es una solicitud |
| Expulsión de una comunidad | Perder permisos locales sin perder la identidad de toda la red | Que salir del proveedor borre automáticamente sanciones o bloqueos válidos |
| Traslado de comunidad | Autoridad y permisos conservados según sus reglas | Apropiación del historial por una persona o cambio de audiencia |

Los criterios deberán incorporar tiempos máximos, pérdida admisible de cambios, costes, proporción de traslados completos y tasa de éxito sin asistencia. No se fijan cifras arbitrarias antes de conocer usuarios, volumen y presupuesto.

## 7. Alternativas a deliberar

1. Extender una solución cercana a Hubzilla/Nomad: investigar primero clonación, permisos y experiencia; no asumir que su adopción limitada invalida la arquitectura.
2. Apoyarse en identidad y repositorios de AT Protocol: investigar recuperación, privacidad y comunidades antes de considerar cubierta la soberanía.
3. Separar almacenamiento al estilo Solid y añadir una capa social: investigar significado compartido de datos y continuidad de direcciones.
4. Adoptar eventos firmados y distribución redundante al estilo Nostr: investigar recuperación, moderación, archivos y retirada.
5. Integrar componentes existentes en una arquitectura propia: solo justificable tras demostrar requisitos incompatibles con las anteriores; implica financiar seguridad, compatibilidad y mantenimiento.

No se recomienda todavía una opción ni se propone blockchain como requisito. El criterio de elección será qué garantías verificables ofrece cada alternativa al público previsto y con qué costes de uso y operación.

## 8. Pendientes y límites de esta entrega

- Verificar versiones y capacidades actuales de Streams y derivados mediante sus repositorios; el acceso falló en esta revisión.
- Comprobar una migración de Diaspora* y otra de Friendica, con inventario antes y después; las fuentes disponibles no certifican cobertura total.
- Probar clones de Hubzilla y contactos en otras redes, incluyendo archivos privados y retirada de un clon.
- Evaluar AT Protocol con control de recuperación independiente y sin proveedor original, incluyendo archivos y estado externo.
- Probar clientes Nostr concretos y sus extensiones; no trasladar garantías de una propuesta opcional a todo cliente.
- Probar traslado de almacenamiento e identidad en Solid con referencias de otra aplicación.
- Evaluar recuperación y uso multidispositivo de Manyverse; su FAQ de permanencia sí acredita el límite de borrado descrito.
- Incorporar estudios empíricos de uso y evolución antes de explicar resultados de adopción.
- Ampliar el registro general con Lens, Farcaster, DeSo y otros antecedentes al analizar sus familias; no se consideran evaluados por este bloque.

La siguiente decisión de diseño requiere deliberar qué garantías de S01–S12 son innegociables. Este análisis propone un marco y alternativas pendientes de evaluación.
