---
title: Spartakos — Modelo mixto de privacidad
lang: es-ES
license: CC-BY-SA-4.0
version: 0.1
date: 2026-10-22
status: Arquitectura candidata; cifrado de grupos pendiente de ensayo y revisión
---

# Modelo mixto de privacidad

## 1. Comparación y recomendación

| Modelo | Qué puede leer el alojamiento | Qué facilita | Principal límite |
| --- | --- | --- | --- |
| Control de acceso en servidor | Contenido privado que procesa en claro | Búsqueda, recuperación y moderación centralizadas | Exposición ante servidor comprometido o acceso exigido al operador |
| Cifrado de extremo a extremo para todo contenido | No necesita leer los cuerpos cifrados | Confidencialidad de espacios cerrados | Un contenido públicamente legible no permanece secreto frente a quien pueda entrar como lector; cifrarlo no evita vigilancia de lo publicado |
| Mixto | Públicos en claro; privados cifrados en dispositivos autorizados | Separa distribución pública y confidencialidad privada | Identidad, dispositivos, recuperación y metadatos siguen necesitando protección propia |

Recomendación: continuar con el modelo mixto como objetivo de arquitectura, sin afirmar que E2EE ya esté implementado. El piloto de control de acceso existente no se renombra como espacio cifrado. Antes de admitir usos de riesgo elevado se debe completar el ensayo y la revisión de cifrado y metadatos.

## 2. Tipos de espacio

**Público:** cualquier persona puede leerlo; indexación y distribución se explican. No promete confidencialidad. El transporte y la autenticidad siguen protegidos.

**Restringido con control de acceso:** lectores autorizados, pero el servicio puede procesar el texto. Es el modo previsto inicialmente en la especificación. La interfaz lo describe como «Acceso limitado; el servicio puede acceder al contenido», sin llamarlo E2EE.

**Privado cifrado:** cuerpos y adjuntos se cifran antes de salir del dispositivo. Solo los dispositivos autorizados tienen material de descifrado. El operador conserva objetos cifrados y los metadatos que precise el diseño; no se promete que desconozca toda membresía o tráfico.

Las plantillas de comunidad seleccionan valores sensatos sin cuestionario criptográfico. Si el modo cifrado no está disponible, no se sustituye silenciosamente por el restringido. Cambiar modo no publica ni recifra automáticamente todo el historial; requiere una operación explícita con consecuencias claras.

## 3. Qué conoce cada participante

| Participante | Contenido público | Contenido privado cifrado | Datos que puede seguir observando |
| --- | --- | --- | --- |
| Dispositivo autorizado | Texto legible | Texto y claves necesarias para sus permisos | Lo que recibe y conserva localmente |
| Alojamiento personal | Originales públicos y datos del servicio | Copias cifradas cuando las custodia | Acceso, tamaño, horarios y referencias según diseño |
| Servicio comunitario de entrega | Publicaciones públicas comunitarias | Objetos cifrados; no claves por ser operador | Rutas de entrega, roles o miembros que necesite el modelo |
| Respaldo | Públicos y objetos autorizados | Copias cifradas | Tamaños, frecuencia y asociación con cuenta si no se evita |
| Índice público | Públicos permitidos | Ningún texto privado | Grafo y actividad públicos |
| Autoridad de identidad | Datos públicos mínimos de identidad | Ninguna clave de contenido por defecto | Cambios de dispositivos y autoridad según contrato |

Un administrador técnico que también sea miembro autorizado puede leer como miembro. La promesa correcta es no necesitar claves por operar el servidor, no que cualquier persona que opere un servidor sea incapaz de leer bajo cualquier rol.

## 4. Separación de claves y dispositivos

Distinguir autenticación, autorización de cambios críticos y descifrado de contenido. Recuperar identidad no entrega automáticamente claves antiguas. Las bibliotecas criptográficas deben gestionar secretos, evolución y borrado seguro según las capacidades reales del dispositivo.

Cada dispositivo nuevo necesita incorporación autorizada. Restablecer contraseña o recuperar cuenta mediante soporte no debe permitir introducir un dispositivo silencioso en todos los grupos cifrados. Mostrar cambios relevantes de dispositivos y comprobar autenticidad; para casos sensibles ofrecer verificación adicional opcional, sin exigirla en cada mensaje.

La entrega web también es una frontera de confianza: un servidor comprometido puede servir código cliente malicioso que lea texto después de descifrar. Evaluar clientes instalables, versiones verificables, actualizaciones y dependencias. Código abierto y builds reproducibles ayudan a revisar, pero no garantizan que cada cliente ejecutado sea correcto ni que su dispositivo esté sano.

## 5. Entrada y salida de miembros

El protocolo debe admitir participantes desconectados y cambios de grupo. Una autorización comunitaria debe traducirse en incorporación criptográfica válida, no solo en un botón visible.

Propuesta inicial para cifrado: nuevos miembros acceden a mensajes futuros por defecto. Una comunidad puede ofrecer un archivo anterior específico, autorizado y claramente separado, sin entregar retrospectivamente secretos de sesiones por comodidad.

Expulsar o revocar dispositivos debe impedir acceso a material nuevo una vez efectiva la actualización de claves. Mensajes pendientes y dispositivos desconectados necesitan reglas de época y pruebas. No se puede borrar lo ya leído, copiado o guardado por un miembro anterior.

## 6. Historial y recuperación

Tres alternativas a ensayar: transferencia desde otro dispositivo autorizado; archivo cifrado recuperable por el titular; recuperación asistida de claves de archivo con acceso explícitamente delegado. No son equivalentes en confianza ni facilidad.

Preferencia: continuidad entre dispositivos y archivo cifrado, sin que el procedimiento ordinario de recuperación de identidad conceda descifrado. El dispositivo puede preparar copias automáticamente, pero recuperarlas exige un medio cuyo custodio y dependencia se expliquen. No prometer simplicidad absoluta si se pierden todos los medios.

Si no existe medio suficiente, la cuenta puede volver a funcionar sin su historial privado. Mostrar esa pérdida con claridad y ofrecer reincorporación autorizada a grupos para actividad futura. La marca «huérfana» se refiere a control de cuenta, no a cualquier archivo que ya no se pueda descifrar.

La confidencialidad de mensajes antiguos frente a compromisos posteriores depende también de copias y claves archivadas. Un protocolo con secreto hacia adelante no convierte un archivo legible o recuperable en inaccesible para quien obtenga su clave de archivo.

## 7. Búsqueda, moderación y recomendaciones

Búsqueda privada en el dispositivo o en un entorno que forme parte explícita de sus extremos de confianza. Primera opción de ensayo: índice local, con límites de almacenamiento y reconstrucción. No enviar el texto a un buscador remoto ordinario.

Moderación por miembros autorizados con los roles correspondientes. Para denunciar, la persona selecciona contenido y contexto que decide compartir con la autoridad competente; explicar que ese fragmento sale de su ámbito cifrado. Diseñar comprobación de procedencia y límites de contexto, sin afirmar que cualquier captura prueba autoría.

El operador puede limitar cuentas o tráfico abusivo y objetos que administra sin leer todo el grupo. Esto no sustituye la moderación de contenidos por personas que sí pueden leerlos. Conservar evidencia mínima y con acceso restringido.

Recomendaciones privadas locales al principio. No activar bots o servicios de resumen remotos como si fueran invisibles: si reciben claves o texto son participantes con acceso y deben anunciarse como tales. Sin acceso autorizado no generan índices privados.

## 8. Protocolos y ensayo

MLS es candidato de evaluación para acuerdo de claves de grupo, no una implementación completa de Spartakos. RFC 9420 define el mecanismo criptográfico; RFC 9750 distingue servicios de autenticación y entrega y decisiones que siguen correspondiendo a la aplicación. Publicación persistente, permisos, archivo y recuperación requieren diseño adicional.

Comparar bibliotecas mantenidas, licencias, auditorías, plataformas, límites de grupos y operabilidad antes de adoptar una. No inventar un protocolo ni asumir que cumplir el formato evita ataques de identidad o entrega.

Ensayo con datos sintéticos: dos nodos, tres personas y varios dispositivos; un miembro desconectado; alta y expulsión; pérdida y revocación de dispositivo; recuperación con y sin archivo; intermediario que sustituye claves; versiones de cliente; adjuntos y búsqueda; denuncias seleccionadas. Son escenarios mínimos, no un tamaño suficiente para acreditar escalabilidad.

## 9. Puerta de aceptación

No anunciar «operador incapaz de leer», recuperación segura o protección frente a intervención de servidores hasta verificar flujos de claves, archivos, clientes y metadatos. La evaluación independiente debe incluir cliente web, autenticación, actualización y copias, no solo la biblioteca criptográfica.

La siguiente entrega técnica debe escoger una implementación candidata y describir el ensayo reproducible, sin pasar directamente al desarrollo completo de funciones sociales.

## Fuentes

- [RFC 9420 — MLS](https://www.rfc-editor.org/rfc/rfc9420.html): acuerdo de claves de grupo; no cubre por sí solo la aplicación.
- [RFC 9750 — Arquitectura MLS](https://www.rfc-editor.org/rfc/rfc9750.html): servicios y supuestos de confianza necesarios alrededor del protocolo.

Las tablas y reglas restantes son propuestas de diseño para Spartakos, pendientes de pruebas.
