---
title: Spartakos — Publicaciones, audiencias y conversaciones
lang: es-ES
license: CC-BY-SA-4.0
version: 0.8
date: 2026-10-24
status: Diseño funcional propuesto; decisiones pendientes identificadas
---

# Publicaciones, audiencias y conversaciones

## 1. Qué puede publicarse

Propuesta: una publicación común admite texto breve o desarrollado, enlaces y adjuntos; título opcional para piezas largas. No obligar a fragmentar argumentos en cadenas para ajustarse a una longitud artificialmente pequeña. Sí habrá límites técnicos explícitos de tamaño y recursos, pendientes de medición.

Texto e imágenes forman el mínimo inicial. Audio y vídeo se incorporan según recursos; no se exige servicio comercial para cualquier contenido audiovisual futuro, aunque pueda ofrecer capacidad adicional. Encuestas, eventos y documentos colaborativos requieren diseño propio y no se presuponen necesarios para el primer recorrido.

Un solo editor, con herramientas básicas y opciones adicionales progresivas. Borrador recuperable, adjuntos con descripción accesible y estado de envío inequívoco. El contenido no publicado permanece privado; su guardado local no se confunde con copia garantizada entre dispositivos.

## 2. Lugar y audiencia

El editor parte de un contexto: espacio personal o comunidad. El destino se determina al entrar en Inicio general o en una comunidad. Cuando solo existe una audiencia válida, se muestra una indicación fija; solo se ofrece el selector «Audiencia» cuando hay alternativas reales, como publicar para todo el público o solo para integrantes de una comunidad pública. La audiencia aparece junto a la acción de publicar, sin exigir recorrer una configuración. Se recuerda dentro del mismo contexto, no se traslada una elección pública a un espacio privado.

| Destino inicial | Audiencia | Regla comprensible |
| --- | --- | --- |
| Espacio personal público | Cualquier lector | Puede circular fuera del contexto inicial |
| Comunidad pública | Cualquier lector | Participación limitada por roles, aunque la lectura sea abierta |
| Comunidad restringida | Personas autorizadas | No compartir fuera ni revelar existencia mediante avisos |
| Archivo personal | Solo titular | Borrador o nota; no se presenta como conversación publicada |

La publicación personal a destinatarios elegidos es una alternativa adicional a evaluar, sin crear círculos obligatorios al registrarse. No se equipara automáticamente «seguidores» con audiencia privada. Seguir, ser aprobado y acceder a un contenido son relaciones distintas.

Para evitar autorización retroactiva confusa, cada modalidad debe especificar si nuevas personas acceden al historial. En comunidad se rige por reglas del espacio y su modo de privacidad; en grupo cifrado se mantiene la propuesta de acceso futuro por defecto. No introducir un selector de estas políticas en cada publicación.

Privacidad y cifrado son dimensiones distintas: un contenido restringido legible por el servicio no se etiqueta como cifrado de extremo a extremo. El bloqueo no vuelve privado un contenido público.

## 3. Responder y leer una conversación

El hilo admite tres niveles en total: publicación inicial (nivel 1), respuesta (nivel 2) y respuesta a esa respuesta (nivel 3). No se permite responder al tercer nivel. Es un límite de creación aplicado en servidor, no solo un límite visual de sangrado. Mantener visible la relación de contexto; comparar navegación por ramas sin ordenar por reacciones acumuladas.

Responder no aumenta la audiencia del contenido al que se responde. El lector accede a una respuesta solo cuando tiene acceso a su contexto y el permiso correspondiente; un enlace reenviado no concede acceso. La vista pública no revela títulos ni autores de ramas privadas.

No ofrecer ramas con audiencias arbitrarias dentro del mismo hilo en la primera experiencia. Para conversar con otra audiencia, crear otra publicación con contexto autorizado y diferenciada. No copiar texto restringido al crearla por defecto.

Los permisos de leer, responder y abrir temas son independientes. Una comunidad puede permitir respuestas a lectores admitidos sin permitirles crear temas. Una mención no concede derechos ni obliga al destinatario a responder.

Seguir una conversación es opcional y privado. Una respuesta propia puede incluir una suscripción predeterminada limitada a respuestas directas, explicada y revocable; no activar todos los avisos de todas las ramas. El matiz final se valida con pruebas de utilidad.

## 4. Interacciones según el contenido

La interacción vigente utiliza «Me gusta» sencillo y reversible y «Guardar» privado. Una reacción no implica acuerdo con cada afirmación ni reputación del autor. Ambas acciones son independientes y respetan la audiencia del contenido. La identidad de quienes dan Me gusta no se muestra al autor ni a otros usuarios; cada cuenta solo conoce su propia elección. El botón es un check verde de aprobación, sin corazón. No se muestran listas de identidades. El total agregado se actualiza cada hora en punto del servicio y muestra la fecha del corte; la elección propia sigue siendo inmediata. Guardar no avisa al autor ni suscribe a novedades. La graduación de «Coincido» está descartada; véase [Interacción útil](FUNCIONAL-02-INTERACCION-UTIL.md).

No medir éxito por volumen de reacciones. Una pregunta resuelta con pocas intervenciones puede resultar más útil que una polémica prolongada. La expresión afectiva no queda prohibida: puede ocurrir en respuestas sin diseñar una competición de aprobación.

## 5. Difusión sin viralidad impuesta

Separar enlace al original, recomendación a personas o espacios con acceso y cita contextualizada. La continuación de un hilo que alcanza el tercer nivel se realiza mediante una publicación propia con cita y aviso al autor citado. No se introduce redistribución masiva sin contexto.

En público puede permitirse cita con atribución, referencia y extensión limitada por diseño; no generar copias completas automáticamente. Permitir al autor limitar la función de cita/recomendación de la aplicación se estudia como control de producto, no garantía de impedir capturas, copias externas o conversación ajena.

En restringido, compartir solo referencia que compruebe permisos; sin vista previa pública ni traslado del cuerpo a otra audiencia. La aplicación no ofrece redistribución externa del contenido privado por defecto. Una imagen ya entregada puede ser copiada por un destinatario: se comunica ese límite sin aparentar control absoluto.

Las recomendaciones entre comunidades no hacen miembros automáticamente a sus receptores. Compartir en otro espacio es una nueva acción con reglas propias y audiencia clara; no fusiona hilos ni contadores.

## 6. Edición y significado de respuestas y acuerdos

El autor puede corregir una publicación sin pagar. Conservar identidad del objeto y mostrar fecha de modificación cuando exista contenido publicado. Distinguir cambios menores de modificaciones sustanciales es útil, pero no confiar solo en que el autor clasifique honestamente su edición.

Propuesta: respuestas y señales de acuerdo conservan referencia de versión; si el texto cambia, se indica que pueden responder a una versión anterior. No obligar a todas las personas a ratificar su acuerdo ni enviarles avisos de presión. La consulta histórica debe equilibrar contexto y privacidad.

El historial visible de ediciones queda pendiente de política: mantener para siempre una dirección o dato sensible eliminado sería contrario a la retirada efectiva. Se propone marca de edición y contexto recuperable cuando proceda, con procedimiento para purgar versiones sensibles y dejar una indicación de indisponibilidad. No prometer simultáneamente historial público inmutable y derecho a retirar contenido.

## 7. Retirada, cierre de comentarios y moderación

Retirar el cuerpo de una publicación no equivale a borrar las aportaciones independientes de otras personas. Mantener un marcador sobrio y respuestas cuando puedan mostrarse sin revelar información que deba retirarse. Ocultar adjuntos y previsualizaciones conforme al proceso de borrado.

El autor controla su texto; la comunidad controla presencia y reglas en su espacio. No puede reescribir la aportación y conservar la atribución original. Una retirada moderadora y una retirada del autor se distinguen cuando comunicarlo sea apropiado.

Cerrar nuevas respuestas preserva lectura e historial permitido. En comunidad lo decide quien tenga competencia; el cierre unilateral por autor dentro de una comunidad queda pendiente de sus reglas. No puede utilizarse como privilegio global para borrar desacuerdos. En espacios personales se estudian controles frente a acoso que no se confundan con modificar textos de terceros.

El autor puede exportar su aportación; no obtiene por ello permiso para hacer público un hilo privado. La desaparición de una comunidad y la custodia de su historial requieren procedimiento específico de continuidad.

## 8. Casos que deben resolver las pruebas funcionales

1. Una persona publica sin configurar formatos, círculos o algoritmos.
2. Una pregunta larga puede leerse y responderse sin fragmentación forzada.
3. Una comunidad pública permite comentar pero reserva la creación de temas.
4. Un enlace privado recibido fuera del espacio no filtra cuerpo, título, autor ni miniatura.
5. Una corrección sustancial no hace parecer que terceros apoyaban el nuevo texto.
6. Una retirada de dato sensible no deja el dato accesible por el historial ordinario.
7. Un autor retira su aportación sin suplantar ni eliminar automáticamente las respuestas ajenas.
8. Seguir una conversación no provoca una avalancha de avisos; dejarla de seguir es inmediato.
9. Compartir conserva atribución y no altera audiencia ni fabrica una comunidad más grande.
10. Interrumpir publicación conserva borrador y no crea duplicados al reintentar.

## 9. Decisiones pendientes

Audiencia personal a destinatarios elegidos; acceso de nuevos miembros al historial; navegación por ramas; señales apropiadas para contenido no argumentativo; alcance de citas y redistribución; exposición de versiones anteriores; cierre de comentarios en espacios personales y comunitarios.

La continuación debe desarrollar comunidades y permisos, porque determina quién autoriza acciones y cómo se resuelven estos casos sin añadir decisiones a cada publicación. No se seleccionan todavía bibliotecas o protocolos.

## 10. Publicación programada y condiciones

### 10.1 Alcance acordado y recorrido

Se incorpora programación por fecha, hora y zona horaria. El recorrido ordinario sigue siendo Publicar; Programar abre las opciones adicionales. Se muestra la fecha efectiva, zona y margen máximo de retraso antes de confirmar. La publicación queda en Programadas, accesible únicamente a su autor salvo una autorización futura expresa de revisión. Puede editarse, reprogramarse, cancelarse o publicarse inmediatamente. La edición conserva destino y audiencia; trasladar el contenido a otro espacio exige una acción explícita distinta.

El servidor responsable guarda y ejecuta la programación aunque el cliente esté cerrado. El laboratorio requiere mantener encendido el proceso local; no ofrece disponibilidad permanente. La fecha se almacena como instante UTC junto a la zona de referencia. Un cambio posterior de zona del dispositivo no desplaza el envío. En el editor se indica la zona del dispositivo; al editar una programación creada en otra zona se muestra la conversión. Las horas inexistentes por cambio estacional se rechazan. Para una hora repetida se muestra la interpretación efectiva con su designación horaria; el producto deberá validar que esta explicación resulte comprensible.

Antes de confirmar, el usuario elige un margen máximo de retraso. El simulador propone 15 minutos y permite 5, 15, 60 o 1.440 minutos; son valores de ensayo. Si el servidor vuelve demasiado tarde, la publicación vence y no se envía. No existe publicación tardía ilimitada por defecto.

### 10.2 Ejecución y continuidad

| Situación | Resultado exigido |
| --- | --- |
| Llega la hora y se conservan permisos | Publicar una vez con autor, destino y audiencia previstos |
| El cliente está cerrado | El servidor ejecuta sin necesitar una sesión activa del cliente |
| Se pierden permisos o desaparece el destino | Bloquear; conservar contenido y explicar el estado al autor |
| Se restauran los permisos | No reactivar automáticamente una publicación bloqueada; exigir revisión |
| Se abre una comunidad antes del envío | Mantener restringida la publicación preparada para integrantes |
| Se supera el margen de retraso | Marcar vencida, sin publicar |
| Se cancela o se publica inmediatamente | Terminar la programación; un reintento no crea otra publicación por el temporizador |
| Dos clientes editan o actúan sobre el mismo pendiente | Comprobar versión; rechazar la acción obsoleta |
| El servidor se reinicia | Recuperar pendientes persistidos; aplicar permisos y margen vigentes |

El simulador guarda en la misma escritura atómica la publicación y el cierre de su programación. Esto evita repetir la ejecución tras un reinicio dentro del modelo de un único proceso y archivo local. No es una garantía distribuida ni cubre corrupción de disco, varios procesos sobre los mismos datos o restaurar una copia antigua.

La portabilidad futura debe trasladar contenido pendiente, fechas y estados con transferencia exclusiva de la autoridad de ejecución. Exportar no activa un segundo ejecutor. El laboratorio incluye programaciones propias en la exportación, pero no implementa su traslado ni importación ejecutable.

### 10.3 Condiciones candidatas; todavía no implementadas

| Condición | Propuesta de funcionamiento | Problemas que debe resolver antes de adoptarse |
| --- | --- | --- |
| Aprobación de una persona o equipo | Autorizar una versión concreta antes de una fecha límite | Revisores expresamente designados; acceso mínimo al borrador; retirar aprobación al editar contenido, destino o audiencia; decidir si hace falta una o varias aprobaciones |
| Publicación previa de otro mensaje | Ejecutar una secuencia cuando el antecedente conste publicado | No confundir hora prevista con éxito; bloquear ciclos y dependencias desaparecidas; detener la cadena ante cancelación o fallo; no copiar contenido privado entre espacios |
| Fecha mínima y fecha límite | Ejecutar al cumplirse la condición dentro del intervalo autorizado | Definir precedencia entre condición, hora y vencimiento; comunicar por qué no se publicó; evitar esperas indefinidas |
| Confirmación final del autor | Avisar de que está preparada y esperar confirmación | Un aviso no equivale a consentimiento; ausencia de respuesta implica no publicar; limitar avisos y permitir cancelación |
| Señal externa verificable | Un servicio autorizado comunica un hecho y activa la condición | Autenticidad, caducidad, duplicados, errores y manipulación; quién responde del disparador; qué datos recibe el servicio y cómo se revoca |

Propuesta de prioridad posterior: aprobación y secuencias, después de comprobar demanda. Los disparadores externos requieren un ensayo separado. No se incluyen condiciones basadas en alcanzar Me gusta, seguidores o actividad; incentivarían la presión de participación. Tampoco se propone un disparador de inactividad del autor: la falta de conexión no prueba su voluntad ni un acontecimiento personal.

Si se combinan condiciones, el diseño deberá expresar claramente si se exigen todas o alguna y qué ocurre al vencer. No se incorpora un editor general de reglas al recorrido básico. Ninguna condición puede conceder permisos, ampliar audiencia, saltarse moderación ni publicar en nombre de otra persona.

### 10.4 Estado de implementación

Implementadas en el simulador: fecha y hora en la zona del cliente, margen de retraso, gestión privada de pendientes, edición con versión, cancelación, publicación inmediata, ejecución periódica por servidor, bloqueo por permisos y recuperación tras reinicio. La programación se limita a publicaciones iniciales de texto; respuestas programadas, adjuntos, revisores, secuencias, avisos externos y traslado entre proveedores quedan pendientes. El contenido pendiente es legible por el operador local; no hay cifrado de extremo a extremo.

## 11. Continuación mediante cita y aviso

Citar en una publicación abre el editor de una publicación propia, con referencia al mensaje concreto y atribución a su autor. Puede citarse cualquier nivel, incluido el tercero. La nueva publicación inicia otro hilo con su propio máximo de tres niveles. La cita no convierte al autor citado en coautor ni expresa su adhesión al nuevo texto. No se incrustan recursivamente cadenas de citas: el prototipo muestra únicamente el fragmento del mensaje directamente citado, con enlace a su contexto.

El autor citado recibe un aviso en Avisos cuando se publica, no cuando se prepara un borrador o se programa. Puede abrir la publicación que lo cita y marcar el aviso como leído. La autocita no genera aviso. La primera implementación no envía correos, avisos externos ni contadores de popularidad. Las preferencias, el agrupado y las medidas frente a citas abusivas requieren desarrollo antes de producción.

Una cita de contenido restringido debe permanecer en la misma comunidad y con audiencia de integrantes. Citar no permite publicar fuera ni eludir el permiso para iniciar temas. Una persona con permiso solo para comentar no obtiene permiso de publicación por alcanzar el límite. Las citas de contenido público pueden abrir una publicación general. El servidor verifica acceso al original y permisos de destino; el cliente conserva los borradores existentes y no copia el texto citado en el texto propio.

El aviso solo se entrega si el citado puede leer el original y la publicación que lo cita. Si pierde acceso a la comunidad, el aviso privado deja de estar disponible. La programación de una cita revalida estas restricciones al ejecutarse y solo entonces genera el aviso. El fragmento se obtiene del original autorizado vigente; no representa una copia histórica inmutable. La edición y retirada del original deberán conservar los controles de privacidad y el contexto de versión previstos en este documento.

El historial previo con más de tres niveles se conserva sin eliminar, aplanar ni reasignar autorías. No admite nuevas respuestas desde el tercer nivel en adelante; se puede continuar mediante cita conforme a permisos. Los recorridos de datos profundos se mantienen robustos para leer ese historial y rechazar ciclos o referencias rotas.

## 12. Borradores recuperables

Guardar borrador es una acción explícita distinta de Guardar una publicación ajena. No se envía texto al servidor mientras se escribe. El editor distingue cambios sin guardar y versión guardada, y Borradores permite retomar una publicación inicial después de recargar, cerrar el cliente o reiniciar el servidor. Se conserva texto, espacio, audiencia y referencia de cita. El contenido pendiente solo se entrega a su autor en la aplicación; el operador local puede leer el almacenamiento, que no tiene cifrado de extremo a extremo.

Retomar abre el editor en el espacio original. Si se perdieron permisos o acceso, el texto sigue disponible para su autor y puede continuar guardándose, pero publicar o programar queda bloqueado. No se convierte en publicación general ni cambia automáticamente a público. Una cita privada sigue restringida incluso si la comunidad se abre. La interfaz no revela el contenido citado si ya no hay acceso; conserva su referencia para que el autor decida.

Los borradores tienen versión. Una pestaña con una versión obsoleta no puede sobrescribir silenciosamente otra. Conserva el texto que estaba editando y ofrece Guardar como copia. También puede guardar una copia si otra pestaña ya publicó o programó el original; esa copia vuelve a ser pendiente y no se publica por sí misma. Cambiar de contexto no traslada el texto ni sustituye el borrador local de otro espacio.

Publicar o programar desde un borrador comprueba versión, propiedad, estado y permisos en el servidor. La transición se guarda junto con el resultado: el borrador pasa a Ya publicado o Transferido a Programadas y un reintento no lo ejecuta otra vez. La versión utilizada queda consultable como referencia. Cancelar una programación se gestiona en Programadas; no reactiva silenciosamente el borrador original. La exportación incluye solo los borradores propios.

Alcance del simulador: publicaciones iniciales de texto, con o sin cita. No se guarda la selección tentativa de fecha al guardar un borrador; la fecha se confirma en Programar. Las respuestas en curso siguen en memoria de la pestaña. Las ediciones no guardadas se pierden al recargar y no se anuncia recuperación de texto anterior a esta función. Quedan pendientes recuperación de respuestas, borrado definitivo con política de retención, historial de versiones completo y pruebas con participantes. El guardado no sustituye copias independientes ni un servicio de alta disponibilidad.

### 12.1 Papelera recuperable de borradores

Mover a papelera aparta el borrador de los pendientes y conserva contenido, destino, audiencia, cita y estado anterior. Restaurar devuelve ese estado sin publicar, programar ni conceder permisos. Ambas acciones comprueban propiedad y versión; una acción obsoleta no sobrescribe otra. La papelera es privada por cuenta y persiste tras reiniciar.

Mover la referencia de un borrador ya publicado o transferido a Programadas no retira la publicación ni cancela su envío. Restaurarla tampoco permite volver a ejecutarla. No hay vaciado automático ni purga definitiva; esta función no se presenta como borrado efectivo de datos. La política de retención, copias y borrado irreversible sigue pendiente de diseño antes de producción.

## 13. Edición y retirada: alcance implementado en el laboratorio

### 13.1 Edición con referencia de versión

Editar publicación permite al autor corregir su texto, con permiso vigente para publicar o responder en su contexto. El servidor comprueba autoría y versión y rechaza una edición obsoleta. No se cambia identidad, autor, espacio, audiencia, padre ni cita mediante la edición del texto. Se muestran versión y fecha de modificación. Guardar sin cambios no crea otra versión. El editor local conserva el texto ante un conflicto para que su autor pueda copiarlo o revisarlo, sin sobrescritura automática.

Cada nueva respuesta conserva la versión del mensaje al que respondió. Las citas mantienen referencia a la versión conocida al crearlas; el fragmento mostrado es el texto actual del original autorizado y se advierte cuando cambió después de la cita. No se presenta un texto actual como una transcripción histórica inmutable. No se almacena ni se ofrece un historial público completo de cuerpos anteriores.

Me gusta conserva internamente la versión sobre la que se marcó. Una edición no renueva silenciosamente esa aprobación; el titular ve que corresponde a una versión anterior. Retirar y volver a marcar es una acción explícita sobre la versión actual. El total horario no se desglosa por versiones ni identifica participantes, y una publicación editada advierte que las aprobaciones pueden ser anteriores. No se atribuyen las respuestas o señales previas a una adhesión al texto modificado.

### 13.2 Retirada del cuerpo y continuidad del hilo

Retirar publicación despliega una explicación y requiere confirmar la retirada del texto. El servidor comprueba autoría y versión, vacía el cuerpo en el objeto activo y deja un marcador con la identidad y audiencia originales. No se ofrece restauración del cuerpo retirado en esta implementación. La operación no modifica ni elimina respuestas o publicaciones independientes de otras personas. Se rechazan nuevas respuestas directas, citas y reacciones a ese marcador; los descendientes existentes siguen conservando su contexto y límite de niveles.

Las vistas de citas dejan de mostrar el cuerpo retirado. Los avisos de cita dejan de entregarse si el original citado o la publicación que lo cita fueron retirados. Las programaciones que necesitan citar un original retirado se bloquean al ejecutarse y requieren revisión; no se publica automáticamente una referencia que ya no está disponible. Los guardados conservan el marcador y permiten quitarlo de la colección. La exportación de aportaciones propias refleja el cuerpo retirado vacío, sin exponer un historial de versiones mediante esa vía.

Perder acceso a una comunidad impide editar allí, pero no impide al autor retirar su propio texto. Mi cuenta ofrece sus aportaciones propias en espacios sin acceso; no devuelve contenido ajeno ni reactiva permisos. No se presupone potestad de una administración para reescribir o retirar texto en nombre de otra persona; la retirada moderadora sigue pendiente.

### 13.3 Límites y protección del texto en curso

Retirar del objeto activo no garantiza eliminar copias externas, exportaciones anteriores, respaldos o textos que otras personas hayan copiado por su cuenta. Los borradores privados propios e independientes tampoco se purgan automáticamente por retirar una publicación. Se distingue esta función de una política completa de borrado y retención, aún pendiente antes de producción.

Si otra pestaña modifica la versión mientras se edita, se conserva el texto local y se rechaza guardar sobre la versión nueva. Si otra pestaña retira la publicación o se pierde el acceso, la edición local puede copiarse desde el marcador propio o Mi cuenta. Sigue siendo memoria del cliente: recargar puede perderla; no se anuncia recuperación de ediciones que nunca se guardaron como borrador. Las copias de texto hechas por el propio autor permanecen bajo su decisión, sin volver a publicarse por sí mismas.
