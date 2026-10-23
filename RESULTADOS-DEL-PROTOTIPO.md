---
title: Spartakos — Resultados de la primera comprobación del prototipo
lang: es-ES
license: CC-BY-SA-4.0
version: 0.5
date: 2026-10-23
status: 57 pruebas automáticas superadas; interacción, programación y citas comprobadas en navegador
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

## 6. Simulador con servidor local y varias cuentas

Se incorpora [simulacion/](simulacion/README.md): cuatro sesiones independientes, servidor HTTP local, persistencia de datos ficticios y comprobación de permisos en servidor. Se han superado catorce pruebas HTTP además de las diez pruebas anteriores, veinticuatro en total. Las pruebas utilizan servidores temporales reales en loopback y escenarios separados.

Se comprueban lectura privada, publicación y comentarios por rol, privacidad de guardados, autoría vinculada a sesión, consentimiento individual, mayoría insuficiente, unanimidad con historial protegido, expulsiones elusivas, cambios de audiencia, revocación de permisos, escrituras simultáneas, reinicio, exportación y restricciones de acceso al servicio local. La prueba de Host utiliza HTTP directo porque el cliente fetch normaliza esa cabecera; no se ha relajado el control para hacer pasar la prueba.

En navegador se observaron cuatro cuentas simultáneas: una publicación privada de Bruno llegó a Alicia y Carla y no apareció en Diego. El borrador de Alicia se conservó durante la actualización. Los consentimientos de Alicia y Bruno no permitieron abrir la comunidad; la negativa de Carla cerró la propuesta. La interfaz de Carla no ofreció responder a publicaciones privadas con su permiso inicial de lectura.

También se comprobó en navegador la revocación de publicación a Bruno mientras mantenía un borrador restringido: se conservó el texto y se deshabilitó el envío, sin seleccionar público. Al restaurar el permiso volvió a poder enviarlo al mismo destino.

Durante revisión se identificó el riesgo de ampliar sin querer la audiencia de un borrador al perder permisos o abrirse la comunidad. La audiencia se envía expresamente al servidor; el cliente mantiene el destino restringido o bloquea el envío cuando pierde permiso, sin cambiar a público. Hay pruebas de regresión para ambos casos.

No se han ejecutado E01–E15 ni A01–A148 como suite de producto. El almacenamiento y el control de acceso corresponden a un único proceso local, con identidades ficticias de acceso libre. No prueban identidad soberana, distribución, cifrado ni usabilidad con participantes.

## 7. Segunda revisión: interacción y espacios separados

Ejecutado con Node.js v22.23.4: `node --test prototipo/modelo.test.mjs simulacion/*.test.mjs`. Resultado: **36 pruebas superadas, 0 fallos**: diez del modelo anterior, 22 HTTP y cuatro de selección y recorrido de conversaciones. Las ocho pruebas HTTP adicionales verifican reacciones reversibles e idempotentes, autoría por sesión, privacidad, respuesta a respuesta, guardado de respuestas, actualización del esquema anterior, persistencia, exportación propia, historial protegido y rechazo de parámetros inválidos. Las pruebas de conversación separan general y comunidades, recorren 2.001 mensajes y controlan ramas, referencias ausentes y ciclos.

En un escenario desechable de navegador con cuatro cuentas se comprobó: borradores independientes para general y comunidad; una respuesta privada de Bruno y otra de Alicia a esa respuesta; acceso de Bruno desde Guardados al contexto de esa respuesta; Me gusta de Carla visible para la audiencia autorizada y retirada posterior; ausencia de respuestas y reacciones privadas en Diego. Carla conserva lectura y reacciones sin poder comentar. Los guardados de Bruno no aparecen en Carla.

El estado local anterior se respaldó antes de actualizarlo. La migración añade el almacén de reacciones sin reiniciar publicaciones ni guardados. Los datos de ensayo del usuario y las capturas que los contengan no se incorporan al repositorio. Los borradores no persisten al recargar la pestaña.

Estas comprobaciones siguen siendo de laboratorio: no ejecutan la matriz A01–A148 ni sustituyen pruebas de usabilidad, accesibilidad, seguridad o infraestructura distribuida.

## 8. Programación y simplificación de audiencia

Se han superado **48 pruebas automáticas, 0 fallos**: diez del modelo anterior, 24 HTTP, cuatro de conversaciones y diez de programación. Las nuevas verificaciones cubren fecha futura, zona y márgenes válidos; ejecución única; privacidad de pendientes; edición y cancelación con versión y propiedad; publicación inmediata; pérdida de permisos; vencimiento; audiencia restringida tras abrir comunidad; migración y conservación de datos. Una prueba HTTP deja de consultar el servidor y comprueba después en disco que el temporizador publicó por sí mismo; reiniciar conserva un único resultado. Otra rechaza acciones sobre programaciones ajenas sin revelar su existencia.

En un escenario separado del contenido del usuario se comprobó en navegador: audiencia fija sin desplegable en comunidad privada; programación de texto privado con fecha, zona y margen visibles; aparición en Programadas; edición del texto pendiente; publicación inmediata y aparición de una sola publicación en el mismo espacio privado. La captura del ensayo utiliza únicamente contenido sintético.

Las condiciones adicionales están documentadas como propuestas, no implementadas. El laboratorio necesita el proceso local encendido y no ofrece un servicio permanente ni ejecución distribuida. La matriz A01–A148 continúa sin ejecutarse como suite de producto.

## 9. Límite de tres niveles, citas y avisos

Resultado: **57 pruebas automáticas superadas, 0 fallos**: diez de modelo anterior, 26 HTTP, cuatro de conversaciones, diez de programación y siete de citas y niveles. Las nuevas comprobaciones rechazan el cuarto nivel en servidor, permiten iniciar otro hilo con cita y preservan privacidad y permisos; verifican avisos solo al autor citado, lectura y persistencia, ausencia de aviso al preparar o cancelar una cita programada, ejecución posterior, retirada de acceso y conservación del historial anterior. Los ensayos de recorridos profundos comprueban lectura robusta de datos anteriores, no autorización para crear hilos nuevos de profundidad ilimitada.

En navegador con datos sintéticos: Bruno creó niveles segundo y tercero; el tercero no ofreció Responder y sí Citar en una publicación. Alicia citó ese mensaje y publicó un tema nuevo en la misma comunidad restringida. Bruno recibió el aviso correspondiente. La nueva publicación mostró atribución y referencia al mensaje citado, con Responder disponible como primer nivel de otro hilo.

Se mantiene pendiente la validación con participantes, las preferencias de avisos y la protección frente a citas abusivas en un servicio real. Estas pruebas locales no ejecutan la matriz completa de producto.
