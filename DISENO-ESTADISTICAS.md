---
title: Spartakos — Catálogo mínimo de estadísticas y límites de publicación
lang: es-ES
license: CC-BY-SA-4.0
date: 2026-10-24
status: Propuesta para revisión; sin implementación ni nueva captación
---

# Estadísticas para gestionar recursos y continuidad

Esta propuesta desarrolla N11 y la [sección 12 del diseño funcional](FUNCIONAL-05-INICIO-BUSQUEDA-Y-DESCUBRIMIENTO.md). Su finalidad es ayudar a comprobar espacio disponible, pendientes y continuidad. Ningún indicador queda aprobado por aparecer en este catálogo. No modifica el simulador ni introduce seguimiento de lecturas, visitas, atención o dispositivos.

## 1. Catálogo de primera fase propuesto

| Indicador | Decisión que facilita | Fuente y definición | Audiencia | Actualización propuesta |
| --- | --- | --- | --- | --- |
| Espacio propio y límite contratado u ofrecido | Exportar, liberar espacio o cambiar de proveedor | Contabilidad del almacenamiento: bytes lógicos propios y cuota; separar réplicas, adjuntos y sobrecoste del proveedor | Titular | Consulta, con fecha del cálculo |
| Pendientes propios | Retomar un borrador o resolver un envío bloqueado | Registros propios: borradores activos, papelera, programaciones pendientes, bloqueadas y vencidas; estados separados, sin sumar referencias utilizadas como pendientes | Titular | Consulta sobre estado actual |
| Resultado de exportación propia | Saber si la copia está disponible | Última operación solicitada: fecha, estado, alcance y caducidad del archivo; no afirmar que existe copia externa | Titular | Al terminar o fallar la operación |
| Estado de copia y restauración | Detectar una protección insuficiente | Declaración del proveedor: última copia completada y última restauración comprobada, fechas distintas; «sin comprobación» si falta evidencia | Titular respecto a sus datos; responsables respecto al servicio | Tras operación y con fecha visible |
| Cuota comunitaria | Prever ampliación de recursos | Espacio lógico ocupado, límite y espacio reservado, con la misma definición de facturación | Responsables autorizados de recursos | Consulta, con fecha |
| Salud de servicios participantes | Elegir dónde consultar una incidencia o pedir capacidad | Declaración pública voluntaria del operador: tipo de servicio, estado declarado, fecha y enlace público de incidencias | Público | Publicación diaria como candidata, con caducidad explícita |

La primera fase propuesta excluye recuentos públicos de cuentas, integrantes, actividad, denuncias, comunidades o capacidad libre exacta. Tampoco estima alcance. El panel público inicial sería un directorio de declaraciones fechadas, no un indicador único de «salud de Spartakos» ni un censo obligatorio. Un servicio ausente o con declaración caducada se muestra sin información vigente, no como caído ni con capacidad cero.

En el simulador solo existen algunos registros necesarios para estos indicadores. No se inventan cuota, copias verificadas o historial de exportaciones donde no hay un servicio que los proporcione. Mostrar «no disponible» es preferible a simular una garantía.

## 2. Permisos y exposición

Las cifras personales se calculan sobre objetos propios; el rol de administrador no concede acceso a borradores, Guardados, intereses o programaciones de otra persona. Los permisos de recursos comunitarios son una capacidad separada: ser moderador no debe otorgarlos automáticamente. El prototipo aún no dispone de ese reparto de capacidades; no se añadirá bajo un nombre estadístico sin definirlo.

Los datos de recursos comunitarios quedan reservados por defecto a responsables autorizados, incluso si la comunidad es pública. Su publicación requeriría un diseño propio: los recursos ocupados pueden delatar existencia o cambios en contenido restringido. Ningún total público mezcla contenido público y privado. Una descarga, API, caché o error debe aplicar la misma regla que la pantalla.

Cambiar permisos invalida el acceso en la siguiente consulta y elimina las copias de presentación del cliente en la medida controlable por la aplicación. El servicio no promete revocar archivos que alguien ya hubiera descargado. El cálculo no devuelve identificadores ajenos, muestras de contenido, lista de reacciones ni marcas de tiempo de acciones individuales. Los datos privados no se transmiten a un panel público central.

## 3. Indicadores aplazados y grupos pequeños

Publicaciones por periodo, conversaciones sin respuesta y carga de moderación quedan fuera del catálogo inicial. Antes de admitirlos deben definirse su utilidad, quién puede inferirse, tratamiento de retiradas y visibilidad histórica. Un tema sin respuesta no implica una tarea incumplida ni autoriza a presionar a participantes.

No se adopta un umbral numérico como garantía. Contar diez personas, por ejemplo, no impide que nueve conozcan sus acciones e infieran la restante. Por ello la propuesta inicial suprime por completo las estadísticas de comportamiento de personas y grupos, también para administradores. No ofrece filtros por persona, tema, hora, rol, intersecciones o ventanas móviles, ni totales complementarios que permitan recuperar una celda omitida mediante restas.

Cualquier ampliación requiere revisar consultas sucesivas, diferencias entre cortes, cambios de pertenencia y combinaciones de exportaciones. Si no puede justificarse una protección suficiente, el indicador se omite. No se amplía la captación para poder calcularlo. Las aprobaciones visibles mantienen únicamente los cortes horarios ya definidos; este catálogo no crea otra serie ni acceso al total en directo.

## 4. Declaraciones públicas de operadores

Formato mínimo candidato: identificador público del servicio, función, estado declarado, instante al que se refiere, instante de emisión, caducidad, versión de definición y enlace público de incidencias. Sin direcciones internas, localización física precisa, inventario de cuentas, topología privada o trazas de usuarios. Una futura firma acredita la procedencia de una declaración, no su veracidad ni solvencia.

La identidad pública del servicio debe poder persistir al cambiar de proveedor. Hasta definir ese mecanismo no se promete deduplicación entre operadores. Un agregador puede contar declaraciones o identificadores distintos de su conjunto observado; no presentar ese número como servidores físicos, personas o capacidad total de la red. La ausencia de comprobador independiente se indica expresamente. No se atribuye una medición de disponibilidad a una mera declaración de estado.

Publicar estas declaraciones es voluntario y no condiciona el derecho a participar ni exige infraestructura de analítica. Los receptores pueden validar estructura y caducidad con trabajo acotado, almacenar la última declaración por servicio y aplicar límites de tamaño y frecuencia. El diseño de identidad, autenticidad y resistencia a declaraciones masivas sigue pendiente; no se construye un directorio operativo antes de resolverlo.

## 5. Conservación y presentación

Propuesta conservadora: calcular pendientes y recursos actuales sin crear series históricas por defecto; reutilizar la retención ya aprobada de las operaciones de origen. No prolongar la conservación de un objeto retirado para mantener una gráfica. Una referencia privada independiente, como un borrador, conserva su propia política y no se hace pública por esta vía.

Para el panel de operadores, conservar solo la última declaración y marcarla como caducada cuando corresponda. No publicar cronologías de cambios de estado durante esta fase. El periodo exacto de caducidad queda pendiente de pruebas operativas; el receptor nunca lo sustituye silenciosamente por un dato vigente. Sin datos vigentes, no hay resumen de disponibilidad.

Cada tarjeta muestra ámbito, definición, unidad, fuente, fecha del dato y límites. Distingue cero de desconocido y dato declarado de comprobado. No incluye comparaciones de popularidad, rachas, objetivos, posición en clasificaciones ni notificaciones por caída de actividad. La pantalla de gestión es opcional y debe poder recorrerse con teclado y lector de pantalla.

## 6. Casos de aceptación del diseño antes de desarrollar

1. Dos cuentas con pendientes distintos: cada una recibe únicamente sus estados, también al descargar o consultar directamente la API.
2. Un administrador intenta consultar borradores ajenos: el servicio deniega, sin revelar su existencia o número.
3. Una comunidad restringida pierde un integrante: la consulta posterior no entrega recursos ni actividad del espacio; sus textos propios siguen el recorrido de retirada ya previsto.
4. Un operador aloja comunidades privadas: su declaración pública no permite contar sus integrantes, almacenamiento o cambios de actividad.
5. Una exportación termina correctamente pero nunca se descarga: se informa del archivo preparado, sin afirmar que el titular posee una copia.
6. Una copia existe sin ensayo de restauración: ambas fechas se distinguen y no aparece «recuperación garantizada».
7. Un servicio deja de informar: se distingue caducidad de caída; no se calcula disponibilidad a partir de ausencia de declaraciones.
8. Dos identificadores representan un mismo equipo: se informa del conjunto observado, sin sumar servidores físicos ni prometer deduplicación.
9. Un solicitante combina filtros o periodos para inferir un grupo pequeño: la primera fase no ofrece tales consultas, ni siquiera a responsables.
10. Una retirada cambia el estado de origen: no se conserva su cuerpo para sostener una estadística y no se renueva una aprobación anterior.

Estos casos son un guion propuesto, no pruebas ejecutadas. Antes de implementar deben ratificarse el catálogo mínimo, las capacidades comunitarias, la caducidad y autenticidad de declaraciones y los costes operativos. Se puede comenzar más adelante por la vista personal de pendientes basada en datos propios existentes; no requiere aprobar el panel público ni recoger nuevas conductas.
