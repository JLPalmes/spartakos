---
title: Migración de entrada — historial y contactos
lang: es-ES
license: CC-BY-SA-4.0
date: 2026-10-21
status: Alcance definido; mecanismos propuestos pendientes de validación
---

# Alcance confirmado

Desarrollo del análisis: [Diseño de la migración de entrada](ANALISIS-02-MIGRACION-DE-ENTRADA.md), con alternativas, cobertura documental y pruebas pendientes.

La interoperabilidad con otras redes no es un requisito. El requisito es que una persona pueda llegar desde las redes populares sin tener que abandonar su historial ni reconstruir desde cero sus vínculos. El derecho a salir de nuestra red sigue siendo un requisito distinto. No se prescribe federación ni sincronización permanente.

## Historial: conservar y poder usar

Propuesta: una biblioteca personal integrada que permita buscar y recorrer publicaciones, archivos y fechas originales. Debe conservar red de procedencia, identificadores originales y contexto disponible; admitir varias redes sin duplicaciones; permitir nuevas importaciones incrementales; y separar archivo privado de publicación ante nuevas audiencias.

Los hilos se reconstruyen cuando los datos lo permiten. Se señalan respuestas, adjuntos o referencias ausentes, sin inventarlos. Las métricas antiguas, si se conservan, son información histórica identificada por origen y fecha, no actividad ni reputación obtenida en nuestra red.

Mensajes privados y contenido de terceros necesitan tratamiento separado. Importar un archivo para consulta personal no equivale a autorizar su difusión. Las audiencias antiguas pueden no tener equivalente exacto; ante la duda, el contenido queda privado hasta que el usuario decida.

## Contactos: tres resultados diferentes

1. Conservar una agenda privada de vínculos anteriores: cuenta de origen, identificador estable si existe y tipo de relación.
2. Reencontrar a quienes ya estén aquí: correspondencia con cuentas externas verificadas y consentimiento de descubrimiento. Un nombre parecido o un archivo subido no prueban identidad.
3. Facilitar la continuidad cuando lleguen después: permitir al usuario activar un aviso de coincidencia y gestionar sus seguimientos o solicitudes conforme a sus preferencias. Una amistad mutua no se crea unilateralmente.

Para quienes no lleguen, se conserva la referencia disponible, sin fabricar cuentas ni presentar contactos como usuarios activos. La capacidad de conversar con personas que permanecen exclusivamente en otra red no se puede garantizar sin comunicación entre redes o participación de esas personas. Esto es un límite a explicar, no un motivo para abandonar la recuperación del grafo social.

El diseño se centra en la llegada individual y no exige coordinación con contactos.

## Evidencia inicial por origen

| Origen | Capacidad documentada | Lo que falta comprobar |
| --- | --- | --- |
| X | Su ayuda enumera publicaciones, medios, mensajes y listas de seguidores y seguidos en el archivo descargable | Formatos y referencias reales, cobertura de adjuntos, hilos y estabilidad de identificadores |
| Facebook e Instagram | Meta documenta descarga de información a través de su centro de cuentas | Categorías efectivas por plataforma, audiencias, relaciones, archivos y variaciones de formato |
| LinkedIn | Documenta descarga de datos y conexiones, con límites en correos de contactos según sus preferencias | Cobertura real de publicaciones, adjuntos y correspondencia de contactos |

Fuentes: [archivo de X](https://help.x.com/en/managing-your-account/how-to-download-your-x-archive), [descarga en Meta](https://about.fb.com/news/2023/10/manage-your-information-across-apps/), [datos de LinkedIn](https://www.linkedin.com/help/linkedin/answer/a1339364/downloading-your-account-data?lang=en).

La existencia de exportación no certifica la integridad de un archivo concreto. TikTok, YouTube, Threads y otras fuentes deben incorporarse al inventario de evaluación; no se consideran verificadas por este documento. La prioridad entre redes queda pendiente de conocer el público previsto.

## Experiencia propuesta

Principio confirmado: llegada individual sencilla, pocas decisiones y ninguna configuración obligatoria. La complejidad técnica debe resolverla el sistema.

Recorrido propuesto: elegir red de origen → autorizar la transferencia o aportar el archivo con ayuda breve → confirmar un resumen comprensible → continuar usando la red. El sistema organiza el historial, evita duplicados y prepara coincidencias de contactos sin exigir decisiones por elemento. Los ajustes y el informe detallado quedan disponibles después.

No se amplían audiencias automáticamente: se conserva la visibilidad cuando puede determinarse y reproducirse con fiabilidad; los casos ambiguos y mensajes privados quedan en el archivo personal, sin bloquear el resto de la importación. Este comportamiento se explica en el resumen, sin convertirlo en un cuestionario.

La importación debe ser reanudable y reversible. Repetir el mismo archivo no debe duplicar contenido. Importar varias redes no debe fusionar identidades por simples coincidencias. No debe generar avisos de miles de publicaciones antiguas como si fueran novedades.

## Criterios de aceptación propuestos

- Comparar inventario del archivo recibido con datos recuperados; informar explícitamente de pérdidas o incompatibilidades.
- Poder buscar historial y abrir archivos sin depender de que el contenido siga en el origen.
- Conservar fechas originales, procedencia y distinción entre archivo e interacción nueva.
- Presentar contactos conservados, coincidencias verificadas y vínculos pendientes como categorías distintas.
- Permitir llegar en momentos diferentes y reencontrarse cuando ambas partes lo autoricen.
- Medir tiempo de importación, abandonos, porcentaje de contenido recuperado y de vínculos restablecidos, sin fijar objetivos numéricos sin pruebas.

## Cambio de prioridades del análisis

La elección de protocolo interno se evaluará por soberanía, seguridad y experiencia propias. La facilidad de adopción se analizará sobre las exportaciones y posibilidades de migración de las redes de origen. No se presumirá que adoptar el protocolo de una red alternativa resuelve la entrada desde las plataformas populares.
