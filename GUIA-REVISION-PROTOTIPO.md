---
title: Spartakos — Recorrido de revisión del prototipo
lang: es-ES
license: CC-BY-SA-4.0
date: 2026-10-26
status: Guion para revisión; no acta de aceptación
---

# Recorrido de revisión

El prototipo permite valorar la experiencia y comprobar algunas reglas en un servidor local con cuatro cuentas ficticias. Esta guía no acredita que se haya completado la matriz de producto. El [registro acumulado](REVISION-PARA-EL-LUNES.md) y el [informe de resultados](RESULTADOS-DEL-PROTOTIPO.md) distinguen lo probado de lo pendiente. Los cambios están en la [propuesta #2](https://github.com/JLPalmes/spartakos/pull/2), sin integrar en main.

## 1. Preparar la prueba sin perder datos

Usar un escenario sintético separado siguiendo las instrucciones de [la simulación](simulacion/README.md), con otro directorio de datos y otro puerto. No borrar ni sustituir `resultados-locales/simulador` para comenzar de nuevo. Los ensayos de bajas, retiradas y conflictos deben hacerse en el escenario separado. El servidor del laboratorio debe permanecer encendido para ejecutar programaciones.

Las cuentas no tienen autenticación de producción; no introducir datos personales. El operador puede leer el contenido del servidor. Cada pestaña es una sesión independiente: dos pestañas pueden representar a la misma cuenta para comprobar conflictos.

Un cliente que ya estaba abierto puede conservar una versión anterior del programa. Para cargar el cliente actual, copiar primero cualquier texto local sin guardar y después recargar la página. Recargar no borra las publicaciones ni los borradores ya persistidos en el servidor, pero sí puede perder el texto que solo existía en memoria.

## 2. Recorrido propuesto

| Paso | Acción | Resultado que revisar |
| --- | --- | --- |
| Espacios | Publicar en Inicio general y después dentro de una comunidad | Los contenidos aparecen en su espacio; el destino no se cambia silenciosamente |
| Interacciones | Guardar una publicación y marcar Me gusta; observar desde otra cuenta | Guardados es privado; Me gusta es un check y no revela identidades. El total espera al corte horario, aunque la marca propia es inmediata |
| Conversaciones | Responder a una publicación y a su respuesta | Tres niveles contando el original. Para continuar desde el último, citar en una publicación propia |
| Citas | Citar contenido restringido | Se conservan restricciones y permisos de destino; el autor recibe aviso interno al publicarse. No se promete que todos los servicios externos retiren copias |
| Borradores | Guardar explícitamente, recargar, retomar, mover a papelera y restaurar | Se conserva texto, destino y audiencia. Restaurar no publica ni reactiva un envío utilizado |
| Conflictos | Abrir el mismo borrador en dos pestañas y guardar versiones distintas | El segundo guardado obsoleto se rechaza. Guardar como copia permite conservar ambas variantes |
| Programación | Elegir una fecha próxima, revisar zona y margen y cerrar el cliente | El servidor encendido ejecuta el pendiente; Programadas muestra bloqueos o vencimientos. No depende de mantener abierta la pestaña |
| Edición | Editar una publicación propia tras recibir una respuesta y Me gusta | Cambia la versión; las referencias previas siguen identificadas y no se renuevan las aprobaciones |
| Edición simultánea | Guardar un cambio desde una segunda pestaña mientras la primera escribe | La primera conserva su texto; el envío obsoleto no sobrescribe la versión nueva |
| Pérdida de permisos | Reducir a lectura y después probar una baja completa mientras hay una edición abierta | Sin permiso no se ofrece guardar. El texto local queda para copiar; tras la baja hay acceso a Mi cuenta sin recuperar historial ajeno |
| Retirada | En el escenario desechable, revisar la confirmación de retirada de texto propio | El servicio deja marcador y conserva respuestas independientes. La retirada del cuerpo no se restaura aquí ni borra copias o respaldos |

La última acción elimina el cuerpo activo de ese escenario: revisar primero la explicación y conservar aparte cualquier texto que interese. No realizarla sobre aportaciones del laboratorio habitual para seguir este guion.

## 3. Qué se conserva y qué puede perderse

| Contenido | Conservación actual |
| --- | --- |
| Borrador guardado explícitamente | En el servidor, privado para su cuenta; disponible tras recargar y reiniciar |
| Publicación o programación aceptada por el servidor | En el estado persistente del laboratorio |
| Texto del editor que nunca se guardó, respuesta en curso o edición local rescatada | En memoria de la pestaña; no garantizado tras recargar, cerrar o volver a entrar |
| Referencia de borrador ya utilizada | Conserva estado y versión de referencia; restaurarla no vuelve a ejecutar el envío |
| Cuerpo retirado | Se vacía del estado activo; esto no garantiza borrar borradores independientes, exportaciones, respaldos o copias externas |

Antes de cerrar sesión, copiar el texto local que se quiera conservar o guardar como borrador cuando esa función esté disponible para el tipo de contenido. La entrada en una cuenta reinicia los editores locales, incluso si se vuelve a elegir la misma cuenta. La exportación de aportaciones del servidor no rescata texto que solo existe en memoria. No se ha añadido un aviso de salida ni guardado automático.

## 4. Qué queda fuera de esta revisión funcional

Las estadísticas son un [catálogo propuesto](DISENO-ESTADISTICAS.md), sin implementación ni captación nueva. También siguen pendientes la identidad soberana real, migración desde redes populares, red distribuida, recuperación de cuentas, cifrado de extremo a extremo, operación voluntaria a escala y servicios comerciales. La especificación de estas materias no equivale a su desarrollo.

La batería vigente suma 92 pruebas automáticas y hay recorridos sintéticos de navegador registrados. No equivale a ejecutar los 148 criterios completos, una auditoría de seguridad, un ensayo de carga o una evaluación completa de accesibilidad. La prueba de una acción concreta no acredita todos los casos de esa función.

## 5. Decisiones para revisar

Revisar primero si los recorridos son comprensibles y si se conserva correctamente el contexto. Después decidir qué carencias impiden una nueva prueba con participantes y cuáles pueden esperar. El catálogo estadístico requiere revisión propia de indicadores y permisos antes de programarlo. Las ediciones persistentes y respuestas recuperables requieren un diseño específico; no deben confundirse con los borradores iniciales ya implementados.

Registrar cada incidencia con cuenta ficticia, espacio, pasos, resultado esperado y resultado observado. Compartir únicamente capturas de escenarios sintéticos. La aceptación de la propuesta y la integración en main siguen siendo decisiones posteriores a la revisión.
