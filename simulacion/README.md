---
title: Spartakos — Prototipo local con varias cuentas
lang: es-ES
license: CC-BY-SA-4.0
version: 0.1
date: 2026-10-22
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
| Carla | Solo lectura; conserva su consentimiento individual para una apertura |
| Diego | No pertenece a la comunidad; no recibe su contenido privado |

Todas las cuentas pueden publicar en el espacio público. Que Carla no pueda publicar en una comunidad no limita su cuenta fuera de ella. Alicia puede cambiar el permiso de Bruno o Carla entre lectura, comentarios y publicación. La sustitución de la administración queda fuera de esta versión.

## Recorridos para probar

1. Desde Bruno, seleccionar «Cuaderno compartido · Solo integrantes» y publicar. Alicia y Carla lo reciben; Diego no.
2. Guardar una publicación desde Carla y abrir «Mi interés» en otras cuentas: el guardado no se comparte.
3. En Alicia, abrir «Comunidades → Permisos de participación» y dar a Carla permiso para leer y comentar. Carla podrá responder, sin iniciar temas en la comunidad.
4. Preparar un borrador privado en Bruno y retirarle permiso de publicación desde Alicia. El cliente conserva texto y destino; bloquea el envío hasta una elección explícita. Nunca cambia automáticamente a público.
5. Proponer apertura desde Alicia. Cada cuenta del censo debe consentir desde su sesión. Una mayoría es insuficiente y una negativa cierra la propuesta.
6. Si hay unanimidad, abrir para publicaciones futuras. El historial anterior y los borradores restringidos conservan su audiencia. Las respuestas a publicaciones antiguas conservan también esa audiencia.
7. Probar una baja de membresía. Se cancela la propuesta vigente y permanece la protección para impedir una apertura elusiva. Una persona retirada puede decidir sobre la propuesta que la afecta sin volver a recibir el historial privado.
8. Exportar desde «Mi cuenta»: incluye aportaciones propias y referencias a guardados autorizados, no sesiones ni aportaciones privadas ajenas.

Los clientes consultan cambios aproximadamente cada segundo y medio mientras están visibles. La actualización conserva el borrador principal, las respuestas en curso y su foco. Una interrupción informa del estado sin presentar un envío fallido como guardado.

## Persistencia y escenarios separados

El servidor guarda datos ficticios en `resultados-locales/simulador/estado.json`, excluido del repositorio. Las escrituras se serializan y reemplazan el archivo de forma atómica. Reiniciar conserva publicaciones, roles, consentimientos y guardados. Las sesiones caducan al detener el proceso; volver a entrar no elimina los datos.

Para otro escenario, usar otra carpeta y otro puerto:

```sh
SPARTAKOS_PORT=8788 SPARTAKOS_DATA_DIR=resultados-locales/otro-escenario node simulacion/servidor.mjs
```

No ejecutar dos procesos sobre la misma carpeta de datos. No hay coordinación entre servidores ni bloqueo entre procesos. Para repetir desde cero, es preferible una carpeta nueva; no hay un botón que borre silenciosamente el escenario existente.

El servidor escucha exclusivamente en `127.0.0.1`. No abrirlo a Internet ni utilizar túneles para cuentas reales. El selector de cuenta es acceso libre de laboratorio, no autenticación de producción. Los datos no están cifrados; quien controla la máquina o el proceso puede leerlos. Las distintas sesiones no aíslan a clientes maliciosos ejecutados en el mismo origen.

## Comprobaciones

```sh
python3 verificar.py
node --test prototipo/modelo.test.mjs simulacion/servidor.test.mjs
```

Hay diez pruebas de la maqueta anterior y catorce pruebas HTTP de este servidor: separación entre sesiones, permisos, audiencia, consentimiento, revocación, privacidad de guardados, persistencia, exportación y escrituras simultáneas. Estas pruebas no constituyen una auditoría de seguridad ni ejecutan la matriz completa A01–A148.

Código bajo AGPL-3.0-or-later y documentación bajo CC-BY-SA-4.0, según el [mapa de licencias](../LICENCIAS.md). La [maqueta anterior](../prototipo/README.md) se conserva como antecedente descartable.
