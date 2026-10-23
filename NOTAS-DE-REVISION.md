---
title: Spartakos — Notas de revisión del prototipo
lang: es-ES
license: CC-BY-SA-4.0
date: 2026-10-23
status: N01–N08 implementadas en el simulador; validación de producto pendiente
---

# Notas de revisión del prototipo

Este registro acumula decisiones de interfaz, limitaciones observadas y propuestas de mejora. Anotar un cambio no significa que ya esté implementado. Las propuestas pendientes no se convierten en decisiones por incorporarlas a este registro.

## N01. Sustituir «Me interesa» por «Guardar»

**Decisión:** denominar «Guardar» a la acción actual de conservar una publicación para consulta propia. Es un término familiar y describe su función sin sugerir una valoración adicional.

La acción sigue siendo privada: no expresa acuerdo, no avisa al autor y no genera reputación. El interés temático privado del perfil es un concepto distinto; este cambio de nombre no lo elimina ni lo redefine.

**Consecuencia propuesta:** llamar «Guardados» a la sección actualmente denominada «Mi interés», manteniendo una explicación breve de su privacidad.

**Estado:** implementado en la segunda revisión: Guardar y Guardados, sin comunicación al autor.

## N02. Responder a una respuesta

**Limitación comprobada:** la interfaz actual ofrece «Responder» en publicaciones iniciales, pero no en sus respuestas. Solo presenta el primer nivel de respuestas. Aunque el servidor admite una referencia a otra respuesta como destino, la interfaz no permite crear ni recorrer correctamente una conversación de varios niveles.

**Mejora propuesta:** permitir responder a una respuesta, mostrando a quién se responde y conservando el contexto de la conversación. Evitar que una profundidad creciente vuelva ilegible la pantalla; la revisión posterior N07 fija un máximo de tres niveles y continuación por cita.

Las respuestas deben conservar la audiencia y comprobar los permisos de su contexto. Responder no puede ampliar acceso ni filtrar una conversación restringida. Debe poder localizarse una respuesta guardada dentro de su hilo.

**Estado:** implementado: respuestas encadenadas, referencia al mensaje anterior, sangrado limitado y acceso al hilo desde Guardados. Comprobado en navegador con varias cuentas y mediante pruebas automáticas.

## N03. Mezcla de publicaciones generales y comunitarias en Inicio

**Problema observado:** el muro inicial reúne publicaciones generales y publicaciones de comunidades, lo que hace confuso el contexto de lectura y participación. Indicar solo «Público» o «Solo integrantes» no identifica suficientemente dónde se ha publicado.

**Propuesta de trabajo:** separar por defecto el espacio general y el espacio de comunidades. Dentro de comunidades, mostrar una comunidad concreta con su nombre, visibilidad y permisos, sin mezclar por defecto publicaciones de distintas comunidades en el mismo muro.

El editor debe conservar un destino explícito y reconocible. Una comunidad puede contener publicaciones públicas: contexto comunitario y audiencia pública/privada son dimensiones distintas, y ambas deben quedar claras. Una eventual vista combinada sería una opción expresa, pendiente de estudiar, no el inicio obligatorio.

**Estado:** implementado: Inicio general, directorio de comunidades y muro propio de cada comunidad. Los borradores conservan su texto y audiencia por espacio.

## N04. «Me gusta» sencillo en lugar de «Coincido» graduado

**Decisión de revisión:** abandonar la graduación de «Coincido» y utilizar una reacción sencilla de «Me gusta». Se prioriza una interacción familiar, sin escala ni menú de grados.

«Me gusta» expresa una valoración o afinidad; no se interpreta automáticamente como acuerdo con cada afirmación, prueba de veracidad o reputación temática. Sigue separado de «Guardar», que conserva contenido de forma privada, y de seguir una conversación.

La reacción debe respetar la audiencia de la publicación: en una comunidad privada no se hace pública fuera de ella. Se mantiene el principio de utilidad sin dependencia emocional. La presentación de recuentos y avisos requiere diseño específico; adoptar el botón no decide por sí solo cómo se muestran ni autoriza rankings, privilegios o presión de reciprocidad.

El primer prototipo ha sido probado en una revisión inicial. Esto no equivale a una validación con una muestra de participantes ni a completar los criterios de producto.

**Estado:** implementado: Me gusta reversible, independiente de Guardar y limitado por audiencia. Sin recuento destacado, ranking, reputación ni avisos. La escala de «Coincido» queda como antecedente descartado, no como alternativa activa. La presentación final sigue pendiente de validación.

## N05. Audiencia sin elección redundante de destino

Inicio general y comunidades privadas muestran una indicación fija. Solo una comunidad con alternativas reales muestra el selector Audiencia. El nombre de la comunidad identifica el destino. La pérdida de permisos conserva el borrador bloqueado, sin conversión a público. **Estado:** implementado y comprobado en el editor de comunidad privada.

## N06. Publicación programada

**Decisión:** fecha, hora, zona horaria y gestión privada de pendientes como alcance inicial. Margen explícito de retraso; permisos y audiencia se verifican al ejecutar. **Estado:** implementado en el servidor local y cliente. Las condiciones adicionales quedan propuestas y pendientes; véase la sección 10 de [Publicaciones y conversaciones](FUNCIONAL-03-PUBLICACIONES-Y-CONVERSACIONES.md).

## N07. Tres niveles de conversación y continuación por cita

**Decisión:** publicación inicial, respuesta y respuesta a respuesta. No se crea un cuarto nivel, ni siquiera mediante una petición directa al servidor. Desde el último nivel se continúa con una publicación propia que cita el mensaje y avisa a su autor. Se aplican los permisos para iniciar publicaciones y las restricciones de audiencia. **Estado:** implementado, incluidos aviso interno, marca de lectura, cita programada e historial anterior conservado. Sustituye la posibilidad de crear respuestas sin límite de profundidad descrita inicialmente en N02.

## N08. Me gusta sin identidad visible y check neutral

**Decisión:** ocultar identidades al autor y otros usuarios, retirar Reacciones y posponer cualquier recuento. Botón con check verde, sin corazón ni animaciones, con texto y estado accesibles. **Estado:** implementado tanto en interfaz como en respuestas del servidor. El vínculo se conserva en el servidor para retirar la reacción; no supone anonimato frente al proveedor. Sustituye las presentaciones anteriores con lista de personas.
