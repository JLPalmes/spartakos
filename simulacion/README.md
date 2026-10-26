---
title: Spartakos — Prototipo local con varias cuentas
lang: es-ES
license: CC-BY-SA-4.0
version: 0.9
date: 2026-10-26
status: Laboratorio funcional de un solo servidor; identidades ficticias
---

# Prototipo local con varias cuentas

Esta versión incorpora servidor, almacenamiento local y clientes con sesiones independientes. Permite simular interacción entre cuentas y comprobar permisos en el servidor. No implementa una red descentralizada, identidad soberana, migración real, cifrado de extremo a extremo ni recuperación de cuentas reales.

## Arranque

Requiere Node.js 22 o posterior, sin instalar dependencias. Desde la raíz del repositorio:

```sh
node simulacion/servidor.mjs
```

Abrir `http://127.0.0.1:8787`. La pantalla muestra cuatro clientes a la vez. Los enlaces de cada panel permiten abrirlo en otra pestaña. Cada sesión utiliza su propia autorización y guardados; ninguna pantalla permite emitir consentimientos como si fuera otra persona. En este laboratorio sí se puede entrar libremente como cualquiera de las cuentas ficticias.

| Cuenta | Situación inicial en Cuaderno compartido |
| --- | --- |
| Alicia | Administración: puede publicar, cambiar permisos y proponer apertura |
| Bruno | Puede leer, comentar e iniciar publicaciones |
| Carla | Lectura y reacciones, sin comentarios ni publicaciones; conserva su consentimiento individual para una apertura |
| Diego | No pertenece a la comunidad; no recibe su contenido privado |

Todas las cuentas pueden publicar en el espacio público. Que Carla no pueda publicar en una comunidad no limita su cuenta fuera de ella. Alicia puede cambiar el permiso de Bruno o Carla entre lectura, comentarios y publicación. La sustitución de la administración queda fuera de esta versión.

## Recorridos para probar

1. Desde Bruno, entrar en «Comunidades → Cuaderno compartido» y publicar con destino «Solo integrantes». Alicia y Carla lo reciben; Diego no. Inicio general contiene únicamente conversaciones generales, incluso cuando una comunidad permita publicaciones públicas.
2. Guardar una publicación desde Carla y abrir «Guardados» en otras cuentas: el guardado no se comparte. «Ver en conversación» permite recuperar su contexto, también cuando es una respuesta.
3. En Alicia, entrar en Cuaderno compartido y abrir «Permisos de participación» y dar a Carla permiso para leer y comentar. Carla podrá responder, sin iniciar temas en la comunidad.
4. Preparar un borrador privado en Bruno y retirarle permiso de publicación desde Alicia. El cliente conserva texto y destino; bloquea el envío hasta una elección explícita. Nunca cambia automáticamente a público.
5. Proponer apertura desde Alicia. Cada cuenta del censo debe consentir desde su sesión. Una mayoría es insuficiente y una negativa cierra la propuesta.
6. Si hay unanimidad, abrir para publicaciones futuras. El historial anterior y los borradores restringidos conservan su audiencia. Las respuestas a publicaciones antiguas conservan también esa audiencia.
7. Probar una baja de membresía. Se cancela la propuesta vigente y permanece la protección para impedir una apertura elusiva. Una persona retirada puede decidir sobre la propuesta que la afecta sin volver a recibir el historial privado.
8. Responder a una respuesta desde Bruno o Alicia: cada mensaje identifica a quién responde y conserva su audiencia. El máximo es de tres niveles contando la publicación inicial; después se continúa mediante Citar en una publicación.
9. Dar y retirar «Me gusta». Es independiente de Guardar. Cada persona solo ve su propia elección; ni el autor ni otros lectores ven identidades. El total visible cambia solo en los cortes horarios, con su fecha. El botón lleva un check verde, sin corazón. No genera reputación, ordenación ni avisos. Carla puede reaccionar aunque no pueda comentar.
10. Exportar desde «Mi cuenta»: incluye aportaciones propias y referencias autorizadas a guardados y reacciones propias, no sesiones ni aportaciones privadas ajenas.

Los clientes consultan cambios aproximadamente cada segundo y medio mientras están visibles. La actualización conserva el borrador principal, las respuestas en curso y su foco. Una interrupción informa del estado sin presentar un envío fallido como guardado.

## Persistencia y escenarios separados

El servidor guarda datos ficticios en `resultados-locales/simulador/estado.json`, excluido del repositorio. Las escrituras se serializan y reemplazan el archivo de forma atómica. Reiniciar conserva publicaciones, roles, consentimientos, guardados y reacciones. La actualización del esquema anterior conserva los datos existentes; los borradores guardados explícitamente se conservan; las ediciones sin guardar y respuestas en curso solo viven en la pestaña. Las sesiones caducan al detener el proceso; volver a entrar no elimina los datos.

Para otro escenario, usar otra carpeta y otro puerto:

```sh
SPARTAKOS_PORT=8788 SPARTAKOS_DATA_DIR=resultados-locales/otro-escenario node simulacion/servidor.mjs
```

No ejecutar dos procesos sobre la misma carpeta de datos. No hay coordinación entre servidores ni bloqueo entre procesos. Para repetir desde cero, es preferible una carpeta nueva; no hay un botón que borre silenciosamente el escenario existente.

El servidor escucha exclusivamente en `127.0.0.1`. No abrirlo a Internet ni utilizar túneles para cuentas reales. El selector de cuenta es acceso libre de laboratorio, no autenticación de producción. Los datos no están cifrados; quien controla la máquina o el proceso puede leerlos. Las distintas sesiones no aíslan a clientes maliciosos ejecutados en el mismo origen.

## Comprobaciones

```sh
python3 verificar.py
node --test prototipo/modelo.test.mjs simulacion/*.test.mjs
```

Hay 92 pruebas: diez de la maqueta anterior, 34 HTTP, cuatro de selección y recorrido de conversaciones, diez de programación, siete de citas y límites, ocho de recuentos horarios, ocho de borradores y once de edición y retirada. Cubren separación entre sesiones, permisos, audiencia, consentimiento, revocación, privacidad de guardados, persistencia, exportación, escrituras simultáneas, reacciones reversibles, migración de datos y lectura de historiales con 2.001 mensajes (no creación de nuevos hilos de esa profundidad), límite de tres niveles, citas, avisos y su privacidad. Estas pruebas no constituyen una auditoría de seguridad ni ejecutan la matriz completa A01–A148.

Código bajo AGPL-3.0-or-later y documentación bajo CC-BY-SA-4.0, según el [mapa de licencias](../LICENCIAS.md). La [maqueta anterior](../prototipo/README.md) se conserva como antecedente descartable.

## Publicación programada

El editor muestra una audiencia fija en Inicio general y en comunidades privadas; solo ofrece selector si hay varias audiencias válidas. Programar abre fecha y hora en la zona indicada del dispositivo, muestra el momento efectivo y permite elegir margen máximo de retraso (15 minutos por defecto). Confirma para guardar en el servidor.

Programadas permite editar contenido y fecha, cancelar o publicar ahora. Los cambios conservan destino y audiencia. Otros usuarios no reciben estos pendientes. El servidor comprueba cada segundo y funciona aunque se cierre el cliente; debe seguir ejecutándose en el ordenador. Después de reiniciarse conserva pendientes y estados. Si vuelve fuera del margen, el envío vence. Si pierde permisos, se bloquea y exige revisión; restaurar permisos no lo reactiva solo.

Solo se programan publicaciones iniciales de texto. Los condicionales (aprobación, secuencias, intervalos y confirmación) quedan [estudiados como propuestas](../FUNCIONAL-03-PUBLICACIONES-Y-CONVERSACIONES.md), sin ejecución en el prototipo. La exportación contiene programaciones propias, pero no se puede importarlas para activar otro servidor.

## Tres niveles y citas

Publicación → respuesta → respuesta a respuesta. El tercer nivel ofrece Citar en una publicación en lugar de Responder, si hay permiso para iniciar publicaciones. La cita conserva referencia y atribución; crea otro hilo y deja un aviso al autor citado en Avisos. El aviso puede abrirse y marcarse leído; no hay correo ni aviso externo. Las autocitas no generan aviso.

Una cita privada no sale de su comunidad ni se convierte en pública. Las citas programadas avisan únicamente al publicarse. Se conserva el historial anterior, aunque sea más profundo, sin permitir nuevas respuestas desde el tercer nivel.

## Privacidad de Me gusta

No hay lista Reacciones. La API entrega `likedByMe` para la sesión actual y el último `likeCount` agregado por hora, con `likesUpdatedAt` (corte) y `likesGeneratedAt` (cálculo). No entrega el total en directo ni los cambios entre cortes. El servidor conserva internamente los vínculos y la exportación solo incluye las reacciones propias; no hay anonimato frente al operador. El botón usa un check verde y el texto Marcado al activarlo, además del estado accesible aria-pressed.

## Recuentos cada hora

El servidor actualiza los totales en cortes comunes de cada hora UTC en punto, aunque no haya clientes abiertos. La pantalla indica Recuento a las HH:mm y fecha, en la zona del dispositivo. El detalle de la fecha distingue el corte del momento de cálculo. No hay cuenta atrás ni avisos.

Marcar o retirar el check cambia inmediatamente la elección propia; su efecto en el total espera al próximo corte. Las reacciones hechas justo a la hora del corte entran en el siguiente, incluso si el cálculo se ejecuta con retraso. Tras instalar o actualizar aparece Recuento pendiente hasta el primer corte posterior; no se reconstruyen recuentos históricos sin evidencia. Una publicación nueva espera también a su primer corte.

Si el servidor se detiene, la última instantánea conserva su fecha. Al volver calcula el último corte alcanzado con los cambios guardados y mantiene las restricciones de acceso. Sigue siendo un laboratorio local, sin garantías de disponibilidad ni anonimato frente al proveedor o inferencias en grupos pequeños.

## Borradores recuperables

Escribe y pulsa Guardar borrador. La acción envía el texto al servidor local, que puede leerlo; escribir por sí solo no lo envía. Borradores permite retomar texto, comunidad, audiencia y cita después de recargar o volver a entrar. No publica ni programa al guardar o abrir. El editor indica si hay cambios sin guardar.

En dos pestañas, un conflicto no sobrescribe: conserva el texto y ofrece Guardar como copia. Si pierdes permiso para publicar, puedes seguir guardando el pendiente en el mismo destino, pero no publicarlo ni cambiarlo automáticamente a público. Al publicar o programar, el servidor controla versión y marca el borrador como utilizado junto con el resultado. Las versiones utilizadas quedan consultables como referencia y la exportación incluye solo las propias.

Por ahora se guardan publicaciones iniciales de texto, no respuestas ni la selección tentativa de fecha. Programar confirma fecha y hora por separado. Las ediciones sin guardar se pierden al recargar. Hay papelera recuperable y restauración; el borrado definitivo y el historial completo de versiones siguen pendientes.

Mover a papelera conserva el borrador y permite restaurarlo. La papelera se abre desde Borradores; no se vacía automáticamente. Si se aparta una referencia ya publicada o programada, su publicación o programación sigue existiendo: esta acción solo organiza los borradores. Restaurar conserva su estado anterior y no repite el envío.

## Editar y retirar publicaciones propias

Editar publicación abre el texto propio y conserva destino, audiencia y referencias. Guardar edición comprueba versión y permisos y muestra la fecha de modificación. Respuestas y citas señalan si se refieren a una versión anterior; tu Me gusta anterior no se renueva automáticamente. Los totales horarios pueden incluir aprobaciones anteriores a una edición, sin desglose por versión o persona.

Retirar publicación abre una explicación antes de Confirmar retirada del texto. Vacía el cuerpo en el estado activo y deja un marcador; no hay restauración del texto aquí. No elimina respuestas ajenas, citas independientes ni respaldos o copias externas. Las citas dejan de mostrar el cuerpo retirado, y una programación que lo necesite se bloquea. Los borradores privados independientes no se purgan automáticamente.

Desde Mi cuenta puedes retirar texto propio de una comunidad a la que ya no tienes acceso, sin recuperar contenido ajeno. El borrado completo con política de copias y la moderación por terceros siguen fuera de esta implementación. Las ediciones locales no guardadas pueden copiarse ante conflictos, pero no sobreviven a recargar.
