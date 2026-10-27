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

La reanudación requiere invocar las tareas oficiales de procesamiento de recibos y de eventos pendientes. No es una garantía de recuperación autónoma de un servicio que todavía no existe. Esta prueba entrega el recibo a la API directamente; la prueba HTTP anterior valida separadamente el transporte. Queda pendiente unir reinicio del coordinador y recibos HTTP en un mismo escenario, ensayar caducidad y cortes durante escritura y contrastar fuentes discrepantes después de reiniciar.

Para ejecutar el conjunto en el entorno privado preparado, desde la raíz del proyecto:

```sh
DYLD_LIBRARY_PATH="/ruta/privada/native/lib" PYTHONPYCACHEPREFIX="/ruta/privada/pycache" /ruta/privada/venv/bin/python -m unittest discover -s laboratorio-identidad -p 'keri_*.py' -v
```

Las 16 comprobaciones incluyen la reproducción de H01. No deben describirse como 16 garantías de seguridad superadas. El simulador social sigue sin cambios y conserva su batería independiente de 109 pruebas.
