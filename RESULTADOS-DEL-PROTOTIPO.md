---
title: Spartakos — Resultados de la primera comprobación del prototipo
lang: es-ES
license: CC-BY-SA-4.0
version: 0.10
date: 2026-10-26
status: 92 pruebas automáticas superadas; bloqueo programado y recuperación de permisos
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

## 10. Me gusta sin identidades visibles

Resultado: **58 pruebas automáticas superadas, 0 fallos**: diez de modelo anterior, 27 HTTP, cuatro de conversaciones, diez de programación y siete de citas y niveles. Se adaptan las comprobaciones de reacciones a la nueva visibilidad y se añade una prueba HTTP con cuatro cuentas: cada sesión recibe únicamente su elección propia, sin lista de identidades ni cantidad; la exportación solo incluye las reacciones propias y no se generan avisos. Se comprueba también la respuesta de un comando para evitar filtraciones por una vía distinta a la consulta de estado.

La interfaz elimina Reacciones y utiliza check verde, texto Me gusta, indicación Marcado y aria-pressed. Los resultados anteriores que describen listas visibles pertenecen a versiones sustituidas. No se promete anonimato frente al proveedor; sigue pendiente decidir sobre la utilidad de recuentos.

En navegador se comprobó que Bruno puede marcar y retirar el check; Alicia no recibe ese estado ni una lista de personas. El botón comunica Marcado y aria-pressed solo en la cuenta que reacciona. La captura utiliza contenido sintético del laboratorio.

## 11. Recuentos horarios

Resultado: **67 pruebas automáticas superadas, 0 fallos**: diez de modelo anterior, 28 HTTP, cuatro de conversaciones, diez de programación, siete de citas y ocho de recuentos. Los nuevos casos verifican marca propia inmediata, totales congelados entre cortes, altas y retiradas, idempotencia, límite exacto del corte, cálculo tardío sin incluir cambios posteriores, migración sin recuentos históricos inventados, publicaciones posteriores al corte, privacidad, persistencia y reloj que retrocede. La prueba HTTP usa reloj inyectado para comprobar ejecución sin cliente, cierre y reinicio, y paso por dos horas sin esperar horas reales. No existe una ruta HTTP para cambiar el reloj del servicio.

La fecha del corte se distingue de la fecha del cálculo. Los datos locales anteriores conservan sus elecciones, con el primer total pendiente hasta el siguiente corte. Las cantidades se entregan solo a lectores autorizados; las identidades y cambios entre cortes permanecen fuera de la API. Los resultados anteriores sin recuentos corresponden a una etapa sustituida. No se ha ejecutado la matriz de producto ni una validación con participantes.

En navegador con reloj de ensayo se observó: check propio inmediato con total pendiente; una aprobación en el corte de las 13:00; retirada inmediata del check sin variar ese total; cero aprobaciones en el corte de las 14:00. Alicia recibió el mismo total sin identidades. El escenario usa únicamente datos sintéticos y está separado del laboratorio habitual.

## 12. Borradores recuperables

Resultado: **75 pruebas automáticas superadas, 0 fallos**: diez del modelo anterior, 30 HTTP, cuatro de conversaciones, diez de programación, siete de citas, ocho de recuentos y seis de borradores. Se verifica separación entre cuentas, ausencia de publicación o avisos al guardar, texto íntegro, citas privadas, persistencia y exportación propia, migración, conflictos sin sobrescritura, copias y pérdida de permisos. Publicar o programar comprueba versión y consume el pendiente de forma atómica; una repetición se rechaza sin duplicar. Los errores de publicación o programación conservan el borrador pendiente.

En navegador con datos sintéticos: Bruno guardó una publicación restringida con cita, recargó y la recuperó en la misma comunidad. Dos pestañas editaron el mismo borrador: el guardado obsoleto se rechazó conservando su texto y Guardar como copia mantuvo ambas variantes. Alicia no vio borradores de Bruno. Tras revocar publicación, el editor de Bruno deshabilitó Publicar, mantuvo Solo integrantes y permitió seguir guardando.

La función no recupera texto anterior que nunca se hubiera guardado, respuestas en curso ni ediciones sin guardar tras recargar. El almacenamiento local es legible por el operador y no tiene cifrado de extremo a extremo. Las pruebas de producto y usabilidad con participantes siguen pendientes.

## 13. Papelera recuperable de borradores

Resultado: **78 pruebas automáticas superadas, 0 fallos**: diez del modelo anterior, 31 HTTP, cuatro de conversaciones, diez de programación, siete de citas, ocho de recuentos y ocho de borradores. Se comprueba que mover y restaurar exige propiedad y versión, conserva contenido y audiencia, persiste al reiniciar y no repite una publicación ya ejecutada. No hay purga ni vaciado automático.

En navegador con datos sintéticos se guardó un borrador, se movió a Papelera de borradores y se restauró. Retomar recuperó el texto original sin publicarlo ni programarlo. El borrado definitivo y su política de copias siguen pendientes.

## 14. Edición y retirada de publicaciones propias

Resultado: **88 pruebas automáticas superadas, 0 fallos**: diez del modelo anterior, 33 HTTP, cuatro de conversaciones, diez de programación, siete de citas, ocho de recuentos, ocho de borradores y ocho de edición y retirada. Se verifican autoría, permisos actuales, conflictos de versión, contexto y audiencia inmutables, referencia de respuestas y aprobación propia a versiones anteriores, marcador sin cuerpo y conservación de aportaciones ajenas. Se comprueba la retirada por el autor tras perder acceso sin recuperar contenido ajeno, el bloqueo de citas programadas retiradas y la eliminación de avisos asociados a cuerpos retirados. Reiniciar conserva edición o retirada; las pruebas HTTP verifican que estado y exportación no entregan el cuerpo anterior.

En navegador, Alicia respondió y marcó Me gusta en una publicación sintética de Bruno; después Bruno la editó. Alicia vio la versión nueva, la advertencia de aprobación anterior y el contexto de su respuesta, sin controles para editar texto ajeno. En una segunda vista de datos sintéticos ya retirados se comprobaron el marcador, la respuesta independiente conservada y la cita sin fragmento del original. No se retiraron publicaciones del laboratorio del usuario.

No es auditoría de seguridad ni ejecución de A01–A148. No se garantiza eliminación de copias externas, respaldos, borradores independientes o texto ya recibido por un cliente. Se mantienen pendientes política completa de retención, moderación por terceros y validación con participantes.


## 15. Consistencia de borradores, versiones y retirada

Resultado: **91 pruebas automáticas superadas, 0 fallos**. Se añaden tres escenarios de dominio a la batería anterior: retirada de una fuente citada por un borrador, conflicto entre edición y retirada desde versiones distintas y restauración de la referencia privada de una publicación ya retirada.

Un envío rechazado conserva el borrador, su estado y su privacidad; no consume el pendiente. Una retirada obsoleta no borra la edición vigente. Tras serializar y recuperar el estado, una edición anterior no restaura el cuerpo retirado y recuperar una referencia de borrador ya utilizada no vuelve a publicarla. Los escenarios utilizan exclusivamente datos sintéticos; no se accede a los datos del laboratorio del usuario.

La persistencia de estos tres escenarios se comprueba mediante serialización y migración del estado; las pruebas HTTP anteriores siguen comprobando reinicios del servidor. Este bloque no añade una nueva comprobación visual de accesibilidad ni confirma usabilidad con participantes. Las ediciones rescatadas siguen siendo texto local que puede copiarse: convertirlas en borradores persistentes requiere un diseño explícito de destino y audiencia, pendiente de revisión.


## 16. Ajuste del editor pendiente de comprobación visual

El cliente conserva como texto local de solo lectura una edición abierta que ha perdido permiso para guardarse. Se proponen identificadores estables y retorno del foco al botón de edición después de guardar o cancelar. La batería existente mantiene **91 pruebas superadas** y la sintaxis del cliente es correcta. No se ha ejecutado una prueba de teclado o lector de pantalla: el canal del navegador dejó de responder antes de abrir el escenario sintético. No se atribuye a las pruebas HTTP una validación visual. El estado de publicación y el recorrido pendiente se registran en [la revisión de continuidad](REVISION-PARA-EL-LUNES.md).


Comprobación posterior, 25 de octubre: se recuperó el navegador y se ejecutó el recorrido con dos pestañas sintéticas de Bruno y una de Alicia en un servidor separado. Guardar y cancelar devuelven el foco al botón de edición. Una versión obsoleta se rechaza conservando el texto local y mostrando la versión vigente. Al reducir el permiso de Bruno a lectura, su edición abierta se conserva en un campo de solo lectura, sin botón para guardarla ni cambio del cuerpo publicado. Se verificó `readOnly` en el control. Esto no equivale a una evaluación completa con teclado o lector de pantalla. No se accedió a datos del laboratorio del usuario.


## 17. Rescate tras perder la membresía

Se añade un aviso y acceso a Mi cuenta para las ediciones locales de aportaciones propias en espacios ya inaccesibles. Si desaparece el editor enfocado, el foco pasa al acceso al rescate; si la lectura se conserva, al campo rescatado. Abrir el recorrido enfoca el texto de solo lectura. No hay publicación ni guardado automático.

Comprobado en navegador con datos sintéticos separados: baja de Bruno aplicada por Alicia mientras había una edición abierta, desaparición del historial privado, aviso enfocado y recuperación visual del texto local junto a su aportación propia. Se verificó la propiedad `readOnly`; no se mostró el historial ajeno. No se ejecutó retirada irreversible en este recorrido. La batería completa mantiene **91 pruebas superadas**. No es auditoría completa de accesibilidad ni garantía de recuperación del texto local tras recargar o cerrar sesión.


## 18. Programación, permisos y continuidad tras reiniciar

Resultado del 26 de octubre: **92 pruebas automáticas superadas, 0 fallos**, incluidas 34 HTTP. Se añade un recorrido integrado con servidor real de loopback, reloj inyectado y almacenamiento temporal separado. Programa una aportación restringida, revoca permisos y comprueba en disco que el temporizador bloquea el envío sin consultas del cliente. Reiniciar conserva el bloqueo. Publicar inmediatamente sin permisos se deniega; recuperar permisos no reactiva el envío automáticamente. Una acción explícita posterior del autor publica una sola vez, mantiene la audiencia y persiste tras otro reinicio. Una acción repetida se rechaza y la cuenta externa no recibe el contenido. Los pendientes siguen siendo privados, incluso frente a la administración comunitaria.

No se detectó un fallo de comportamiento ni fue necesario cambiar código de producción. Esta comprobación automatizada no evalúa por sí sola la comprensión del mensaje de bloqueo. Se mantienen los límites de identidad ficticia y operación local. No se accedió al escenario de prueba del usuario ni a sus datos anteriores.
