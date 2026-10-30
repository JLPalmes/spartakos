---
title: Spartakos — Balance de identidad y preparación del traslado
lang: es-ES
license: CC-BY-SA-4.0
date: 2026-10-27
updated: 2026-10-30
version: "0.43"
status: Balance consolidado del laboratorio; sin elección de arquitectura de producción
---

# Balance actual de identidad, entrega y traslado

## 1. Conclusión y alcance

El laboratorio ya ejecuta una integración pública acotada: control de claves, perfiles y objetos verificables, autorización de entrega y restauración desde copias. **No demuestra todavía un traslado social completo, independencia de toda autoridad común ni protección de producción. KERI sigue siendo candidata.**

La batería completa confirmada reúne **107 comprobaciones**. Incluye la reproducción de H01 y no equivale a garantías de seguridad aprobadas. Las 109 pruebas del simulador social son otra batería; no se han añadido capacidades distribuidas a ese cliente. **Ninguno de los quince casos E ni los diez T se considera completado.** La cobertura parcial actual se presenta abajo.

Este documento sustituye sus tablas iniciales, anteriores a los ensayos de inventario. La secuencia de cambios y autorizaciones se conserva en [el resumen acumulado](REVISION-PARA-EL-LUNES.md). El detalle reproducible y los límites por suite están en [el laboratorio](laboratorio-identidad/README.md) y [el informe de inventario público](ENSAYO-03-INVENTARIO-PUBLICO.md).

## 2. Qué está demostrado en escenarios locales

| Pieza | Evidencia ejecutada | Límite decisivo |
| --- | --- | --- |
| Control de identidad | Persistencia, rotación con ID estable y rechazo de clave ajena o anterior | No recuperación sin medios, seguridad de dispositivo o independencia global |
| Recibos de testigos | Umbral sintético, rechazo de duplicados/impostores, procesos HTTP y caída/reinicio | No política de confianza aprobada, operadores independientes o consenso |
| Historial contradictorio | Detección al recibir otra rama; evidencia conservada; registro local de conflicto | No detección durante aislamiento, arbitraje o convergencia automática |
| Rol y dirección | Titular autoriza/revoca; proveedor firma dirección; proveedor no suplanta al titular | agent es múltiple; vistas no actualizadas conservan autorizaciones anteriores; igual fecha puede divergir |
| Perfil y revisión | Huella anclada a eventos validados; copia, alteración, historial y rotación | Semántica de aplicación experimental; cabeza local no significa actualidad global |
| Entrega pública | A/B HTTP, origen apagado; F09 añade concesión, dirección y corte por buzón con restauración real | Un proveedor/tema en F09; URL inicial y preparación coordinadas; sin descubrimiento independiente |
| Inventario y referencias | Inventario autorizado, versiones, referencia guardada, ausencia/alteración, retiradas y rechazo de reescritura/retroceso | No todos los tipos sociales, relaciones ni datos privados; entrada básica sin puerta de acceso |
| Composición autorizada | Rol/dirección y conflicto conocido antes de red y antes de aplicar; reintento en procesos nuevos | Composición con un objeto; no todas las variantes multiobjeto reunidas en un mismo flujo |
| Persistencia y fallos | Recepción durable, marcas de validación, catálogo e intento separados; repetición tras terminación; corte durante descarga | Sin transacción global; cortes durante escrituras, corrupción y fallos de disco pendientes |
| Diagnóstico | Solo lectura de registros, incógnitas explícitas y ausencia de cuerpos en salida | No revalidación criptográfica, permiso, actualidad o foto atómica entre almacenes |

Las pruebas operan con datos sintéticos, procesos y directorios separados en el mismo equipo. No prueban caída del equipo completo ni independencia de administradores. La autorización para entregar no da claves del titular al proveedor ni permiso para editar el perfil. Múltiples proveedores son compatibles con Spartakos.

## 3. Cobertura actual del programa E

«Parcial» identifica evidencia útil de piezas del caso; no cambia su condición de aceptación. «Sin ejecutar» se refiere a la integración estructural definida, aunque existan funciones locales del simulador con nombres parecidos.

| Caso | Estado | Evidencia actual y brecha restante |
| --- | --- | --- |
| E01 — Identidad y dispositivos | Parcial | Identidad, claves, roles y direcciones; faltan registro/revocación de dispositivos y recuperación integrada |
| E02 — Publicación A/B y repetición | Parcial | Objetos públicos, IDs, revisiones, referencias y repetición de restauración; falta entrega social integrada y deduplicación de efectos |
| E03 — Grupo cifrado | Sin ejecutar | MLS y vínculo con identidades sin integrar |
| E04 — Cliente desconectado y permisos | Sin ejecutar | Caída de proveedor/testigo no prueba sincronización comunitaria y permisos del cliente |
| E05 — Dispositivo expulsado | Sin ejecutar | Rotación de identidad no demuestra exclusión de mensajes de época MLS posterior |
| E06 — Nuevo miembro sin archivo previo | Sin ejecutar | Sin ensayo criptográfico de incorporación y archivo comunitario |
| E07 — Persistencia de clientes | Parcial | Historias, perfiles, inventario y registros reabiertos; falta estado de cliente/dispositivos y de cifrado de grupos |
| E08 — Traslado sin origen | Parcial | F01 reúne inventario público, referencias y autorización de entrega con A apagado; faltan alcance social completo, contextos privados y distribución independiente |
| E09 — Traslado interrumpido y autoridad anterior | Parcial | Estados parciales, revocación, conflictos y procesos nuevos; no traslado completo de todos los objetos/efectos ni escritura delegada |
| E10 — Autoridad común ausente | Sin ejecutar | Pérdida de testigo o servidor de datos no equivale a perder una autoridad común de resolución y poder seguir cambiando destino |
| E11 — Recuperación de cuenta | Sin ejecutar | No se recuperan claves/dispositivos perdidos mediante un procedimiento definido |
| E12 — Archivo cifrado | Sin ejecutar | Catálogo público y SQLite no prueban privacidad frente al proveedor o restauración sin clave |
| E13 — Búsqueda y denuncia privada | Sin ejecutar | Sin flujos distribuidos ni análisis de exposición de esas funciones |
| E14 — Credenciales y entrega alteradas | Parcial | Firmas falsas, objetos alterados, identidad inesperada y ramas; faltan credenciales sociales y evaluación de metadatos |
| E15 — Navegador | Sin ejecutar | Ensayos Python no acreditan distribución de cliente, múltiples pestañas o almacenamiento web seguro |

No se rebajan los requisitos del [programa E](ENSAYO-01-COMPONENTES-Y-VALIDACION.md) para hacerlos coincidir con los casos que ya pasan.

## 4. Cobertura actual del traslado T

| Caso | Estado | Evidencia actual y brecha restante |
| --- | --- | --- |
| T01 — Línea base | Parcial | Perfil/objetos públicos, inventario y referencia guardada; faltan relaciones declaradas y todos los contextos/audiencias del contrato |
| T02 — Traslado cooperante | Parcial | F01 integra inventario multiobjeto y observador; faltan otras entidades/audiencias sociales y distribución sin coordinador |
| T03 — Origen indisponible | Parcial | F01 integra A apagado, B y control del titular separado, con actualización posterior al corte; no recuperación sin respaldo/medios ni alcance privado |
| T04 — Copia sin autoridad | Parcial | Identidad falsa, cuerpo sin anclaje y proveedor sin rol rechazados; no activación integral de cuenta/servicios en B |
| T05 — Interrupción y repetición | Parcial | Estados persistidos, procesos nuevos y fallos antes/después de aplicar; faltan etapas completas de traslado y efectos sociales/programados |
| T06 — Autoridad anterior | Parcial | Clave anterior rechazada, rol revocado y retorno de A no restaura permiso en la vista actualizada; escritura delegada y observadores desactualizados no resueltos |
| T07 — Autoridad principal caída | Sin ejecutar | Consulta y cambio de ubicación con autoridad común desaparecida no demostrados |
| T08 — Privacidad | Sin ejecutar | Sin transporte de borradores, claves y permisos comunitarios; fixtures aislados no prueban esa privacidad |
| T09 — Retiradas y consumidos | Parcial | Retirada y revisiones públicas no resucitan en restauración; faltan borradores consumidos, avisos, ediciones y programaciones |
| T10 — Datos faltantes/corruptos | Parcial | Objeto ausente/alterado, inventario no autorizado y rechazo persistido; no cobertura completa de formatos, recursos o recuperación |

Los [casos T](ENSAYO-02-TRASLADO-INDIVIDUAL.md) siguen siendo el contrato del ensayo. F01 y F09 aportan evidencia pública integrada parcial, sin completar privacidad, referencias sociales completas o independencia de autoridad común. La migración de historial y contactos desde redes externas es un requisito distinto, todavía no ensayado aquí.

## 5. Integración pública prioritaria ejecutada en su alcance

**Un único flujo público que reúna las piezas existentes**, en vez de añadir más variantes de cada pieza por separado:

1. Titular con medios de control separados de A/B, servicios de entrega y un observador con referencias guardadas antes del cambio.
2. Inventario multiobjeto de perfil, publicaciones, versiones y retirada, con autoridad validada. Las referencias del observador no se cambian para apuntar a B.
3. Apagar A antes de solicitar el cambio de proveedor de entrega; recibir las declaraciones firmadas de autorización/dirección y recuperar desde B a través de la puerta autorizada.
4. Emitir una actualización del inventario después del corte, no limitarse a servir una actualización fabricada antes de apagar A. Comprobar cuerpo, versión, referencia histórica y retirada en la nueva vista.
5. Reabrir el verificador en otro proceso, repetir sin duplicar y volver a A con copia antigua, sin restablecer autorización ni resucitar contenido.
6. Registrar de forma separada catálogo, recepción, último intento, conflicto y falta de prueba de actualidad. Un diagnóstico no sustituye una validación.

**Condición de paso del bloque:** el informe debe mostrar esos hechos en la misma ejecución con datos sintéticos y direcciones obtenidas del estado autorizado. El coordinador puede distribuir mensajes, pero se declara. Si falla, se registra el fallo y no se sustituye por resultados de suites independientes. Este bloque no altera el formato del simulador ni publica una API estable.

**Resultado actual:** F01 ejecuta esta secuencia acotada con inventario público, autorización y referencia en la misma prueba. [Informe](ENSAYO-03-INVENTARIO-PUBLICO.md). La condición de paso de este bloque se considera demostrada en ese alcance; no equivale a completar los E/T sociales ni sus variantes de fallo. F02–F09 han ampliado el transporte de declaraciones, la recepción durable y su integración con la entrega pública, con las fronteras que se resumen a continuación.

## 6. Brechas que no debe ocultar ese éxito local

- Distribución y descubrimiento independientes: recibir una autorización por el coordinador no demuestra que un contacto real se actualice sin configuración.
- Conflictos y confianza: las ramas conocidas pueden bloquearse, pero no existe arbitraje o convergencia general. La política de confianza requiere decisión explícita antes de adoptarse.
- Atomicidad y recuperación: resolución, historia KERI, catálogo y registros siguen separados. No se han probado cortes dentro de transacciones, pérdida de evidencia, disco lleno o corrupción general.
- H01: el endpoint de recibos fijado conserva un comportamiento no aprobado; el adaptador es experimental y no una corrección oficial verificada. No se aprueba su uso público.
- Dependencias: firma de distribución nativa pendiente; consulta de avisos PyPI sin incidencias no equivale a auditoría. No se actualizarán componentes silenciosamente para ocultar fallos.
- Privacidad: faltan MLS, credenciales de grupos, revocación de dispositivos y archivo cifrado. Los roles de lectura/comentario/publicación no nacen automáticamente de la membresía criptográfica.
- Experiencia y operación: faltan navegador, móvil, recuperación comprensible, distribución confiable del cliente y mediciones de coste para voluntarios. El prototipo social local no cubre esas garantías.

No se decide todavía proveedor obligatorio, directorio común, umbral de testigos o mecanismo de recuperación. Si una integración solo funciona aceptando una dependencia común imprescindible, debe presentarse como decisión crítica, no como ajuste oculto.

## 7. Flujo público actual y contratos

F09 une en una ejecución local la recepción por HTTP, persistencia, validación y restauración pública. El titular y el proveedor sintéticos firman creación, dirección, concesión y corte; sus almacenes se cierran antes del consumo. El servidor de buzón no recibe sus claves. Una publicación restaurada antes del corte conserva sus bytes después de revocar al proveedor.

| Etapa | Registro o evidencia | Lo que permite afirmar | Frontera pendiente |
| --- | --- | --- | --- |
| Recibir por HTTP | Sobre de fuente local, destinatario, tema, ordinal, bytes y huella | Esos bytes se han recibido desde la ruta observada | La URL y el ordinal no acreditan autoridad o actualidad |
| Confirmar recepción | Sobre y siguiente ordinal en una transacción SQLite | Hay una entrada durable para validar después | No garantiza durabilidad ante fallo físico ni integridad autenticada del disco |
| Validar | Parser e historial nativos; marca local posterior | La creación/respuesta del escenario ha sido aceptada en esa vista | Historial nativo y marca SQLite no son una transacción conjunta |
| Repetir tras terminación | Corte pendiente validado otra vez sin restablecer concesión | La repetición conserva el resultado en estos eventos | Sin efectos sociales exactamente una vez |
| Comprobar entrega | Resolver de la misma vista, dirección validada y ausencia de pendientes/conflictos del ensayo | Se puede iniciar la restauración conforme a los registros locales comprobados | Bloqueo conservador para una fuente; no política general de toda la red |
| Aplicar catálogo | Revisión de rol/dirección y precaución del buzón antes del commit | El corte recibido en el punto instrumentado impide aplicar | Existe ventana entre última comprobación y commit; no atomicidad global |
| Diagnosticar | Lecturas de solo lectura separadas | Distingue recepción, marcas locales, intento anterior y copia guardada | No revalida firmas, autorización o actualidad; no foto atómica |

Un intento anterior completo puede coexistir con un corte recibido pendiente. Después de validarlo, un intento nuevo puede quedar bloqueado y la copia pública anterior seguir en catálogo. Estos estados no se reducen a un único indicador de «traslado correcto».

## 8. Qué aportan los ensayos de transporte

| Ensayo | Resultado relevante | Límite que conserva |
| --- | --- | --- |
| F02 — Introducción OOBI | Transporta historia, rol y dirección por HTTP nativo | Volver a consultar no entrega por sí mismo el corte probado; no sincroniza revocaciones |
| F03 — Entrada nativa de respuestas | Concesión/corte firmados cambian el estado al validar; firma ajena rechazada | Un 204 confirma cola en RAM; perderla puede exigir reenvío |
| F04 — Buzón nativo | Mensajes prefirmados sobreviven al emisor y otros procesos los validan | Almacenamiento local con índices elegidos por coordinador |
| F05 — Lector HTTP y cursor | Repetición ante terminación; rechazo de firma ajena/hueco; silencio obsoleto no revoca | Adaptación finita, sin MailboxDirector; rechazar puede bloquear un corte posterior |
| F06 — Cursor del Poller | Progreso nativo puede persistir tras encolar sin haber validado | Generador real y base real con transporte sustituido por dobles; no fallo completo de MailboxDirector demostrado |
| F07 — Entrada durable propuesta | Persistir antes del cursor y repetir tras validación; INSERT abortado no salta corte | Una fuente/tema, transporte sustituido; no fallo físico de disco |
| F08 — HTTP y sobre durable | Validación posterior sin servidor; rechazo de alteración y conservación de conflicto | Fuente/tema acotados; huella local no autentica todo el almacén |
| F09 — Entrega integrada | Dirección/concesión por buzón permiten descarga real; corte bloquea nuevos intentos sin borrar copia | Un objeto/proveedor/tema; no traslado social, descubrimiento o actualidad global |

El detalle reproducible, las terminaciones instrumentadas y los dobles de transporte se mantienen en el [informe de inventario](ENSAYO-03-INVENTARIO-PUBLICO.md). El balance no convierte resultados de piezas distintas en una prueba conjunta que no se haya ejecutado.

F10 ya reúne consulta mbx prefirmada, HttpEnd/parser/cue y SSE reales con sobre durable en otro proceso. Tras detener el servidor se valida y se repite el corte antes de su marcador, conservando revocación. El cliente es un lector urllib acotado; progreso de recepción local, sin Poller/MailboxDirector, consulta ajena o fallo de persistencia de esta ruta todavía probados.

## 9. Bloqueo local y conflictos: precaución experimental

El flujo de un único buzón se detiene ante entradas pendientes o una contradicción conocida de posición. Conserva los bytes originales y la evidencia contradictoria sin elegir una rama ni atribuir culpa. La precaución se comprueba al iniciar y de nuevo antes de aplicar catálogo. Si impide recibir un corte válido posterior, el ensayo muestra ese bloqueo; no lo oculta bajo un descarte automático.

Esto no autoriza a cualquier fuente a paralizar toda la cuenta o la red. Extenderlo a varias fuentes exige separar alcance, procedencia observada, validación y efectos; no se adopta todavía orden global, equivalencia de cursores, cuarentena o arbitraje. Una decisión de confianza que resulte necesaria se presentará expresamente.

La introducción positiva, un cursor avanzado, una cola vacía, la ausencia de conflictos conocidos y un intento previo completo no demuestran actualidad global. Ni el diagnóstico ni una huella local sustituyen comprobación criptográfica de contenido o protección del dispositivo.

## 10. Próximos bloques y decisiones abiertas

1. Conservar el contrato revisado del buzón de una fuente: las marcas desconocidas se rechazan sin promover permisos; bytes o tema alterados y contradicciones conocidas bloquean el ensayo. La recuperación explícita y protección autenticada del almacén siguen pendientes.
2. Completar F10 tras reunir consulta, cue/SSE reales y recepción durable con recuperación entre procesos. La consulta ajena de otra identidad conocida obtiene los mensajes públicos en la configuración ensayada: esta ruta no acredita aislamiento de lectura. El INSERT abortado durante SSE conserva progreso dos y otra consulta firmada explícita recupera el corte; Poller y su cliente HTTP reales ya conservan el sobre antes del cursor mediante un adaptador experimental; su recuperación tras terminar y MailboxDirector completo siguen pendientes. La lectura privada continúa sin aislamiento acreditado.
3. Preparar el ensayo de grupos privados antes de instalar componentes: verificar fuentes, versión, licencia y dependencias; separar membresía criptográfica de permisos de leer, comentar o publicar. KERI no sustituye MLS.
4. Tratar recuperación, vigilancia/censura, incentivos para voluntarios y migración externa como trabajos con requisitos propios. Un archivo público portable no resuelve pérdida de contactos, seguridad de dispositivos o recuperación sin medios.

No hay elección definitiva de KERI, directorio común, proveedor obligatorio, umbral de testigos o recuperación. Si avanzar requiere adoptar una autoridad común imprescindible o una política de confianza nueva, será una decisión crítica del proyecto. La arquitectura se decide por evidencia y compromisos explícitos, sin equiparar número de pruebas a garantías.
