---
title: Spartakos — Inventario público y referencias con origen apagado
lang: es-ES
license: CC-BY-SA-4.0
date: 2026-10-27
version: "0.34"
status: Ensayo local ejecutado; sin traslado completo ni adopción de formato
---

# Inventario público autorizado y restauración comprobable

## 1. Resultado

Nueve pruebas de [keri_inventory.py](laboratorio-identidad/keri_inventory.py) superadas; **87 comprobaciones de laboratorio en total**. Se amplía la copia de perfil a objetos públicos propios, revisiones y retirada explícita. Un observador mantiene una referencia guardada y recupera su objeto desde el catálogo restaurado, sin cambiar el ID o la revisión de esa referencia.

El ensayo no completa los casos T ni E. Demuestra restauración pública acotada desde B con A apagado, no un cambio integral de alojamiento ni disponibilidad frente a perder la máquina. Los servicios solo entregan datos y no reciben claves privadas del titular.

## 2. Preparación y autoridad

El coordinador prepara una identidad sintética y firma dos eventos de interacción KERI con las huellas de dos inventarios. El verificador conoce por separado la identidad esperada y valida con KERIpy los eventos firmados recibidos por HTTP. El inventario se acepta solo si sus bytes coinciden con la huella del último anclaje de inventario aceptado en esa vista.

El esquema `spartakos-public-inventory-lab-v1` y su enlace `spartakos_public_inventory_lab_v1` son semántica experimental de aplicación. No son un formato nativo de KERI, un estándar de portabilidad aprobado ni un mecanismo nuevo de consenso. Los IDs, revisiones, estados y huellas forman parte del inventario autorizado; comprobar solo la huella de un objeto no le concede autoridad.

A y B se ejecutan en procesos HTTP locales de solo lectura con directorios separados. El observador usa una base KERI y un catálogo SQLite propios. Cada recepción se ejecuta en un proceso verificador nuevo. Los endpoints solo sirven inventario, prueba y objetos identificados por huella; no permiten listar directorios. Comparten equipo y administrador.

## 3. Objetos del escenario

El inventario inicial contiene un perfil público mínimo y tres publicaciones públicas sintéticas. El posterior conserva ese perfil, conserva las primeras revisiones de dos publicaciones, incorpora la segunda revisión de una y sustituye la tercera publicación por un marcador de retirada de revisión dos.

La referencia del observador apunta a la primera revisión de la publicación editada. Se guarda antes de restaurar B y se resuelve después por el mismo ID y revisión, recuperando los mismos bytes. No se importa una lista de contactos ni se modifica la referencia para acomodar el destino.

Las versiones del perfil de este inventario usan el formato público genérico del fixture; no se declara interoperabilidad automática con el esquema mínimo de los ensayos anteriores. La serialización, límites y lectura de objetos siguen siendo de laboratorio.

## 4. Casos ejecutados

| Caso | Comprobación y resultado |
| --- | --- |
| I01 — Restauración completa y regreso de A | Se carga el catálogo inicial desde A, se apaga A y se observa fallo de conexión; se restaura B, se resuelve la referencia guardada, se repite la recepción sin duplicados y se rechaza el inventario anterior al volver A |
| I02 — Objeto ausente | Una respuesta 404 deja incompleta la recepción y señala el ID; el catálogo anterior queda intacto; al restaurar el objeto el reintento completa la recepción |
| I03 — Objeto alterado | La huella recibida no coincide con la autorizada; se señala el ID y no se aplica ninguna parte al catálogo; corregir el objeto permite reintentar |
| I04 — Inventario modificado sin nueva autoridad | Se alteran los bytes del inventario sin un nuevo anclaje firmado; se rechaza por el error de autoridad esperado y se conserva el catálogo anterior |
| I05 — Recepción interrumpida antes de aplicar | Se termina el proceso después de guardar la recepción y validar objetos, antes de la transacción del catálogo; una conexión nueva comprueba estado pendiente, secuencia esperada dos y aplicada uno; otro proceso reintenta y termina con ambas secuencias en dos |

Los casos I son nombres de esta suite y no sustituyen los T. Las pruebas negativas de inventario exigen el error de validación concreto, no cualquier fallo del proceso.

## 5. Aplicación y retiradas

Los objetos se descargan y verifican antes de abrir la transacción que actualiza el catálogo. Se comprueba ID, revisión y audiencia pública del cuerpo, además de su huella. Un catálogo previo no puede perder un objeto del inventario por omisión silenciosa: necesita representación explícita en este esquema acotado.

Si falta un objeto o hay uno inválido no se aplica parcialmente el catálogo. El estado KERI puede haber avanzado ya al anclaje posterior: conservar el catálogo anterior **no significa que esté actualizado**. La incompletitud se devuelve y se guarda en un registro de recepción, con secuencia esperada, secuencia aplicada y detalle de objetos ausentes o alterados. No existe todavía una interfaz de recuperación. KERI y SQLite no comparten una transacción y no se han probado cortes entre ambos.

Una retirada autorizada conserva el marcador de revisión dos y elimina los cuerpos anteriores de ese objeto del catálogo recuperado, dejando su constancia de revisión como contenido retirado. Las otras versiones públicas se conservan. Repetir B no duplica filas. A conserva su copia antigua, pero reenviar su inventario no reemplaza el último anclaje ya conocido ni hace reaparecer el cuerpo retirado en el catálogo del observador.

Esto no borra las copias del proveedor anterior, lectores o nodos hostiles, ni demuestra borrado físico seguro de páginas SQLite o archivos del sistema. Tampoco prueba una política general de restauración de todas las versiones de Spartakos.

## 6. Límites antes de ampliar el resultado

- Las direcciones de A/B siguen proporcionadas por el coordinador. La composición de autorización de servicios probada para perfil aún no se integra en este restaurador de inventario.
- No se demuestra actualidad global ni descubrimiento de actualizaciones: se compara con el último anclaje conocido. Una vista aislada puede seguir sin conocer el inventario posterior.
- No se compone todavía este restaurador con el registro duradero de conflictos. La validación de una cadena no demuestra ausencia de otra rama; el caso general de confirmación ante conflicto sigue pendiente.
- No se prueban ejecución única de notificaciones, envíos o programaciones, roles comunitarios, datos privados, contactos, importación externa ni recuperación de claves.
- Se prueban reinicios entre recepciones, no fallos durante la transacción, disco lleno, pérdida del catálogo o cortes durante descarga. Tampoco se mide escala o coste de voluntariado. La terminación de I05 no ocurre dentro de una transacción en curso.
- El historial de autoridad usa una clave y no incorpora testigos, rotaciones o delegación en esta suite. Esas piezas tienen ensayos separados; no se suman como si toda la integración estuviera probada.

El campo `complete` solo se refiere al inventario solicitado y validado en la vista. No certifica traslado completo, seguridad de producción o última versión global. No se conecta este formato al simulador ni se modifican datos del usuario.

## 7. Siguiente unidad

Componer inventario, resolución autorizada y registro de conflicto, aprovechando la recepción incompleta ya persistida para reanudarla explícitamente. La confirmación deberá distinguir autoridad conocida, integridad, cobertura del inventario, estado de conflicto y límite de actualización. Solo después se ampliará el balance de T01–T10 sin trasladar a ellos éxitos de componentes que no cubran su alcance completo.

## 8. Estado persistido de recepción

Antes de descargar los objetos se registra la intención de recepción, después de verificar el anclaje del inventario. Sus estados de laboratorio son receiving, incomplete y complete. Se conserva por separado la secuencia esperada y la aplicada: después de recibir autoridad de la revisión dos, el catálogo puede seguir legítimamente en la revisión uno mientras faltan datos. No se presenta como actualizado.

El cambio a complete y la actualización del catálogo comparten una transacción SQLite. El registro inicial y la historia KERI siguen en transacciones separadas. Un fallo fuera de los casos de ausencia/alteración puede dejar receiving; ese estado no equivale a un proceso todavía activo ni a éxito. El reintento es explícito y vuelve a descargar y validar objetos; no hay reanudación automática por fragmentos ni política de caducidad implementada.

La prueba I05 termina el proceso sin cierres normales en un punto controlado, antes de aplicar el catálogo. Confirma que la recepción esperada y el catálogo anterior sobreviven y que un proceso posterior completa y verifica la aplicación. No sustituye una prueba de pérdida de alimentación durante escrituras.

## 9. Inmutabilidad de una revisión ya referenciada

La prueba I06 añade un inventario posterior con firma y anclaje válidos, pero cambia los bytes de una publicación manteniendo el mismo ID y número de revisión. El restaurador lo rechaza y conserva la publicación y el catálogo anteriores. La firma del titular no sustituye la regla experimental de que una modificación debe tener revisión nueva: de otro modo una referencia guardada cambiaría de significado.

Se añaden comprobaciones de transición que impiden retroceder la cabeza conocida o restaurar como activo el cuerpo de una revisión local ya retirada o expurgada. La nueva prueba cubre específicamente la reescritura de contenido; los otros límites requieren regresiones propias antes de considerarlos una cobertura completa. El formato sigue siendo experimental y no se adopta como política definitiva de archivo.

Si una transición se rechaza después de validar el anclaje, el registro puede quedar en receiving con el catálogo previo intacto. Ese estado no significa que haya una descarga activa ni que se haya aplicado la revisión nueva. La clasificación persistida de todos los errores de transición permanece pendiente junto a la composición con autorizaciones y conflictos.

## 10. Rechazo persistido de transiciones y reintento posterior

I07 usa un inventario posterior firmado correctamente que intenta retroceder la cabeza de una publicación desde revisión dos a uno. I08 intenta convertir en activa la revisión dos ya retirada, con cuerpo y huella autorizados por un nuevo evento. Ambos se rechazan antes de cambiar el catálogo. Una conexión nueva verifica que el registro conserva secuencia esperada tres, aplicada dos y estado rejected, con código de error estable.

El caso I06 comprueba ahora también el rechazo persistido de reescritura de contenido. Las transiciones clasificadas usan códigos revision_rollback, retired_revision_reactivation, revision_content_rewrite y missing_previous_object; esta última sigue sin regresión dedicada. No se guardan cuerpos en el detalle de error. El catálogo anterior y la retirada siguen intactos.

En I07 e I08, el titular emite después una nueva intención en la secuencia cuatro que vuelve a describir el inventario válido. Otro proceso la valida, aplica y deja estado complete con secuencia esperada y aplicada cuatro. No se retrocede la historia KERI ni se reetiqueta como válido el inventario rechazado: se acepta una instrucción posterior comprobada.

La semántica es una regla de transición del arnés de aplicación, no una prohibición nativa de KERI ni una política definitiva de restauración. Otros errores de formato, autoridad o red no tienen aún una clasificación persistida exhaustiva y pueden dejar receiving; la tabla no demuestra un proceso activo. Sigue pendiente componer autorización de proveedor y registro duradero de conflictos, sin deducir actualidad global.

## 11. Composición con autorización y conflicto conocido

Cuatro pruebas de [keri_inventory_access.py](laboratorio-identidad/keri_inventory_access.py) componen el restaurador con las declaraciones nativas de rol/dirección y el registro local de conflictos. El envoltorio restore_authorized es una entrada experimental distinta del restaurador básico, que continúa usándose para los ensayos de integridad aislados.

- Un proveedor autorizado en el rol agent y con dirección validada permite restaurar y repetir el inventario.
- Una dirección conocida sin autorización se rechaza antes de llamar al transporte. La prueba verifica que no se emiten peticiones HTTP ni se crea el catálogo.
- Un conflicto persistido bloquea igualmente antes de la red. La evidencia sintética se valida mediante el mecanismo acotado del registro —dos ramas sn=1—, no mediante una bandera recibida del proveedor.
- Si llega una revocación durante la descarga, la comprobación repetida antes de aplicar impide modificar el catálogo; la recepción queda receiving y no se devuelve complete.

La dirección de red se obtiene del estado de resolución validado; la distribución de declaraciones sigue siendo controlada por el coordinador. El rol agent representa entrega únicamente para este arnés. La comprobación se repite contra conflicto, autorización y dirección antes de aplicar. No es una operación atómica entre resolución, registro de conflictos y catálogo: persiste una ventana entre comprobación y commit, sin concurrencia general probada.

La composición usa un objeto público y reabre los almacenes en el mismo proceso. Los procesos nuevos y el inventario completo de perfil/publicaciones se prueban separadamente en otras suites; no se presenta esa suma como un ensayo conjunto de todas las variantes. Las pruebas solo cubren conflicto ya registrado y la revocación inducida en el punto de descarga; ausencia de registro no prueba ausencia de conflicto.

La puerta de autorización es optativa en la API de laboratorio: la entrada restore básica y el servidor de prueba no constituyen un servicio público protegido. No se despliega ni se conecta al simulador. Actualidad global, registro general de ramas y coordinación atómica siguen pendientes. La composición añade cuatro comprobaciones a las ocho de inventario, sin sustituirlas ni completar un E/T.

## 12. Omisión explícita y persistencia del bloqueo de acceso

I09 prueba un inventario posterior autorizado que omite un objeto ya presente sin incluir una retirada. Se rechaza y se conserva el catálogo anterior; el registro de recepción guarda rejected con código missing_previous_object. Se completa así la regresión dedicada pendiente de esta transición, sin convertir omisión de inventario en orden de borrado.

La entrada restore_authorized conserva ahora un registro local del último intento por identidad/proveedor, separado de la recepción: checking, blocked, incomplete o complete, con código de bloqueo cuando se conoce. Las cuatro pruebas de composición comprueban ese registro desde otra conexión SQLite. El conflicto conocido y la falta de permiso quedan blocked antes de HTTP; una revocación durante descarga queda blocked aunque la recepción de contenido conserve receiving. Una nueva autorización válida del titular permite un intento posterior que termina complete.

El registro describe el último intento local, no el estado global ni la vigencia futura de una autorización. Se reemplaza por clave identidad/proveedor; no incorpora un historial de actividad ni estadísticas de uso. Solo se utiliza con datos sintéticos de laboratorio. No convierte checking o receiving en prueba de que exista un proceso activo, ni complete en permiso permanente.

El registro de intentos no es la evidencia de conflicto: esta continúa en su almacén y con su alcance de validación limitado. El catálogo, la recepción, la resolución y los dos registros no forman una transacción conjunta. Fallos no clasificados de red, formato o almacenamiento siguen pendientes y pueden dejar el intento en checking. La composición entre procesos nuevos e interrupción aún debe ensayarse de forma específica.

## 13. Restauración autorizada entre procesos e interrupción

Tres pruebas adicionales de composición elevan el laboratorio a 69 comprobaciones; la suite de acceso tiene siete. Se usa un objeto público y cada petición de restauración autorizada puede ejecutarse ahora en un proceso verificador nuevo sobre sus almacenes persistidos, sin recibir la clave del titular.

1. Un proceso restaura desde el proveedor autorizado y otro repite la operación. Se conserva un único objeto, su cuerpo y el estado complete con secuencias esperada/aplicada iguales.
2. El proceso termina abruptamente en el punto de instrumentación previo a aplicar el catálogo. Otro acceso SQLite comprueba catálogo vacío, recepción receiving con secuencias uno/cero e intento checking. Un proceso nuevo valida otra vez autorización, dirección y conflicto, reintenta y completa; otro lo repite sin duplicar el objeto.
3. Después de esa interrupción se entrega al almacén de resolución una revocación firmada. El siguiente proceso se bloquea con código unauthorized_provider y no aplica el catálogo. Solo una autorización posterior válida del titular permite que otro proceso complete.

La salida estructurada del trabajador distingue un resultado complete de un bloqueo conocido; la terminación instrumentada tiene un código propio y no se interpreta como éxito. La prueba comprueba de forma explícita la recepción persistida antes de reintentar.

Son procesos nuevos en el mismo equipo y con servicios disponibles, no una red de operadores independientes. El coordinador sigue distribuyendo declaraciones de rol y el punto de terminación ocurre después de comprobaciones y commits previos, antes de la transacción del catálogo. No se prueban cortes dentro de escrituras, recuperación tras pérdida del registro de conflictos ni concurrencia entre la última comprobación y el commit. La composición con conflicto previo y la caída de proveedor tienen pruebas separadas; no se presume aquí una combinación completa de todos los fallos.

Próximo bloque: clasificar fallos operativos persistidos y contrastar que un conflicto recibido entre interrupción y reintento también bloquee, manteniendo el alcance acotado de evidencia. El resultado no completa T05/T06 o E09 en su alcance social y no acredita actualidad global.

## 14. Conflicto sobrevenido y fallos operativos registrados

Tres pruebas adicionales elevan el conjunto a 72 comprobaciones y la suite de acceso a diez. Tras terminar el trabajador antes de aplicar, se incorpora evidencia verificada de dos ramas en el registro persistido. Dos procesos posteriores se bloquean por known_conflict; el segundo lo hace incluso después de recibir una nueva autorización válida del proveedor. El catálogo continúa vacío y la recepción pendiente uno/cero. Renovar un rol no elimina ni resuelve la contradicción de la identidad.

Los fallos HTTP y de transporte de la entrada autorizada pasan a registrar failed con un código, sin guardar URL, texto del error o cuerpos. Un proveedor apagado produce transport_unavailable; un endpoint de prueba ausente produce http_404. Se comprueba el registro con otra conexión y que no se aplica el catálogo ni se crea una recepción de inventario al fallar antes de obtener la prueba. Tras reiniciar el proveedor y recibir su dirección firmada nueva, o restaurar el endpoint ausente, un reintento válido completa y reemplaza el estado del último intento.

Solo se ensayan esos dos fallos operativos y su recuperación inicial. La clasificación HTTP usa el código de respuesta; no se presume probada cada respuesta HTTP posible. Los errores de formato, disco o validación no clasificados pueden todavía dejar checking/receiving. Tampoco se prueba aquí un fallo después de aplicar catálogo pero antes de registrar complete en el almacén de acceso.

El alcance del registro de conflicto sigue siendo el fixture de ramas sn=1 sin rotación o testigos. No existe procedimiento automático de desbloqueo, elección de rama ni recurso implementado. Estas pruebas confirman una negativa segura en el caso conocido, sin demostrar detección de conflictos todavía no recibidos ni actualidad global.

Próximo bloque: estado verificable después de aplicar el catálogo e interrumpir antes de registrar el último intento, y comprobación de que ese estado no se presenta como traslado confirmado. No se introduce una nueva regla de confianza para cerrar el intervalo entre almacenes.

## 15. Catálogo aplicado e intento todavía sin confirmar

Dos pruebas adicionales elevan el laboratorio a 74 comprobaciones; la suite de acceso tiene doce. Se instrumenta una terminación inmediata después de que el restaurador haya aplicado catálogo y recepción, pero antes de marcar complete en el registro del último intento. La salida del trabajador identifica ese punto con un código distinto de la interrupción anterior a aplicar; no devuelve un resultado de restauración completada al solicitante.

Una conexión nueva observa un objeto verificado y recepción complete con secuencias uno/uno, mientras el último intento sigue checking. Son hechos compatibles de almacenes distintos: no se inventa una transacción conjunta ni se borra el catálogo para hacer coincidir las etiquetas. Un nuevo proceso revalida autorización y conflicto, repite y termina con un único objeto y el intento complete.

En el segundo caso se incorpora una revocación firmada antes del reintento. El proceso nuevo se bloquea por unauthorized_provider y mantiene el objeto ya verificado y la recepción aplicada. Revocar permiso de entrega del proveedor no elimina esa copia pública local. Solo una autorización posterior válida permite que otro intento vuelva a completar. La prueba verifica que el cuerpo no cambia ni se duplica.

La instrumentación termina el proceso fuera de una escritura activa. No se simula pérdida de alimentación ni una modificación concurrente entre última comprobación y commit. El registro del último intento describe lo observado y no se convierte en autorización futura o actualidad global. El estado aplicado puede coexistir con un intento bloqueado después; la interfaz posterior deberá distinguirlos.

Siguiente unidad propuesta: observación de esos estados persistidos sin consultar red ni modificar autorización, para que revisión de resultados y reanudación no infieran éxito o actividad a partir de una sola etiqueta. No se adopta una regla de consenso ni se conecta esta instrumentación al simulador.

## 16. Diagnóstico local sin modificar ni confirmar estados

El módulo [keri_diagnostics.py](laboratorio-identidad/keri_diagnostics.py) lee catálogo, recepción, último intento y registro de conflicto mediante conexiones SQLite con mode=ro y query_only. No abre el gestor de identidad, no genera claves, no consulta red ni cambia autorizaciones. Requiere el marcador del escenario sintético y no crea bases cuando faltan.

El resultado conserva dimensiones separadas y distingue archivo ausente, fila ausente y base/esquema ilegible. Un registro de conflicto que no se puede leer queda desconocido, no «sin conflicto». El catálogo solo informa número de revisiones almacenadas; no revalida criptográficamente su contenido. La autorización aparece not_checked, la actualidad not_proven y atomic_snapshot es false porque se leen almacenes distintos.

Se añaden tres pruebas de límites: escenario sin bases no crea archivos; una base ilegible no se informa como vacía ni se modifica; metadatos ajenos al esquema no se reflejan como secuencias, estados o códigos válidos. Se usan campos tipados y códigos conocidos, sin cuerpos, eventos, firmas, rutas o URLs en el resultado.

Las pruebas existentes de composición comprueban además el diagnóstico sobre estados reales del arnés: recepción complete/catálogo aplicado con intento checking, y recepción complete con intento bloqueado por revocación posterior. En el primero se comparan bytes y fechas de modificación de las bases antes y después del diagnóstico. No se atribuye un permiso o éxito agregado a esas etiquetas coexistentes.

El conjunto suma 77 comprobaciones, incluidas las tres nuevas. No se prueban todos los modos de journaling, escrituras concurrentes ni archivos manipulados arbitrariamente; no es una auditoría del almacén o una herramienta de recuperación general. Es un comando de diagnóstico del laboratorio, no una pantalla del producto ni captación de actividad.

Reproducción desde el entorno del laboratorio: `python laboratorio-identidad/keri_diagnostics.py --state-dir RUTA_ESCENARIO --owner IDENTIDAD_SINTETICA --provider PROVEEDOR_SINTETICO`. Los escenarios temporales de las pruebas se eliminan al terminar; el comando solo puede inspeccionar uno que aún exista y esté marcado.

Siguiente unidad propuesta: balance actualizado de escenarios integrados frente a condiciones E/T y lista corta de brechas prioritarias, antes de añadir más variantes. Se mantendrá explícito que el banco experimental no es una red distribuida operativa ni una garantía de protección de alto riesgo.

## 17. Balance consolidado y siguiente prioridad

El [balance actualizado](BALANCE-01-IDENTIDAD-Y-TRASLADO.md) sustituye las tablas iniciales anteriores al inventario y clasifica la cobertura E/T actual como parcial o sin ejecutar. La próxima prioridad es un flujo público multiobjeto integrado que reúna autorización, origen apagado, actualización posterior al corte, referencias y reapertura en procesos nuevos. No se sumarán suites separadas para afirmar que esa ejecución ya existe. El total permanece en 77 comprobaciones.

## 18. F01 — Flujo público integrado ejecutado

Una prueba de [keri_public_flow.py](laboratorio-identidad/keri_public_flow.py) reúne en la misma ejecución las piezas antes ensayadas por separado. El conjunto del laboratorio suma 78 comprobaciones. F01 usa un perfil genérico público y dos publicaciones propias sintéticas, dos servicios HTTP de solo lectura, control del titular separado y verificador ejecutado en procesos nuevos por recepción.

Secuencia observada:

1. Se ancla un inventario inicial y se preparan copias A/B. El observador guarda una referencia a una publicación y su primera revisión, antes del cambio.
2. Solo A tiene inicialmente autorización de entrega. La recepción usa la entrada autorizada y la dirección validada, no una URL pasada al restaurador básico.
3. Se apaga A y se comprueba fallo de conexión. Después se entregan la revocación de A y la autorización de B. Un proceso nuevo recupera desde B el inventario inicial.
4. Con A todavía apagado, el titular crea y firma realmente un inventario posterior: conserva el perfil y la primera revisión de una publicación, añade una revisión nueva y retira la otra mediante marcador. No es una actualización prefirmada antes del corte.
5. B entrega la revisión nueva; otros procesos la validan y repiten sin duplicar. La referencia guardada resuelve los bytes originales por el mismo ID y revisión, mientras la publicación retirada conserva marcador y pierde su cuerpo previo en el catálogo local.
6. A vuelve con su inventario antiguo y anuncia su puerto nuevo mediante declaración propia válida. La puerta autorizada lo bloquea por rol revocado; B sigue entregando la revisión dos. El diagnóstico distingue recepción/último intento de la falta de prueba de actualidad global.

Se comprueban cinco filas de versiones/marcadores, referencia sin modificar, rechazo estructurado de A y ausencia de duplicados tras repetir B. Las claves del titular no se escriben en los directorios HTTP. No es una frontera de seguridad entre administradores: todos los procesos comparten equipo y usuario.

Se satisface la condición del flujo público acotado fijada en el balance. No se completan E08 o T02/T03 en su alcance social: faltan relaciones, contextos privados, recuperación y distribución independiente de declaraciones. Roles y direcciones se entregan al parser por el coordinador. El formato del perfil sigue siendo el genérico del inventario, no un formato final de cuenta.

F01 prueba la secuencia válida y el retorno del origen. Las interrupciones y defectos se cubren en otras suites y no se añaden retroactivamente a F01. No hay TLS, prueba de actualidad global, resolución de ramas, pérdida total del origen y de respaldos, ni protección frente a operadores coludidos. H01 permanece abierto y no se despliega un servicio público.

Siguiente prioridad: investigar el transporte de las declaraciones nativas para que el observador las obtenga sin inyección directa del coordinador. La autenticidad, el estado conocido y los límites de actualidad deberán conservarse por separado; no se inventará descubrimiento global ni consenso para presentar éxito.

## 19. F02 — Transporte HTTP de introducción OOBI y límite de revocación

Dos pruebas de [keri_oobi_transport.py](laboratorio-identidad/keri_oobi_transport.py) usan OOBIEnd de la revisión fijada, servido mediante Falcon y WSGI en bucle local. No se implementa un formato propio de declaraciones. Un observador obtiene por HTTP la historia del titular, su autorización de rol y la dirección firmada del proveedor, y los entrega al parser nativo. El laboratorio suma 80 comprobaciones.

La identidad esperada del titular está fijada por el escenario. El observador conoce previamente la identidad del proveedor mediante su creación entregada por el coordinador: la prueba aísla transporte de rol/dirección y no demuestra bootstrap recursivo o descubrimiento global. El servicio OOBI usa el Habery real del controlador con sus medios de clave disponibles; no es uno de los servidores A/B de datos sin claves y no se propone mover ese entorno a un proveedor. Se ejecuta en un hilo y las peticiones/escrituras se serializan deliberadamente.

Resultado de revocación: tras registrar localmente el corte del rol en el controlador, otra consulta al mismo endpoint de introducción deja al observador con su autorización anterior. El código nativo replyEndRole incluye proveedores permitidos/habilitados; en esta configuración no incorpora el corte que ya quitó al proveedor de ese conjunto. Entregar al parser el mensaje nativo de corte sí cambia el registro del observador a revocado.

Por tanto, esta consulta de introducción **no se adopta como canal de sincronización de revocaciones**. Una respuesta correcta y una lista actual sin un proveedor no autorizan al cliente a inferir por su cuenta un corte firmado. La prueba mide este uso acotado; no evalúa todos los roles, testigos, endpoints o políticas posibles de KERI y no implica que la introducción tenga que cumplir una función de sincronización que no se ha demostrado.

No se modifica el endpoint ni se inventa un feed o arbitraje para superar el límite. Se mantiene la distribución explícita de cortes en F01 hasta identificar y ensayar un transporte existente adecuado. Tampoco se acredita independencia si ese transporte exige siempre al controlador original disponible.

Próxima unidad: inventariar en el componente fijado los mecanismos de entrega/consulta de respuestas firmadas que puedan transportar adiciones y cortes, incluyendo estado obsoleto y origen indisponible. La prueba de introducción se conserva separada del flujo F01 y no se eleva a actualidad global o traslado completo.

## 20. F03 — Ingreso nativo de respuestas firmadas y significado del acuse

Tres pruebas de [keri_rpy_ingress.py](laboratorio-identidad/keri_rpy_ingress.py) usan HttpEnd de la revisión fijada, servido con Falcon/hio en bucle local. El conjunto suma 83 comprobaciones. Se envían mensajes nativos firmados de concesión y corte mediante POST con cuerpo CESR y sus adjuntos en la cabecera prevista por la biblioteca. La identidad del titular y la del proveedor están conocidas previamente por el observador.

La concesión y el corte llegan realmente por HTTP. El endpoint devuelve 204 y deja bytes en rxbs; el estado del rol solo cambia cuando el consumidor ejecuta el parser y la validación nativos. Una firma ajena que pretende cortar el rol también recibe acuse de cola, pero no revoca la autorización después de validarse. Repetir una concesión anterior tras un corte no la restablece en el escenario de fechas ordenadas probado.

La tercera prueba borra deliberadamente la cola de memoria después del 204 y antes de validarla: el corte no se aplica. Reenviar el mismo corte y procesarlo sí revoca el rol. Es pérdida instrumentada de memoria, no terminación real del proceso ni ensayo de fallo eléctrico. La cola rxbs no se presenta como un registro durable y el 204 no se interpreta como prueba de validación o persistencia.

El planificador hio mantiene el servidor de transporte en un hilo; el consumidor se activa explícitamente entre peticiones, sin procesamiento concurrente del mismo estado. No hay HTTP público, autenticación TLS, límites de abuso probados ni descubrimiento de receptores. La entrada HTTP no se ofrece como servicio de producción protegido.

Resultado: existe transporte nativo para entregar cortes explícitos, a diferencia del uso de introducción de F02 como lista consultada. Esto no prueba reparto automático a todos los contactos, reenvío durable, confirmación firmada del receptor o continuidad con emisor/receptor indisponibles. Se conserva la separación entre recepción en cola, validación y efecto persistido.

Siguiente prioridad: investigar los mecanismos de buzón/entrega duradera existentes en el componente para distribuir respuestas ya firmadas sin depender de que el titular esté conectado en cada recepción. No se inventará consenso ni se tomará un acuse HTTP como prueba de autoridad actualizada.

## 21. F04 — Buzón nativo persistido y emisor terminado

Dos pruebas de [keri_mailbox.py](laboratorio-identidad/keri_mailbox.py) usan Mailboxer de la revisión fijada. Un proceso emisor crea identidad y respuestas nativas firmadas, escribe creación/concesión/corte en el buzón y termina antes de invocar al receptor. Las claves privadas solo viven en ese proceso y no se serializan: el fichero auxiliar conserva únicamente los identificadores públicos y el buzón conserva mensajes y firmas. El laboratorio suma 85 comprobaciones.

Otros procesos reabren el mismo buzón nativo y el estado del observador: primero validan la creación y concesión; después el corte, su repetición y la reapertura sin mensajes nuevos. El segundo escenario intercala un corte firmado por otra identidad: estar guardado y tener un ordinal no lo hace válido para revocar; el corte correcto posterior sí cambia el rol.

El buzón ofrece un índice ordinal por tema; la prueba escoge explícitamente desde qué ordinal leer mediante el coordinador. Repetir una respuesta puede ocupar otro ordinal; se comprueba que repetir el corte no restaura el rol, no una garantía general de entrega exactamente una vez. No se ha implementado un cursor de consumo persistido, acuse de procesamiento o sincronización automática de todos los contactos.

Es persistencia local entre procesos con emisor terminado, no transporte HTTP de buzón ni caída durante escritura. Mailboxer guarda índice y cuerpo mediante sus métodos nativos; no se presume transacción conjunta o tolerancia a corte entre ambos. El directorio de buzón está aislado en el escenario y no requiere el almacén privado del titular para consumir los mensajes ya firmados. Eso no demuestra aislamiento frente a un administrador de la misma máquina, acceso autorizado al buzón ni recuperación de claves del titular.

Se usa la API de almacenamiento nativa para respuestas serializadas; no se afirma que este ensayo despliegue el flujo completo de agentes, enrutamiento o autorización de lectura de buzón. La ausencia de mensajes posteriores no acredita actualidad global. La persistencia del rol es validada por la biblioteca, no deducida del ordinal del buzón.

Siguiente bloque propuesto: transporte nativo de lectura del buzón y conservación del progreso de consumo sin saltar una revocación tras interrumpir el receptor. Se mantendrán separados almacenamiento, recepción y validación. No se añade consenso, política de confianza o despliegue público.

## 22. F05 — Lectura HTTP de buzón y cursor persistido

Dos pruebas de [keri_mailbox_http.py](laboratorio-identidad/keri_mailbox_http.py) reúnen mensajes prefirmados, emisor terminado, servidor sin claves del titular, lectura HTTP y consumidores en procesos nuevos. El laboratorio suma 87 comprobaciones.

El servidor adapta a una respuesta HTTP finita las tramas del MailboxIterable nativo. No es la ruta completa de consulta firmada, suscripción continua o MailboxDirector del componente: esa integración sigue pendiente. Se usan tema y destinatario sintéticos conocidos, sin autorización de lectura del buzón o descubrimiento probados. La URL inicial la proporciona el coordinador.

El consumidor conserva el siguiente índice ordinal en SQLite y valida las respuestas con el parser/registro nativos antes de avanzarlo. Se exige continuidad del índice en las tramas: no se salta una posición para alcanzar otra más reciente. Este lector solo interpreta creación y respuestas de rol del escenario; no es un cliente SSE general ni un verificador universal de mensajes.

En ambos casos, un primer consumidor recibe creación/concesión y deja cursor dos. Otro termina de forma instrumentada al llegar al corte de índice dos:

- Antes de validar: el cursor sigue dos y el rol sigue permitido. El proceso siguiente recibe de nuevo el corte y lo aplica.
- Después de validar pero antes de guardar el cursor: el cursor sigue dos y el rol ya está revocado. El proceso siguiente repite el corte sin restaurar el permiso y avanza.

Al final se obtiene cursor cuatro, rol revocado y una consulta posterior sin eventos nuevos que no mueve el cursor. El emisor que firmó los mensajes ya había terminado antes de arrancar el servidor de buzón. No se serializan sus claves privadas ni el consumidor necesita abrir su almacén.

Los almacenes de validación y cursor no son una transacción conjunta. La repetición es deliberada y solo se demuestra idempotencia de estas respuestas, no ejecución exactamente una vez de efectos sociales. La terminación ocurre en puntos instrumentados fuera de una escritura activa. Las dos pruebas iniciales no cubren pérdida de cursor, corrupción, disco lleno, caducidad ni los casos de rechazo y huecos examinados a continuación. Un rechazo no debe saltarse automáticamente sin una política comprobada.

No se deduce actualidad global de no recibir eventos. Tampoco se añade acceso público al buzón o protección frente a vigilancia: todo el escenario es local. Las ampliaciones siguientes examinan lectura obsoleta, mensajes rechazados y huecos de índice. La integración del flujo de entrega nativo completo sigue pendiente.

### F05: rechazo persistente ante firma ajena o hueco

Dos pruebas adicionales verifican el comportamiento ante una respuesta de corte firmada por otra identidad y ante la eliminación del índice dos del buzón sintético, conservando en tres un corte válido. En ambos casos, el consumidor se detiene con error concreto y mantiene cursor dos; otro proceso vuelve a detenerse en el mismo punto. La concesión anterior sigue presente en la vista local. No se declara recepción completa, revocación ni actualidad global.

Esto identifica una brecha operativa: un mensaje rechazado o un hueco puede impedir alcanzar un corte válido posterior. Conservar el cursor evita saltos silenciosos, pero no proporciona disponibilidad frente a un buzón defectuoso o malicioso. El ensayo no adopta una política de descarte, cuarentena o reparación. Queda como propuesta estudiar una vía de recuperación verificable que distinga posición recibida, validación y aplicación sin dar autoridad al proveedor para omitir eventos. La lectura obsoleta y la recuperación de cursor perdido siguen pendientes.

Las cuatro pruebas focalizadas del lector HTTP se han superado con ResourceWarning tratado como error. La última batería completa confirmada mantiene 87 comprobaciones; con las dos nuevas hay 89 previstas, sin nueva ejecución completa en este bloque porque solo se han añadido escenarios de prueba. Los 109 casos del simulador social son una batería separada.

### F05: una respuesta vacía no acredita actualidad

Una quinta prueba usa dos servidores HTTP con buzones públicos de la misma identidad. El primero conserva únicamente creación y concesión; el segundo también tiene el corte. El consumidor recibe dos mensajes de la fuente antigua y, en otro proceso, una respuesta vacía: mantiene cursor dos y permiso anterior en su vista local aunque el corte exista en otra fuente.

El coordinador elige expresamente la segunda URL. Con ella, el mismo consumidor recibe el corte, avanza a cuatro y conserva la revocación cuando vuelve a consultar la fuente antigua. Esto verifica continuidad del cursor entre estas copias compatibles y ausencia de restauración por silencio; no demuestra detección de obsolescencia, descubrimiento, conmutación automática o equivalencia de índices entre proveedores arbitrarios. En este ensayo se han copiado por API nativa las dos primeras posiciones, de modo que comparten su secuencia ordinal. Un cursor de transporte no constituye una posición global del historial de identidad.

Cinco pruebas focalizadas superadas; última batería completa confirmada: 87, total actual previsto: 90. La siguiente unidad debe abordar la integración del transporte nativo y sus contratos de cursor, antes de ampliar recuperación o políticas de descarte. Sin decisiones de confianza nuevas ni cambios en el simulador social.

### F05: contrato del transporte nativo antes de integrarlo

La revisión de Poller.eventDo en la revisión fijada de KERIpy muestra que el cursor nativo se almacena por pareja identidad/testigo y tema. El componente introduce el mensaje en su cola, cede el control al planificador y después persiste el índice recibido. En ese punto no comprueba un resultado de validación criptográfica o de aplicación. Es una observación del código, no una reproducción de pérdida de mensajes con MailboxDirector completo. No puede sustituirse sin más nuestro cursor posterior a validación por ese cursor de transporte.

Se ha ejecutado además una prueba directa del MailboxIterable nativo con un tema sintético cuyos índices son cero, uno y tres. Al solicitar desde dos, la primera lectura de datos devuelve tres; la segunda devuelve tres de nuevo y la siguiente queda vacía. El componente incrementa su posición interna por mensaje emitido en lugar de situarla directamente después del ordinal emitido. Este comportamiento se reproduce en la versión fijada y en un tema con hueco preparado expresamente; no supone que los buzones normales tengan huecos ni demuestra un fallo de seguridad. El consumidor estricto del ensayo ya rechaza la discontinuidad antes de avanzar.

Referencia inspeccionada: [indirecting.py de la revisión fijada](https://github.com/WebOfTrust/keripy/blob/4ce4cc79e06653f77342be1bf604086b89b1f090/src/keri/app/indirecting.py), clases Poller y MailboxIterable. No se ha modificado el código de terceros.

Propuesta técnica pendiente de ensayo integrado: distinguir cursor de recepción por fuente y tema, entrada durable de mensajes pendientes y resultado de validación/aplicación. No se adopta una regla para saltar índices, descartar mensajes ni equiparar cursores de proveedores. La siguiente unidad debe comprobar el punto de persistencia del Poller nativo con interrupción y cola pendiente, antes de diseñar una adaptación. Seis pruebas focalizadas superadas; última batería completa confirmada 87, total previsto actual 91.

## 23. F06 — Persistencia del cursor del Poller sin validación

[keri_poller_checkpoint.py](laboratorio-identidad/keri_poller_checkpoint.py) ejecuta el generador eventDo real de Poller y su base persistente, con cliente HTTP y envío de consulta sustituidos por dobles controlados. No hay servidor SSE, planificador HTTP ni flujo completo de MailboxDirector en esta prueba. La carga es un mensaje sintético sin validar, no un evento de identidad aceptado.

Un caso con dos subescenarios termina el proceso en puntos instrumentados: tras encolar en RAM, antes de persistir el cursor; y después de persistir ese cursor, sin ejecutar un parser. En el primero, reabrir conserva ausencia de progreso. En el segundo, reabrir conserva el índice cero aunque la cola del Poller nuevo esté vacía y no haya habido validación. Se observa la distinción entre progreso de transporte y resultado de validación; no se atribuye una pérdida inevitable al planificador completo ni se demuestra una vulnerabilidad. El ensayo no modifica el componente de terceros.

Este resultado impide tratar el índice nativo como confirmación de aplicación. La integración debe demostrar cómo conserva o recupera mensajes recibidos antes de usar ese progreso para evitar una nueva entrega. La entrada durable y la repetición posterior son propuestas de adaptación pendientes; no se adopta aún una política de salto, descarte o confianza. Tampoco se prueban cortes dentro de escrituras activas o errores físicos del almacenamiento.

La prueba focalizada supera ambos subescenarios con ResourceWarning como error. La batería completa posterior confirma 92 comprobaciones superadas en 61,476 segundos. Persiste el aviso conocido de deprecación de hio; no se han parcheado dependencias.

## 24. F07 — Entrada durable y repetición de validación

[keri_durable_inbox.py](laboratorio-identidad/keri_durable_inbox.py) ensaya una adaptación local explícita: la cola del Poller real se sustituye por un objeto cuyo append confirma el mensaje en SQLite antes de devolver el control. El cliente HTTP y el envío de consulta siguen sustituidos por dobles; no es todavía una integración de MailboxDirector o SSE real. Solo hay una fuente y un tema sintéticos fijos. El emisor firma creación, concesión y corte en otro proceso, que termina antes de recibirlos.

Un proceso ejecuta el generador nativo hasta persistir su cursor tres y termina sin validar: otro proceso encuentra las cuatro entradas pendientes y la identidad emisora todavía ausente del historial validado del receptor. La recepción durable y el progreso del transporte no se presentan como aprobación.

El siguiente proceso valida creación, concesión y corte con el parser nativo y termina después de validar el corte, antes de marcar esa entrada como validada en SQLite. Un proceso nuevo repite el corte pendiente y su duplicado, conserva la revocación y deja cero pendientes. Otra apertura no procesa entradas adicionales ni restablece permiso. No hay una transacción conjunta entre el historial nativo y el marcador SQLite; la repetición se demuestra para estas respuestas, sin afirmar efectos sociales exactamente una vez.

La prueba focalizada supera todo el flujo con ResourceWarning como error. La última batería completa confirmada sigue siendo 92; el conjunto previsto con esta prueba es 93. No se repite la batería completa porque el nuevo módulo no modifica componentes compartidos.

Esta propuesta no adopta una cola de producción: append recibe solo bytes, y aquí la fuente y el tema se conocen por el escenario; no se conserva un sobre general con fuente, tema y ordinal ni se acredita su asociación. No se han ensayado varios temas, cuotas, mensajes rechazados, corrupción o fallo físico durante commit. Tampoco se han unido todavía esta cola y el transporte HTTP del laboratorio en un flujo nativo completo. Siguiente unidad: verificar la frontera de fallo de persistencia antes de avanzar el cursor y acotar el sobre de recepción; no introducir descarte o confianza nuevos.

### F07: fallo de inserción antes del corte y reintento explícito

Una segunda prueba instala, únicamente en la base sintética, un trigger SQLite que aborta el tercer INSERT. Las dos primeras entradas quedan recibidas; al intentar persistir el corte se propaga el error y el proceso termina sin adelantar el cursor nativo: al reabrir hay dos pendientes y progreso uno. La identidad emisora todavía no se ha validado. Esto comprueba la frontera de un fallo lógico real de transacción, no disco lleno, corrupción o pérdida física de datos.

Tras retirar el trigger de prueba, un proceso nuevo recibe desde la posición posterior al cursor guardado. El doble de transporte entrega los mensajes desde ese índice; no hay servidor real ni descubrimiento. El corte y su duplicado completan cuatro pendientes, con cursor tres. Otro proceso valida los cuatro, conserva la revocación y deja cero pendientes. La retirada de la causa del fallo y el reintento son acciones explícitas del escenario, no recuperación automática del producto.

Las dos pruebas de esta unidad superan ResourceWarning como error. Última batería completa confirmada: 92; total previsto con las ampliaciones focalizadas: 94. No cambian los componentes compartidos ni se repite la batería completa.

Propuesta de sobre mínimo para la siguiente integración: identificador local de fuente y destinatario, tema, ordinal de transporte, bytes originales y huella local de esos bytes, con estado de recepción separado del resultado de validación. Los datos de ruta describirían procedencia observada, sin otorgar autoridad al emisor del mensaje. La unicidad debería delimitarse por fuente/destinatario/tema/ordinal; bytes distintos para la misma posición deberían conservar un conflicto visible, sin sobrescribir ni elegir automáticamente. Esta propuesta todavía no está implementada o adoptada como formato. append del Poller entrega solo bytes, por lo que la asociación a ese sobre necesita un punto de integración que conserve metadatos y requiere un ensayo de transporte real.

## 25. F08 — HTTP real, sobre durable y validación sin servidor

[keri_http_inbox.py](laboratorio-identidad/keri_http_inbox.py) reúne el servidor HTTP local finito de F05, los mensajes prefirmados del buzón nativo y una entrada SQLite con metadatos. El proceso emisor ya ha terminado antes del servicio. Un consumidor independiente recibe cuatro mensajes; cada transacción conserva fuente local (URL), destinatario sintético, tema, ordinal, bytes y huella, junto al siguiente ordinal de recepción. Este progreso no marca los mensajes como validados. Una nueva consulta no duplica las entradas.

Se comprueba que la identidad emisora aún no figura en el historial validado del receptor y que las cuatro filas siguen pendientes. El servidor se detiene; la validación continúa en otros procesos únicamente desde la entrada durable. Uno termina después de validar el corte con el parser nativo, antes de marcarlo. Otro repite el corte y su duplicado, conserva la revocación y deja cero pendientes; una nueva apertura no produce efectos adicionales en este escenario.

La prueba focalizada supera ResourceWarning como error. Última batería completa confirmada: 92; total previsto con los bloques focalizados posteriores: 95. El nuevo módulo no modifica helpers compartidos y no se repite la batería completa en este bloque.

Es una adaptación HTTP finita experimental, todavía distinta del flujo nativo de consultas firmadas, SSE continuo y MailboxDirector. La URL identifica una procedencia observada; no acredita autoridad sobre el mensaje ni autenticación de lectura. No se añade descubrimiento o conmutación automática. La prueba solo admite una combinación de fuente, destinatario y tema al validar: rechaza varias en lugar de inventar orden entre proveedores. Una huella local permite detectar cambios de bytes respecto al registro, pero no autentica metadatos de ruta. La equivalencia de índices entre servidores, conflictos en una misma posición, cuotas y fallos de disco siguen pendientes. No se adopta el sobre como formato de producto ni se publica el buzón.

Siguiente unidad: comprobar metadatos o bytes alterados y posición repetida con contenido distinto sin convertir el cursor de recepción en validación; conservar evidencia y bloqueo sin adoptar arbitraje o descarte automático.

### F08: alteración local y posición contradictoria

Dos pruebas nuevas comprueban que recepción no equivale a validación. Tras recibir por HTTP real, alterar los bytes de la primera entrada sin cambiar su huella o sustituir el tema impide validar: un proceso nuevo conserva cuatro entradas pendientes, progreso de recepción cuatro e identidad emisora ausente del historial validado. La huella local no protege frente a un atacante que modifique coherentemente tanto bytes como huella o metadatos; no se afirma integridad autenticada del almacén local.

La segunda prueba conserva la recepción original por HTTP y después inyecta una respuesta conflictiva en el límite de transporte, con el índice cero y bytes distintos. No se ha simulado un segundo servidor malicioso completo. El receptor conserva los bytes originales y registra los nuevos en una tabla separada, sin sobrescribir ni avanzar. Un proceso nuevo detecta ese conflicto conocido y bloquea la validación pendiente. Es una precaución del ensayo, sin resolución automática, atribución de culpa o política de consenso. Puede detener el progreso y no supone disponibilidad frente a una fuente maliciosa.

Tres pruebas focalizadas superadas con ResourceWarning como error. La batería completa posterior confirma 97 comprobaciones superadas en 65,506 segundos, con el aviso de deprecación conocido de hio y sin parchear terceros. La siguiente integración debe conectar el resultado de validación durable con la comprobación de autorización de entrega ya ensayada, para que una recepción pendiente o bloqueada no se presente como permiso actualizado; no se amplía la política de conflictos en este bloque.

### F08: corte pendiente y comprobación de autorización

Una cuarta prueba conecta la validación del buzón al mismo almacén nativo resolver que consulta la puerta de autorización de inventario. Primero recibe y valida creación/concesión. Después recibe por HTTP el corte y su duplicado: el cursor de recepción llega a cuatro, pero la vista nativa aún conserva la concesión. Una puerta conservadora del ensayo rechaza restaurar mientras haya entradas pendientes, sin invocar la restauración de inventario.

Un proceso nuevo valida el corte en resolver y deja cero pendientes. La puerta de inventario existente consulta ese mismo historial y rechaza al proveedor como no autorizado, antes de intentar restaurar. La prueba sustituye la función de restauración por un observador de llamadas para comprobar que no se invoca; no demuestra una descarga autorizada completa ni la ruta de éxito con dirección validada. Aquí solo se integran la frontera pendiente/validado y el rechazo posterior al corte.

La precaución de bloquear ante pendientes o conflictos es experimental para este buzón de una fuente; no se adopta una política general que permita a cualquier fuente detener todo el servicio. La consulta de pendientes y la comprobación de permiso no son una transacción conjunta. No se deduce actualidad global de que no queden pendientes y no se añade el buzón al cliente social. Cuatro pruebas focalizadas superadas con ResourceWarning como error; última batería completa confirmada 97 y total previsto 98. La inicialización del directorio aislado resolver se corrigió tras el primer ensayo fallido.

## 26. F09 — Concesión, entrega pública y revocación mediante buzón

Una quinta prueba de [keri_http_inbox.py](laboratorio-identidad/keri_http_inbox.py) completa la ruta de éxito que faltaba en F08. Un titular sintético ancla un inventario con una publicación pública y firma la concesión/corte de entrega. El proveedor sintético firma su dirección HTTP. El buzón nativo conserva las dos creaciones, dirección, concesión, corte y duplicado. Los almacenes efímeros de los firmantes se cierran antes de consumir el buzón; no se exportan claves. A diferencia de las pruebas de emisor sin almacén de F04, aquí sí se usan almacenes temporales del escenario, eliminados al terminar.

El receptor recibe por HTTP y confirma en SQLite las primeras cuatro entradas. Otro proceso valida creaciones, dirección y concesión en el mismo resolver que usa la puerta de inventario. Un proceso independiente restaura efectivamente el inventario y la publicación desde el servidor HTTP autorizado, comprobando pruebas y bytes. No se sustituye la restauración por un doble en esta ruta.

Después se reciben el corte y su duplicado. Mientras están pendientes, la puerta experimental rechaza un nuevo intento. Otro proceso valida el corte; la puerta existente vuelve a rechazar por proveedor no autorizado. La publicación ya restaurada conserva exactamente sus filas y bytes en el catálogo local: revocar entrega no borra la copia pública obtenida antes. El ensayo no atribuye a esa copia actualidad global ni permiso para futuras descargas.

Cinco pruebas focalizadas superadas con ResourceWarning como error. Última batería completa confirmada 97; conjunto previsto actual 99. Se corrigió el nombre de un argumento de la API nativa al preparar el corte del escenario. No se modifican dependencias o helpers compartidos y no se repite la batería completa en este bloque.

Este flujo reúne buzón HTTP finito, persistencia, validación, dirección autorizada, descarga pública real y revocación. Continúa siendo local y experimental, con un titular, un proveedor y un tema. No es consulta firmada/SSE continuo/MailboxDirector completo, traslado social, acceso privado, garantía de independencia o política de confianza aprobada. El bloqueo por pendientes no es una regla general adoptada. La siguiente unidad propuesta es consolidar un diagnóstico de este flujo que distinga recepción, validación y último intento de restauración, sin mostrar cuerpos ni interpretar ausencia de pendientes como actualidad.

### F09: diagnóstico de recepción, validación e intento anterior

El diagnóstico de solo lectura incorpora recuentos de mensajes recibidos, pendientes, marcados como validados y con estado no reconocido, además de conflictos conservados y progreso de transporte. Solo muestra el siguiente ordinal cuando hay una única secuencia. No incluye fuentes URL, destinatarios, temas, bytes o cuerpos; no consulta red ni abre el gestor de claves. Son registros locales y marcas del ensayo, no una nueva validación criptográfica o prueba de actualidad.

El flujo integrado verifica tres momentos: tras concesión y restauración hay cuatro marcas validadas y último intento completo; tras recibir el corte quedan dos pendientes aunque el último intento de inventario siga completo; tras validar y rechazar el proveedor quedan cero pendientes, intento bloqueado por revocación y una copia anterior en catálogo. El bloqueo previo por pendientes sucede antes de la puerta de inventario y no modifica aquel registro de intento: se presenta cada estado por separado para no confundir el resultado anterior con permiso actual.

Se comprueba que consultar no modifica bytes ni fechas de modificación de las bases existentes. Una prueba adicional verifica que rutas y contenido inesperados no salen en el resumen, que los estados desconocidos no cuentan como validados y que una base ilegible se declara ilegible. Una base ausente sigue siendo desconocida y no se crea. Las lecturas entre almacenes no forman una foto atómica; las marcas locales no autentican una modificación coherente del almacén.

Cuatro pruebas de diagnóstico y cinco del buzón superadas con ResourceWarning como error. La batería completa confirma 100 comprobaciones superadas en 69,172 segundos. Persiste el aviso conocido de deprecación de hio, sin parche a terceros. La siguiente unidad debe revisar los contratos de estos módulos y reducir divergencias entre el resumen del flujo y sus registros antes de extender funcionalidad.

### F09: corte recibido durante una descarga

La revisión del contrato encontró una ventana concreta: el buzón se comprobaba al iniciar, pero recibir un corte sin validarlo durante la descarga podía dejar la concesión anterior en resolver hasta aplicar el catálogo. La puerta de inventario admite ahora una comprobación adicional opcional antes de aplicar; el flujo de buzón repite ahí su precaución sobre pendientes/conflictos. Los consumidores que no usan buzón conservan la comprobación de rol y dirección anterior.

Una sexta prueba del módulo descarga realmente el objeto por HTTP y, justo al recibir sus bytes, hace llegar el corte mediante el servidor de buzón real. El rol nativo todavía conserva la concesión, pero la comprobación final detecta dos pendientes y rechaza aplicar: cero objetos en catálogo e intento registrado como bloqueado con código inbox_pending. Después, otro proceso valida el corte y el intento siguiente se rechaza por proveedor no autorizado. El diagnóstico reconoce ese código sin mostrar contenido. La llegada se coordina mediante instrumentación del punto posterior a la lectura HTTP del objeto; no es una prueba de estrés con escritores simultáneos.

Se han superado seis pruebas del buzón, doce de autorización y cuatro de diagnóstico, todas con ResourceWarning como error. Última batería completa confirmada 100; total previsto 101. Se usan estas 22 comprobaciones pertinentes sin repetir el conjunto completo en este bloque.

La comprobación final y el commit del catálogo siguen perteneciendo a almacenes y operaciones distintos. Se evita el caso instrumentado; no se afirma cierre de toda carrera posible o transacción distribuida. Tampoco se deshace un historial de identidad ya validado al comprobar pruebas públicas. Siguiente revisión propuesta: documentar de forma compacta estas fronteras y el alcance del bloqueo local antes de añadir más variantes de concurrencia.

### F09: estados locales desconocidos no equivalen a validación

La revisión del contrato detectó una omisión: contar solo validated=0 como pendiente dejaba fuera marcas inesperadas. El validador rechaza ahora cualquier marca distinta de cero o uno, sin omitirla, reiniciarla o convertirla en validada. La puerta de entrega exige que todas las entradas estén explícitamente marcadas como uno; una marca desconocida también impide iniciar/aplicar según la precaución del ensayo.

Una séptima prueba integrada restaura primero la publicación autorizada y recibe el corte. Después altera únicamente las marcas locales de las dos entradas de corte, asignándoles un valor desconocido. En procesos nuevos, restaurar se bloquea y validar rechaza el estado. El resolver conserva la concesión anterior, las marcas se mantienen sin reparación automática y la copia pública anterior queda intacta. El diagnóstico muestra dos estados desconocidos y cero pendientes con marca cero: ese cero no significa recepción validada completa.

Se han superado siete pruebas del buzón y cuatro de diagnóstico con ResourceWarning como error. Última batería completa confirmada 100; conjunto previsto actual 102. No se repite la batería completa porque el cambio se limita al módulo de recepción y las comprobaciones pertinentes cubren su flujo y diagnóstico.

No se afirma integridad autenticada de las marcas locales. Un atacante que modifique coherentemente bytes, huellas y estados exige otro modelo de protección del dispositivo; la ruta observada tampoco acredita autoridad. El siguiente bloque debe delimitar el contrato del transporte nativo pendiente y la conservación de metadatos, en vez de acumular nuevas variantes de corrupción sintética.

## 27. F10 — Contrato propuesto para consulta nativa y metadatos

**Estado: contrato preparado; primer paso ejecutado en el apartado siguiente, integración completa pendiente y sin interfaz adoptada.** Se mantiene la revisión fijada de KERIpy y no se instala otra versión. La inspección del código distingue cuatro componentes que F09 no reúne todavía:

| Componente inspeccionado | Contrato observado | Comprobación pendiente |
| --- | --- | --- |
| Poller.eventDo | Crea consulta nativa mbx, recibe eventos SSE con id/name/data y conserva progreso por identidad/fuente/tema | Ejecutarlo con cliente HTTP y servidor reales, sin dobles |
| HttpEnd.on_post | Encola la consulta y prepara QryRpyMailboxIterable para una respuesta SSE | Vincular consulta validada, cue de stream y destinatario correcto |
| Kevery.processQuery, ruta mbx | Consulta identidad conocida y genera cue con pre/src/topics | Separar conocer la identidad de autorizar leer el buzón; ensayo negativo antes de cualquier dato privado |
| MailboxDirector | Recoge bytes de Poller y los entrega al parser; el punto de salida de Poller ya no incluye ordinal/tema | Conservar sobre antes de perder metadatos, sin equiparar cola o cursor a validación |

Estas observaciones proceden del código local de la revisión fijada: [indirecting.py](https://github.com/WebOfTrust/keripy/blob/4ce4cc79e06653f77342be1bf604086b89b1f090/src/keri/app/indirecting.py) y [eventing.py](https://github.com/WebOfTrust/keripy/blob/4ce4cc79e06653f77342be1bf604086b89b1f090/src/keri/core/eventing.py). No se deduce una vulnerabilidad de comentarios o de una función aislada; la validación y el acceso deben comprobarse en la ruta completa. Una consulta firmada tampoco implica por sí sola autorización de lectura.

### Secuencia de ejecución propuesta

1. Un destinatario sintético conocido y un buzón con mensajes públicos; consulta nativa enviada a HttpEnd por HTTP local real. Registrar por separado petición, cue de stream y recepción SSE. No introducir MLS, datos personales o servicio público.
2. Capturar fuente configurada, destinatario, tema, ordinal y bytes en el límite de eventos del cliente, antes de reducir el evento a bytes. Confirmar el sobre durable antes de aceptar progreso de transporte. Instrumentar únicamente el adaptador del ensayo; no parchear dependencias.
3. Terminar el receptor después de recibir, reabrir en otro proceso y validar desde las entradas durables; repetir el corte si la validación se confirmó antes de su marcador. Mantener identificadores de transporte locales a su fuente y tema.
4. Comprobar un rechazo de persistencia y una consulta ajena al destinatario, conservando evidencia del resultado. Si el acceso no se restringe con las reglas existentes, declarar esa brecha y limitar el ensayo a mensajes públicos; no inventar una política de lectura o un directorio común.
5. Solo después decidir si integrar MailboxDirector completo conserva ese contrato. Usar HttpEnd y Poller reales no autoriza a llamar completa a una integración que deja fuera el director o sustituye parte de su planificador.

### Criterio de paso y límites

El resultado debe demostrar consulta y SSE reales, sobre durable con metadatos correspondientes a los bytes recibidos, progreso de transporte separado de validación y recuperación en otro proceso. Debe declarar preconfiguración de URL/identidades, quién conserva medios de firma, dónde se valida la consulta y qué se ha comprobado sobre acceso. Si falla una parte, no se sustituirá por resultados de F05–F09 presentados como una única ejecución.

El siguiente bloque ejecutable es el primer paso, con consulta, cue y SSE reales. No se requiere una decisión de confianza para ensayarlo en datos públicos sintéticos. Autorización privada, descubrimiento, cuotas, resistencia a vigilancia y producción permanecen fuera del criterio. Esta preparación no añade pruebas: última batería completa 100, conjunto previsto 102 tras las ampliaciones focalizadas anteriores.

### F10: primer paso ejecutado — consulta, cue y SSE reales

[keri_native_query.py](laboratorio-identidad/keri_native_query.py) ejecuta una consulta mbx firmada con un destinatario sintético conocido por el controlador del buzón. HttpEnd nativo recibe el POST por HTTP local real. Un adaptador del ensayo ejecuta el parser nativo después de encolar y comparte sus cues con QryRpyMailboxIterable; el servidor emite SSE nativo a través de hio/Falcon. El cliente de esta prueba usa urllib y un lector acotado de las tramas ASCII, no Poller o MailboxDirector.

La prueba comprueba que la consulta genera un cue de stream correspondiente a su SAID, destinatario y tema. Recibe índices cero/uno con exactamente los dos mensajes públicos sintéticos guardados en Mailboxer. Otra consulta desde uno recibe únicamente el segundo mensaje, conservando su ordinal. Los almacenes y conexiones son temporales locales; no se modifica código de terceros. Se corrigió una conversión de bytearray a bytes en el lector del ensayo tras su primera ejecución.

Esta unidad verifica petición, parser/cue y SSE en la misma ejecución. No conserva sobre durable, no valida el texto de aplicación, no prueba autorización de lectura o rechazo de consulta ajena, ni demuestra recuperación entre procesos. La consulta está firmada por construcción, pero no se equipara esa propiedad con autorización privada. La selección inicial de URL e identidades sigue preconfigurada. El criterio completo de F10 permanece pendiente.

Una prueba focalizada superada con ResourceWarning como error. Última batería completa confirmada 100; conjunto previsto 103. Siguiente unidad: unir esta ruta nativa real con recepción durable de metadatos y recuperación, manteniendo explícita la ausencia de Poller/MailboxDirector completos mientras corresponda.

### F10: consulta/SSE nativos con sobre durable y validación sin servidor

Una segunda prueba de keri_native_query.py une consulta mbx prefirmada, HttpEnd/parser/cue y SSE reales con recepción SQLite en un proceso independiente. El destinatario sintético se registra previamente en el controlador; firma la consulta y cierra su almacén antes de recibir. El emisor de creación/concesión/corte ya terminó. La consulta y la configuración de destinatario son material del escenario, sin exportar claves privadas.

El lector confirma cada sobre de fuente URL, destinatario real del ensayo, tema, ordinal, bytes y huella junto al siguiente índice de recepción en una transacción. Se comprueban cuatro entradas pendientes y progreso cuatro, además del cue correspondiente a la consulta. El proceso receptor termina después de recibir y antes de validar. No es el cursor del Poller: es progreso local de la recepción durable, sin afirmar que se haya integrado ese componente.

El servicio SSE y el controlador se cierran antes de continuar. Otro proceso valida las entradas durables y termina después de aplicar el corte, antes de marcarlo; el siguiente repite dos pendientes, conserva revocación y deja cero. Una apertura posterior no procesa entradas adicionales. Antes de validar se comprueba que la identidad emisora no figuraba en el historial de aplicación del receptor. La validación reutiliza el componente del ensayo con destinatario esperado explícito, conservando el caso previo de destinatario fijo por defecto.

Dos pruebas nativas y siete del buzón superadas con ResourceWarning como error. La batería completa confirma 104 comprobaciones superadas en 82,110 segundos, con el aviso conocido de deprecación de hio y sin parche a terceros. La consulta/SSE y la recepción durable ya están reunidas en esta ejecución; todavía faltan el rechazo de persistencia en esta ruta, la consulta ajena al destinatario y la integración Poller/MailboxDirector. No se declara criterio completo F10, autorización privada, descubrimiento o actualidad global.

### F10: consulta de una identidad distinta del destinatario

Una tercera prueba repite la ruta HTTP nativa con un firmante diferente del destinatario del buzón, ambos conocidos por el controlador. No se emite una concesión de lectura entre ellos. En esta configuración, la consulta ajena también obtiene el cue del destinatario y los dos mensajes públicos sintéticos; consultar desde uno devuelve el segundo mensaje. El parser, endpoint y SSE son reales, sin añadir una regla de acceso en el adaptador.

Este resultado es una brecha del criterio de lectura privada del laboratorio, no evidencia de acceso a datos reales o de una vulnerabilidad en todos los despliegues KERIpy. La ruta del ensayo no proporciona aislamiento de lectura por destinatario. Firmar la consulta y conocer ambas identidades no equivalen a demostrar permiso. No se enviarán datos privados a esta ruta; se mantiene limitada a material público sintético y no se presenta como buzón privado.

No se elige una política de acceso, directorio o autoridad nueva para ocultar el resultado. Antes de incorporar contenido privado hará falta definir y ensayar quién puede leer, cómo acredita ese derecho y cómo se revoca, distinguiéndolo del permiso del proveedor para entregar. El ensayo público puede continuar sin esa decisión. Falta todavía el fallo de persistencia de esta ruta y Poller/MailboxDirector completos; F10 no se declara completo.

Tres pruebas focalizadas superadas con ResourceWarning como error. Última batería completa confirmada 104; conjunto previsto actual 105. Siguiente unidad: comprobar rechazo de persistencia durante la recepción nativa durable, conservando este límite de acceso explícito.

### F10: fallo de persistencia durante SSE y reanudación explícita

Una cuarta prueba instala un trigger SQLite exclusivamente en el receptor sintético para abortar el tercer INSERT de la ruta SSE nativa. Un proceso recibe y confirma dos mensajes y termina con el error de persistencia al llegar al corte. Al reabrir hay dos entradas y siguiente ordinal dos: no se ha confirmado recepción del corte ni avanzado sobre él. Se trata de un fallo lógico de transacción real, no disco lleno o corrupción física.

El escenario retira el trigger, vuelve a abrir el almacén efímero del destinatario y firma otra consulta desde dos. Un proceso nuevo recibe por HTTP nativo los dos mensajes restantes y confirma cuatro entradas con progreso cuatro. La elección del índice, la nueva firma y la retirada de la causa son acciones explícitas del escenario, no descubrimiento o recuperación automática del producto. El cliente sigue siendo urllib acotado, no Poller.

Después se detiene el servicio. La validación desde el sobre durable vuelve a terminar después del corte y antes del marcador; los siguientes procesos repiten pendientes y conservan la revocación. Así se comprueban fallo de escritura, nueva consulta y recuperación en la misma ruta nativa, sin sustituirlos por resultados de F07.

Cuatro pruebas focalizadas superadas con ResourceWarning como error. Última batería completa confirmada 104; conjunto previsto 106. El nuevo caso modifica solo este módulo y conserva los anteriores; no se repite la batería completa en este bloque.

La frontera pública de consulta/SSE/recepción/reanudación está ejecutada en ese alcance. F10 no se declara una integración completa: lectura privada no aislada en la configuración probada, Poller/MailboxDirector sin integrar y controles de producción pendientes. Siguiente unidad propuesta: revisar el acoplamiento del cliente nativo a la ruta ya comprobada, conservando sobre antes del cursor y sin imponer una política nueva de lectura.

### F10: Poller y cliente HTTP reales con sobre anterior al cursor

Una quinta prueba ejecuta Poller con su planificador y cliente HTTP nativos contra la ruta HttpEnd/parser/cue/SSE real. El destinatario conoce previamente al controlador y valida su dirección firmada. El adaptador del ensayo envuelve la fábrica de clientes, que sigue creando el cliente y su doer reales; únicamente sustituye el contenedor de eventos compartido por cliente y parser HTTP. No se sustituye la red por una respuesta prefabricada ni se modifica la dependencia instalada.

Al retirar un evento del cliente, el adaptador conserva primero fuente local, destinatario, tema, ordinal, bytes y huella junto al siguiente índice en SQLite. Solo después devuelve el evento a Poller, que conserva su cola de bytes y su progreso nativo habituales. La ejecución comprueba dos entradas durables todavía sin validar, los mismos dos mensajes en la cola de Poller y su último ordinal nativo uno. El progreso local siguiente dos y el último recibido nativo uno son convenciones distintas y se presentan como tales.

Los mensajes son texto público sintético, sin validación de aplicación. El controlador denominado witness en el parámetro nativo es un único servicio del escenario; no se adopta una política de testigos o umbral. El contexto inicial y la URL están preconfigurados. Esta prueba no termina el proceso receptor ni demuestra recuperación del Poller completo; esa propiedad no se toma prestada del caso con cliente urllib. MailboxDirector sigue sin integrar, igual que autorización privada de lectura.

Cinco pruebas focalizadas superadas con ResourceWarning como error. La batería completa confirma 107 comprobaciones superadas en 76,436 segundos, con el aviso conocido de deprecación de hio y sin parche a terceros. El siguiente bloque debe ensayar la persistencia al interrumpir este cliente nativo concreto, sin ampliar todavía la política de lectura o afirmar privacidad.
