---
title: Spartakos — Componentes candidatos y primer ensayo estructural
lang: es-ES
license: CC-BY-SA-4.0
version: 0.1
date: 2026-10-22
status: Selección provisional y protocolo de ensayo; no ejecutado
---

# Primer ensayo estructural

## 1. Decisión que debe permitir tomar

Determinar si un sistema de dos nodos de Spartakos puede preservar identidad y referencias al trasladarse, coordinar permisos comunitarios y entregar publicaciones cifradas sin que la infraestructura de entrega necesite claves de lectura. Comparar facilidad de operación y límites, sin construir todavía una red social completa.

Un resultado funcional no certifica seguridad, escala ni independencia institucional. El ensayo puede ejecutarse inicialmente en una máquina con procesos y credenciales separados; eso permite estudiar protocolos, pero no acredita resistencia a caída de la máquina ni a administradores coludidos.

## 2. Componentes candidatos

### Cifrado de grupos

| Candidato | Evidencia documental | Uso propuesto | Condición de descarte o revisión |
| --- | --- | --- | --- |
| OpenMLS | Implementación Rust de RFC 9420; repositorio con pruebas de compatibilidad y persistencia; licencia MIT indicada | Primera biblioteca para el ensayo de grupo en clientes nativos de laboratorio | No poder persistir/reanudar estado con seguridad, errores en cambios de miembros, coste o mantenimiento incompatibles |
| mls-rs | Declara MLS, WASM y almacenamiento configurable; MIT/Apache-2.0; advierte que no ha recibido auditoría completa externa | Alternativa con el mismo guion y pruebas independientes | Proveedor criptográfico requerido experimental, comportamiento incorrecto o falta de cobertura de seguridad para el uso previsto |

La selección provisional de OpenMLS prioriza disponer de un candidato concreto, no afirma superioridad criptográfica. No se decide por número de estrellas ni por el nombre de la entidad mantenedora.

El README de OpenMLS distingue plataformas probadas de otras solo compiladas, incluida WASM; sus bindings web se describen como experimento. Compilar no acredita funcionamiento ni almacenamiento de claves seguro en navegador. El primer ensayo puede usar clientes de laboratorio para aislar problemas del protocolo; después es obligatorio repetir flujos en navegador y móvil antes de aceptar la experiencia web propuesta.

Registrar versión o commit, hash de dependencias, licencia, proveedor criptográfico y configuración al ejecutar. No usar una rama mutable sin referencia fija. Desactivar opciones que impriman contenido o claves; usar marcadores sintéticos para inspeccionar exposición accidental.

Fuentes: [OpenMLS](https://github.com/openmls/openmls), [README y plataformas](https://raw.githubusercontent.com/openmls/openmls/main/README.md), [bindings WASM](https://raw.githubusercontent.com/openmls/openmls/main/openmls-wasm/README.md), [mls-rs](https://github.com/awslabs/mls-rs). Estas fuentes no constituyen auditorías de integración de Spartakos.

### Identidad y continuidad

Comparar una implementación existente con el contrato exigido, sin inventar un registro criptográfico propio para el ensayo.

**Referencia de laboratorio:** DID PLC y su implementación de directorio, únicamente en entorno aislado con identidades sintéticas. Permite estudiar operaciones de cambio y rotación. No se crean identidades ni dependencias de producción en el directorio público. Verificar condiciones de despliegue y licencia de cada paquete antes de integrarlo.

**Límite decisivo:** el diseño documentado utiliza directorio central. Las réplicas de lectura aumentan observación y disponibilidad de consulta, pero no equivalen a una autoridad alternativa para aceptar operaciones. No satisface por sí solo la resistencia al cierre o censura del directorio que interesa a Spartakos.

Separar dos resultados: traslado sin el alojamiento original y continuidad sin la autoridad común original. Si solo pasa el primero, registrar independencia de alojamiento y dependencia de directorio, no éxito completo. Un servidor nuevo que interprete operaciones por reglas propias no prueba continuidad del mismo sistema.

Como contraste documental, did:web introduce dependencia de dominio y resolución web; no se selecciona como salida automática al problema. La alternativa de autoridad distribuida permanece pendiente de componente existente, reglas de confianza y revisión. No se reemplaza por un «dos de tres» sin definir qué operaciones autoriza y cómo resuelve conflictos.

Fuentes: [DID PLC](https://github.com/did-method-plc/did-method-plc), [réplicas de lectura](https://atproto.com/blog/plc-replicas), [métodos DID en AT Protocol](https://atproto.com/specs/did).

### Almacenamiento y entrega

Nodos modulares con base transaccional, cola durable y objetos separados de metadatos. PostgreSQL y almacenamiento local por directorios con interfaz sustituible son candidatos suficientes para este ensayo; no hace falta desplegar almacenamiento comercial ni un índice global.

Persistir el estado de MLS del cliente separado del almacenamiento del nodo. No guardar claves de descifrado en el servidor para facilitar una prueba. Un archivo cifrado y sus claves de recuperación tienen inventario separado.

La comunicación mínima entre nodos transporta objetos y eventos con IDs, versiones, autorización y deduplicación. No diseñar una nueva criptografía: los mecanismos de firma y autenticación deben proceder de bibliotecas revisadas. La integración de identidad en credenciales MLS necesita validación explícita; incluir un ID de cuenta en texto no demuestra que su poseedor esté autorizado.

## 3. Topología y datos

- Nodo A: alojamiento inicial de Alicia y servicio comunitario del ensayo.
- Nodo B: alojamiento de Bruno y destino del traslado de Alicia.
- Cliente de Carla: participante con periodos desconectados y un dispositivo adicional.
- Clientes de Alicia y Bruno: estado criptográfico propio, separado de nodos.
- Directorio de identidad de laboratorio y réplica de consulta, cuando el componente lo permita.
- Respaldo independiente a nivel de proceso/credenciales; se declara si comparte máquina y administrador.

El servicio comunitario continúa en A al mover la cuenta personal. Esto evita confundir traslado de alojamiento y traslado comunitario. La pérdida completa de A es otro escenario: no se afirma continuidad de esa comunidad sin respaldo y autoridad comunitarios restaurados.

Usar publicaciones públicas y cifradas, imágenes sintéticas, varios tamaños, relaciones y roles conocidos. No datos reales, cuentas de plataformas externas, correo real ni mensajes a terceros. Ningún cliente de ensayo se distribuye como producto de privacidad.

## 4. Guion reproducible

| Caso | Acción | Evidencia requerida | Resultado que invalida la candidata o exige rediseño |
| --- | --- | --- | --- |
| E01 | Crear identidades y registrar dispositivos | Estado inicial, autoridad y ubicaciones | El alojamiento conserva el único medio de cambiar destino |
| E02 | Publicar de A a B y repetir entrega | Mismo ID, versiones, recepción y duplicados | Reintento crea publicaciones o autoridad distinta |
| E03 | Crear grupo cifrado y añadir dispositivos autorizados | Credenciales verificadas y destinatarios | Servidor recibe claves o admite identidad no validada |
| E04 | Desconectar a Carla y emitir cambios | Secuencia y sincronización posterior | Desconexión corrompe estado o acepta permisos antiguos como vigentes |
| E05 | Expulsar un dispositivo y publicar después | Cambio efectivo de época y mensaje nuevo | Dispositivo revocado descifra mensajes posteriores al cambio aceptado |
| E06 | Incorporar nuevo miembro | Lectura futura y ausencia de archivo previo no autorizado | Entrada entrega historial anterior por accidente |
| E07 | Reiniciar clientes con almacenamiento persistente | Estado reanudado sin reutilización insegura ni pérdida silenciosa | Solo funciona dejando todo en memoria o exponiendo secretos |
| E08 | Trasladar Alicia a B sin cooperación de su alojamiento | Identidad estable, autoridad, referencias y manifiesto | Solo funciona aprobando el cambio desde el origen |
| E09 | Interrumpir traslado y enviar operación antigua | Reanudación y rechazo de autoridad caducada | Dos destinos pueden escribir como autoridad vigente |
| E10 | Desactivar directorio principal | Resolución observada y posibilidad real de cambios | Llamar continuidad a consultas antiguas sin poder cambiar ubicación |
| E11 | Perder dispositivo y recuperar identidad | Medios utilizados, credenciales revocadas y estado privado | Recuperación incorpora dispositivo silencioso o afirma recuperar historia sin claves |
| E12 | Restaurar archivo cifrado y probar sin clave | Integridad, resultado de descifrado y límites | Respaldo contiene texto legible para un rol no autorizado |
| E13 | Buscar y denunciar una selección privada | Tráfico, índice local y fragmentos compartidos | Se envía historial completo a buscador o moderador |
| E14 | Alterar credenciales y entrega desde nodo de laboratorio | Rechazos, alertas, metadatos expuestos | Confiar en sustitución de claves no autorizada sin detección prevista |
| E15 | Repetir integración en navegador | Persistencia, múltiples pestañas, actualización y almacenamiento | Presentar prueba nativa como seguridad web ya conseguida |

Las inspecciones de tráfico y registros verifican el alcance observado, no demuestran ausencia universal de filtraciones. Las pruebas criptográficas específicas siguen los procedimientos y vectores de la biblioteca.

## 5. Límites de interpretación

MLS no proporciona por sí mismo portabilidad de cuentas, archivo, permisos editoriales o anonimato. Una membresía criptográfica de lector no implementa automáticamente «puede leer pero no publicar». La capa de aplicación y clientes deben validar el rol y las operaciones autorizadas; un servidor no necesita descifrar todo para rechazar ciertos envelopes no autorizados, pero ese control no sustituye validación de recepción.

Un miembro malicioso que conserve claves puede copiar contenido o fabricar tráfico. La revocación protege futuro según condiciones de protocolo, no borra el pasado. La moderación y los reportes necesitan procedencia y permisos sin convertir capturas en prueba infalible.

La prueba de cliente web no elimina el riesgo de actualizaciones maliciosas desde el origen. Registrar distribución del cliente, dependencias y proceso de verificación, además de resultados funcionales.

## 6. Resultados y puertas de decisión

No hay pruebas ejecutadas. El informe deberá incluir instalación desde cero, versiones, topología, pasos, artefactos saneados, rendimiento observado, defectos y límites. Secretos y estados sensibles no se publican junto a resultados.

Aceptar el candidato de cifrado para prototipo solo si supera ciclo de vida, credenciales, persistencia y navegador en su alcance documentado. La revisión independiente continúa siendo requisito antes de prometer protección de alto riesgo.

Aceptar identidad únicamente con la garantía concreta demostrada. Un resultado dependiente de directorio puede servir para piloto declarado; no cierra la condición de independencia para F5. Si no existe alternativa que satisfaga continuidad con coste viable, presentar ese compromiso como decisión de arquitectura, no avanzar con garantía falsa.

## 7. Orden de ejecución propuesto

1. Resolver licencia inicial del proyecto y preparar repositorio abierto con guía experimental y canal de seguridad.
2. Inventariar entorno, versiones, recursos y licencias de componentes.
3. Ejecutar E01–E07 y evaluar los roles comunitarios.
4. Ejecutar E08–E14, registrando cada dependencia común.
5. Ejecutar E15 y repetir los flujos sensibles en navegador.
6. Revisar resultados y decidir implementación social posterior.

La selección documental no equivale a instalar componentes, publicar repositorio ni aprobar su uso en producción.
