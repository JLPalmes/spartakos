---
title: Spartakos — Prototipo local con varias cuentas
lang: es-ES
license: CC-BY-SA-4.0
version: 0.3
date: 2026-10-23
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
8. Responder a una respuesta desde Bruno o Alicia: cada mensaje identifica a quién responde, conserva su audiencia y permite continuar el hilo sin aumentar indefinidamente el sangrado.
9. Dar y retirar «Me gusta». Es independiente de Guardar. Las reacciones son visibles solo para quienes pueden leer la publicación; no generan reputación, ordenación ni avisos. Carla puede reaccionar aunque no pueda comentar.
10. Exportar desde «Mi cuenta»: incluye aportaciones propias y referencias autorizadas a guardados y reacciones propias, no sesiones ni aportaciones privadas ajenas.

Los clientes consultan cambios aproximadamente cada segundo y medio mientras están visibles. La actualización conserva el borrador principal, las respuestas en curso y su foco. Una interrupción informa del estado sin presentar un envío fallido como guardado.

## Persistencia y escenarios separados

El servidor guarda datos ficticios en `resultados-locales/simulador/estado.json`, excluido del repositorio. Las escrituras se serializan y reemplazan el archivo de forma atómica. Reiniciar conserva publicaciones, roles, consentimientos, guardados y reacciones. La actualización del esquema anterior conserva los datos existentes; los borradores solo viven en la pestaña y se pierden al recargar. Las sesiones caducan al detener el proceso; volver a entrar no elimina los datos.

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

Hay 48 pruebas: diez de la maqueta anterior, 24 HTTP, cuatro de selección y recorrido de conversaciones y diez de programación. Cubren separación entre sesiones, permisos, audiencia, consentimiento, revocación, privacidad de guardados, persistencia, exportación, escrituras simultáneas, reacciones reversibles, migración de datos y conversaciones con 2.001 mensajes. Estas pruebas no constituyen una auditoría de seguridad ni ejecutan la matriz completa A01–A148.

Código bajo AGPL-3.0-or-later y documentación bajo CC-BY-SA-4.0, según el [mapa de licencias](../LICENCIAS.md). La [maqueta anterior](../prototipo/README.md) se conserva como antecedente descartable.

## Publicación programada

El editor muestra una audiencia fija en Inicio general y en comunidades privadas; solo ofrece selector si hay varias audiencias válidas. Programar abre fecha y hora en la zona indicada del dispositivo, muestra el momento efectivo y permite elegir margen máximo de retraso (15 minutos por defecto). Confirma para guardar en el servidor.

Programadas permite editar contenido y fecha, cancelar o publicar ahora. Los cambios conservan destino y audiencia. Otros usuarios no reciben estos pendientes. El servidor comprueba cada segundo y funciona aunque se cierre el cliente; debe seguir ejecutándose en el ordenador. Después de reiniciarse conserva pendientes y estados. Si vuelve fuera del margen, el envío vence. Si pierde permisos, se bloquea y exige revisión; restaurar permisos no lo reactiva solo.

Solo se programan publicaciones iniciales de texto. Los condicionales (aprobación, secuencias, intervalos y confirmación) quedan [estudiados como propuestas](../FUNCIONAL-03-PUBLICACIONES-Y-CONVERSACIONES.md), sin ejecución en el prototipo. La exportación contiene programaciones propias, pero no se puede importarlas para activar otro servidor.
