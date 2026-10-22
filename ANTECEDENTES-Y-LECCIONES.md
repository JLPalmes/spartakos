---
title: Spartakos — Antecedentes y lecciones de diseño
lang: es-ES
license: CC-BY-SA-4.0
version: 0.1
date: 2026-10-22
status: Revisión documental con cobertura desigual; sin conclusiones causales universales
---

# Antecedentes y lecciones

## Método

No se identifica éxito únicamente con número de cuentas ni fracaso con tamaño reducido. Una iniciativa puede servir bien a su público y no resolver nuestro problema. Se distinguen mecanismos documentados, limitaciones reconocidas y resultados de adopción. Esta revisión acredita principalmente los primeros; no contiene un estudio empírico exhaustivo de todas las iniciativas existentes.

La lección de diseño es razonamiento propio, no un hecho demostrado sobre las causas de evolución del proyecto. Los antecedentes no convierten interoperabilidad externa en requisito.

## Antecedentes directamente utilizados

| Iniciativa o familia | Evidencia examinada | Lección aplicada a la especificación |
| --- | --- | --- |
| Hubzilla | Documenta canales como identidades, traslado y clonación; capacidades de permisos dependen del tipo de conexión | Copia operativa y control de acceso merecen ensayo; no asumir que portabilidad significa lo mismo en todos los contextos |
| Streams/Nomad y extensiones de objetos portables | FEP-ef61 recoge antecedentes y propone identificadores independientes del servidor; es borrador | No descartar toda una arquitectura por una aplicación; distinguir extensión e implantación general |
| Mastodon | Documenta traslado de seguidores y exportaciones, pero no reimportación del historial de publicaciones/medios | Medir continuidad de historial y vínculos por separado; no dar por resuelta la salida por existir un botón |
| AT Protocol/Bluesky | Separa componentes y documenta migración/recuperación con condiciones | La separación conceptual no elimina concentración práctica en identidad, entrega o aplicación |
| Nostr | Eventos firmados y relays; solicitudes de retirada sin garantía de eliminar todas las copias | Autoría, conservación, recuperación y retirada son garantías diferentes |
| Solid | Distingue aplicaciones, identidad y almacenamiento autorizado | Compartir almacenamiento no basta para acordar significado, permisos y referencias sociales |
| Diaspora* | Notas oficiales incluyen tratamiento de migración e importación; cobertura completa no certificada aquí | Evitar diagnósticos antiguos repetidos sin verificar versión y flujo actual |
| Friendica | Ayuda de traslado con diferencias por red de contacto; incidencia de usuario sobre facilidad de traslado | Interconexión, cobertura de datos y sencillez requieren evaluaciones separadas |
| SSB/Manyverse | FAQ reconoce limitaciones de borrado derivadas de copias distribuidas | Máxima réplica no equivale a máximo control posterior del autor |
| IndieWeb/POSSE | Publicar en sitio propio y distribuir copias o enlaces | El original independiente no resuelve por sí solo continuidad de conversaciones o contactos |
| Lemmy | Comunidades, votos y distintos órdenes | Separar calidad de conversación, orden de contenido y reputación de personas |
| Discourse | Documenta niveles de confianza y evolución de numerosos permisos hacia grupos | Evitar que una escala única de confianza controle permisos heterogéneos |
| Stack Overflow/Stack Exchange | Vincula reputación basada en votos con privilegios | Nuestro objetivo discreto requiere separar reconocimiento temático, popularidad y derechos |
| Minds e Hive | Sus páginas presentan funciones económicas e incentivos de participación/gobierno | No confundir contraprestación, financiación, reputación y legitimidad de gobierno |
| IPFS | Persistencia exige retención/pinning; puede prestarse como servicio | Los datos distribuidos siguen necesitando recursos y responsables de conservación |

## Fuentes por antecedente

- [Hubzilla: conceptos](https://help.hubzilla.hu/en/basicconcepts.html) y [compatibilidad](https://hub.hubzilla.hu/help/member/connections).
- [FEP-ef61](https://fediverse.codeberg.page/fep/fep/ef61/). No acredita por sí solo todas las versiones de Streams y derivados.
- [Mastodon: migración](https://docs.joinmastodon.org/user/moving/).
- [AT Protocol: estructura](https://atproto.com/guides/the-at-stack), [migración](https://atproto.com/guides/account-migration) y [recuperación](https://atproto.com/guides/account-recovery).
- [Nostr: NIP-01](https://raw.githubusercontent.com/nostr-protocol/nips/master/01.md) y [NIP-09](https://raw.githubusercontent.com/nostr-protocol/nips/master/09.md).
- [Solid: FAQ](https://solidproject.org/faq).
- [Diaspora*: versiones](https://github.com/diaspora/diaspora/releases).
- [Friendica: traslado](https://friendica.michael-mints.ru/help/Move-Account), [incidencia 15627](https://github.com/friendica/friendica/issues/15627). Una incidencia no es una medición representativa.
- [Manyverse: permanencia](https://www.manyver.se/faq/permanence/).
- [IndieWeb: POSSE](https://indieweb.org/POSSE).
- [Lemmy](https://join-lemmy.org/).
- [Discourse: niveles de confianza](https://blog.discourse.org/2018/06/understanding-discourse-trust-levels/). La versión consultada describe evolución hacia permisos de grupo; no se evalúa aquí cada instalación.
- [Stack Overflow: reputación](https://stackoverflow.com/help/whats-reputation).
- [Minds](https://www.minds.com/) y [Hive](https://hive.io/). Descripciones propias de producto, no auditorías de resultados.
- [IPFS: persistencia](https://docs.ipfs.tech/concepts/persistence/).

## Hipótesis transversales que deben probarse

1. El usuario aprecia continuidad y control si no le exigen entender infraestructura.
2. La disponibilidad de relaciones significativas importa más que reproducir contadores de contactos externos.
3. Un proveedor predeterminado facilita entrada pero puede concentrar la red.
4. La autonomía comunitaria sin recursos de moderación y recurso resulta insuficiente.
5. El código abierto necesita documentación, tareas y mantenedores; su publicación no garantiza contribuciones.
6. La base voluntaria necesita cuotas, respaldo y financiación explícita; gratuidad para el usuario no significa coste cero.

Se prueban mediante recorridos y operación, no se presentan como explicación causal demostrada de las iniciativas anteriores.

## Investigación pendiente y límites

Lens, Farcaster, DeSo, Steem/Steemit, GNU social/StatusNet, Pleroma/Akkoma, Misskey y derivados, Mbin/Kbin, MeWe, Ello, WT.Social y sus continuaciones, Social.coop y otros modelos cooperativos merecen fichas específicas si sus mecanismos pueden cambiar una decisión. No se los declara evaluados por aparecer en esta lista ni se les atribuye fracaso, abandono o limitación concreta sin fuente.

También faltan estudios comparables de retención, coste, gobernanza y experiencia. Las métricas de redes distintas y épocas diferentes no se mezclarán para justificar una narrativa. Antes de elegir un componente de un proyecto, registrar versión, licencia, mantenimiento, cobertura de pruebas y dependencias.

La especificación integral está preparada para revisión sin fingir que esta investigación histórica es exhaustiva. La elección de protocolo en F1 y las funciones nuevas deben incorporar evidencia adicional donde pueda modificar el resultado.
