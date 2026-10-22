---
title: Spartakos — Contrato preliminar de datos y autoridad
lang: es-ES
license: CC-BY-SA-4.0
version: 0.1
date: 2026-10-22
status: Diseño independiente de componentes; pendiente de ensayos estructurales
---

# Contrato preliminar de datos y autoridad

## 1. Alcance

Este contrato fija separaciones que deben sobrevivir a elegir una base de datos o protocolo. No especifica criptografía nueva ni constituye una API implementada. Permite detectar dependencias antes de comprometer persistencia definitiva.

## 2. Entidades y autoridad

| Entidad | Datos mínimos lógicos | Autoridad para modificar | Límite |
| --- | --- | --- | --- |
| Identidad | Identificador persistente, estado y referencia a control vigente | Mecanismo de identidad y recuperación adoptado | El alojamiento no decide por sí solo titularidad |
| Perfil | Nombre mostrado, descripción y visibilidad por campo | Titular o delegación explícita | Nombre mostrado no es identificador exclusivo |
| Destino de alojamiento | Identidad, destino, revisión y vigencia | Control autorizado de continuidad | El antiguo nodo no recupera autoridad por reenviar eventos viejos |
| Dispositivo o sesión | Identidad, alcance, vigencia y revocación | Titular y procedimiento de recuperación | Añadir dispositivo no entrega automáticamente todo el pasado cifrado |
| Publicación | ID estable, autor, contexto, audiencia, revisión y fechas | Autor sobre su texto; comunidad sobre presencia y acceso | Moderador no reescribe como si fuese el autor |
| Comunidad | ID estable, reglas, alojamiento y versión de permisos | Gobierno comunitario válido | Promotor no adquiere propiedad ni veto perpetuo |
| Membresía | Identidad, rol, alcance e intervalos | Procedimiento comunitario | Pertenecer no obliga a seguir ni permite publicar en todo caso |
| Interés privado | Titular, objeto o tema y fecha opcional | Solo titular y servicios expresamente autorizados | Nunca se convierte por defecto en reacción pública |
| Reconocimiento | Emisor, aportación/versionado, tema, audiencia y estado | Emisor sobre atribución; destinatario sobre exhibición en perfil | No genera puntos universales ni permisos |
| Importación | Origen, versión del formato, inventario e integridad | Titular del archivo, dentro de sus derechos | Autoría externa declarada no equivale a firma nativa |
| Propuesta de apertura | Comunidad, texto exacto, censo protegido y versión | Procedimiento comunitario restringido por unanimidad | Ni mayoría ni expulsión sustituyen consentimientos |
| Credencial de servicio | Emisor, afirmación, alcance, evidencia y caducidad | Emisor con mandato; estados conforme a recurso | Firma no prueba verdad, capacidad ni legitimidad |

## 3. Publicaciones y cambios

Separar identidad del objeto, su versión y su ubicación de entrega. Un reintento transporta la misma operación; no crea otra publicación. Un traslado conserva referencias conforme al protocolo elegido. La base debe poder representar importaciones sin fingir firmas históricas ni actividad reciente.

Un acuerdo o reconocimiento apunta a una versión concreta. Al editar sustancialmente, no se atribuye al emisor adhesión al texto nuevo. Si se purga una versión sensible, puede conservarse una constancia mínima de que hubo una edición sin conservar públicamente el dato retirado.

La retirada debe propagarse a réplicas cooperantes y restauraciones posteriores mediante el mecanismo definido. No se promete borrado de copias de lectores o nodos hostiles. La restauración no debe resucitar silenciosamente información retirada.

## 4. Audiencia y permisos

Evaluar por separado: descubrir existencia, ver perfil, leer objeto, acceder al historial, comentar, iniciar tema, invitar, moderar y administrar. Evitar un único valor «miembro» que conceda todos los poderes. Los bloqueos de seguridad y sanciones locales constituyen otra dimensión.

La audiencia efectiva se limita por los permisos del contexto, la audiencia del objeto y el estado vigente aplicable. Una copia de un objeto privado no autoriza a ampliar acceso. En E2EE, autorización de aplicación y posesión de claves son controles complementarios; ninguno sustituye al otro.

Ante permisos no verificables por desconexión, no ampliar acceso ni conceder roles. La política de lectura ya autorizada sin conexión se define explícitamente; no puede revocar lo que una persona ya descargó. No enviar títulos, miniaturas o avisos a alguien que no pueda conocer el contenido.

## 5. Operaciones y concurrencia

Cada operación sensible identifica emisor, ámbito, objeto, revisión esperada y mecanismo de autenticación. La implementación debe distinguir repetición válida, operación caducada, conflicto y falta de autoridad. Un número de versión por sí solo no garantiza orden global ni resuelve bifurcaciones maliciosas.

Cambiar alojamiento, recuperar identidad, cambiar administradores o abrir una comunidad requiere reglas específicas de conflicto. No aceptar «gana la última fecha» con relojes de clientes no fiables. El mecanismo existente que se elija deberá demostrar resolución o detección; esta especificación no inventa un consenso para resolverlo.

## 6. Exportación por paquetes

Propuesta de inventario portable: versión del formato, identidad referenciada, fechas de generación, aportaciones propias, medios autorizados, relaciones exportables, preferencias y listado de exclusiones. Separar material personal de respaldos comunitarios, y contenido cifrado de claves necesarias para leerlo.

Cada entrada declara procedencia e integridad comprobable mediante mecanismos estándar. El destino informa qué reconoce y qué no. No exportar credenciales de sesión, contraseñas ni datos privados de terceros por conveniencia. El paquete no concede derechos adicionales a quien lo importa.

La prueba de salida exige abrir medios sin depender de URLs del proveedor original, conservar fechas y enlaces internos cuando sea posible y detectar pérdidas. Descargar un archivo de metadatos no basta para declarar portabilidad completa.

## 7. Trazabilidad y privacidad

Conservar el mínimo registro necesario para resolver autoridad, abuso y recuperación, con política de acceso y conservación. Un registro público e inmutable de todas las relaciones sería incompatible con perfiles reservados y comunidades cuya existencia debe permanecer privada. Publicar auditorías agregadas o comprobantes acotados cuando proceda, sin convertir la transparencia institucional en vigilancia de participantes.

## 8. Dependencias para implementación

La identidad, validación de operaciones, sincronización y recuperación necesitan componentes y pruebas E01–E15. Este contrato permite revisar esquemas y casos adversos antes de esa elección; no autoriza presentar un almacenamiento local como solución distribuida.
