---
title: Spartakos — Revisión de continuidad para el lunes 26 de octubre
lang: es-ES
license: CC-BY-SA-4.0
date: 2026-10-27
status: Registro de trabajo en curso; no aprobación ni versión de producción
---

# Revisión de continuidad

La revisión prevista es el lunes 26 de octubre de 2026. Este registro reúne resultados, límites y propuestas para facilitar la revisión conjunta. No sustituye la especificación ni la matriz de aceptación.

## Estado vigente antes de la revisión

- Funcionalidad disponible: borradores privados con papelera, edición con versión, retirada del cuerpo, citas y tres niveles, programación, Me gusta con cortes horarios y rescate local al perder permisos o membresía.
- Validación vigente: 109 pruebas automáticas superadas y recorridos sintéticos registrados; 49 documentos verificados. Los recuentos menores de los bloques anteriores son resultados históricos.
- Estadísticas: catálogo propuesto, sin aprobar ni implementar. La identidad distribuida, migración real y operación con proveedores siguen fuera del simulador.
- Preparación: seguir la [guía de revisión](GUIA-REVISION-PROTOTIPO.md) con un escenario separado. Antes de recargar un cliente abierto para cargar la versión actual, copiar el texto local que no se haya guardado.
- Rama de #2 sin integrar en main. No hay despliegue público ni nueva captación. Los datos del laboratorio del usuario se mantienen separados de los ensayos.

## Estado de partida

- Rama de trabajo: `prototipo-segunda-revision`; propuesta pública [#2](https://github.com/JLPalmes/spartakos/pull/2), sin integrar en main.
- Laboratorio local: `http://127.0.0.1:8787`; acceso libre con cuentas ficticias, no autenticación de producción.
- Última batería ejecutada al inicio de este bloque: 75 pruebas automáticas superadas; la matriz completa de producto sigue sin ejecutarse.
- Borradores recuperables implementados para publicaciones iniciales, con guardado explícito, versiones y copias ante conflictos.
- Estadísticas personales, comunitarias y globales documentadas como propuesta N11; sin captación nueva ni implementación.

## Orden de trabajo

1. Completar la gestión reversible de borradores y comprobar persistencia, privacidad y conflictos.
2. Desarrollar edición y retirada de publicaciones, preservando autoría, contexto de respuestas y restricciones de audiencia. Distinguir la retirada del cuerpo de una garantía de borrado de copias externas.
3. Revisar consistencia de editor, citas, avisos, programaciones y borradores después de los cambios.
4. Concretar el catálogo y permisos de estadísticas sin inventar seguimiento de lecturas, métricas globales exhaustivas ni clasificaciones de personas.
5. Consolidar resultados, límites, comprobaciones y propuestas pendientes para revisión.

## Límites de este trabajo

Conservar los datos locales existentes y separar los escenarios sintéticos. No publicar datos de ensayo del usuario. No integrar la rama principal, desplegar un servicio público ni contactar con terceros. No dar por aprobadas alternativas pendientes. Cualquier continuación debe inspeccionar los cambios presentes antes de editar y preservar el trabajo previo.

## Resultados acumulados

### Bloque 1 — 23 de octubre: gestión reversible de borradores

Implementada papelera privada y persistente, con restauración de contenido y estado anterior. Mover una referencia no retira publicaciones ni cancela programaciones; restaurarla no ejecuta de nuevo el envío. Se comprueban propiedad y versión. No hay borrado definitivo ni vaciado automático.

Comprobaciones: 78 pruebas automáticas superadas y recorrido de navegador con datos sintéticos. Se conservaron los datos locales del laboratorio. Se incorporan también las notas de estadísticas N11 y su desarrollo funcional, todavía sin implementación.

### Bloque 2 — 24 de octubre: edición propia y retirada del cuerpo

Implementada edición con versión, autoría y permisos, sin cambio de audiencia o contexto. Respuestas, citas y Me gusta anteriores conservan su referencia; se advierte sobre versiones anteriores y no se renueva automáticamente la aprobación. La retirada vacía el cuerpo activo, deja marcador y conserva respuestas ajenas. Las citas no muestran el cuerpo retirado y las programaciones que lo necesitan quedan bloqueadas. El autor puede retirar su propio texto tras perder acceso, sin recibir historial ajeno.

Comprobaciones: 88 pruebas automáticas superadas; edición y referencias anteriores comprobadas con dos clientes; vista sintética de marcador y cita retirada comprobada en navegador. No se modificaron publicaciones del laboratorio del usuario durante esas pruebas. Límites: sin borrado garantizado de copias/respaldos, historial público de cuerpos anteriores o moderación por terceros.

### Bloque 3 — 24 de octubre: consistencia de operaciones

Añadidos tres escenarios sintéticos de regresión: un borrador conserva estado y privacidad cuando se retira su fuente citada; una retirada obsoleta no borra una edición vigente; restaurar una referencia privada ya utilizada no reactiva el cuerpo retirado. Recuperar el estado serializado mantiene estos resultados. Batería completa: **91 pruebas superadas**, incluidos los 33 ensayos HTTP anteriores. Verificación documental y diferencias sin errores.

No se han modificado datos del laboratorio, comportamiento de producción ni configuración del servidor. Los controles de accesibilidad y el rescate persistente de ediciones siguen pendientes; no se presentan como verificados en este bloque. Los cambios se conservan en la rama de la propuesta #2, sin integrar en main.

### Bloque 4 — 24 de octubre: catálogo propuesto de estadísticas

El [diseño de estadísticas](DISENO-ESTADISTICAS.md) concreta fuentes, audiencias, actualización y conservación de una primera fase de gestión de recursos y pendientes. Propone excluir recuentos de comportamiento en grupos, sin atribuir anonimato a un umbral numérico. El panel público se limita como candidato a declaraciones voluntarias y fechadas de servicios, con cobertura y caducidad explícitas; no mide por sí mismo disponibilidad ni capacidad global.

Diez casos de aceptación documentales quedan pendientes de ejecución si se aprueba desarrollar el catálogo. No se ha añadido captación, implementación ni acceso a datos del laboratorio. Verificación editorial de 48 documentos y diferencias sin errores; la batería funcional vigente sigue siendo de 91 pruebas, sin repetirla por este cambio exclusivamente documental. Catálogo enlazado en la documentación de la rama de #2 para revisión, no decisión ratificada.

### Bloque 5 — 25 de octubre: controles del editor y pérdida de permisos

Ajuste local del cliente: cuando el autor conserva lectura pero pierde permiso de edición, el texto que estaba editando se presenta como rescate local de solo lectura, en lugar de ofrecer Guardar edición. La conservación no publica, no persiste el texto por sí misma ni recupera permisos. El mensaje de rescate también se aplica a retirada o pérdida de acceso. Se añaden identificadores estables a los controles de edición y retorno del foco al botón Editar publicación tras guardar o cancelar.

Comprobaciones realizadas: sintaxis del cliente correcta, batería completa de **91 pruebas superadas**, metadatos y enlaces de 48 documentos y diferencias sin errores. Estas pruebas de dominio y HTTP no validan el foco del navegador. El recorrido visual, los conflictos entre pestañas y teclado/lector de pantalla siguen pendientes: el canal del navegador dejó de responder antes de abrir el escenario sintético. No se modificaron datos del usuario ni se reinició su servidor.

**Comprobación posterior — 25 de octubre:** recuperado el navegador, se ejecutó el recorrido con datos sintéticos en un servidor separado. Guardar y cancelar devuelven el foco a Editar publicación. Dos pestañas de Bruno comprobaron el rechazo de una edición obsoleta, conservando su texto y mostrando la versión nueva. Al reducir Alicia el permiso de Bruno a lectura, su edición abierta apareció como rescate de solo lectura, sin Guardar edición y sin cambiar el cuerpo publicado. Se comprobó la propiedad `readOnly` del control. No se ha realizado evaluación con lector de pantalla ni auditoría completa de accesibilidad.

**Estado de publicación:** bloque incorporado a la rama de la propuesta #2 junto con esta evidencia. Los cambios permanecen en `prototipo-segunda-revision`, sin integrar en main. La copia local debe verificarse contra el remoto después de publicar; no descartar commits locales sin comprobar igualdad de contenido.

### Bloque 6 — 25 de octubre: rescate tras pérdida de membresía

Al perder acceso completo a una comunidad, la edición local ya conservada necesita un recorrido visible. Se añade aviso y botón para abrir Mi cuenta cuando existe texto propio en edición fuera de los espacios accesibles. Si el editor enfocado desaparece, el foco pasa al acceso al rescate; en una reducción de permisos con lectura, pasa al campo rescatado. Abrir el recorrido enfoca el texto local de solo lectura. No se publica ni guarda automáticamente, ni se recupera acceso al historial ajeno.

Recorrido sintético comprobado en servidor separado: Bruno publicó y dejó una edición abierta; Alicia le retiró la membresía. Desapareció el historial de comunidad, apareció el aviso con foco y Mi cuenta mostró únicamente la aportación propia y su edición local, con `readOnly` verificado. Se conservan los controles de retirada del texto propio ya existentes, sin ejecutarlos en este recorrido. La batería completa mantiene **91 pruebas superadas**; sintaxis, 48 documentos es-ES y diferencias correctos. No se accedió a datos del laboratorio del usuario. El bloque se incorpora a la rama de #2 para revisión, sin integrar en main.

### Bloque 7 — 25 de octubre: guion de revisión y límites de sesión

Preparada la [guía de revisión](GUIA-REVISION-PROTOTIPO.md), con recorrido por espacios, interacciones, conversaciones, borradores, programación, versiones y pérdida de permisos. Distingue persistencia del servidor de texto en memoria y orienta a usar un escenario separado. La inspección del cliente confirma que entrar en una cuenta reinicia los editores locales; la exportación no incluye texto que nunca se envió. No se añade aviso de salida, guardado automático ni promesa de recuperación tras cerrar sesión.

Cambio exclusivamente documental: verificación editorial de 49 documentos y diferencias sin errores. La batería funcional vigente sigue en **91 pruebas superadas**, sin repetirla por esta guía. El guion es para revisión, no una nueva acta de pruebas ni aprobación de estadísticas. Documentación incorporada a la rama de la propuesta #2, sin integrar en main.

### Bloque 8 — 25 de octubre: coherencia del cierre

Contrastados guía, informe y estado del cliente. Los 91 casos declarados coinciden con la batería vigente registrada; no se repiten pruebas de comportamiento sin cambio de código. Se añade una síntesis actual para distinguir resultados históricos y una instrucción de recarga que protege el texto local sin guardar. Verificación editorial de 49 documentos y diferencias sin errores. No hay nuevas funciones ni cambios de datos. Ajuste documental conservado en un commit local de la rama de #2, pendiente de publicación: el control de permisos del navegador agotó su tiempo de espera. No es una denegación ni un cambio del estado de los bloques ya publicados.

### Consolidación previa a la revisión — noche del 25 de octubre

No se inicia otro desarrollo. El cliente y las pruebas publicados siguen siendo los de la rama de #2; los últimos cambios pendientes son exclusivamente documentales. El navegador sigue sin conexión en esta comprobación, por lo que no se atribuye publicación al ajuste local. No se han modificado credenciales, desplegado servicios públicos ni integrado cambios en main.

Para la revisión quedan estas decisiones y comprobaciones:

- Valorar el recorrido de la guía y decidir si la experiencia permite otra prueba con participantes antes de integrar #2.
- Revisar el catálogo de estadísticas; sigue sin aprobación, implementación ni captación añadida.
- Priorizar respuestas recuperables y ediciones persistentes: actualmente solo los borradores de publicaciones iniciales tienen guardado explícito.
- Definir política de retención y copias; retirada del cuerpo activo no equivale a borrar respaldos o referencias privadas independientes.
- Planificar evaluación de accesibilidad, seguridad y matriz completa de producto; las 91 pruebas de laboratorio no las sustituyen.
- Mantener fuera de las garantías del prototipo la identidad distribuida, migración real, recuperación de cuentas y operación entre proveedores.

### Siguiente paso

Publicar los ajustes documentales locales cuando vuelva el acceso al navegador, comprobando igualdad de contenido antes de alinear referencias. Al llegar al lunes, confirmar este estado y detener los bloques autónomos. No ampliar alcance ni repetir recorridos ya registrados sin motivo; cualquier bloqueo de publicación debe quedar explícito para la revisión.

### Disciplina de continuidad

Inspeccionar rama, cambios locales y propuesta de revisión antes de continuar. La automatización no confirma por sí misma nuevas decisiones de producto. No empezar otro bloque tras el lunes 26; consolidar los resultados y límites. Registrar aquí las pruebas reales y el estado de publicación de cada bloque.


## Continuación autorizada tras la revisión — 26 de octubre

Reanudadas las comprobaciones por indicación del usuario, sin exigirle ejecutar ensayos funcionales automatizables. Al comenzar, árbol limpio y rama sincronizada tras fetch. Los ajustes documentales anteriores ya figuran en el remoto; su condición pendiente en los bloques históricos queda superada. El ajuste del cursor al final fue confirmado por el usuario y publicado en el commit `93aae8a`.

La nueva prueba integrada de programación verifica bloqueo sin cliente, persistencia tras reinicio, rechazo sin permisos, ausencia de reactivación al recuperarlos y publicación única solo por acción explícita. Resultado global: **92 pruebas superadas**, 34 de ellas HTTP. No cambia el comportamiento del producto ni se accede a datos del usuario. La nueva prueba y el recuento documental se reúnen en esta unidad para su incorporación autorizada a la rama de la propuesta #2. La revisión estadística y las limitaciones estructurales siguen pendientes. No se integra en main.


## Borradores de respuesta y edición — 27 de octubre

Implementados los guardados explícitos privados de respuesta y edición, recuperación en Borradores, conservación de contexto/versión, copias ante conflictos y revisión expresa cuando cambia el original. Enviar o aplicar consume el pendiente de manera atómica con el resultado y revalida permisos. La migración a esquema 8 conserva los borradores anteriores. Programación y guardado automático de estos tipos no se añaden.

**109 pruebas superadas**, incluidas tres HTTP nuevas con reinicios reales y catorce de dominio. No se usa ni modifica el escenario de prueba del usuario o su almacenamiento anterior. La comprobación visual de la ampliación queda pendiente porque no hay herramienta de control del navegador disponible; la sintaxis y el comportamiento del servicio sí se han verificado. La nueva unidad se incorpora a la rama de la propuesta #2 con autorización para guardar y publicar. La comprobación visual permanece pendiente; no integrar en main.

Siguiente comprobación: recorrido visual de Guardar, Retomar, copia y revisión de versión cuando vuelva a estar disponible el control del navegador. Después revisar las decisiones de producto pendientes, sin pedir al usuario ejecutar las pruebas de permisos o persistencia que ya están automatizadas.


## Cierre de borradores y preparación estructural — 27 de octubre

Ampliación de borradores revisada y publicada en `64bf832` en la rama de #2, sin integrar en main. Repetida la batería final: **109 pruebas superadas**, 49 documentos verificados antes de añadir el protocolo estructural. La comprobación visual sigue pendiente por falta de herramienta de navegador. La actualización del título/descripción de #2 mediante el conector fue denegada por permisos de la integración (403); esto no impidió publicar el código mediante Git. No se modificó la autenticación ni se contactó con terceros.

Preparado [el ensayo de traslado individual](ENSAYO-02-TRASLADO-INDIVIDUAL.md), con diez casos, condiciones de control de identidad, interrupción, autoridad caducada, pérdida del directorio, privacidad y reanudación. Es un protocolo no ejecutado: no convierte una copia de archivos ni una identidad ficticia en prueba de soberanía. El siguiente bloque ejecutable requiere inventariar y comparar componentes existentes antes de elegir la integración de laboratorio; no se adopta una arquitectura de producción. Verificación documental ampliada a 50 documentos con idioma es-ES.


## Investigación de identidad y continuidad — 27 de octubre

Revisadas fuentes primarias de nueve alternativas o familias: claves estáticas, Nostr básico, did:web, PLC, PKARR, did:dht, did:webvh, KERI y ION/Sidetree. La [comparación](ARQUITECTURA-04-CANDIDATOS-DE-IDENTIDAD.md) propone KERIpy para el primer laboratorio de continuidad, sin adoptar la arquitectura. PLC queda como contraste explícito de dependencia de un directorio común. Se inventariaron siete repositorios por SHA; se verificó KERIpy 1.3.6 como etiqueta numérica candidata, diferenciándola del HEAD de desarrollo. La compatibilidad de didwebvh-py con la especificación v1.0 no se presume a partir de su versión de paquete.

No se instalaron componentes ni se ejecutaron ensayos estructurales. No hay nuevas pruebas funcionales ni cambios del simulador: la batería vigente sigue en 109 pruebas. Verificación editorial ampliada a 51 documentos es-ES y validación del inventario JSON. El bloque documental se incorpora a la rama de revisión mediante commit y push autorizados. La rama se verificó inicialmente limpia y sincronizada mediante fetch. No se integra main ni se modifican los datos del usuario.

Siguiente bloque propuesto: entorno aislado para KERIpy con revisión fijada, dependencias e integridad inventariadas; comprobar persistencia, rotación y rechazo de autoridad antes de ejecutar traslado entre dos alojamientos. Si no puede comprobarse una garantía, se declara pendiente o fallida, sin sustituirla por identidades ficticias ni criptografía propia.

## Primer laboratorio real de identidad — 27 de octubre

Preparado el [laboratorio KERIpy](laboratorio-identidad/README.md) en un entorno temporal separado, sin cambios globales ni datos del usuario. Cinco pruebas superadas: persistencia en tres procesos, rotación conservando identidad, firma inválida, clave no comprometida, clave antigua y repetición de evento. Las dos primeras propiedades se verifican juntas en una prueba. Comprobación de dependencias sin conflictos y 101 pruebas propias de libsodium superadas; cifras separadas de las 109 funcionales del simulador, que no se ha modificado.

Inventariadas versiones, fuentes y hashes, sin claves ni rutas privadas. No se ha verificado la firma de la distribución nativa ni completado una auditoría de vulnerabilidades. Pendientes testigos, particiones y traslado entre proveedores. Cambios locales en la rama de revisión, sin integrar main ni publicar este bloque. Siguiente propuesta: testigos de referencia y disponibilidad antes de ampliar el ensayo de traslado.

## Recibos de testigos y vistas discrepantes — 27 de octubre

Siete pruebas nuevas superadas, doce de identidad en total, separadas de las 109 funcionales. Se verifican recibos suficientes/insuficientes, duplicados, impostores, conservación del estado previo y contradicciones entre eventos y entre dos verificadores aislados. Se usan claves sintéticas y bases temporales; sin cambios del simulador ni datos del usuario.

Hallazgo: si el titular y un testigo compartido firman dos ramas, los verificadores aislados pueden aceptarlas por separado. Detectan el conflicto cuando se les entrega la otra rama; no convergen automáticamente. Los recibos se entregaron directamente a la API: quedan pendientes servidores de testigos, transporte, reanudación automática y contraste operativo entre fuentes. El [laboratorio](laboratorio-identidad/README.md) recoge el alcance y la reproducción. Cambios locales pendientes de commit y push; remoto comprobado mediante fetch, sin integración en main.

## Continuación autónoma: HTTP, caída abrupta y diagnóstico — 27 de octubre

Ejecutadas tres pruebas HTTP adicionales: dos escenarios completos de continuidad con cierre normal/terminación abrupta y una reproducción diagnóstica de H01. Total: 15 comprobaciones del laboratorio, separadas de las 109 funcionales. Testigos en procesos con almacenes separados; sockets solo locales, sin servicios permanentes ni datos del usuario. Se comprueban conexión rechazada, conservación del estado, reapertura con la misma identidad, recibo persistido, reenvío explícito, rotación y rechazo de claves/recibos antiguos.

H01: el endpoint de referencia devuelve un recibo firmado para un evento con firma de autor inválida ausente de su historial aceptado. El verificador completo sí lo rechaza. La reproducción correcta de ese comportamiento no aprueba la seguridad del endpoint. Integración de ese servicio en producción descartada mientras no se resuelva y verifique; no es una decisión sobre adoptar o descartar todo KERI. No se contacta con terceros.

Consulta OSV para 34 versiones PyPI sin avisos devueltos; no sustituye auditoría ni cubre dependencias nativas. Pendientes firma de libsodium, reanudación tras reinicio del coordinador y contraste operativo entre fuentes. Cambios conservados localmente en la rama de revisión, sin commit/push ni integración en main. La continuidad autónoma no se condiciona a una respuesta rutinaria del usuario.

### Recuperación del evento pendiente entre tres procesos

Añadida una prueba de persistencia de escrow: guardar con un recibo, cerrar, reabrir, añadir solo el recibo faltante y procesar las colas oficiales, volver a cerrar y comprobar el resultado en un tercer proceso. No se reenvía el evento. Total de laboratorio: 16 comprobaciones, incluida la reproducción de H01; no equivale a 16 garantías de seguridad aprobadas. La recuperación del verificador se prueba separadamente del transporte HTTP. Documentación y reproducción conjunta actualizadas. Sin necesidad de decisión del usuario para estas pruebas; pendientes composición completa, caducidad y contraste persistido.

### Cierre autorizado del laboratorio para revisión

El usuario autoriza commit y push de esta unidad. Repetidas las 16 comprobaciones del laboratorio y la validación de los 52 documentos; revisión de archivos nuevos sin claves privadas, credenciales, datos del usuario ni rutas del entorno temporal. Se prepara su publicación en la rama de la propuesta #2, sin integrar main. Las anotaciones anteriores de cambios pendientes describen el estado previo a esta autorización. H01 sigue reproducido y sin resolver; no se aprueba el endpoint para producción.

## Revisión de H01 y protección local de laboratorio

Inicio con árbol limpio y remoto verificado mediante fetch. Leída por SHA una revisión oficial posterior de desarrollo: conserva el flujo relevante por inspección, sin acreditar una corrección ejecutada. Se mantiene KERIpy 1.3.6; no se instala código de desarrollo.

Añadido AcceptedHistoryHab como adaptador experimental opcional: exige coincidencia de digest por secuencia y bytes almacenados antes de delegar la firma del recibo. Dos pruebas nuevas verifican rechazos de eventos no aceptados y continuidad con caída/rotación. Total: 18 comprobaciones, incluida la reproducción del problema original. No se aprueba concurrencia ni servicio completo para producción; no se modifica código ajeno, simulador ni datos del usuario. Fuentes y hashes en laboratorio-identidad/revision-h01.json. Unidad local pendiente de commit/push, separada del commit 9184af4 ya publicado. Próximo bloque: combinar HTTP, escrow persistido y reinicio del verificador.

## Ensayo combinado de HTTP y recuperación persistida

Inicio con cambios locales del adaptador conservados y remoto verificado mediante fetch. Añadida una prueba que combina testigos HTTP, terminación abrupta de un testigo y procesos verificadores separados sobre la misma base. Se conserva el evento pendiente mientras falla la conexión; tras reabrir el testigo, un verificador nuevo obtiene por HTTP el recibo persistido y completa el evento sin reenviarlo. Otros procesos confirman el resultado. Total: 19 comprobaciones, incluida la reproducción de H01, con el simulador intacto.

El coordinador de pruebas actualiza explícitamente el puerto del testigo reiniciado; no se afirma descubrimiento automático. Los procesos verificadores cierran normalmente y el testigo se termina después de responder: no se simula pérdida de alimentación durante escritura. Pendientes caducidad y contraste persistido de fuentes discrepantes. Cambios locales de esta unidad y del adaptador pendientes de commit/push; no se integra main ni se cambia una política de confianza.

### Publicación autorizada de la protección y el ensayo combinado

El usuario autoriza commit y push de ambas ampliaciones. Repetidas las 19 comprobaciones y la validación de 52 documentos; inventarios JSON revisados sin credenciales, claves privadas ni rutas del entorno temporal. Se prepara la publicación en la rama de la propuesta #2, sin integrar main. Las notas anteriores de cambios pendientes corresponden al estado previo a esta autorización; la mitigación de H01 sigue siendo experimental.

## Caducidad y contraste persistido

Inicio con árbol limpio y sincronización remota verificada mediante fetch. Añadido keri_lifecycle.py con tres escenarios ejecutados: frontera de caducidad y reenvío explícito, conservación de evidencia tras caducidad de la cola de contradicciones, y contraste entre dos bases que aceptaron ramas distintas tras reiniciar sus procesos. Total: 22 comprobaciones, incluida la reproducción de H01. Reloj controlado solo en pruebas; bases sintéticas separadas, sin cambios del simulador ni datos del usuario.

Hallazgos: salir de una cola no revoca un evento ni resuelve una contradicción. Tras caducar la entrada de posible duplicidad, la evidencia sigue disponible en este ensayo, pero ya no aparece en esa cola. Se proponen registros separados de conflictos y cancelaciones explícitas. No se afirma retención indefinida, sincronización automática ni convergencia. Cambios locales pendientes de commit y push. Próximo bloque: balance documental de garantías demostradas y pendientes frente a E/T, sin necesidad de decisión del usuario para elaborarlo.

### Publicación autorizada del ciclo de vida

El usuario autoriza commit y push de las pruebas de caducidad y contraste persistido. Repetidas las 22 comprobaciones y la validación de 52 documentos; archivo nuevo revisado sin credenciales, claves privadas ni rutas locales. Se prepara la publicación en la rama de la propuesta #2, sin integrar main. Las notas de cambios pendientes anteriores describen el estado previo a esta autorización.

## Balance de viabilidad de identidad y traslado

Inicio con árbol limpio y sincronización remota comprobada mediante fetch. Preparado BALANCE-01-IDENTIDAD-Y-TRASLADO.md: conclusión provisional, garantías observadas y límites, cobertura individual de E01–E15 y T01–T10 y condiciones de paso. Ningún caso estructural se da por completo. Las 22 comprobaciones siguen siendo de componentes; no hay traslado ejecutado ni arquitectura de producción adoptada.

Próxima unidad concreta: investigar y ensayar autorización y resolución de destinos con mecanismos existentes de KERIpy, separando claves del titular y autoridad del servicio. Solo después preparar perfil público A/B, observador y origen apagado. Se conserva H01 abierto, firma de distribución nativa pendiente y límites de confianza/operación. Documento y enlaces locales preparados; no se modifica código ni datos del simulador. Cambios locales pendientes de commit/push. No se necesita decisión del usuario para el siguiente ensayo reversible; una dependencia común obligatoria sí exigiría decisión explícita antes de adoptarla.

## Roles y direcciones de proveedores con mecanismos existentes

Inicio conservando el balance documental local pendiente y con remoto verificado mediante fetch. Añadido keri_destinations.py: cinco pruebas con makeEndRole, makeLocScheme y verificación nativa. Total de laboratorio: 27 comprobaciones, sin cambios del simulador ni datos del usuario. Se comprueban autorización independiente de dirección, revocación tras reabrir almacenes, reenvío antiguo y declaraciones falsas de proveedor.

Límites observados: agent permite varios proveedores y una vista no actualizada conserva A. No se demuestra exclusividad de escritura ni traslado; los endpoints son valores sintéticos sin servidores de perfil. Se actualiza el balance a cobertura parcial de autorización, sin dar por completo ningún E/T. Próxima unidad: orden, igualdad de fechas y cambios de claves en declaraciones de destino. Cambios del balance y esta unidad locales, pendientes de commit/push; sin adopción de arquitectura de producción.

### Publicación autorizada del balance y los destinos

El usuario autoriza commit y push del balance de garantías y del ensayo de roles y direcciones. Repetidas las 27 comprobaciones y la validación de 53 documentos; archivos nuevos revisados sin credenciales, claves privadas ni rutas del entorno temporal. Se prepara la publicación en la rama de la propuesta #2, sin integrar main. Las notas de cambios pendientes anteriores corresponden al estado previo a esta autorización.

## Orden, fechas iguales y época de firma en destinos

Inicio con árbol limpio y remoto comprobado mediante fetch. Cuatro pruebas nuevas elevan el laboratorio a 31 comprobaciones. Con fechas distintas converge el caso concesión/revocación en ambos órdenes; con igual fecha/época cada observador conserva lo primero recibido, incluso tras reapertura y repetición. Una declaración de nueva época prevalece en el escenario probado; rotar sin nueva declaración no revoca roles.

Se precisa el criterio del balance: varios proveedores son compatibles con Spartakos; lo que falta es delimitar autoridad y revisión de cada objeto, no imponer un servidor único. No se adoptan respuestas de rol como registro global exclusivo ni se inventa desempate. Próxima unidad: alcance de autorización del perfil mínimo y su vinculación a eventos ordenados del componente, conservando conflicto y actualidad como límites explícitos. Sin cambios del simulador ni datos del usuario; unidad local pendiente de commit/push.

## Ensayo de autoridad de revisiones de perfil

Inicio preservando cambios locales de orden y vigencia; remoto comprobado mediante fetch. Añadido keri_profiles.py con siete pruebas, total 38 de laboratorio. Un perfil público sintético se vincula mediante huella a eventos KERI validados; el enlace de aplicación es experimental, no un protocolo de perfil nativo. Se comprueban copia, alteración, firma ajena, identidad del cuerpo, historial, rotación, vista atrasada y ramas firmadas incompatibles.

La inspección distingue cabeza en la vista de actualidad global desconocida. No se usa esa cabeza como permiso de actuación ni se oculta el conflicto. A/B son copias de bytes, no servidores; faltan persistencia del enlace y bloqueo duradero por conflicto. Próxima unidad: persistencia y conflicto del perfil antes de entrega A/B con origen apagado. No se modifica el simulador ni datos del usuario. Cambios de orden y perfil locales pendientes de commit/push.

### Publicación autorizada de orden y perfil

El usuario autoriza commit y push de los ensayos de orden y perfil, y continuar después con persistencia y conflicto. Repetidas las 38 comprobaciones y la validación de 53 documentos; archivo nuevo revisado sin secretos ni rutas privadas. Se prepara la publicación en la rama de #2 sin integrar main. Las notas previas de cambios pendientes corresponden al estado anterior a esta autorización.

## Publicación y continuación con persistencia de perfil

Publicado eb238b3 con los ensayos de orden y perfil, tras repetir 38 comprobaciones y verificar 53 documentos; rama limpia y coincidencia remota confirmadas antes de continuar. La propuesta #2 permanece asociada y no se integra main.

Continuación autorizada: añadido keri_profile_state.py con tres pruebas nuevas, total 41. El perfil y su referencia sobreviven a otro proceso; un registro local separado mantiene bloqueo por conflicto después de reinicio y caducidad de la cola; una firma ajena no crea evidencia verificada. La validación de ramas del arnés se limita a sn=1 sin rotación/testigos/delegación. No se prueban cortes entre KERI y SQLite, corrupción o pérdida del registro; no estar bloqueado no equivale a autorización ni actualidad global.

Datos sintéticos temporales, sin cambios del simulador ni datos del usuario. La continuación queda local pendiente de commit/push; la autorización previa se ejecutó para los cambios existentes antes de continuar. Siguiente unidad: entrega HTTP A/B con origen apagado y verificador separado, declarando que recuperación de entrega no es traslado completo de autoridad.

## Entrega HTTP del perfil con A apagado

Inicio preservando la ampliación local de persistencia y con remoto verificado mediante fetch. Añadido keri_profile_http.py con cinco pruebas, total 46 de laboratorio. Dos servicios HTTP locales de solo lectura entregan perfil e historia firmada desde directorios separados, sin claves del titular; el verificador tiene su base e identidad esperada propias. A se apaga y se comprueba la conexión fallida antes de recuperar B. Se rechazan por validación específica contenido alterado, cuerpo sin anclaje y sustitución de titular; un cuerpo anterior queda histórico en la vista actualizada.

Es recuperación de entrega, no traslado completo: direcciones proporcionadas por el coordinador, autorización de roles no compuesta aún con HTTP, sin escritura delegada ni cambio de destino. No se modifica el simulador ni los datos del usuario. Pendientes unir resolución autorizada y entrega, actualizar con A apagado y contrastar la copia anterior al volver A. La ampliación de persistencia y esta unidad quedan locales pendientes de commit/push.

### Publicación autorizada de persistencia y entrega

El usuario autoriza commit y push y continuar después. Repetidas las 46 comprobaciones y la validación de 53 documentos; archivos nuevos revisados sin claves privadas ni rutas privadas. Se prepara la publicación de persistencia y entrega HTTP en la rama de #2, sin integrar main. Las notas previas de trabajo local corresponden al estado anterior a esta autorización.

## Publicación y composición de resolución autorizada con HTTP

Publicado 9d94a47 con persistencia y entrega HTTP tras repetir 46 comprobaciones y verificar 53 documentos. Árbol limpio y remoto coincidente antes de continuar; propuesta #2 asociada, sin integrar main.

Continuación autorizada: añadido keri_authorized_delivery.py con tres pruebas, total 49 de laboratorio. Dirección sin autorización se rechaza antes de abrir HTTP. Con A apagado, revocación recibida y B autorizado se obtiene el perfil; el titular firma una nueva revisión y B la entrega. A vuelve y anuncia dirección nueva, pero no restaura el rol; su copia anterior se reconoce histórica en la vista actualizada. Se verifica reapertura de almacenes del observador, sin reinicio completo en esta composición.

Roles, direcciones y revisiones se distribuyen explícitamente al parser por el coordinador. No hay descubrimiento automático, escritura delegada, actualidad global ni E/T completado. Próxima unidad: cambios parciales e interrupción con procesos verificadores nuevos. La continuación queda local pendiente de commit/push; la autorización de publicación anterior ya se ejecutó para los cambios que existían antes de continuar. Sin cambios del simulador ni datos del usuario.

## Pruebas de cambios parciales e interrupciones solicitadas

Inicio con la composición local anterior conservada y remoto comprobado mediante fetch. Añadido keri_partial_delivery.py con cuatro pruebas, total 53 de laboratorio. Cinco procesos sucesivos comprueban inicialización, recepción parcial, persistencia de la vista parcial, completado repetido y persistencia final. Solo revocación deja sin proveedor autorizado; solo autorización deja ambos; ninguna conserva A. Los cuatro escenarios terminan con B y sin A tras completar mensajes, sin duplicar el cuerpo del perfil.

Una salida abrupta después de commits y lecturas, sin cierres normales, conserva la vista parcial en el proceso siguiente. No se interrumpe una transacción ni se simula fallo de alimentación. Los proveedores permanecen disponibles en este bloque; su caída se prueba separadamente. No hay sincronización automática ni cambio atómico de roles. La composición anterior y este ensayo quedan locales pendientes de commit/push, sin cambios del simulador ni datos del usuario. Próxima unidad: consolidar condiciones de aceptación y estados incompletos del perfil público mínimo.

### Publicación autorizada de composición e interrupciones

El usuario autoriza commit y push y continuar después. Repetidas las 53 comprobaciones y la validación de 53 documentos; archivos nuevos revisados sin secretos ni rutas privadas. Se prepara la publicación de entrega autorizada y estados parciales en la rama de #2, sin integrar main. Las notas previas de cambios locales se refieren al estado anterior a esta autorización.

## Publicación y cierre de alcance del perfil público

Publicado f1f121d con entrega autorizada y vistas parciales tras repetir las 53 comprobaciones y verificar 53 documentos. Rama limpia y coincidencia remota confirmadas antes de continuar, con la propuesta #2 asociada y sin integrar main.

Continuación documental: preparado PERFIL-01-ACEPTACION-DEL-ENSAYO-PUBLICO.md con doce criterios trazables, estados independientes y límites explícitos de integridad, autoridad, historial, conflicto y actualidad. Propuestas de comportamiento aún no implementadas; no se eleva el total de 53 comprobaciones ni se completa un E/T. Siguiente bloque: inventario público firmado, objetos y referencias estables desde observador independiente, con origen apagado, ausencias, alteración y retiradas. No se incluyen datos privados ni migración externa en ese ensayo. La unidad documental queda local pendiente de commit/push; no se modifican código ni datos del simulador.

### Publicación autorizada del cierre público mínimo

El usuario autoriza commit y push y continuar después. Validados 54 documentos, enlaces e idioma; esta unidad solo modifica documentación y no requiere repetir las 53 comprobaciones de código ya superadas. Se prepara su publicación en la rama de #2, sin integrar main. Las notas de cambios pendientes anteriores corresponden al estado previo a esta autorización.

## Publicación documental y ensayo del inventario público

Publicado 8991ea5 con el cierre del perfil tras verificar 54 documentos. La unidad era documental; no se repitieron sin cambios las 53 comprobaciones de código. Árbol limpio y remoto coincidente antes de continuar, con #2 asociada y sin integrar main.

Continuación autorizada: añadido keri_inventory.py con cuatro pruebas, total 57 de laboratorio, e informe ENSAYO-03-INVENTARIO-PUBLICO.md. Inventario público anclado por el titular, servidores A/B de solo lectura y verificador en proceso nuevo por recepción. Con A apagado, se conservan IDs y versiones y se resuelve una referencia preexistente del observador. Ausencia/alteración impide aplicar el catálogo; el reintento corregido funciona. El marcador de retirada elimina el cuerpo anterior del catálogo y un inventario viejo no lo resucita al volver A.

Límites: autorización de servicios y registro de conflicto aún separados del restaurador; incompletitud informada pero no persistida como etapa; anclaje KERI y catálogo no son una transacción conjunta. Sin datos privados ni cambios del simulador. Siguiente unidad: composición y recepción incompleta persistida. Esta continuación queda local pendiente de commit/push, distinta de la unidad documental ya publicada.

## Continuación autónoma hasta nueva interacción

El usuario pide continuar hasta su próxima interacción humana, sin fecha de corte. Reactivada la automatización existente con el directorio correcto /Users/juanluis/Projects/spartakos, comprobación horaria y término por regreso humano; los latidos no cuentan como regreso. Se conserva la política de notificación previa. No se autoriza publicar automáticamente nuevos bloques ni integrar main. Antes de iniciar cada bloque se comprobará si ya ha regresado y se eliminará la automatización al detectarlo.

Revisado Git: cambios locales de inventario preservados y remoto verificado mediante fetch. La sesión de la batería anterior ya no estaba accesible, por lo que no se atribuye un resultado recuperado a aquella ejecución. Se añade y ejecuta una quinta prueba de inventario: intención de recepción persistida, secuencia esperada/aplicada y salida abrupta antes de aplicar. Otra conexión verifica el pendiente y el catálogo anterior; un nuevo proceso reintenta y completa. Ausencia y alteración comprueban también su estado persistido. Total previsto actualizado a 58 y nueva batería completa a ejecutar para confirmación.

Estados receiving/incomplete/complete solo del arnés; KERI y SQLite siguen separados y no se prueba corte durante transacción. Documentación e inventario actualizados. Siguiente unidad autónoma: composición del inventario con autorización de servicio y conflicto duradero, conservando actualidad desconocida. Todos los cambios posteriores a 8991ea5 permanecen locales pendientes de commit/push; no se modifica el simulador ni datos del usuario.

### Verificación final de esta continuación

Confirmadas 58 comprobaciones completas y 55 documentos validados. La ejecución completa mostró avisos por conexiones SQLite de inspección sin cerrar; se corrigió su cierre explícito y se repitieron las cinco pruebas de inventario con ResourceWarning tratado como error, sin avisos. No se repitieron las demás suites por ese cambio limitado al cierre de conexiones de prueba. Automatización actualizada y activa hasta nueva interacción humana; siguiente bloque pendiente: composición de inventario con autorización y conflicto. Cambios locales conservados, sin commit/push adicional ni integración en main.

## Continuación automática: revisiones inmutables — 27/28 de octubre

No se detecta una nueva interacción humana tras la autorización de trabajo autónomo; los cambios de contexto horario no se consideran regreso. Árbol con cambios locales de inventario conservados y fetch completado; rama publicada sin divergencia. La verificación previa confirma 58 comprobaciones y 55 documentos, sin repetir bloques ya cerrados.

Antes de componer nuevas piezas se cierra una brecha de integridad referencial: inventario posterior autorizado no puede cambiar los bytes de una publicación conservando ID y revisión. Añadida I06 y ejecutadas seis pruebas de inventario con ResourceWarning tratado como error, todas correctas. Controles adicionales impiden retroceder cabeza y reactivar revisiones retiradas; sus regresiones dedicadas quedan pendientes y no se presume cobertura. Una transición rechazada puede conservar receiving; queda por clasificar esos errores de forma persistida.

Total del laboratorio actualizado a 59; pendiente repetir batería completa para confirmarlo. Siguiente bloque: regresiones de transición y estado de error persistido, antes de composición con autorización y conflicto. Ningún cambio del simulador, datos del usuario, commit/push, despliegue o contacto con terceros. No se necesita decisión crítica.

Verificación del cierre automático: 59 comprobaciones completas superadas, 55 documentos es-ES y enlaces/licencias verificados; diff sin errores de formato. Trabajo local conservado en la rama de #2, sin publicación. Pendientes inmediatos registrados; no hay decisión crítica ni acción necesaria del usuario.

## Continuación automática: transiciones rechazadas persistidas — 28 de octubre

No hay nueva interacción humana desde la autorización; continúa el latido. Git comprobado con cambios locales conservados y fetch correcto, sin divergencia publicada. Leídos los resultados previos de 59 comprobaciones y 55 documentos para no repetir trabajo.

Añadidas I07 e I08: inventarios posteriores autorizados que intentan retroceder cabeza o reactivar la misma revisión retirada se rechazan antes de modificar el catálogo. InventoryTransitionError guarda rejected y código estable, con secuencia esperada/aplicada conservadas. I06 comprueba también su registro. I07/I08 terminan con una intención posterior válida que se acepta en otro proceso sin retroceder la historia KERI. Ocho pruebas de inventario superadas con ResourceWarning tratado como error; total previsto 61, pendiente confirmación completa.

No se presume clasificación exhaustiva de errores; receiving puede permanecer en otros fallos. Pendiente una regresión para omisión de objeto anterior y composición con autorización y conflicto. Sin decisiones críticas, publicación, cambios del simulador, datos reales, despliegue o contacto con terceros. Documentación en es-ES actualizada y cambios conservados localmente.

Cierre de verificación: 61 comprobaciones completas superadas, 55 documentos validados con idioma es-ES, enlaces y licencias; diff sin errores. Estado local conservado sin commit/push. No se requiere intervención del usuario; siguientes límites y regresiones pendientes registrados.

## Continuación automática: inventario con puerta de autorización y conflicto — 28 de octubre

No hay regreso humano; fetch correcto y cambios locales preservados. Revisados resultados previos de 61 comprobaciones y 55 documentos. Añadido keri_inventory_access.py: cuatro pruebas componen el restaurador con rol/dirección nativos y registro local de conflicto. Una dirección sin permiso y un conflicto previamente verificado bloquean antes de HTTP; la entrega autorizada funciona y una revocación recibida durante descarga impide aplicar el catálogo. El restaurador acepta un callback opcional antes de aplicar, sin romper su entrada básica de laboratorio.

Corregida durante preparación una ausencia del directorio del fixture; las cuatro pruebas focalizadas pasan con ResourceWarning como error. Total previsto 65, pendiente confirmación completa. Alcance: un objeto, reapertura en el mismo proceso, registro acotado de conflicto sn=1 y distribución explícita de declaraciones. Repetir controles no elimina la ventana comprobación/commit ni crea transacción entre almacenes. La entrada básica sigue sin puerta y no es servicio protegido.

Pendientes: omisión de objeto previo, estados de bloqueo persistidos y composición en proceso nuevo/interrupción. No se completa E/T ni se adopta arquitectura. Sin commit/push, main, despliegue, datos reales o terceros; no se requiere decisión crítica.

Cierre confirmado: 65 comprobaciones completas superadas, 55 documentos es-ES validados y diff sin errores de formato. Corrección de la generación documental completada y verificada. Cambios locales conservados; sin commit/push adicional. No hay decisión crítica ni intervención necesaria.

## Continuación automática: omisión y bloqueo persistido — 28 de octubre

Sin interacción humana nueva; estado Git y fetch comprobados, cambios previos conservados. Leído cierre confirmado de 65 comprobaciones/55 documentos. Añadida I09 para omisión de objeto anterior sin retirada: rechazo persistido y catálogo intacto. La composición guarda ahora checking/blocked/incomplete/complete como último intento por identidad/proveedor, con código conocido. Las cuatro pruebas de acceso verifican persistencia desde otra conexión y reintento válido tras nueva autorización del titular.

Nueve pruebas de inventario y cuatro de acceso pasan con ResourceWarning tratado como error; total previsto 66, pendiente confirmación completa. No hay telemetría ni historial de actividad: solo estado sintético del intento local. checking/receiving pueden permanecer en fallos no clasificados y no prueban proceso activo; complete no concede autorización futura. Pendientes composición entre procesos nuevos y cortes entre almacenes.

Sin commit/push, main, servicios públicos, datos del usuario o terceros. Ninguna decisión crítica requerida; documentación es-ES y resumen actualizados.

Cierre confirmado: 66 comprobaciones completas superadas y 55 documentos validados en es-ES; diff sin errores. Trabajo local conservado sin commit/push. Continuar por composición en procesos nuevos e interrupciones, sin repetir estas regresiones salvo cambios relevantes. No se requiere intervención del usuario.

## Continuación automática: composición en procesos nuevos — 28 de octubre

Sin regreso humano; comprobados Git y fetch, preservado el inventario local y revisado cierre anterior de 66 comprobaciones/55 documentos. Añadida entrada de trabajador experimental a keri_inventory_access.py y tres regresiones de composición. Procesos nuevos restauran y repiten sin duplicar objeto; salida abrupta instrumentada antes de aplicar conserva catálogo vacío, recepción receiving uno/cero e intento checking; otro proceso revalida y completa. Una revocación firmada entre interrupción y reintento bloquea hasta una nueva autorización válida.

Siete pruebas de acceso focalizadas superadas con ResourceWarning tratado como error. Total previsto 69, pendiente batería completa. No se interrumpe una escritura activa ni se elimina la ventana comprobación/commit; solo un objeto, mismo equipo y distribución de declaraciones por coordinador. Conflicto entre interrupción y reintento y errores operativos persistidos quedan como siguiente bloque.

Sin commit/push, cambios de main, despliegues, datos reales ni terceros; documentación en es-ES actualizada. No se requiere decisión crítica ni intervención humana.

Cierre confirmado: 69 comprobaciones completas superadas, 55 documentos es-ES verificados y diff sin errores. No se publica ni integra; estado local conservado. Pendientes inmediatos registrados para no repetir bloques al siguiente latido. Sin intervención humana necesaria.

## Continuación automática: conflicto tras interrupción y fallos de entrega — 28 de octubre

No hay regreso humano. Git y fetch correctos, cambios locales preservados y cierre previo de 69 comprobaciones/55 documentos leído. Añadidas tres regresiones: evidencia de conflicto incorporada tras interrupción bloquea dos procesos nuevos, incluso con nueva autorización de proveedor; proveedor apagado y prueba HTTP 404 registran failed con código y completan tras corregir disponibilidad. No se guardan URLs o textos de error en el registro del último intento.

Diez pruebas focalizadas de acceso pasan con ResourceWarning como error; total previsto 72, pendiente confirmación completa. El registro de conflicto sigue limitado a ramas sn=1. No se clasifica todo formato/almacenamiento/validación ni se resuelve el conflicto. Próxima unidad: interrupción después de aplicar catálogo y antes de registrar complete en el último intento, verificando qué estado puede justificarse sin falsa confirmación.

Sin commits, push, main, despliegues, datos reales o terceros. Documentos es-ES actualizados; ninguna decisión crítica requerida.

Cierre confirmado: 72 comprobaciones completas superadas y 55 documentos validados en es-ES; diff sin errores. Cambios locales conservados, sin publicación. Próximo punto de reanudación registrado; no se requiere intervención del usuario.

## Continuación automática: catálogo aplicado e intento pendiente — 28 de octubre

Sin interacción humana nueva. Git y fetch comprobados, cambios locales preservados y cierre anterior de 72 comprobaciones/55 documentos revisado. Dos pruebas nuevas instrumentan salida inmediata tras aplicar catálogo/recepción y antes de marcar complete en el intento. Otra conexión observa objeto verificado, secuencias uno/uno y recepción complete con intento checking; proceso nuevo revalida y repite sin duplicar. Revocación antes de reintentar bloquea sin borrar la copia pública local; solo nueva autorización válida permite completar.

Doce pruebas focalizadas de acceso superadas con ResourceWarning como error. Total previsto 74, pendiente confirmación completa. No se prueban escrituras activas ni se elimina la ventana comprobación/commit. Próxima unidad: diagnóstico local sin red de catálogo, recepción, intento y bloqueo para no inferir un estado agregado falso.

Sin commit/push, main, despliegue, datos del usuario o terceros; documentos es-ES actualizados. No se necesita decisión crítica.

Cierre confirmado: 74 comprobaciones completas superadas, 55 documentos es-ES verificados y diff sin errores. Cambios locales conservados sin commit/push. Siguiente bloque de diagnóstico y límites registrados; no se requiere intervención del usuario.

## Continuación automática: diagnóstico local de estados — 28 de octubre

Sin regreso humano. Git y fetch comprobados, cambios locales preservados y cierre anterior de 74 comprobaciones/55 documentos leído. Añadido keri_diagnostics.py con lectura SQLite mode=ro/query_only de catálogo, recepción, intento y conflicto; no usa red ni gestor de identidad ni crea bases ausentes. Estados desconocidos/ilegibles no se convierten en vacío o éxito. No devuelve cuerpos/URLs/rutas y filtra metadatos ajenos al esquema.

Tres pruebas nuevas de límites y aserciones integradas sobre estados reales de composición: catálogo aplicado con intento checking y con revocación posterior. Verificados bytes/mtime de bases sin cambios en escenario sintético. Tres pruebas diagnósticas y doce de acceso focalizadas pasan con ResourceWarning como error. Total previsto 77, pendiente batería completa.

No es validación criptográfica, permiso, actualidad global o snapshot atómico. No se ha cambiado interfaz del simulador ni captado actividad. Siguiente unidad: balance de integración y brechas E/T antes de más variantes. Sin commit/push, main, despliegue, datos reales o terceros; sin decisión crítica requerida.

Cierre confirmado: 77 comprobaciones completas superadas y 55 documentos es-ES verificados; diff sin errores. Cambios locales conservados sin commit/push. Continuar por balance de integración y prioridades E/T, no por repetir variantes ya cubiertas. Sin intervención humana necesaria.

## Continuación automática: balance consolidado y prioridad de integración — 28 de octubre

No hay regreso humano. Git y fetch correctos; cambios locales conservados. Leído cierre de 77 comprobaciones y 55 documentos. Reescrito BALANCE-01-IDENTIDAD-Y-TRASLADO.md como estado actual coherente, sustituyendo tablas iniciales obsoletas y veinticinco actualizaciones acumuladas. La historia detallada permanece en este resumen y en el informe del inventario.

Cobertura E/T actualizada sin declarar casos completos: perfiles/objetos públicos, referencias, retiradas, autorización y persistencia aportan evidencia parcial. Próxima prioridad concreta: una sola ejecución multiobjeto con autorización, A apagado, inventario actualizado después del corte, referencia independiente, retiro, reapertura y regreso de A. No se presentará suma de suites como esa prueba integrada. Se mantienen H01, actualidad desconocida, confianza, privacidad/MLS y límites de operación como brechas.

Unidad documental: no se repiten sin cambios las 77 pruebas previas ni se incrementa la cifra. Sin commit/push, main, instalación, despliegue, datos reales o terceros. No hace falta decisión crítica para preparar el siguiente flujo acotado.

Cierre documental confirmado: 55 documentos es-ES y enlaces/licencias validados, diff correcto e inventario estático de 77 pruebas coherente con la última ejecución completa. Sin nuevas pruebas ni publicación. Próximo bloque definido con condición de paso observable; no se necesita intervención humana.

## Continuación automática: F01 público integrado — 28 de octubre

Sin regreso humano. Git/fetch correctos, cambios locales conservados y balance consolidado revisado. Añadido keri_public_flow.py con una prueba que reúne perfil genérico, dos publicaciones, referencia previa, resolución autorizada, A apagado, B y verificador en procesos nuevos. El titular firma el inventario posterior después de comprobar que A está apagado; se edita una publicación y se retira otra. La referencia conserva ID/revisión y resuelve el texto original; repetición no duplica. A vuelve con copia vieja y nuevo puerto firmado, pero sigue bloqueado por rol revocado.

F01 focalizada pasa con ResourceWarning como error; total previsto 78, pendiente confirmación completa. Se cumple la condición del flujo público mínimo, sin elevarlo a E/T completo. El coordinador distribuye declaraciones; no hay descubrimiento independiente, actualidad global, TLS, privacidad o consenso. Las variantes de fallo de otras suites no se atribuyen a F01.

Actualizado balance actual y documentación. Siguiente prioridad: transporte de declaraciones nativas sin inyección directa al parser, manteniendo límites de confianza. Sin commit/push, main, servicios públicos, datos reales o terceros; no se necesita decisión crítica.

## Cierre recuperado de F01 y transporte OOBI — 28 de octubre

Los latidos posteriores no son regreso humano. Git y fetch correctos, cambios locales preservados. La salida de herramienta anterior confirma 78 pruebas completas y 55 documentos validados de F01; se registra aquí porque su cierre quedó pendiente de anotar entre latidos. No se repite aquel bloque.

Añadido keri_oobi_transport.py con dos pruebas del endpoint nativo OOBIEnd en HTTP local. Para usar el Habery real, el fixture store admite devolver el entorno opcionalmente sin alterar su interfaz por defecto. Se corrigió la suposición inicial de que Hab expusiera hby; las dos pruebas focalizadas pasan con ResourceWarning como error. Historia/rol/ubicación llegan por red con proveedor previamente conocido. Tras cortar un rol, otra introducción no actualiza la revocación del observador en esta configuración; el corte nativo entregado al parser sí lo hace.

No se adopta OOBI de introducción como sincronización de cortes ni ausencia de lista como revocación. El entorno controlador conserva medios de clave; no se mueve a A/B. Total previsto 80, pendiente confirmación completa. Próxima unidad: investigar transporte nativo de respuestas firmadas con cortes y dependencia de disponibilidad. Sin commits, push, main, despliegues, datos del usuario o terceros; sin decisión crítica necesaria.

Cierre confirmado: 80 comprobaciones completas superadas, 55 documentos es-ES verificados y diff sin errores. Cambios locales conservados sin publicación. El límite de introducción/revocación queda documentado; continuar por transporte nativo de cortes, sin pedir decisión crítica ni repetir F01.

## Continuación automática: ingreso HTTP nativo de cortes — 28 de octubre

No hay regreso humano. Git/fetch correctos y cierre previo de 80 comprobaciones/55 documentos revisado. Inspeccionados HttpEnd, rutas de query y endpoints de ubicación de la revisión fijada. Añadido keri_rpy_ingress.py con tres pruebas: concesión/corte/repetición por HTTP nativo, firma ajena no válida aunque se acuse entrada y pérdida instrumentada de cola RAM tras 204 antes de parsear. Reenvío del corte permite validarlo y revocar.

Corregida una configuración inicial del planificador que no conservaba sus generadores de servicio; las tres pruebas focalizadas pasan con ResourceWarning como error. Total previsto 83, pendiente confirmación completa. 204 no significa validación ni persistencia y la pérdida es por vaciado explícito de cola, no caída real. Consumidor activado explícitamente e identidades previamente conocidas; sin concurrencia del estado, TLS, descubrimiento o acuse firmado probados.

Próximo bloque: investigar buzones/entrega duradera existentes para respuestas ya firmadas con titular desconectado, sin nuevo consenso. Sin commit/push, main, despliegue, datos reales o terceros; documentos es-ES actualizados y sin decisión crítica requerida.

Cierre confirmado: 83 comprobaciones completas superadas, 55 documentos es-ES verificados y diff sin errores. hio emite un aviso de deprecación de datetime.utcnow con Python 3.14; no es fallo de prueba y no se ha modificado ni silenciado código ajeno. Compatibilidad futura pendiente. Cambios locales sin publicación; continuar por buzón/entrega duradera de respuestas firmadas. No se requiere intervención humana.

## Regreso humano y continuación solicitada — 29 de octubre

El mensaje humano «Sigue» marca el regreso posterior a la autorización autónoma. Eliminada la automatización continuar-spartakos-hasta-el-lunes antes de emprender el bloque nuevo. La petición actual autoriza continuar este trabajo; ya no queda el seguimiento horario hasta regreso. Git comprobado con cambios locales conservados y fetch correcto; no se publica sin nueva orden específica.

Añadido keri_mailbox.py con dos pruebas de Mailboxer nativo. Emisor en un proceso crea respuestas firmadas y termina; procesos posteriores reabren buzón y observador, validan concesión/corte, repetición y estado persistido. Segundo escenario prueba que corte de firmante ajeno almacenado no revoca y el correcto posterior sí. No se serializan claves privadas; el fichero auxiliar solo contiene dos identificadores públicos.

Dos pruebas focalizadas superadas con ResourceWarning como error. Total previsto 85, pendiente confirmación completa. Lectura local con índices ordinales elegidos por coordinador, sin cursor de consumo durable, transporte HTTP, acceso de buzón o caída durante escritura probados. Próxima unidad: transporte de lectura y consumo persistido ante interrupción. Sin commit/push, main, despliegue, datos reales ni terceros; el simulador sigue intacto.

Cierre confirmado tras el regreso: 85 comprobaciones completas superadas y 55 documentos es-ES verificados; diff sin errores. Persiste el aviso de deprecación conocido de hio, sin parche ajeno. La automatización está eliminada y la continuación actual queda local pendiente de commit/push, junto con las ampliaciones autónomas previas.

## Nueva continuación programada: buzón HTTP y cursor — 29 de octubre

La nueva petición humana de programación posterior al regreso es la referencia vigente; no se considera que aquel regreso anterior termine esta nueva automatización. No hay otra interacción humana desde la nueva petición. Git y fetch comprobados con cambios locales preservados y cierre anterior de 85 comprobaciones/55 documentos revisado.

Añadido keri_mailbox_http.py: dos pruebas de adaptación HTTP finita del MailboxIterable nativo, con emisor terminado y cursor SQLite del receptor. Procesos nuevos conservan cursor dos al salir antes de validar el corte o después de validarlo antes de guardar cursor; reintentar no lo salta y acaba en cuatro con rol revocado. Consulta posterior sin eventos no altera cursor. Dos pruebas focalizadas superadas con ResourceWarning como error; total previsto 87, pendiente confirmación completa.

No es MailboxDirector/consulta firmada o SSE continuo completo; faltan acceso de buzón, política de mensajes rechazados, huecos, cursor perdido y fallo dentro de escritura. La repetición es deliberada, sin exactamente una vez ni actualidad global. Próximo bloque: lectura obsoleta, mensajes rechazados y huecos sin salto de revocaciones. Sin commit/push, main, despliegue, datos reales o terceros; sin decisión crítica necesaria.

Cierre confirmado de la nueva programación: 87 comprobaciones completas superadas, 55 documentos es-ES verificados y diff sin errores. Sigue el aviso conocido de hio sin parche ajeno. Cambios locales conservados sin publicación; siguiente bloque y límites registrados, sin intervención humana necesaria.

## Buzón: límites comprobados ante rechazo y huecos — 29 de octubre

Git conserva los cambios locales en prototipo-segunda-revision; fetch de origin completado y HEAD sin desfase respecto al remoto verificado. No hay nueva interacción humana desde la última programación; no se considera regreso el contexto del entorno.

Dos casos nuevos del lector HTTP reproducen un corte con firma ajena y un hueco ordinal anterior a un corte válido. Dos consumidores sucesivos rechazan cada situación, conservan cursor dos y la concesión anterior en su vista local. Se documenta el bloqueo de progreso como brecha operativa; no se inventa descarte automático ni una política de confianza. Cuatro pruebas focalizadas superadas con ResourceWarning como error. Última batería completa confirmada: 87; total previsto tras añadir estos casos: 89. Documentación y metadatos actualizados; lectura obsoleta, recuperación y flujo nativo completo siguen pendientes. KERI experimental, H01 abierto, actualidad global sin probar y ningún E/T completo. Sin commit/push ni cambios en datos del simulador.

## Buzón obsoleto y alcance del cursor — 29 de octubre

Fetch de origin completado; rama prototipo-segunda-revision sin desfase en los commits, con cambios locales pendientes conservados. No se detecta regreso humano posterior a la nueva programación.

Quinta prueba focalizada del lector HTTP: dos buzones con los mismos mensajes iniciales; el obsoleto omite el corte y responde vacío después de la concesión. El consumidor conserva cursor dos y permiso anterior. Una URL alternativa elegida explícitamente permite recibir el corte y avanzar a cuatro; volver al buzón antiguo no restablece el permiso. No acredita detección de obsolescencia, descubrimiento o índices universales entre proveedores. La copia parcial se prepara por API nativa y solo contiene material público sintético.

Cinco pruebas focalizadas superadas con ResourceWarning como error. Última batería completa confirmada: 87; total previsto actual: 90. Se corrige la presentación del balance para distinguir ambas cifras y una referencia numérica antigua en garantías. Sigue pendiente integrar el transporte nativo y estudiar el contrato de cursor antes de inventar recuperación o descarte. KERI candidata experimental, H01 abierto, sin actualidad global probada ni E/T completo. Sin commit/push ni datos del usuario modificados.

## Contrato del iterador y cursor nativos — 29 de octubre

Git revisado con cambios conservados; fetch completado y sin desfase de commits respecto a origin. No hay nuevo regreso humano. Revisados balance e informe para evitar repetir escenarios anteriores.

Antes de integrar MailboxDirector, se inspecciona Poller.eventDo de la revisión fijada: encola y posteriormente persiste cursor de recepción, sin comprobar ahí resultado de validación/aplicación. Se documenta como revisión estática, sin afirmar una pérdida reproducida del flujo completo. Una sexta prueba focalizada ejecuta MailboxIterable con hueco preparado: al pedir desde dos y existir tres, devuelve tres dos veces antes de quedar vacío. No se modifican terceros ni se presenta como vulnerabilidad. El consumidor estricto mantiene su rechazo previo del hueco.

Seis casos focalizados superados con ResourceWarning como error; última batería completa confirmada 87 y total previsto actual 91. Siguiente unidad: comprobar el punto de persistencia del Poller con cola pendiente e interrupción. Propuesta de recepción durable separada de validación, todavía sin política adoptada para descarte, recuperación o confianza. Sin commit/push, despliegue, terceros ni datos reales. KERI experimental, H01 abierto y ningún E/T completo.

## F06: cursor nativo y cola pendiente entre procesos — 29 de octubre

Fetch de origin completado tras reintentar una revisión automática que agotó su plazo; commits sin desfase y cambios locales conservados en prototipo-segunda-revision. No se ha producido regreso humano desde la última programación.

Añadido keri_poller_checkpoint.py: generador eventDo real, base persistente real y transporte sustituido por dobles, sin servidor SSE ni MailboxDirector completo. Dos subescenarios terminan un proceso después de encolar: antes de persistir no queda cursor; después de persistir sí queda índice cero, aunque no se haya ejecutado validación y la cola del Poller nuevo esté vacía. Se confirma esta frontera aislada, sin afirmar fallo inevitable del planificador completo. No se modifican terceros ni se adopta descarte, salto o confianza nuevos.

La prueba focalizada supera ambos subescenarios con ResourceWarning como error. Consolidación completa: **92 comprobaciones superadas en 61,476 segundos**, 55 documentos es-ES y diff sin errores. Sigue el aviso conocido de deprecación de hio. Los 109 casos del simulador social siguen separados. Siguiente unidad: comprobar una adaptación de recepción durable y repetición verificable conectada al generador nativo, manteniendo separados recepción, validación y aplicación; no sustituir el cursor nativo por una supuesta aprobación. KERI experimental, H01 abierto, actualidad global no probada y ningún E/T completo. Sin commit/push, main, despliegue, contacto o datos reales.

## F07: recepción durable antes de progreso nativo — 29 de octubre

Estado Git revisado y fetch de origin completado; sin desfase de commits y con cambios locales preservados. No hay interacción humana posterior a la última programación. Revisados balance, informe y cierre anterior de 92 pruebas para evitar repetir bloques.

Añadido keri_durable_inbox.py: propuesta local de append SQLite durable conectada al generador Poller real, con transporte sustituido por dobles y fuente/tema únicos sintéticos. El proceso termina con cursor tres y cuatro mensajes pendientes, sin validar identidad emisora. Otros procesos validan y terminan tras aplicar corte, antes de marcarlo; reabrir repite los pendientes y conserva revocación. No se serializan claves privadas, no hay exactamente una vez ni flujo completo de MailboxDirector. Falta sobre general de recepción y prueba de fallo de persistencia; no se adoptan reglas de descarte o confianza.

Flujo focalizado superado con ResourceWarning como error; última batería completa confirmada 92 y total previsto 93. Se conservan separadas las 109 pruebas del simulador social. Siguiente unidad: fallo de persistencia antes del cursor nativo y alcance del sobre de recepción. KERI experimental, H01 abierto, actualidad global no probada y ningún E/T completo. Sin commit/push ni modificación de datos del usuario.

## F07: fallo de persistencia antes del corte — 29 de octubre

Git revisado, fetch de origin completado y sin desfase de commits; cambios locales pendientes conservados. Sin regreso humano posterior a la última programación. Revisados balance e informe para continuar el bloque pendiente.

Segunda prueba de entrada durable: trigger sintético SQLite aborta el tercer INSERT. El proceso falla y reabrir confirma dos mensajes pendientes y cursor nativo uno, sin identidad emisora validada. Retirar el trigger y reintentar explícitamente recibe desde dos, completa cuatro entradas y permite validar el corte conservando revocación. Es fallo lógico real de transacción, sin afirmar disco lleno, corrupción o recuperación automática. Transporte sigue sustituido por dobles.

Dos pruebas focalizadas superadas con ResourceWarning como error; última batería completa confirmada 92 y total previsto 94. Se acota como propuesta el sobre de fuente/destinatario/tema/ordinal y bytes, con conflictos conservados y sin autoridad inferida de la ruta. No se implementa todavía porque append nativo no entrega esos metadatos. Siguiente unidad: integrar recepción y metadatos con un transporte real acotado, sin políticas automáticas de descarte o consenso. KERI experimental, H01 abierto, actualidad global no probada y ningún E/T completo. Sin commit/push, datos reales o cambios del simulador.

## F08: recepción HTTP real y validación posterior sin servidor — 29 de octubre

Git revisado y fetch de origin completado; sin desfase de commits, con cambios locales pendientes conservados. Sin regreso humano desde la última programación. Revisados balance y ensayo para integrar el bloque pendiente en lugar de repetir variantes aisladas.

Añadido keri_http_inbox.py: servidor HTTP local finito reutilizado, emisor terminado, sobre SQLite y cursor de recepción confirmados juntos. Cuatro entradas conservan fuente URL, destinatario, tema, ordinal, bytes y huella sin validarse. Nueva consulta no duplica entradas. Servidor detenido antes de validar; procesos nuevos validan y terminan tras corte, antes del marcador, y luego repiten pendientes conservando revocación. La fuente es procedencia observada, no autoridad; solo se admite una combinación al validar, sin inventar orden entre fuentes. No es MailboxDirector, consulta firmada o SSE continuo completo.

Flujo focalizado superado con ResourceWarning como error; última batería completa confirmada 92 y total previsto 95. Se conservan las 109 pruebas del simulador como batería separada. Siguiente unidad: alteración de bytes/metadatos y posición repetida con contenido distinto, preservando evidencia sin arbitraje automático. Documentación es-ES y límites actualizados; KERI experimental, H01 abierto, actualidad global sin probar y ningún E/T completo. Sin commit/push, despliegue, terceros o datos reales.

## F08: rechazo de alteraciones y evidencia de posición contradictoria — 29 de octubre

Git revisado, fetch de origin completado y commits sin desfase; cambios locales pendientes conservados. No se ha producido nueva interacción humana desde la programación vigente. Revisados balance, informe y cierre anterior antes del bloque.

Dos pruebas adicionales del módulo HTTP durable: bytes o tema local alterados mantienen entradas pendientes y no validan la identidad emisora. Una respuesta inyectada con índice ya recibido y bytes distintos conserva original y evidencia separada sin avanzar cursor. Un proceso nuevo bloquea validación ante ese conflicto conocido. Primera recepción por HTTP real; respuesta contradictoria inyectada en el límite de transporte, sin afirmar servidor malicioso completo. No se resuelve el conflicto ni se infiere autoridad de la ruta; la huella local no protege modificaciones coherentes del almacén.

Tres pruebas focalizadas superadas con ResourceWarning como error. Consolidación completa: **97 comprobaciones superadas en 65,506 segundos**; persiste aviso conocido de hio sin parche ajeno. Se conservan separadas las 109 pruebas del simulador social. Siguiente bloque: conectar validación durable y autorización de entrega, distinguiendo recepción pendiente o bloqueada de permiso actualizado. KERI experimental, H01 abierto, actualidad global no probada y ningún E/T completo. Sin commit/push, despliegue, contacto o datos reales.

## F08: buzón validado y puerta de autorización conectados — 29 de octubre

Git revisado y fetch de origin completado; sin desfase de commits y cambios locales conservados. No hay regreso humano desde la programación vigente. Revisados balance e informe y conectado el resultado durable con la autorización existente.

Cuarta prueba HTTP durable: validar creación/concesión en access/resolver; recibir corte todavía pendiente conserva el permiso anterior en la vista nativa, pero la precaución experimental del buzón impide iniciar restauración. Un proceso nuevo valida corte en ese mismo resolver y la puerta existente rechaza al proveedor por revocación. Se observa que no se llama a restauración, sin atribuir descarga autorizada completa o actualidad global. El bloqueo por pendientes sigue limitado a la fuente sintética; no es política general de producto ni transacción conjunta. Corregida la inicialización del directorio aislado tras el primer ensayo fallido.

Cuatro pruebas focalizadas del buzón superadas con ResourceWarning como error y 12 pruebas de autorización existentes superadas. Última batería completa confirmada 97; total previsto 98. Próximo bloque: integrar también la ruta de éxito con dirección y contenido público autorizados mediante el buzón, para completar un flujo de concesión, entrega y revocación, sin modificar decisiones de confianza. 109 pruebas sociales separadas; KERI experimental, H01 abierto y ningún E/T completo. Sin commit/push, despliegue, contacto o datos reales.

## F09: flujo integrado de concesión, entrega pública y revocación — 29 de octubre

Git revisado y fetch de origin completado, commits sin desfase y cambios locales pendientes conservados. Sin regreso humano posterior a la programación vigente. Revisados balance e informe antes de completar la ruta de éxito pendiente.

Quinta prueba del módulo HTTP durable: titular y proveedor sintéticos preparan dos creaciones, dirección HTTP, concesión, corte y duplicado en buzón nativo; sus almacenes efímeros se cierran antes del consumo. Receptor HTTP durable y procesos nuevos validan los cuatro mensajes iniciales en resolver y restauran realmente inventario/publicación públicos. Recibir corte pendiente bloquea otro intento; validarlo hace que la puerta existente rechace al proveedor. Filas y bytes del catálogo anterior permanecen intactos. Sin dobles en la restauración de esta ruta; transporte sigue finito, un tema y un proveedor. Corregido el nombre de un argumento de la API nativa en la preparación sintética.

Cinco pruebas focalizadas superadas con ResourceWarning como error. Última batería completa confirmada 97 y total previsto 99; helpers compartidos y dependencias sin modificar, sin repetir batería completa. Las 109 pruebas sociales siguen separadas. Siguiente unidad: diagnóstico consolidado del flujo que distinga recepción, validación y último intento sin cuerpos o falsa actualidad. KERI experimental, H01 abierto, actualidad global no probada y ningún E/T completo. Sin commit/push, despliegue, contacto o datos reales.

## F09: diagnóstico consolidado del flujo — 29 de octubre

Git revisado, fetch de origin completado y commits sin desfase; cambios locales preservados sin publicación. Sin nueva interacción humana posterior a la programación vigente. Revisados balance e informe para consolidar el flujo ya ejecutado.

Diagnóstico de solo lectura ampliado con recuentos de recibidos, pendientes, marcados validados y estados desconocidos; progreso por única secuencia y conflictos. No expone cuerpos, rutas, fuentes o temas ni abre claves. F09 comprueba tres momentos reales: concesión/restauración, corte recibido pendiente con intento anterior aún completo, y corte validado con intento bloqueado y copia anterior en catálogo. Las lecturas no modifican bytes o fechas de las bases. Nuevo caso verifica contenido inesperado oculto, marcas desconocidas separadas y base ilegible no confundida con vacía; ausencia sigue sin crear bases. No es foto atómica ni revalidación criptográfica.

Cuatro pruebas de diagnóstico y cinco del buzón superadas con ResourceWarning como error. Consolidación completa: **100 comprobaciones superadas en 69,172 segundos**, con aviso conocido de hio sin parche ajeno. 55 documentos es-ES y diff verificados; 109 pruebas sociales separadas. Siguiente unidad: revisar contratos y fronteras de concurrencia del flujo, especialmente recepción de corte durante restauración, antes de ampliar funcionalidad. KERI experimental, H01 abierto, actualidad global no probada y ningún E/T completo. Sin commit/push, despliegue, contacto o datos reales.

## F09: corte pendiente recibido durante descarga — 29 de octubre

Git revisado y fetch de origin completado; commits sin desfase y cambios locales conservados. No hay nueva interacción humana posterior a la programación vigente. Revisados balance e informe antes de revisar el contrato de concurrencia.

Se identifica que comprobar pendientes solo al iniciar no cubre su llegada durante la descarga. restore_authorized admite comprobación adicional opcional antes de aplicar; el flujo del buzón vuelve a revisar pendientes/conflictos. Nueva prueba descarga el objeto por HTTP real y coordina recibir corte por buzón al terminar esa lectura: rol nativo aún permitido, pero dos pendientes bloquean aplicar, dejan cero objetos y registro inbox_pending. Validar en otro proceso lleva al rechazo posterior por proveedor no autorizado. Diagnóstico actualizado para el código. No es estrés con escritores simultáneos y sigue existiendo ventana entre última comprobación y commit; no se declara atomicidad o cierre general de carreras.

Seis pruebas de buzón, doce de autorización y cuatro de diagnóstico superadas con ResourceWarning como error: 22 pertinentes. Última batería completa confirmada 100; total previsto 101. Próxima unidad: consolidar contratos y fronteras en una presentación compacta del flujo y revisar el bloqueo local, antes de acumular variantes. 109 pruebas sociales separadas; KERI experimental, H01 abierto, actualidad global no probada y ningún E/T completo. Sin commit/push, despliegue, contacto o datos reales.

## Consolidación de contratos y límites — 30 de octubre

Git revisado, fetch de origin completado y commits sin desfase; cambios locales conservados. El cambio de fecha y el contexto del entorno no son regreso humano: la programación continúa vigente. No se inicia otro bloque de código en esta unidad documental.

Reorganizado el balance para sustituir el apéndice cronológico por contratos actuales: recibir, confirmar recepción, validar, repetir, comprobar entrega, aplicar y diagnosticar. Tabla F02–F09 con límites, alcance del bloqueo de un buzón y orden pendiente. Se corrigen prioridades antiguas que ya se habían ejecutado y cifras históricas que podían confundirse con el total. La secuencia técnica detallada permanece en el informe y en este resumen; el laboratorio identifica al inicio el estado vigente y distingue cifras de cierres anteriores.

No se cambian reglas de confianza, interfaces de producto o pruebas. Última batería completa 100; 22 comprobaciones pertinentes posteriores superadas y conjunto previsto 101. Validación documental es-ES y diff aplicables, sin repetir pruebas de código para una consolidación textual. Siguiente bloque: revisar estados desconocidos e integridad del sobre en el flujo de una fuente; integración MailboxDirector y plan privado siguen pendientes. KERI experimental, H01 abierto, actualidad global no probada y ningún E/T completo. Sin commit/push, despliegue, terceros o datos reales.

## F09: marcas desconocidas no promueven permiso — 30 de octubre

Git revisado y fetch de origin completado; sin desfase de commits y cambios locales preservados. No hay regreso humano desde la programación vigente. Revisados contratos consolidados y último resultado antes del bloque.

Se corrige la omisión de marcas distintas de cero/uno: antes contar solo cero podía ocultarlas. La validación las rechaza sin omitir o reparar; la puerta exige marca uno en todas las entradas. Nueva prueba integrada restaura publicación, recibe corte y altera sus dos marcas a valor desconocido. Procesos nuevos bloquean restauración y rechazan validar; permanecen concesión anterior, marcas originales alteradas y copia pública intacta. El diagnóstico informa dos estados desconocidos y cero pendientes con marca cero: no equivale a validación completa. No se afirma integridad autenticada del dispositivo ni de metadatos de ruta.

Siete pruebas del buzón y cuatro de diagnóstico superadas con ResourceWarning como error: once pertinentes. Última batería completa 100; total previsto 102. Siguiente bloque: delimitar transporte nativo pendiente y conservación de metadatos, evitando más variantes sintéticas aisladas. 55 documentos es-ES y diff aplicables; 109 pruebas sociales separadas. KERI experimental, H01 abierto, actualidad global no probada y ningún E/T completo. Sin commit/push, despliegue, contacto o datos reales.

## F10: contrato de consulta nativa y conservación de metadatos — 30 de octubre

Git revisado, fetch de origin completado y commits sin desfase; cambios locales preservados. No hay regreso humano desde la programación vigente. Revisados balance e informe y fuentes locales fijadas, sin actualizar dependencias.

Se documenta como propuesta no ejecutada la cadena Poller → consulta mbx → HttpEnd → cue/iterador SSE y MailboxDirector → parser. El límite que conserva id/tema/datos está antes de que Poller entregue solo bytes; el sobre durable debe capturarse ahí antes de aceptar progreso. Se distingue consulta firmada de autorización de lectura, sin concluir vulnerabilidad a partir de una función aislada. F10 concreta precondiciones, secuencia y criterio de paso, sin inventar directorio, consenso o política de acceso.

Primer bloque ejecutable pendiente: petición/cue/SSE nativos por HTTP real con mensajes públicos sintéticos. Después se estudiará el adaptador durable en el límite de eventos y recuperación entre procesos; MailboxDirector completo no se dará por supuesto. Preparación documental, sin pruebas nuevas ni repetir baterías: última completa 100, conjunto previsto 102 y once comprobaciones focalizadas anteriores superadas. 55 documentos es-ES y diff aplicables; 109 pruebas sociales separadas. KERI experimental, H01 abierto, actualidad global no probada y ningún E/T completo. Sin commit/push, despliegue, contacto o datos reales.

## F10: consulta nativa y SSE por HTTP ejecutados — 30 de octubre

Git revisado; fetch de origin completado tras reintentar una revisión automática que agotó su plazo. Commits sin desfase y cambios locales conservados. Sin regreso humano desde la programación vigente; revisados balance e informe antes del primer paso F10.

Añadido keri_native_query.py: consulta mbx firmada de destinatario conocido, POST a HttpEnd real, adaptador del ensayo ejecuta parser nativo y enlaza cue a QryRpyMailboxIterable. SSE nativo real con servidor hio/Falcon; cliente urllib y lector ASCII acotado. Se comprueban SAID/destinatario/tema del cue, bytes e índices cero/uno y segunda consulta desde uno. Corregida conversión bytearray/bytes del lector tras primera ejecución. No se modifican terceros.

Una prueba focalizada superada con ResourceWarning como error. No es Poller/MailboxDirector, no hay entrada durable o recuperación entre procesos ni acceso privado demostrado; el criterio completo F10 sigue pendiente. Última batería completa 100; total previsto 103. Siguiente bloque: unir ruta nativa real, metadatos durables y recuperación sin confundirlos con autorización. 55 documentos es-ES y diff aplicables; 109 pruebas sociales separadas. KERI experimental, H01 abierto, actualidad global no probada y ningún E/T completo. Sin commit/push, despliegue, contacto o datos reales.

## F10: ruta nativa con sobre durable y recuperación — 30 de octubre

Git revisado, fetch de origin completado y commits sin desfase; cambios locales conservados. Sin regreso humano desde la programación vigente. Revisados balance e informe antes de unir la ruta nativa y el sobre.

Segunda prueba de keri_native_query.py: consulta mbx prefirmada por destinatario conocido, HttpEnd/parser/cue y SSE reales; lector de otro proceso confirma fuente/destinatario/tema/ordinal/bytes/huella con progreso de recepción. Termina tras cuatro pendientes sin validar. Servidor/controlador se cierran; otros procesos validan y terminan tras aplicar corte antes del marcador, repiten dos pendientes y conservan revocación. Progreso local, no cursor de Poller; destinatario esperado se pasa explícitamente al validador, manteniendo su caso anterior por defecto. Sin exportar claves privadas.

Dos pruebas nativas y siete del buzón superadas con ResourceWarning como error. Consolidación completa: **104 comprobaciones superadas en 82,110 segundos**, con aviso conocido de hio y sin parche a terceros. 55 documentos es-ES y diff verificados; 109 pruebas sociales separadas. F10 sigue parcial: faltan fallo de persistencia en esta ruta y consulta ajena; acceso privado, Poller/MailboxDirector completos y actualidad global no probados. Siguiente bloque: comprobar esas dos fronteras del contrato existente, sin inventar autorización de lectura. KERI experimental, H01 abierto y ningún E/T completo. Sin commit/push, despliegue, contacto o datos reales.

## F10: consulta ajena y límite de lectura privada — 30 de octubre

Git revisado, fetch de origin completado y commits sin desfase; cambios locales conservados. Sin regreso humano desde la programación vigente. Revisados balance e informe antes de ejecutar la frontera de consulta ajena.

Tercera prueba nativa: otro firmante conocido consulta el buzón del destinatario sin concesión de lectura emitida y obtiene los mensajes públicos sintéticos por HttpEnd/parser/cue/SSE reales, incluida consulta desde índice uno. Se conserva la configuración nativa, sin inventar control de acceso en el adaptador. La ruta no acredita aislamiento de lectura y queda limitada a material público sintético; no se afirma vulnerabilidad general de KERIpy o exposición de datos reales. Una consulta firmada no demuestra permiso privado.

Tres pruebas focalizadas superadas con ResourceWarning como error; última batería completa 104 y total previsto 105. Se documenta la brecha sin adoptar política de lectura, consenso o autoridad nueva. No bloquea continuar el ensayo público; antes de incorporar contenido privado será necesaria esa definición y su ensayo. Próxima unidad: rechazo de persistencia de la recepción nativa durable. KERI experimental, H01 abierto, actualidad global sin probar y ningún E/T completo. 55 documentos es-ES y diff aplicables; sin commit/push, despliegue, contacto o datos reales.

## F10: fallo de persistencia durante SSE nativo y reanudación — 30 de octubre

Git revisado y fetch de origin completado; commits sin desfase y cambios locales conservados. No hay regreso humano desde la programación vigente. Revisados balance e informe antes de comprobar la frontera pendiente.

Cuarta prueba nativa: trigger SQLite aborta el tercer INSERT en receptor de SSE real. Proceso termina con error y conserva dos entradas/progreso dos. Retirar el trigger y volver a firmar explícitamente consulta desde dos permite a otro proceso recibir el corte y completar cuatro entradas/progreso cuatro. Servidor cerrado antes de validar; se repite corte tras terminación entre validación y marcador y se conserva revocación. No es fallo físico, cliente Poller o recuperación automática; los pasos de reparación y consulta son explícitos.

Cuatro pruebas focalizadas superadas con ResourceWarning como error. Última batería completa 104; total previsto 106. La ruta pública queda comprobada en ese alcance, sin declarar F10 completo: consulta ajena sigue sin aislamiento, no se incorpora contenido privado y faltan Poller/MailboxDirector y controles de producción. Siguiente bloque: revisar acoplamiento del cliente nativo con sobre durable antes de su cursor, sin nueva política de lectura. 55 documentos es-ES y diff aplicables; 109 pruebas sociales separadas. KERI experimental, H01 abierto, actualidad global no probada y ningún E/T completo. Sin commit/push, despliegue, contacto o datos reales.

## F10: Poller y cliente HTTP reales con sobre durable — 30 de octubre

Git revisado, fetch de origin completado y commits sin desfase; cambios locales conservados. Sin regreso humano posterior a la programación vigente. Revisados balance e informe y el acoplamiento del cliente nativo antes de ejecutar.

Quinta prueba nativa: Poller y planificador/cliente HTTP reales frente a HttpEnd/parser/cue/SSE reales. Dirección del controlador validada por destinatario preconfigurado. Fábrica envuelta por instrumentación que sigue creando cliente/doer reales y sustituye solo contenedor de eventos compartido con parser. Al retirar cada evento confirma sobre/progreso SQLite antes de devolverlo a Poller. Se comprueban dos entradas sin validar, bytes en cola y último ordinal nativo uno frente a siguiente local dos. Sin datos de aplicación privados, política de testigos nueva o dependencia parcheada. No se atribuye a este caso recuperación tras proceso terminado ni MailboxDirector completo.

Cinco pruebas focalizadas superadas con ResourceWarning como error. Consolidación completa: **107 comprobaciones superadas en 76,436 segundos**, con aviso conocido de hio sin parche ajeno. 55 documentos es-ES y diff verificados; 109 pruebas sociales separadas. Próximo bloque: interrumpir este cliente nativo concreto y comprobar su recuperación con el sobre, sin extender permisos privados. Consulta ajena sigue sin aislamiento acreditado; KERI experimental, H01 abierto, actualidad global no probada y ningún E/T completo. Sin commit/push, despliegue, contacto o datos reales.

## Regreso humano y preparación de publicación — 30 de octubre

La petición humana «commit y push» termina la continuación autónoma vigente. Automatización continuar-spartakos-hasta-tu-regreso eliminada; no se inicia otro bloque autónomo. Usuario autoriza consolidar y publicar los cambios acumulados en prototipo-segunda-revision y la propuesta #2, sin integrar main.

Fetch completado sin divergencias antes de preparar publicación. Revisados 19 archivos de documentación, inventario y código de laboratorio: sin secretos detectados, datos de usuario, bases, claves privadas, dependencias instaladas o artefactos regenerables que incorporar. AST Python y JSON válidos, licencias comprobadas; 55 documentos es-ES y diff sin errores. Batería completa repetida antes de publicar: **107 pruebas superadas en 80,128 segundos**. Persiste el aviso conocido de deprecación de hio sin parche ajeno; no se ha cambiado el simulador social.

El siguiente trabajo pendiente continúa siendo recuperación del Poller real con el sobre; no se toma prestada del caso urllib. La ruta de lectura ensayada sigue restringida a material público sintético, KERI es experimental, H01 continúa abierto y ningún E/T está completo. No hay despliegue público ni contacto con terceros.
