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
