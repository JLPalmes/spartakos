---
title: Laboratorio aislado de identidad KERI
lang: es-ES
license: CC-BY-SA-4.0
date: 2026-10-27
---

# Laboratorio aislado de identidad

Primer ensayo ejecutado con KERIpy 1.3.6, revisión `4ce4cc79e06653f77342be1bf604086b89b1f090`. No adopta todavía KERI como arquitectura de Spartakos. No utiliza ni modifica los datos del simulador.

## Resultado comprobado

Cinco pruebas de integración con la biblioteca real, todas superadas:

1. Crear estado, reabrirlo y rotar en tres procesos independientes, conservando identificador y usando la nueva clave tras otra reapertura.
2. Rechazar una firma incorrecta sin avanzar el estado; aceptar después la operación legítima.
3. Rechazar una rotación hacia una clave no comprometida previamente.
4. Rechazar la clave anterior después de rotar; aceptar la vigente.
5. Rechazar la repetición de un evento ya aceptado sin avanzar el estado.

Se generan claves sintéticas aleatorias y directorios temporales privados. El programa no muestra claves privadas ni abre servidores. La configuración de KERIpy se proporciona explícitamente para que también su fichero de configuración quede dentro del directorio de ensayo. Cada ejecución elimina únicamente su estado sintético temporal al terminar.

## Entorno y reproducción

Entorno observado: macOS arm64, Python 3.14.7, KERIpy 1.3.6, hio 0.6.19 y libsodium 1.0.22. [Inventario de versiones, fuentes y hashes observados](entorno-verificado.json). Las [dependencias fijadas](requirements.txt) recogen esta resolución concreta; no son una garantía universal ni un bloqueo completo de herramientas de compilación.

Preparación realizada enteramente en un directorio temporal: descargar el archivo de KERIpy de la revisión indicada, crear un entorno virtual con `python3 -m venv`, instalar las dependencias fijadas y el código extraído mediante el Python de ese entorno. La instalación usa `pip --isolated`, caché propia y las restricciones de requirements.txt. No sustituir silenciosamente la revisión por la rama principal.

No había libsodium disponible para la biblioteca Python. Se compiló el archivo oficial indicado en el inventario, con `./configure --prefix=RUTA_PRIVADA`, `make`, `make check` y `make install`. Sus **101 pruebas propias** pasaron. La variable `DYLD_LIBRARY_PATH` se establece solo para el proceso del ensayo, apuntando a `RUTA_PRIVADA/lib`; no se cambia la configuración global. Véanse las [instrucciones oficiales](https://doc.libsodium.org/installation).

Con ese entorno preparado, ejecutar desde la raíz del proyecto, sustituyendo las rutas por las del entorno privado:

```sh
DYLD_LIBRARY_PATH="/ruta/privada/native/lib" PYTHONPYCACHEPREFIX="/ruta/privada/pycache" /ruta/privada/venv/bin/python laboratorio-identidad/keri_smoke.py
/ruta/privada/venv/bin/python -m pip check
```

El inventario incluye SHA-256 observados de las descargas. La firma de distribución de libsodium **no se verificó**; un hash observado junto con una descarga HTTPS no sustituye esa comprobación. No se ha completado una auditoría de vulnerabilidades de las dependencias. KERIpy emite avisos de sintaxis de cadenas con Python 3.14; estas pruebas no demuestran compatibilidad completa de toda la biblioteca. No se distribuyen entornos, binarios, fuentes ajenas ni claves con este laboratorio.

## Alcance pendiente

El primer bloque no prueba testigos; la ampliación siguiente comprueba recibos y verificadores aislados. La ampliación HTTP posterior prueba el servicio de recibos con procesos locales separados. Siguen pendientes nodos completos, observadores operativos, particiones de red entre equipos, recuperación tras perder claves, costes y traslado de perfil. No se han completado los casos E01–E15 o T01–T10. Estas cinco pruebas no se suman a las 109 pruebas funcionales del simulador, que permanece sin cambios.

La ampliación de transporte y sus límites se documentan al final de este archivo. No se fija todavía una política de recuperación ni un umbral propio.

## Ampliación: recibos y discrepancias — 27 de octubre

[Ensayo ejecutable de recibos](keri_witnesses.py): **siete pruebas adicionales superadas**, doce en total en el laboratorio de identidad. Se usa un ejemplo sintético de tres testigos y dos firmas necesarias; no es una política adoptada para Spartakos. Los recibos se generan mediante la biblioteca y se entregan directamente a sus verificadores, sin sockets ni servidores. Omitir un recibo comprueba la condición criptográfica de aceptación; no demuestra una caída de red ni mide disponibilidad real.

| Caso | Resultado observado |
| --- | --- |
| Dos recibos válidos de tres | El verificador externo acepta el evento aunque falte el tercero |
| Un solo recibo | No acepta el evento; al reenviarlo explícitamente con dos, lo acepta |
| Recibo duplicado | No cuenta como dos testigos |
| Firma de un impostor en lugar del segundo testigo | No satisface el umbral |
| Nueva interacción con recibos insuficientes | Conserva el estado anterior; acepta después con recibos suficientes |
| Dos eventos contradictorios en la misma secuencia | Kevery señala LikelyDuplicitousError y conserva la rama previamente aceptada |
| Dos verificadores aislados reciben ramas distintas, cada una con dos firmas | Cada uno acepta inicialmente su rama; detecta la contradicción al recibir la otra, sin sustituir automáticamente su estado |

El último caso usa un titular que firma ambas ramas y un testigo compartido que también firma ambas. No demuestra una ruptura con testigos honestos: comprueba el comportamiento ante ese supuesto adversarial. Tampoco demuestra detección espontánea mientras los verificadores siguen aislados. Una mayoría de recibos **no debe presentarse como consenso automático ni como elección de la historia legítima**.

Para reproducir, usar el mismo entorno del primer bloque y sustituir `keri_smoke.py` por `keri_witnesses.py`. Se proporciona la cola de avisos requerida por la API de bajo nivel para los eventos sin suficientes recibos. Las pruebas esperan excepciones concretas de la biblioteca; no interpretan cualquier fallo como una protección correcta.

Consecuencia provisional de diseño: distinguir estado creado, estado suficientemente respaldado para terceros y estado con conflicto detectado. Antes de presentar una identidad como trasladable deben ensayarse contraste entre fuentes, persistencia y reanudación de eventos pendientes, transporte, y tratamiento explícito de discrepancias. Esta consecuencia es una propuesta técnica, no una nueva característica ya implementada en el cliente.

## Ampliación HTTP: interrupción, persistencia y rotación

[Ensayo HTTP](keri_http.py): tres pruebas adicionales ejecutadas, **15 comprobaciones en esta etapa**. Dos escenarios prueban continuidad; el tercero reproduce un comportamiento problemático del endpoint. Que la reproducción pase no significa que el servicio cumpla una garantía de seguridad.

Se usa ReceiptEnd de KERIpy, Falcon y el servidor HTTP hio de referencia. Cada testigo vive en un proceso con su propio almacén persistente temporal. Solo escucha en `127.0.0.1`, en puertos libres. No se arranca el conjunto completo setupWitness, que por defecto escucha en todas las interfaces e incorpora servicios fuera del alcance. Los procesos se cierran al terminar; no queda un servicio permanente. No se modifica ninguna biblioteca ajena.

Los dos escenarios de continuidad comprueban:

1. Obtener recibos de tres testigos y validar la creación de identidad.
2. Detener uno y validar una interacción con los otros dos.
3. Detener otro mediante cierre normal o terminación abrupta, según el escenario; comprobar conexión rechazada y que un recibo no basta para avanzar al verificador.
4. Reiniciar ese testigo sobre su almacén anterior, conservando identidad; consultar y verificar su recibo del evento anterior.
5. Reenviar explícitamente el evento pendiente, obtener el segundo recibo y avanzar.
6. Rotar conservando el identificador, obtener recibos HTTP y verificar la nueva clave.
7. Rechazar la clave anterior y recibos de otro evento; aceptar la siguiente interacción con la nueva clave y recibos propios.

Es recuperación tras un proceso terminado después de responder, no caída durante una escritura ni pérdida del disco. El coordinador de prueba gestiona el reenvío; no se atribuye reanudación automática a Receiptor. Los dos verificadores del bloque de discrepancias tampoco son aún observadores operativos desplegados.

### Hallazgo H01: un recibo no equivale a aceptación

En la revisión fijada, tras conocer una identidad, ReceiptEnd puede responder 200 y firmar el recibo de una interacción enviada con firma de autor inválida. El evento no aparece en el historial consultable del testigo: su consulta devuelve 404. El verificador completo rechaza el evento por firma inválida y conserva el estado anterior. La tercera prueba reproduce ambas cosas con claves sintéticas.

Esto **impide aprobar este endpoint tal cual para producción**. No demuestra suplantación del titular ni una vulnerabilidad de todo KERI. Se requiere analizar el flujo completo de validación antes de decidir entre otra revisión, otro componente o una corrección. No se ha comunicado el hallazgo a terceros ni se ha publicado este bloque. No se debe convertir el recibo o el código HTTP en indicador suficiente de validez en el futuro cliente.

Reproducción: usar el mismo entorno del bloque inicial y ejecutar `laboratorio-identidad/keri_http.py`. El laboratorio necesita permiso para abrir sockets locales. La biblioteca interpreta el puerto cero como el puerto 80; el ensayo selecciona explícitamente puertos efímeros y reintenta si la asignación falla.

### Consulta de dependencias

El 27 de octubre se consultó la API pública OSV para las **34 versiones PyPI inventariadas**; no devolvió avisos asociados. Esto no es una auditoría ni descarta vulnerabilidades; excluye herramientas de compilación, entorno y bibliotecas nativas. Tampoco invalida H01. La firma del archivo de libsodium sigue sin verificar.

Próximos bloques técnicos: comprobar las colas pendientes tras reiniciar también el coordinador; analizar el límite de validación de H01; preparar contraste persistido entre fuentes. El traslado completo continúa pendiente y no se conecta este laboratorio al simulador.

## Cola pendiente tras reiniciar el verificador

[Ensayo de escrow persistido](keri_pending.py): una comprobación adicional, **16 en total**. Se ejecutan tres procesos independientes sobre la misma base sintética: el primero guarda el evento sin recibos suficientes y termina; el segundo reabre la base, comprueba que sigue pendiente, recibe únicamente el recibo faltante y procesa las colas oficiales; el tercero verifica el estado final y que no quedan pendientes. No se reenvía el evento ni se copian claves privadas entre procesos.

La reanudación requiere invocar las tareas oficiales de procesamiento de recibos y de eventos pendientes. No es una garantía de recuperación autónoma de un servicio que todavía no existe. Esta prueba entrega el recibo a la API directamente; la prueba HTTP anterior valida separadamente el transporte. La ampliación combinada siguiente une el reinicio del verificador con recibos HTTP. Siguen pendientes caducidad, cortes durante escritura y contraste de fuentes discrepantes después de reiniciar.

Para ejecutar el conjunto en el entorno privado preparado, desde la raíz del proyecto:

```sh
DYLD_LIBRARY_PATH="/ruta/privada/native/lib" PYTHONPYCACHEPREFIX="/ruta/privada/pycache" /ruta/privada/venv/bin/python -m unittest discover -s laboratorio-identidad -p 'keri_*.py' -v
```

Las 16 comprobaciones incluyen la reproducción de H01. No deben describirse como 16 garantías de seguridad superadas. El simulador social sigue sin cambios y conserva su batería independiente de 109 pruebas.

## H01: revisión posterior y mitigación experimental

El 27 de octubre se leyó el código oficial de la revisión `bd5a0bb7a7b105fcd3951f6dda838dc89d3b5281`, cuyo manifiesto declara 2.1.0-dev1. En ReceiptEnd.on_post sigue visible el flujo parsear → comprobar identidad conocida → firmar recibo, sin exigir en ese punto la coincidencia del evento con la secuencia aceptada. Es inspección estática: no se instaló esa revisión y no se afirma haber reproducido H01 en ella. No se ha acreditado una corrección oficial. Las fuentes inmutables y hashes figuran en [la revisión registrada](revision-h01.json).

Se ensaya localmente AcceptedHistoryHab, un adaptador explícito en keri_http.py que delega en KERIpy y, antes de firmar, exige dos condiciones: el digest aceptado para esa secuencia coincide con el solicitado y los bytes del evento almacenado coinciden exactamente. Si no se cumplen devuelve HTTP 409 y no llama a la firma del recibo. No implementa criptografía ni sustituye la validación de la biblioteca. El servicio original continúa disponible en el ensayo para reproducir H01; el modo protegido se activa solo con `--guarded` en el proceso de laboratorio.

Dos pruebas adicionales, **18 comprobaciones en total**, verifican:

- Rechazo de firma inválida en un evento nuevo, rama contradictoria firmada por el titular y enlace incorrecto al evento anterior; conservación del recibo aceptado y repetición legítima.
- Escenario completo de caída abrupta, reinicio persistido y rotación usando el servicio con adaptador.

La mitigación supera estos casos concretos, pero no supone aprobación para producción. Quedan por estudiar concurrencia entre comprobación y firma, configuración completa del servicio, delegación, cambios de testigos, eventos pendientes y compatibilidad con otros transportes. El servidor del ensayo atiende secuencialmente; no demuestra seguridad frente a escrituras concurrentes. H01 permanece abierto en la implementación fijada. No se ha modificado código ajeno ni contactado con terceros.

Conclusión provisional: mantener KERI como candidata de laboratorio, conservar la reproducción original y continuar con el ensayo combinado de transporte, cola persistida y reinicio del coordinador. No se conecta todavía este adaptador al simulador ni se cambia la política de confianza de Spartakos.

## Ensayo combinado: HTTP y verificador persistente

Añadida una prueba completa en keri_pending.py, **19 comprobaciones en total**. Mantiene tres servicios de recibos en procesos separados con el adaptador experimental activado y una base persistente propia del verificador. Todos los datos son sintéticos y temporales.

1. Los testigos reciben la creación de identidad por HTTP; dos reciben también la interacción siguiente.
2. Un primer proceso verificador recibe solo un recibo de esa interacción, la deja en la cola persistida y termina.
3. Se termina abruptamente el segundo testigo. Un nuevo proceso verificador intenta consultarlo por HTTP: la conexión falla y conserva el estado anterior y el evento pendiente.
4. Se reinicia el testigo sobre su almacén anterior. Se conserva su identidad y se comunica al ensayo su nuevo puerto local.
5. Otro proceso verificador reabre la misma base y consulta por HTTP el recibo del evento ya guardado. No recibe de nuevo el evento ni dispone de las claves del autor o del testigo. Procesa las colas oficiales y acepta el evento al completar los recibos necesarios.
6. Otros procesos verificadores confirman el estado aceptado y la ausencia del pendiente.

El ensayo compone las piezas que antes se verificaban por separado. No demuestra descubrimiento automático del nuevo puerto: el coordinador de pruebas actualiza explícitamente esa dirección. El verificador se reinicia tras un cierre normal; la terminación abrupta corresponde al testigo y ocurre después de haber respondido. No se prueban pérdida de disco, caída durante transacción, caducidad del pendiente ni traslado entre proveedores. La mitigación de H01 sigue siendo experimental.

Siguiente bloque técnico: comprobar caducidad de pendientes y contraste persistido de historiales discrepantes. Las pruebas de laboratorio no obligan todavía a elegir umbrales, operadores o mecanismos de recuperación de cuentas para Spartakos.

## Caducidad y contradicciones después de reiniciar

[Ensayo de ciclo de vida](keri_lifecycle.py): tres comprobaciones nuevas, **22 comprobaciones de laboratorio en total**, incluida la reproducción de H01. Los escenarios usan bases temporales propias y procesos nuevos para cada fase. El reloj se sustituye únicamente durante llamadas de prueba; no se cambia el reloj del equipo ni las fechas de datos del usuario.

### Pendientes de recibos

La revisión fijada define TimeoutPWE en 3600 segundos. Se comprueba que la entrada sigue pendiente un segundo antes y exactamente en ese límite; al superarlo un segundo sale de la cola, sin avanzar el estado aceptado. Los bytes del evento permanecen almacenados en este ensayo. Un reenvío explícito posterior del mismo evento con recibos suficientes puede aceptarse y el resultado persiste tras otro reinicio.

Es un tiempo de retención de la biblioteca, no una decisión adoptada para Spartakos. La salida de una cola no revoca un evento firmado ni implementa la cancelación de una publicación o de una operación de traslado.

### Contradicciones persistidas

Después de aceptar una rama y recibir otra contradictoria, Kevery señala la discrepancia y conserva la rama previa. La entrada de posible duplicidad, los bytes de la otra rama y su firma válida del titular sobreviven a la reapertura. Al superar TimeoutLDE, también de 3600 segundos en esta revisión, la entrada sale de la cola, pero los bytes y la firma siguen disponibles tras otra reapertura. El estado aceptado no cambia. No se demuestra conservación indefinida ni una política de archivo.

Otro escenario comienza con dos bases independientes que aceptan ramas diferentes. Después de cerrar sus procesos, cada una recibe la otra rama en un proceso nuevo. Ambas detectan la contradicción, conservan su historia previa y mantienen la evidencia al volver a abrirse. La entrega entre fuentes está controlada por el ensayo y usa la API: no se prueban descubrimiento de observadores ni sincronización de red automática. No hay convergencia automática demostrada.

### Consecuencias propuestas

- Un registro duradero de conflictos deberá distinguirse de una cola temporal de reintentos. Una cola vacía no puede presentarse como ausencia de conflictos.
- La cancelación necesita una regla explícita de autoridad y estado; no puede deducirse de que haya caducado una cola.
- Antes de escoger KERI para producción, deben concretarse retención de evidencia, contraste entre fuentes y comportamiento ante conflicto, además de resolver los límites de H01.

Son propuestas derivadas de los resultados; no se han añadido estados al cliente social ni se ha aprobado una política de consenso. Próximo bloque: elaborar el balance de garantías demostradas y pendientes frente a los ensayos E y T, para decidir qué falta antes del traslado de identidad entre alojamientos. No se requieren decisiones del usuario para completar ese balance documental.

El [balance de garantías frente a E/T](../BALANCE-01-IDENTIDAD-Y-TRASLADO.md) registra la cobertura parcial y las condiciones antes del primer traslado. Ningún caso E/T completo se da por superado por estas 22 comprobaciones.

## Autorización de proveedores y resolución de direcciones

[Ensayo de destinos](keri_destinations.py): cinco pruebas nuevas, **27 comprobaciones de laboratorio en total**. Se usan identidades de titular, proveedores A/B y observadores en almacenes separados. La biblioteca genera y verifica los mensajes existentes `/loc/scheme` y `/end/role/add` o `/end/role/cut`. El rol estudiado es `agent`; no se crea un rol de alojamiento propio ni se le atribuyen permisos de publicación de Spartakos.

| Prueba | Resultado observado |
| --- | --- |
| Dirección sin autorización | La dirección anunciada por A queda conocida, pero no aparece como destino autorizado del titular hasta que este concede el rol |
| Revocar A y autorizar B | El observador actualizado resuelve B; tras cerrar y reabrir sus almacenes, repetir la autorización antigua de A no la restablece |
| A suplanta al titular o a B | A no logra concederse el rol, revocar a B en nombre del titular ni sustituir la dirección firmada de B |
| Añadir B sin revocar A | Ambos proveedores quedan autorizados: la operación no sustituye automáticamente al anterior |
| Observador sin actualización | Conserva A mientras otro observador que recibió el cambio resuelve B |

El titular firma sus autorizaciones desde su almacén propio. Los proveedores no reciben sus claves y sus almacenes no registran la identidad del titular como identidad propia. Las direcciones son valores ficticios de bucle local: no se abren servicios de perfil ni se comprueba la conectividad. Los mensajes se entregan directamente al parser; esta prueba no demuestra descubrimiento, distribución de revocaciones, traslado ni resistencia a la censura.

El orden de respuestas de KERIpy utiliza su política existente de aceptación de datos disponibles. En esta prueba se usan firmas de la misma época y fechas ordenadas, con microsegundos en el formato requerido por Dater. No se deduce una secuencia global independiente del reloj ni exclusión mutua de destinos. La reapertura del observador se prueba cerrando y abriendo los almacenes en el mismo proceso; los escenarios anteriores cubren por separado otros reinicios en procesos nuevos.

Consecuencia: hay un mecanismo existente para atribuir roles y direcciones sin entregar las claves del titular al proveedor. **No hay todavía una demostración de autoridad única de escritura del perfil.** Un `agent` autorizado no es por ese solo hecho el alojamiento vigente ni puede modificar publicaciones. Revocar un rol en la vista de un observador no elimina datos ni capacidad de actuar ante observadores desactualizados.

Antes de trasladar perfil, el siguiente ensayo debe estudiar orden y vigencia de esas declaraciones —incluidos mensajes contradictorios con igual fecha y cambios de claves— y delimitar si el mecanismo permite cumplir el contrato de destino. Si no permite acreditarlo, se conserva como autorización de servicios y se registra la brecha de continuidad, sin escoger arbitrariamente un ganador ni crear consenso propio.

## Orden y época de firma de las declaraciones

Cuatro pruebas adicionales en keri_destinations.py: **31 comprobaciones del laboratorio en total**, nueve dedicadas a destinos. Se mantienen el componente y las claves sintéticas; no hay despliegue ni nueva regla de resolución.

| Escenario | Resultado observado |
| --- | --- |
| Conceder con fecha anterior y revocar con fecha posterior, entregando en ambos órdenes | Los dos observadores terminan con el rol revocado |
| Conceder y revocar con la misma fecha y época de firma, entregando en órdenes opuestos | Cada observador conserva lo primero que aceptó; la discrepancia continúa al reabrir y repetir los mensajes |
| Conceder con una clave anterior y fecha mayor; revocar con la nueva época y fecha menor | La declaración de la nueva época prevalece en el escenario probado; repetir la anterior no recupera el rol |
| Rotar claves sin una declaración nueva de rol | La autorización existente del proveedor permanece |

Estos resultados corresponden a la política nativa de aceptación de respuestas firmadas. No equivalen a consenso ni a confirmación de actualidad global. La prueba de fechas iguales observa los registros de autorización; no certifica que no haya trazas o mensajes conservados en otras tablas. No se añade una elección local de ganador que pueda ocultar el desacuerdo entre observadores.

### Separar proveedor y autor del perfil

Que el rol agent admita varios proveedores no es un defecto: Spartakos contempla múltiples servicios y réplicas. La propiedad que falta es la relación explícita entre control del titular, permisos de cada servicio y versión aceptada del perfil. No debe confundirse «misma autoridad válida sobre una revisión» con «solo puede existir un proveedor».

Las declaraciones de rol y dirección son una pieza útil para descubrir servicios autorizados en una vista conocida. Por sí solas no se adoptan como registro exclusivo y globalmente ordenado de alojamiento ni como permiso de editar el perfil. Ningún servidor adquiere las claves del titular por aparecer en estas declaraciones.

Próxima unidad propuesta: definir el alcance de autorización del perfil mínimo con el contrato ya existente y evaluar cómo vincular una revisión de perfil a eventos ordenados del componente, dejando entrega y almacenamiento como funciones separadas. Deben distinguirse integridad, firma, orden validado, ausencia de actualizaciones conocidas y conflicto. Si se necesita una regla nueva de confianza o resolución de ramas, se registrará como decisión pendiente, sin presentarla como propiedad nativa de KERI.

## Perfil público y autoridad de revisión

[Ensayo de perfil](keri_profiles.py): siete pruebas nuevas, **38 comprobaciones en total**. El titular firma eventos de interacción KERI que incluyen la huella de unos bytes de perfil público sintético. El formato `spartakos_profile_lab_v1` es un enlace de aplicación experimental del arnés, no una capacidad de perfil nativa de KERI ni un formato de producción aprobado. No se implementan nuevas firmas, criptografía ni reglas de consenso.

La biblioteca verifica eventos y evolución de claves. El arnés interpreta el perfil mínimo —tipo, ID derivado del titular y nombre mostrado— y contrasta su huella con anclajes del historial aceptado localmente. Se usa una serialización fija del fixture, sin afirmar canonicalización universal. La lectura presupone una base local alimentada por el verificador: importar una base ofrecida por un proveedor sin validar su historia no está autorizado por este ensayo.

| Escenario | Resultado observado |
| --- | --- |
| Copiar el mismo cuerpo a A y B | Conserva ID de perfil y evento de autorización; el lugar de la copia no concede autoridad |
| Alterar el cuerpo y calcular otra huella | Se rechaza al no existir anclaje aceptado del titular para esos bytes |
| Firmar el supuesto cambio con clave de proveedor ajena | El verificador rechaza el evento; el cambio no pasa a ser una revisión aceptada |
| Entregar una revisión anterior tras conocer otra posterior | Sigue verificándose como histórica, pero no como cabeza del perfil en esa vista |
| Anclar un cuerpo que declara otra identidad | El enlace de aplicación rechaza el cuerpo aunque el evento KERI esté aceptado |
| Rotar y actualizar el perfil | Conserva el ID del perfil; la clave anterior no autoriza la actualización y la nueva sí |
| Vista aislada o ramas incompatibles | La cabeza local no prueba actualidad global; al intercambiar ramas firmadas aparece la discrepancia y no hay convergencia automática |

Las dos últimas situaciones se verifican en pruebas separadas: una compara vista atrasada/actualizada y otra dos ramas contradictorias; las alteraciones y firmas ajenas se agrupan en una prueba. El total de siete cuenta funciones de prueba, no filas de esta tabla.

La inspección devuelve `head_in_this_view` y `globally_current: null`. El segundo valor indica ausencia de prueba de actualidad, no un error recuperado ni una propiedad inferida del primero. La cabeza local puede existir aun con conflicto conocido; **no es permiso para publicar, trasladar o confirmar un cambio**. El arnés no incorpora todavía un registro duradero de bloqueo por conflicto, ya señalado como pendiente en el ensayo de caducidad.

A y B en esta unidad son copias de bytes dentro de la prueba, no servidores ejecutados. Los verificadores usan bases sintéticas temporales; la persistencia de este enlace de perfil no se ha probado entre procesos. No se transportan contactos, publicaciones, borradores ni datos comunitarios, no hay cifrado de perfil privado y no se prueba recuperación sin medios previos.

Resultado: se ha demostrado una vinculación acotada entre cuerpo público, titular y revisión en una historia validada. **No se ha ejecutado el traslado de un perfil entre alojamientos.** Siguiente unidad: persistir el estado de revisión y conflicto del perfil, después ejecutar A/B como servicios locales de entrega con el origen apagado y con el titular y el verificador separados. La prueba deberá dejar explícito qué actualización falta y rechazar una copia sin anclaje autorizado.

## Persistencia del perfil y registro local de conflicto

[Ensayo de estado de perfil](keri_profile_state.py): tres pruebas adicionales, **41 comprobaciones de laboratorio en total**. El cuerpo público se conserva en un almacén SQLite local del arnés y se contrasta contra el historial KERI persistido al abrir otro proceso verificador. No se confía en una columna de versión recibida del proveedor para acreditar la revisión.

El registro de conflictos está separado de las colas temporales de KERI. El ensayo verifica dos ramas de interacción independientes contra la misma creación de identidad mediante verificadores nativos de la biblioteca, antes de guardar evidencia pública sintética. Después comprueba que:

1. Cuerpo y vínculo con el evento sobreviven al cambio de proceso.
2. El conflicto registrado bloquea la confirmación local, incluso tras otro reinicio, caducidad controlada de la cola de posibles contradicciones y posterior reapertura.
3. Una firma de otra identidad no crea una entrada de conflicto verificado en ese registro.

El arnés usa dos interacciones de secuencia 1, sin testigos, delegación ni rotación; rechaza escenarios fuera de ese alcance. No se afirma que el verificador de evidencia de esta prueba sea una solución general para cualquier historial. La firma ajena rechazada tampoco demuestra resistencia completa a denegación de servicio.

`confirmation_blocked` indica bloqueo por un conflicto ya registrado. Su valor falso **no autoriza ninguna acción**: la actualidad global continúa sin probarse y no existe todavía una puerta de activación del traslado. El registro no elige una rama ni ofrece desbloqueo automático o procedimiento de recurso. La evidencia conservada contiene eventos y firmas públicos sintéticos, nunca claves privadas.

La prueba registra el conflicto antes de procesar la caducidad. Las transacciones de KERI y SQLite no son una única transacción: no se han probado cortes entre detección y registro, corrupción de esos almacenes, sincronización con otros observadores ni recuperación del registro perdido. Resolver ese intervalo y la recuperación de evidencia es requisito de una integración posterior; no se presenta este arnés como protección de producción.

Próxima unidad propuesta: entrega del perfil desde dos servicios HTTP locales, con titular y verificador independientes, origen apagado y copia sin autoridad rechazada. El flujo será un ensayo de recuperación de entrega; no afirmará transferencia completa de autoridad ni actualidad global por el mero hecho de responder desde B.

## Entrega HTTP desde B con A apagado

[Ensayo de entrega de perfil](keri_profile_http.py): cinco pruebas nuevas, **46 comprobaciones de laboratorio en total**. A y B son procesos HTTP de solo lectura, con directorios separados y acceso limitado a `/profile` y `/proof`. Solo escuchan en bucle local y se cierran al terminar. No permiten listar el directorio ni recibir escrituras; no contienen claves privadas del titular.

El coordinador prepara antes del corte el perfil público sintético y los eventos firmados. El verificador usa su propia base persistente y recibe la identidad esperada por un canal separado del proveedor. Cuando parte sin historia, valida con KERIpy los eventos entregados por HTTP y contrasta el cuerpo con su anclaje. Una historia firmada válida se acepta como historia conocida, **sin certificar que sea completa o globalmente actual**.

| Prueba | Resultado observado |
| --- | --- |
| Apagar A y recuperar desde B | Se comprueba conexión fallida a A y lectura desde B con el mismo ID y revisión; funciona con verificador reabierto y también con uno nuevo que valida la historia |
| B modifica el cuerpo | Se rechaza específicamente por ausencia de anclaje aceptado para esos bytes; al restaurar el cuerpo correcto puede verificarse |
| B entrega cuerpo correcto sin historia validada | Un verificador nuevo lo rechaza; después lo acepta al validar los eventos firmados disponibles |
| B sustituye al titular por otra identidad con firmas válidas | Se rechaza específicamente por no coincidir con la identidad esperada independiente |
| B entrega una revisión antigua | El observador que ya conoce la posterior la clasifica como histórica, sin confundirla con la cabeza de su vista |

Los rechazos exigen el error de validación previsto, no simplemente que el proceso falle. Las respuestas se limitan a 1 MiB en este arnés, sin proxies ni redirecciones; no es un dimensionado de producto. El servicio estándar HTTP de Python usado aquí es únicamente un medio de transporte de laboratorio, sin despliegue público ni evaluación de seguridad de un servidor de producción.

### Qué se ha conseguido y qué falta

Se demuestra recuperación de **entrega** desde una copia preparada antes del corte, preservando la referencia verificable del perfil. No existe una solicitud de traslado, cambio autorizado de ubicación, descubrimiento automático de B ni revocación de una capacidad de escritura de A. A y B son almacenes de solo lectura: no se puede presentar que A «perdió permiso de editar» cuando nunca recibió ese permiso.

Las direcciones de A/B las proporciona el coordinador; la autorización de roles se probó separadamente y aún no está unida a estas peticiones HTTP. El origen permanece apagado durante la recuperación. No se prueba su retorno hostil, pérdida de todas las copias, actualización después del corte, traslado de publicaciones o datos privados ni recuperación de la clave del titular. Las pruebas de conflicto persistido son otra suite; esta entrega HTTP no recibe ni registra nuevas ramas contradictorias por sí misma.

El campo `globally_current` permanece desconocido. `accepted_copy` solo indica cuerpo coincidente con un anclaje de una historia validada en la vista local; no es autorización de traslado ni confirmación de actualidad. Los esquemas experimentales de perfil no se convierten en formatos de producción por superar este ensayo.

Próxima unidad: unir resolución de servicios autorizados con la entrega HTTP, sin aceptar una URL anunciada por el proveedor como autorización del titular. Después comprobar actualizaciones con origen apagado y retorno del origen con copia anterior. No se modifica el simulador social.

## Resolución autorizada y entrega compuestas

[Ensayo de entrega autorizada](keri_authorized_delivery.py): tres pruebas nuevas, **49 comprobaciones en total**. El observador valida primero el rol agent concedido por el titular y obtiene después la dirección anunciada y firmada por el proveedor. Solo entonces consulta `/profile` y contrasta el cuerpo contra su historial KERI validado y su registro local de perfil.

1. Una dirección conocida sin autorización del titular se rechaza antes de efectuar HTTP. La prueba comprueba que la función de transporte no se llama. Tras recibir la autorización, se entrega y verifica el perfil.
2. Con A autorizado y después apagado, se observa fallo real de conexión. El titular revoca A y autoriza B mediante mensajes nativos entregados al observador. Este rechaza A por autorización y obtiene desde la dirección validada de B el mismo perfil. Al reabrir su almacén se conserva el resultado.
3. Con A apagado, el titular firma una nueva revisión, B recibe el cuerpo y el observador recibe el evento firmado. La revisión nueva se verifica desde B. A vuelve con su copia anterior y anuncia su nuevo puerto mediante una declaración propia válida: eso no restaura su rol revocado. La lectura autorizada lo rechaza; una lectura directa de diagnóstico muestra que su cuerpo antiguo es histórico en la vista actualizada.

Los servicios HTTP son de solo lectura y no poseen la clave del titular. El coordinador conserva esa clave sintética y prepara las actualizaciones; no existe una API de escritura ni se entrega autoridad de edición a B. El rol agent se interpreta como proveedor de entrega **solo para este ensayo de aplicación**; no se aprueba como mapa definitivo de permisos de Spartakos.

Los mensajes de creación de identidad, autorización, revocación, dirección y revisión se distribuyen mediante el coordinador directamente al parser. La URL usada para la petición ya se toma del estado verificado, pero no se ha demostrado descubrimiento ni propagación automática de esas declaraciones. No se ofrece una garantía de actualidad global, exclusividad de proveedor, resolución de ramas o autenticación TLS de servidores. Los valores de identidad y el estado previo esperado se mantienen separados de las respuestas HTTP.

La persistencia de esta composición se comprueba cerrando y reabriendo los almacenes del observador en el mismo proceso. Los ensayos anteriores de perfiles y entrega prueban por separado procesos nuevos. No se afirma todavía una prueba conjunta con reinicio completo del cliente durante el cambio de proveedores.

Resultado: autorización de entrega y ubicación se componen sin dar claves del titular al proveedor, y se conserva una referencia verificable al volver el origen con contenido antiguo en una vista ya actualizada. Sigue siendo una integración local acotada, no traslado completo: faltan publicaciones, inventario, relaciones, estado privado, interrupciones durante el cambio y prueba de dependencia de la autoridad de identidad. Ningún E/T se da por completo.

Siguiente unidad propuesta: interrumpir y reanudar esa composición con procesos verificadores nuevos, incluyendo cambios recibidos parcialmente. No se inventará un cambio atómico de roles: habrá que mostrar qué vista queda al recibir solo la revocación, solo la autorización o ninguna de ambas.

## Cambios parciales e interrupción del verificador

[Ensayo de entrega parcial](keri_partial_delivery.py): cuatro pruebas nuevas, **53 comprobaciones de laboratorio en total**. Cada escenario inicia servicios HTTP A/B separados y ejecuta cinco procesos verificadores sucesivos sobre los mismos almacenes: inicializar, recibir cambios parciales, verificar la vista parcial sin modificarla, completar cambios y comprobar el resultado. Cada proceso valida autorización antes de acceder al perfil.

| Cambios recibidos en la fase parcial | Vista comprobada y persistida |
| --- | --- |
| Solo revocación de A | Ningún proveedor autorizado; las lecturas de A y B se rechazan por autorización |
| Solo autorización de B | A y B autorizados; ambas entregas se verifican como el mismo perfil |
| Ninguno | A sigue autorizado y B no; no se infiere que la vista esté actualizada |
| Autorización de B y terminación abrupta posterior del verificador | El siguiente proceso conserva A y B antes de recibir la revocación faltante |

Después se entregan ambas declaraciones firmadas dos veces deliberadamente. En los cuatro casos se alcanza y persiste B autorizado y A revocado, conservando una única copia del cuerpo en el almacén del arnés. Esto no prueba deduplicación general de publicaciones o notificaciones: solo la persistencia del cuerpo de perfil indexado por huella y la repetición de declaraciones de rol.

La salida abrupta usa terminación inmediata del proceso después de los commits y las lecturas, sin ejecutar cierres normales; el nuevo proceso comprueba primero la vista parcial, antes de completarla. No se interrumpe una transacción en curso ni se simula pérdida de alimentación, corrupción o disco lleno. Los servidores permanecen disponibles en este bloque para distinguir la falta de autorización de la falta de conectividad; su caída se comprueba en los ensayos anteriores.

Las declaraciones son mensajes públicos sintéticos prefirmados por el coordinador; ningún proceso verificador dispone de la clave del titular. Las direcciones provienen de declaraciones verificadas. El coordinador sigue controlando la distribución y el momento de reanudación: no existe sincronización automática ni una transacción distribuida que abarque revocar A y autorizar B.

La multiplicidad temporal no concede a los proveedores permiso de editar. La ausencia temporal de proveedor tampoco elimina el perfil conservado. `globally_current` continúa desconocido en todas las vistas. Ningún estado parcial se presenta como traslado confirmado ni como error de consenso resuelto.

Próximo bloque propuesto: consolidar las condiciones de aceptación del ensayo público mínimo y el tratamiento explícito de estado incompleto, antes de ampliar a objetos y referencias sociales. No se cambia la interfaz del simulador ni se da por completo un caso E/T.
