---
title: Spartakos — Comunidades y permisos
lang: es-ES
license: CC-BY-SA-4.0
version: 0.2
date: 2026-10-22
status: Diseño funcional propuesto; decisiones pendientes identificadas
---

# Comunidades y permisos

## 1. Propósito y creación sencilla

Una comunidad es un espacio con finalidad, participantes, reglas y administración propios. No es propietaria de las cuentas personales ni se confunde con el nodo que la aloja. Puede continuar con otros responsables u otro alojamiento conforme a sus reglas.

Crear requiere nombre, descripción breve y elección de una plantilla comprensible. Se aplican reglas básicas de convivencia y permisos predeterminados. Los ajustes avanzados son posteriores; no exigir configurar rol por rol ni redactar una Constitución particular antes de conversar.

Las reglas locales complementan los derechos comunes, no los anulan. Participar en una comunidad no obliga a seguir a todos sus miembros, hacer públicos intereses privados ni recibir todos sus avisos.

## 2. Plantillas de participación

| Plantilla | Lectura | Comentarios | Nuevos temas | Incorporación predeterminada |
| --- | --- | --- | --- | --- |
| Pública participativa | Cualquiera | Miembros | Miembros | Libre, con controles proporcionados contra abuso |
| Pública editorial | Cualquiera | Miembros | Autores designados | Libre para participar; designación para publicar |
| Pública de difusión | Cualquiera | Desactivados | Autores designados | Seguir sin hacerse miembro activo |
| Privada participativa | Miembros admitidos | Miembros | Miembros | Solicitud o invitación |
| Privada editorial | Miembros admitidos | Miembros | Autores designados | Solicitud o invitación |

Son propuestas para probar con lenguaje de producto. «Comentar» significa responder a una publicación existente; «publicar» en esta tabla significa abrir un tema. Evitar que una misma palabra oculte ambos permisos.

La visibilidad de la comunidad es otra dimensión: pública, localizable sin mostrar contenido o no listada. Una comunidad no listada no se anuncia como indetectable: sus miembros pueden revelar su existencia. Las privadas se crean no listadas por defecto; el creador puede habilitar solicitudes mediante una ficha mínima sin exponer miembros o contenido.

Privada describe audiencia, no cifrado. La etiqueta de protección indica separadamente si el operador puede acceder al contenido o si existe E2EE. No degradar esta protección silenciosamente para ampliar funciones.

## 3. Roles iniciales

| Rol | Función | Límites |
| --- | --- | --- |
| Visitante | Leer lo abierto | No accede a privados ni actúa como miembro |
| Lector admitido | Leer contenido autorizado | No comenta o abre temas si no tiene esos permisos |
| Participante | Comentar y, según plantilla, abrir temas | No administra a otras personas |
| Autor | Abrir temas en espacios editoriales | No modera por ser autor |
| Moderador | Aplicar normas de participación y atender incidencias | No cambia identidad, medios de recuperación ni textos atribuidos a terceros |
| Administrador | Gestionar configuración, roles y continuidad | No adquiere titularidad sobre cuentas ni derecho a exponer historial privado |

El creador recibe administración inicial, no propiedad perpetua de participantes y conversaciones. Los permisos pueden combinarse, pero las pantallas normales muestran funciones comprensibles; no una jerarquía de prestigio. Ser moderador no es una recompensa automática por reputación.

Un administrador técnico del servidor no se convierte por ello en moderador de cada comunidad. En espacios cifrados, administrar infraestructura tampoco concede claves de lectura. Los poderes técnicos reales del operador deben mantenerse declarados.

## 4. Entrada, invitaciones y salida

En públicas abiertas, participar puede formalizar membresía mediante una acción clara, sin cuestionario. En privadas, solicitud breve o invitación con acceso definido. No utilizar solicitudes para exigir datos ajenos al propósito del espacio por defecto.

Las invitaciones no son pases ilimitados ni prueban identidad civil. Deben caducar y poder revocarse. Una solicitud denegada no se convierte en etiqueta pública del solicitante. Limitar reintentos abusivos sin obligar a moderadores a responder repetidamente.

Seguir una comunidad pública permite recibir sus publicaciones sin pedir acceso a privados. Abandonar deja de generar avisos y retira permisos futuros; no borra automáticamente publicaciones ni respuestas propias o ajenas. Ofrecer acceso a gestión de aportaciones propias según la política común, sin eludir reglas de privacidad del resto.

La lista de miembros y solicitudes no es pública por defecto. Los roles con acceso a ella están delimitados. Incorporación y salida no generan anuncios generales obligatorios.

## 5. Lectura histórica y cambios de audiencia

Propuesta: en comunidades privadas con control de acceso, los nuevos miembros reciben el historial permitido por la plantilla, con esa regla visible antes de publicar. En comunidades cifradas, acceso futuro por defecto; un archivo anterior exige mecanismo y autorización propios. No presentar ambos modelos como equivalentes.

Para simplificar, la política histórica pertenece al espacio, no se pregunta en cada publicación. Cambiar una comunidad privada a pública requiere aprobación expresa y unánime de todos sus integrantes, incluidos quienes no administran o solo leen. La condición se mantiene aunque el historial anterior permanezca privado y solo se pretenda publicar contenido futuro. Proteger el historial es una garantía adicional, no una excepción a la unanimidad.

El silencio, la inactividad y la ausencia no equivalen a consentimiento. Sin unanimidad, la comunidad permanece privada. Las facultades administrativas no permiten omitir integrantes ni expulsarlos para eludir la regla. El procedimiento debe fijar un censo verificable y tratar cambios de membresía durante la consulta sin reducir artificialmente el conjunto que debe consentir.

La unanimidad tampoco autoriza a publicar aportaciones históricas de antiguos integrantes o ampliar derechos sobre contenido ajeno automáticamente. Abrir el historial requiere comprobar permisos de esas aportaciones por separado. Una comunidad pública nueva es otra entidad: no hereda automáticamente miembros, historial, identidad ni representación de la comunidad privada.

Una comunidad pública que se vuelve privada no puede garantizar que desaparezcan copias o índices externos. La interfaz debe explicarlo antes de confirmar el cambio.

## 6. Organización de contenidos y experiencia

Empezar con un espacio de temas y conversaciones. Añadir secciones solo si ayudan a orientarse; no obligar a crearlas al inicio. Cada sección puede tener permisos diferentes, pero debe indicar su audiencia y evitar que mover una publicación la haga más visible sin control.

El espacio admite descripción, reglas breves, publicaciones fijadas y orden editorial explicado. Orden cronológico siempre accesible dentro del contenido autorizado. La comunidad no impone su orden a todo el inicio personal.

Notificaciones iniciales: respuestas directas, menciones pertinentes y avisos administrativos relevantes; no cada alta, reacción o tema por defecto. Seguir temas o secciones es opcional. Las decisiones de seguridad o permisos no se ocultan entre avisos promocionales.

## 7. Autor, moderador y administrador

El autor puede editar o retirar su aportación bajo las reglas comunes. La comunidad puede limitar su presencia, cerrar una conversación o moderar, pero no reescribirla conservando la firma del autor. Los registros de decisiones no deben convertirse en copias públicas de datos retirados.

Propuesta: cerrar respuestas en una comunidad corresponde a moderación o a un rol explícitamente delegado; ser autor no concede poder unilateral para borrar desacuerdos. El autor puede solicitar cierre y dispone de bloqueo, silenciamiento y denuncia frente a acoso. La política de espacios personales se diseña por separado.

Un moderador puede tener conflicto de interés en una discusión. Ofrecer derivación a otro responsable y recurso fuera del equipo local cuando exista capacidad común. Si la comunidad es pequeña, declarar el límite y ofrecer canal de revisión, sin fingir independencia inexistente.

Bloquear a una persona no impide recibir decisiones moderadoras necesarias ni concede al moderador acceso a datos privados adicionales. En conversaciones compartidas puede plegarse contenido e interacción, con explicación de los límites del bloqueo.

## 8. Moderación local y garantías comunes

Acciones separadas: aviso, retirada local, limitación temporal de participación, cierre de hilo y expulsión. Deben indicar motivo, duración o revisión, ámbito y recurso. Una comunidad puede no admitir ciertos temas por su finalidad sin declarar prohibida esa expresión en toda la red.

No usar «coincido», reputación o encuestas espontáneas como procedimiento automático de sanción. Una mayoría que discrepa no convierte una aportación en abuso. Reportar no equivale a votar contra ella.

Los permisos de moderación se aplican a su ámbito. Expulsar de comunidad no elimina identidad ni publicaciones personales externas. El operador conserva sus responsabilidades de servicio, pero sus medidas se identifican como tales y no se hacen pasar por voluntad comunitaria.

## 9. Continuidad y administración

La iniciativa promotora no otorga propiedad sobre la comunidad ni poder permanente de veto, venta o cierre unilateral. La administración es una responsabilidad delegada y sustituible. El reconocimiento a quien inició el espacio no concede derechos de control perpetuos ni altera los derechos de autor sobre aportaciones individuales.

La continuidad es un requisito: toda comunidad debe disponer de un procedimiento de sustitución de responsables, recuperación de administración y cambio de alojamiento. La plantilla proporciona una política inicial sin exigir elegir sucesores al crearla. La continuidad requiere autoridad y respaldo verificables; no basta con una advertencia de fragilidad. Los detalles del procedimiento deben validarse antes de ofrecer la garantía, sin prometer recursos indefinidos.

Una ausencia no autoriza apropiarse del espacio automáticamente. Si todos los administradores pierden acceso, aplicar procedimiento distinto al de una cuenta personal huérfana: evidencia, reglas comunitarias, revisión y protección de privados. No otorgar administración solo por ser operador o miembro más activo.

Cambiar alojamiento conserva identidad comunitaria, roles, reglas y referencias conforme a autoridad válida. No implica trasladar cuentas personales ni permitir acceso a todo el historial a quien aloja el destino. En cifrado, las claves de lectura no se entregan al operador receptor por el traslado.

Cerrar una comunidad requiere avisar cuando sea posible, explicar conservación y permitir exportación de aportaciones propias dentro de los permisos. No prometer hospedaje perpetuo gratuito de un archivo completo. Los miembros no heredan automáticamente el derecho a republicar intervenciones ajenas.

## 10. Validación y decisiones pendientes

Comprobar: crear con una plantilla sin asistencia, distinguir leer/comentar/abrir tema, solicitar acceso sin revelar privados, impedir ampliación silenciosa de audiencia, seguir sin avisos excesivos, retirar aportación sin suplantación y recurrir una decisión con ámbito claro.

Quedan por resolver mediante recorridos: número y nombres finales de plantillas; historial para nuevos miembros; secciones con permisos; continuidad cuando no hay administradores; alcance del cierre por autor; perfiles de entidades frente a comunidades. La moderación común y la representación política requieren bloques específicos adicionales.
