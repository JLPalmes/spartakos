---
title: Spartakos — Publicaciones, audiencias y conversaciones
lang: es-ES
license: CC-BY-SA-4.0
version: 0.2
date: 2026-10-23
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

Propuesta: hilo con respuesta a una publicación concreta y ramas que puedan plegarse. Mantener visible la relación de contexto sin anidación ilimitada que haga ilegible el móvil. Comparar orden cronológico y navegación por ramas, sin ordenar por coincidencias acumuladas.

Responder no aumenta la audiencia del contenido al que se responde. El lector accede a una respuesta solo cuando tiene acceso a su contexto y el permiso correspondiente; un enlace reenviado no concede acceso. La vista pública no revela títulos ni autores de ramas privadas.

No ofrecer ramas con audiencias arbitrarias dentro del mismo hilo en la primera experiencia. Para conversar con otra audiencia, crear otra publicación con contexto autorizado y diferenciada. No copiar texto restringido al crearla por defecto.

Los permisos de leer, responder y abrir temas son independientes. Una comunidad puede permitir respuestas a lectores admitidos sin permitirles crear temas. Una mención no concede derechos ni obliga al destinatario a responder.

Seguir una conversación es opcional y privado. Una respuesta propia puede incluir una suscripción predeterminada limitada a respuestas directas, explicada y revocable; no activar todos los avisos de todas las ramas. El matiz final se valida con pruebas de utilidad.

## 4. Interacciones según el contenido

La interacción vigente utiliza «Me gusta» sencillo y reversible y «Guardar» privado. Una reacción no implica acuerdo con cada afirmación ni reputación del autor. Ambas acciones son independientes y respetan la audiencia del contenido. Guardar no avisa al autor ni suscribe a novedades. La graduación de «Coincido» está descartada; véase [Interacción útil](FUNCIONAL-02-INTERACCION-UTIL.md).

No medir éxito por volumen de reacciones. Una pregunta resuelta con pocas intervenciones puede resultar más útil que una polémica prolongada. La expresión afectiva no queda prohibida: puede ocurrir en respuestas sin diseñar una competición de aprobación.

## 5. Difusión sin viralidad impuesta

Separar enlace al original, recomendación a personas o espacios con acceso y cita contextualizada. Propuesta inicial: compartir enlace al original; posponer un botón de redistribución masiva sin contexto hasta justificar su utilidad y riesgos.

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
