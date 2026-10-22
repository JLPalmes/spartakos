---
title: Análisis 02 — Migración de entrada desde redes populares
lang: es-ES
license: CC-BY-SA-4.0
date: 2026-10-22
status: Propuestas para deliberación; capacidades documentadas sin pruebas con archivos reales
---

# Migración de entrada desde redes populares

## 1. Objetivo y límites del estudio

Requisito confirmado: superar la barrera de perder historial y contactos al llegar a nuestra red. No se requiere interoperabilidad, federación ni comunicación permanente entre plataformas. El derecho posterior a salir de nuestra red se analiza por separado.

Se propone evaluar el resultado como continuidad personal y social, no como cantidad de archivos procesados. La persona debería poder localizar una publicación antigua, abrir sus fotografías, reconocer el contexto y reencontrar a personas significativas.

Esta entrega añade diseño de producto y mecanismos a los requisitos anteriores. No hay importadores implementados, archivos de usuarios examinados, permisos de APIs obtenidos ni tasas de recuperación medidas. Las categorías anunciadas por un proveedor no certifican lo que contendrá una exportación concreta.

## 2. Dos vías de adquisición complementarias

### Archivo descargado por la persona

La persona solicita una exportación en la plataforma de origen y la entrega a nuestra herramienta. Ventajas: permite trabajar sin integración directa aprobada y conservar una copia independiente. Inconvenientes: solicitud externa, espera, archivos voluminosos o divididos, opciones de formato y calidad, y posible uso difícil desde el móvil.

Propuesta: asistente específico por origen, detección de archivos y volúmenes incompletos, reanudación y análisis previo. No considerar que el usuario ha abandonado porque la plataforma tarda en preparar la exportación. Permitir usar la cuenta mientras espera.

### Transferencia autorizada

La persona autoriza a nuestra aplicación a recibir categorías concretas de información mediante mecanismos de portabilidad del origen. No equivale a mantener conversación entre redes.

Ventajas: puede reducir pasos y errores manuales. Inconvenientes: aprobación del proveedor, permisos, cobertura territorial, cuotas, cambios de servicio y datos no incluidos. Propuesta: ofrecerla donde sea viable y mantener la alternativa por archivo; evitar que un rechazo de acceso bloquee toda la migración.

No se presupone que una API de publicaciones o inicio de sesión conceda acceso al archivo histórico completo. Tampoco se propone pedir la contraseña de la red de origen. Una descarga autorizada recurrente puede ayudar durante una transición, pero no es un requisito de sincronización permanente.

## 3. Cobertura documental inicial por origen

| Origen | Vía acreditada | Evidencia relevante | Verificación pendiente |
| --- | --- | --- | --- |
| X | Archivo descargable | La ayuda enumera publicaciones, mensajes, medios y listas de seguidores y seguidos | Cobertura real, adjuntos, relaciones y contexto de respuestas |
| Facebook | Descarga en el centro de cuentas | Meta documenta la descarga conjunta o separada de información de sus aplicaciones | Categorías actuales, audiencias, álbumes y relaciones en archivos reales |
| Instagram | Descarga en el centro de cuentas | Mismo mecanismo general documentado por Meta | Historias, vídeos, pies, secuencias, contactos e identificadores |
| LinkedIn | Descarga y API de portabilidad | La ayuda documenta conexiones; Microsoft documenta acceso autorizado a datos históricos | Cobertura por categorías, aprobaciones, territorio y archivos multimedia |
| TikTok | API de portabilidad | El producto anuncia perfil, publicaciones, seguidores y seguidos; también otras categorías autorizables | Contenido audiovisual realmente entregado, identificadores, región y aprobación |
| YouTube | Google Takeout y descarga de vídeos propios | Google acredita descarga de vídeos subidos por el titular | Metadatos, comentarios, suscripciones y cuentas de marca; no asumir transferencia de espectadores |
| Threads | Pendiente de comprobación suficiente | No se extrapola automáticamente la cobertura de Instagram | Exportación propia, categorías, relaciones y diferencias de cuenta |

Fuentes primarias y alcance:

- [X: archivo](https://help.x.com/en/managing-your-account/how-to-download-your-x-archive). La existencia de HTML/JSON y categorías anunciadas no demuestra que el archivo contenga todas las respuestas ajenas ni contenido eliminado.
- [Meta: centro de cuentas](https://about.fb.com/news/2023/10/manage-your-information-across-apps/). Es un anuncio oficial del mecanismo, no un esquema vigente detallado de cada categoría. La ayuda específica de Instagram intentada redirigió a inicio de sesión y no permitió completar esa comprobación.
- [LinkedIn: descarga](https://www.linkedin.com/help/linkedin/answer/a1339364/downloading-your-account-data?lang=en). Los correos de conexiones pueden faltar según preferencias de estas personas.
- [LinkedIn: acceso para terceros](https://learn.microsoft.com/en-us/linkedin/dma/member-data-portability/member-data-portability-3rd-party/). Requiere solicitud y aprobación; la página técnica consultada limita el consentimiento al EEE. No se presupone acceso universal.
- [LinkedIn: datos históricos](https://learn.microsoft.com/en-us/linkedin/dma/member-data-portability/shared/member-snapshot-api). La API Snapshot se diferencia del registro de cambios posteriores al consentimiento. Es necesario evaluar ambos para no confundir actividad nueva con historia completa.
- [TikTok: producto](https://developers.tiktok.com/products/data-portability-api/), [incorporación](https://developers.tiktok.com/docs/en/data-portability-api-get-started). El producto declara cobertura de usuarios del EEE y Reino Unido; exige revisión. Hay permisos de una sola solicitud y continuados. Los nombres de categorías no certifican archivos de vídeo completos.
- [Google Takeout](https://support.google.com/accounts/answer/3024190?hl=en), [vídeos propios de YouTube](https://support.google.com/youtube/answer/56100?hl=en). La documentación distingue cuentas de marca y limita la descarga descrita a vídeos propios.

La lista no pretende clasificar redes por popularidad ni cerrar prioridades. Reddit, Snapchat, Pinterest y otras fuentes quedan en el inventario ampliable según el público. WhatsApp, Messenger y Telegram requieren un bloque específico si se incorpora mensajería: una conversación exportada plantea problemas distintos de un perfil público.

## 4. Historial: de archivo legible a trayectoria utilizable

Se propone distinguir tres estados de un mismo contenido:

1. Conservado en una biblioteca privada, accesible y buscable.
2. Mostrado en el perfil como historial procedente de otra red, por decisión del titular y sin ampliar permisos de terceros automáticamente.
3. Utilizado como punto de partida de una conversación nueva aquí, con interacciones locales separadas de las antiguas.

La biblioteca privada es una etapa segura de incorporación, no la definición completa del requisito. Limitar el resultado a una carpeta de recuerdos dejaría sin resolver la continuidad de la trayectoria pública.

Cada elemento debe conservar origen, fecha original, fecha de importación, referencia original, autoría declarada, adjuntos y estado de completitud. No debe afirmarse autenticidad verificada por el mero hecho de proceder de un archivo subido. Si la titularidad de origen se comprueba después, se añade esa evidencia sin reescribir el registro.

Un comentario antiguo ajeno puede conservarse como contexto privado cuando proceda, pero no convertirse en una publicación nueva atribuida a una persona que no participa aquí. Las reacciones y cifras externas son información histórica, no votos de usuarios locales ni reputación automáticamente transferida.

### Contexto perdido

Cuando falte el mensaje al que responde una publicación, se conserva la respuesta y se señala la ausencia. No se completa mediante texto inventado. Cuando un archivo solo contenga una dirección externa, el informe distingue referencia conservada de archivo recuperado. Un enlace no cuenta como fotografía migrada.

### Duplicados y varias redes

Reimportar el mismo elemento debe actualizar el estado sin multiplicarlo. La clave de origen debe incluir red, cuenta e identificador de publicación cuando exista. Si falta un identificador fiable, debe aplicarse un procedimiento conservador y revisable.

Textos iguales en dos plataformas no son necesariamente duplicados: pueden tener distintas fechas, audiencias y conversaciones. Propuesta: agrupar visualmente posibles versiones y permitir mantenerlas separadas, sin fusionar automáticamente sus relaciones ni borrar procedencias.

## 5. Contactos: conservar, identificar y reactivar

### Registro privado de vínculos

Se propone conservar el tipo de relación disponible: a quién seguía el usuario, quién le seguía, amistad mutua, solicitud pendiente, cuenta bloqueada o silenciada. No son equivalentes y no deben transformarse todas en amistad.

La conservación de bloqueos es parte de la continuidad. No tendría sentido facilitar reencuentros y sugerir inmediatamente a quien el usuario había bloqueado. Una coincidencia de seguridad puede utilizarse para prevenir sugerencias sin publicar ni revelar esa relación.

### Correspondencias de identidad

La clave de correspondencia preferible es red de origen más identificador estable de cuenta, cuando esté disponible. Los nombres pueden cambiar y reutilizarse. Si solo hay un nombre, el vínculo queda como candidato y necesita revisión; no se asigna con certeza falsa.

Para vincular una cuenta externa a una cuenta nueva, se pueden evaluar autorización del origen, un mecanismo de verificación pública o evidencias alternativas según plataforma. Subir un archivo no basta para certificar el control: los archivos se pueden modificar. Toda vinculación requiere revocación, protección frente a suplantación y manejo de cuentas de origen vendidas o comprometidas.

Descubrir una cuenta puede revelar una identidad que alguien desea mantener separada. Por ello, demostrar titularidad y permitir que antiguos contactos encuentren la nueva cuenta son decisiones distintas. No debe existir un directorio público obligatorio de todas las identidades externas vinculadas.

### Llegadas en momentos distintos

Ejemplo de diseño: Ana importa una relación con la cuenta externa de Luis. Esa referencia se conserva privadamente. Meses después Luis verifica esa cuenta y autoriza el reencuentro correspondiente. El sistema puede presentar una coincidencia, sin revelar listas de terceros ni fabricar una cuenta de Luis durante la espera.

El seguimiento unilateral podría restablecerse mediante una preferencia expresa del usuario y sujeto a las condiciones del destinatario. Una amistad o acceso privado requiere el consentimiento que corresponda. Las notificaciones de coincidencia deben ser opcionales y limitadas para no convertir la migración en una fuente de presión.

### Qué no puede trasladarse por decisión unilateral

Se puede conservar la referencia a una persona que no participa. No se puede trasladar su actividad, disponibilidad o atención. Si nuestro requisito se interpretase como poder conversar aquí con quien permanece exclusivamente fuera, exigiría un mecanismo adicional que no forma parte del alcance confirmado.

La respuesta de producto es facilitar el reencuentro de personas que llegan individualmente, sin exigir coordinación ni fingir contactos activos a partir de registros importados.

## 6. Entrada individual sencilla

La experiencia se diseña para una persona que llega por iniciativa propia, sin organizar a sus contactos ni comprender la arquitectura del sistema.

El sistema debe detectar formatos, ordenar el historial, evitar duplicados, conservar bloqueos y preparar coincidencias verificadas. No debe pedir al usuario que seleccione algoritmos de correspondencia, revise cada publicación, configure cada tipo de dato o decida todas sus preferencias antes de entrar.

Las decisiones explícitas se limitan a lo necesario para autorizar la importación y comprender su resultado. Los controles avanzados son opcionales y posteriores. Los casos ambiguos se resuelven con valores conservadores sin detener el proceso completo; no se hacen públicos mensajes privados ni se unen identidades por coincidencia de nombre.

## 7. Experiencia y comprobación

Propuesta de recorrido: elegir origen, autorizar la transferencia o aportar el archivo con ayuda breve, confirmar un resumen y continuar. La vía recomendada se presenta primero, sin pedir al usuario que evalúe alternativas técnicas. La cuenta sigue siendo utilizable durante la espera. No se exige configurar el reencuentro ni publicar manualmente cada elemento: se aplican valores predeterminados comprensibles, sin ampliar audiencias. Los casos de visibilidad incierta quedan en la biblioteca privada y se explican sin bloquear el resto.

El informe distingue cuatro estados: recuperado, referencia externa sin copia, contenido ausente y formato todavía no compatible. Debe mostrar un inventario por categorías y permitir reparar un caso incompleto sin rehacerlo todo. No basta con decir «importación completada» cuando se han omitido archivos.

La reversión se explica antes de publicar: un lote privado puede retirarse; una publicación ya distribuida aquí puede tener respuestas y copias. No debe prometerse que revertir una importación borra automáticamente actividad ajena generada después.

## 8. Pruebas necesarias

| Prueba | Resultado que se debe comprobar |
| --- | --- |
| Cuenta pequeña y cuenta con años de actividad | Mismo criterio de inventario y reanudación, sin pérdidas silenciosas |
| Exportación dividida en varios archivos | Detección de partes ausentes antes de declarar integridad |
| Móvil con poca memoria o interrupción de red | Reanudación sin repetir toda la carga |
| Archivos con textos, imágenes, vídeos y referencias ausentes | Distinción clara entre copia recuperada y enlace conservado |
| Dos importaciones del mismo archivo | Ninguna duplicación de publicaciones o relaciones |
| Una publicación repetida en varias redes | Procedencias conservadas y agrupación revisable |
| Contacto que cambió de nombre | Evitar asignación errónea por nombre reutilizado |
| Contacto que llega después | Reencuentro conforme a las preferencias de ambas partes |
| Contacto bloqueado o cuenta externa robada | Ninguna reactivación automática insegura |
| Archivo manipulado | No convertir contenido subido en prueba de titularidad |
| Conversaciones privadas | Ninguna publicación ni ampliación de audiencia por defecto |

La integridad se mide respecto del material recibido; la cobertura respecto de toda la cuenta original es otra medida y exige referencias adicionales. Un importador puede procesar correctamente un archivo incompleto. Ambas limitaciones deben quedar visibles.

## 9. Decisiones propuestas y pendientes

Propuestas: entrada individual con pocas decisiones; historial integrado con visibilidad conservada cuando sea fiable; importadores por origen; vías directa y por archivo; reencuentro diferido con verificación; inventario y reparación de pérdidas accesibles sin configuración obligatoria. Ninguna implica interoperabilidad. La migración colectiva queda fuera del diseño.

Pendiente: elegir plataformas de primera cobertura, acordar tratamiento público de conversaciones ajenas y señales históricas, validar descubrimiento con identidades separadas, analizar costes de grandes archivos y probar muestras de exportación con consentimiento. No se fija una promesa de recuperación completa sin esos resultados.
