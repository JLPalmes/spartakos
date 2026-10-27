---
title: Spartakos — Balance de identidad y preparación del traslado
lang: es-ES
license: CC-BY-SA-4.0
date: 2026-10-27
version: 0.4
status: Evaluación de laboratorio; sin elección de arquitectura de producción
---

# Qué permite afirmar el laboratorio de identidad

## 1. Conclusión y decisión provisional

KERIpy sigue siendo una candidata razonable para investigar el control de identidad. Las pruebas actuales no permiten elegirla como infraestructura de producción ni afirmar que Spartakos ya permite cambiar de proveedor. El ensayo de rol y dirección demuestra autorización de proveedores en la vista del observador, pero no exclusividad ni autoridad única para escribir el perfil. La siguiente unidad debe estudiar orden, vigencia y mensajes incompatibles antes de copiar un perfil entre dos alojamientos.

El [laboratorio](laboratorio-identidad/README.md) contiene 38 comprobaciones ejecutadas con KERIpy 1.3.6 fijada por commit. Incluye una reproducción de un comportamiento defectuoso, H01: que esa reproducción pase no significa que el defecto esté corregido. Las 109 pruebas del simulador social son otra batería y no añaden garantías distribuidas.

**Ninguno de los quince casos E ni de los diez casos T se considera completado.** Algunas pruebas proporcionan evidencia parcial útil, que se detalla a continuación. La comparación de [nueve familias de identidad](ARQUITECTURA-04-CANDIDATOS-DE-IDENTIDAD.md) sigue vigente como investigación; este balance no acredita superioridad global de KERI.

## 2. Garantías y límites observados

| Aspecto | Evidencia ejecutada | Lo que todavía no demuestra |
| --- | --- | --- |
| Identidad estable | Rotación y reapertura conservan identificador | Resolución pública de ubicación, continuidad de referencias sociales o disponibilidad global |
| Control de claves | Rechazo de firmas ajenas, clave no comprometida y clave anterior tras rotación | Recuperación sin medios previos, delegación de servicios o seguridad del dispositivo |
| Respaldo por testigos | Verificador externo exige recibos suficientes; duplicados e impostores no completan el umbral | Que dos de tres sea una política adecuada para Spartakos o que los operadores sean independientes |
| Continuidad local | Procesos HTTP separados, caída de testigo, persistencia y reinicio del verificador | Pérdida de máquina, caída durante transacción, censura de red o coste real de operación |
| Pendientes | Cola persistida, recibo posterior por HTTP y aceptación sin reenviar evento | Descubrimiento automático de destino, cancelación o ejecución única de publicaciones programadas |
| Contradicciones | Dos verificadores detectan la otra rama cuando la reciben, incluso tras reiniciar | Detección durante aislamiento, elección automática de una rama o convergencia |
| Caducidad | Sale la entrada temporal; el estado aceptado se conserva | Que el evento quede revocado o que una contradicción haya desaparecido |
| Evidencia almacenada | Bytes y firma de la rama contradictoria sobreviven a reapertura y caducidad de su cola | Registro duradero de alertas, conservación indefinida o archivo resistente a manipulación |
| Servicio de recibos | H01 reproducido; adaptador experimental exige evento exacto aceptado | Corrección oficial, seguridad concurrente o aprobación del servicio completo |

Referencias ejecutables: [claves y persistencia](laboratorio-identidad/keri_smoke.py), [recibos y discrepancias](laboratorio-identidad/keri_witnesses.py), [HTTP y adaptador](laboratorio-identidad/keri_http.py), [recuperación combinada](laboratorio-identidad/keri_pending.py) y [caducidad y contraste persistido](laboratorio-identidad/keri_lifecycle.py). El [inventario](laboratorio-identidad/entorno-verificado.json) fija entorno y resultados; la [revisión de H01](laboratorio-identidad/revision-h01.json) distingue inspección estática posterior de ejecución real.

## 3. Cobertura del programa estructural E

«Parcial» significa evidencia de una pieza, no aceptación del caso completo. «Sin ejecutar» significa que no existe una integración probada para ese caso; no es un fallo observado.

| Caso | Estado | Evidencia parcial y trabajo necesario |
| --- | --- | --- |
| E01 — Identidades y dispositivos | Parcial | Identidad, claves y rotación probadas; faltan registro y revocación de dispositivos, ubicación y separación efectiva de alojamiento |
| E02 — Entrega de publicaciones | Sin ejecutar | Repetir eventos KERI no equivale a entregar publicaciones entre A y B con versiones y deduplicación |
| E03 — Grupo cifrado | Sin ejecutar | No se ha instalado ni probado MLS ni su enlace con las identidades |
| E04 — Cambios con cliente desconectado | Sin ejecutar | Las caídas de testigos no prueban permisos comunitarios ni sincronización del cliente |
| E05 — Revocación de dispositivo | Sin ejecutar | Invalidar una clave de identidad no prueba exclusión de mensajes de una época MLS posterior |
| E06 — Nuevo miembro sin pasado | Sin ejecutar | No hay ensayo de claves y archivo comunitarios |
| E07 — Persistencia de clientes | Parcial | Estado de identidad y verificador reabiertos; faltan cliente, dispositivos y estado criptográfico de grupos |
| E08 — Traslado sin origen | Sin ejecutar | No existen dos alojamientos de perfil ni un cambio de destino validado |
| E09 — Traslado interrumpido | Parcial | Rotación rechaza clave anterior y escrow se recupera; falta autoridad de servicios A/B, interrupción del traslado y rechazo de operaciones del origen |
| E10 — Pérdida de autoridad común | Sin ejecutar | Caer un testigo no equivale a perder una autoridad de resolución; consulta y nuevos cambios no se han probado en ese escenario |
| E11 — Recuperación de cuenta | Sin ejecutar | Rotación con medios disponibles no es recuperación tras pérdida de dispositivo o claves |
| E12 — Archivo cifrado | Sin ejecutar | La reapertura de bases no prueba cifrado frente al proveedor ni restauración sin clave |
| E13 — Búsqueda y denuncia privada | Sin ejecutar | No se han inspeccionado flujos distribuidos de esas funciones |
| E14 — Entrega o credenciales alteradas | Parcial | Firmas falsas y contradicciones probadas; faltan credenciales sociales, nodo de entrega y análisis de metadatos |
| E15 — Navegador | Sin ejecutar | Python local no acredita distribución del cliente, almacenamiento web ni múltiples pestañas |

El [programa E](ENSAYO-01-COMPONENTES-Y-VALIDACION.md) conserva sus condiciones de aceptación. No se modifica para hacer coincidir sus criterios con lo que ya ha resultado sencillo de probar.

## 4. Cobertura del traslado individual T

| Caso | Estado | Evidencia y brecha |
| --- | --- | --- |
| T01 — Línea base | Sin ejecutar | Falta inventario de perfil y objetos en A con referencias desde un observador social |
| T02 — Traslado cooperante | Sin ejecutar | Falta cambio de destino autorizado, restauración en B y resolución del observador |
| T03 — Origen indisponible | Sin ejecutar | Detener un testigo no demuestra traslado con A apagado y respaldo independiente |
| T04 — Copia sin autoridad | Parcial | Firmas ajenas rechazadas; no se ha intentado activar en B un inventario íntegro sin control de identidad |
| T05 — Interrupción y repetición | Parcial | Escrow persiste y se completa; faltan etapas persistidas del traslado y deduplicación de objetos y envíos |
| T06 — Autoridad anterior | Parcial | Clave anterior deja de autorizar tras rotación; falta revocar autoridad de servicio sin entregar a A la clave del titular |
| T07 — Autoridad principal caída | Sin ejecutar | No se ha demostrado resolución y cambio de ubicación con una autoridad común ausente |
| T08 — Privacidad | Sin ejecutar | No hay traslado de borradores y permisos comunitarios; el aislamiento de los fixtures no prueba privacidad del producto |
| T09 — Retiradas y consumidos | Sin ejecutar | No se han restaurado marcadores y pendientes consumidos entre alojamientos |
| T10 — Incompletitud y corrupción | Sin ejecutar | Los hashes del entorno no son un inventario firmado de perfil ni validación de una restauración incompleta |

Se mantienen las exclusiones del [ensayo T](ENSAYO-02-TRASLADO-INDIVIDUAL.md): cambiar de proveedor dentro de Spartakos no es importar historial y contactos de redes externas. Esa migración de entrada continúa siendo un requisito distinto y pendiente.

## 5. Obstáculos antes de los dos alojamientos

### Autoridad del titular y del servicio

Debe demostrarse qué operación existente autoriza un destino y cómo se revoca la capacidad del anterior. El alojamiento no debe poseer por defecto la clave que controla la identidad. Rotar esa clave en una prueba no basta para demostrar separación de responsabilidades.

Se investigarán las declaraciones de rol, autorización y localización de servicio que ya proporciona KERIpy, fijando sus API y sus reglas. No se dará autoridad a una URL por aparecer en un archivo firmado sin comprobar el alcance, la vigencia y la resolución exigidos por el componente. Si sus mecanismos no permiten cubrir el contrato, se declara la brecha; no se inventa consenso para ocultarla.

### Vigencia y contradicciones

El observador debe distinguir una autorización anterior, una vigente en su estado validado y una discrepancia. Una firma válida aislada no prueba que la autorización siga vigente. Durante una partición puede no ser posible establecer actualidad; el ensayo deberá registrar esa limitación, no llamar definitivo a un estado antiguo.

La resolución de contradicciones y la aceptación de dependencias comunes son decisiones de arquitectura y gobierno. Aún no hace falta decidirlas para probar detección y negativa a presentar éxito ante evidencia contradictoria.

### Recibos, archivo y operación

H01 permanece abierto en la implementación fijada. El adaptador permite un ensayo local acotado; no aprueba el servicio para producción. Siguen pendientes concurrencia, configuraciones completas y revisión independiente. La firma de distribución de libsodium no se verificó; la consulta OSV sin avisos para 34 versiones PyPI no sustituye una auditoría.

Un archivo íntegro no concede control de identidad. Los medios de control y el inventario restaurable deben estar disponibles antes de apagar A. La restauración debe conservar IDs, versiones y retiradas; las programaciones se mantienen inactivas. No se pretende recuperar datos que solo existían en el origen perdido.

Los testigos del laboratorio comparten máquina y administrador. No hay medidas suficientes para afirmar costes asumibles, incentivos de voluntariado o independencia institucional. Esa evaluación necesita despliegues medidos, documentación de operación y escenarios de mantenimiento.

## 6. Próximas unidades y condiciones de paso

| Orden | Unidad concreta | Condición de paso | Si no se cumple |
| --- | --- | --- | --- |
| 1 | Ensayo de autorización y resolución de destino con API existentes | Titular autoriza B; tercero verifica alcance; destino anterior no se presenta como vigente tras conocer el cambio; no hace falta la clave del titular en A | Registrar incompatibilidad o límite de integración; no construir un directorio propio para simular éxito |
| 2 | Estados antiguos y contradictorios en resolución | Operaciones obsoletas se rechazan o se señala conflicto; una vista sin actualización no se presenta como confirmación reciente | Mantener explícito el estado no confirmado y revisar la integración |
| 3 | Traslado cooperante de perfil mínimo público A → B | Misma identidad, IDs y referencias desde un observador que no se traslada; copia sin autoridad rechazada | No conectar el flujo al cliente social |
| 4 | Repetir con A apagado antes de solicitar cambio | Respaldo y control independientes permiten el flujo; faltas de datos y control informadas | No afirmar independencia del alojamiento |
| 5 | Interrupciones, origen que vuelve y archivo privado | Reanudación sin duplicados, autoridad anterior controlada, retiradas conservadas y permisos no ampliados | Mantener el resultado acotado y declarar los casos T pendientes |

Estas unidades ordenan la investigación; no son nuevas características aprobadas. El punto inmediato es **autorizar y resolver el destino**, no copiar archivos de perfil. Si solo funciona con un servicio común imprescindible, esa dependencia se presenta al usuario como decisión crítica antes de adoptarla para Spartakos.

## 7. Condiciones para una decisión posterior

Para aprobar una candidata para el prototipo distribuido deberán existir resultados reproducibles sobre destino, autoridad anterior, persistencia, conflictos y privacidad en su alcance. Para producción harán falta además revisión de seguridad, recuperación, navegador, operación y costes, y una política de confianza explícita. Las pruebas funcionales del simulador no cubren esos requisitos.

Por ahora se puede continuar autónomamente con la investigación y los ensayos reversibles de destino. No se adopta un directorio obligatorio, umbral de testigos, procedimiento de recuperación ni árbitro de conflictos. Tampoco se requiere que el usuario configure esos detalles para poder usar la futura red.

## 8. Actualización tras ensayar roles y direcciones

Cinco pruebas adicionales con API existentes elevan el laboratorio a 27 comprobaciones. La dirección anunciada por el proveedor y la autorización firmada por el titular se verifican por separado. A no consigue autorizarse como si fuese el titular ni sustituir la dirección de B; una revocación recibida persiste y el reenvío de la autorización anterior no la anula en el escenario ordenado probado. Los proveedores no reciben las claves del titular.

La cobertura sigue siendo parcial: no cambia el estado completo de ningún E/T. La primera unidad de la tabla anterior queda **parcialmente ejecutada**. No se ha demostrado su condición de destino vigente con autoridad de escritura: el rol `agent` admite A y B a la vez, y un observador que no recibe la revocación sigue resolviendo A. Autorización de endpoint y exclusividad de escritor son propiedades distintas.

Siguiente paso ajustado: ensayar fechas iguales, orden inverso de entrega y actualización de claves con la política nativa de aceptación. Después precisar el alcance del servicio frente al contrato. No iniciar una copia de perfiles presentándola como traslado con autoridad resuelta, ni convertir por cuenta propia un rol múltiple en una regla de consenso.

## 9. Resultado de orden y vigencia; precisión del criterio

Cuatro pruebas adicionales elevan el laboratorio a 31 comprobaciones. Con fechas distintas y la misma época de firma, el escenario de concesión/revocación converge al entregar los mensajes en ambos órdenes. Con igual fecha y época, los observadores conservan el primer valor aceptado y no convergen al reabrir. Una declaración en una época de claves posterior prevalece en el caso probado incluso con fecha menor; rotar sin nueva declaración no revoca el rol existente.

No se adopta la respuesta de rol como registro exclusivo de alojamiento. Tampoco se exige que Spartakos tenga un único proveedor: la multiplicidad es compatible con servicios separados y réplicas. Las referencias anteriores a autoridad única de escritura deben entenderse como autoridad y revisión de cada objeto, no como prohibición de varios servidores. Lo pendiente es delimitar qué puede modificar cada servicio y cómo se valida el estado del perfil sin confiar en un proveedor por el mero hecho de alojarlo.

La siguiente unidad investigará la vinculación de una revisión del perfil mínimo con eventos ordenados del mecanismo existente, separando autorización, integridad, entrega y actualidad de la vista. El ensayo deberá rechazar una copia sin autoridad y registrar ramas incompatibles o ausencia de actualización sin atribuirse consenso. No se diseña criptografía nueva ni se da por cumplido el traslado con un hash firmado aislado.

## 10. Ensayo del perfil público vinculado a eventos

Siete pruebas adicionales verifican el enlace experimental entre bytes del perfil, ID del titular y huella incluida en eventos KERI aceptados. Las copias mantienen autoridad y referencia; la modificación sin anclaje o firma válida no se acepta. Una revisión anterior queda identificada como histórica después de conocer una posterior. Rotar conserva el ID de perfil y la clave anterior no puede autorizar otra revisión. El enlace semántico y el formato mínimo pertenecen al arnés de aplicación; no se atribuyen a KERI como protocolo nativo de perfil.

El resultado no completa E02, E08 ni T01–T03: no existen servicios A/B de perfil en este ensayo. Sigue pendiente persistir el enlace y el estado duradero de conflicto antes de presentar un traslado. La cabeza local del perfil no demuestra actualidad global ni ausencia de bifurcaciones; tampoco concede permiso automático para una acción sensible. Las pruebas de vista atrasada y ramas firmadas conservan ese límite.

Siguiente unidad: persistencia de revisiones y señalización de conflicto del perfil; después entrega desde dos servicios locales, separada del control del titular, con origen apagado. No se amplían permisos comunitarios ni se trasladan datos privados en ese primer flujo.
