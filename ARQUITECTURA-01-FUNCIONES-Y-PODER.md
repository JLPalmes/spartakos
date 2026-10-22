---
title: Arquitectura 01 — Funciones, autoridad e independencia
lang: es-ES
license: CC-BY-SA-4.0
date: 2026-10-22
status: Hipótesis híbrida preferente; propuesta de descomposición sin tecnología elegida
---

# Funciones, autoridad e independencia

## 1. Punto de partida

La hipótesis de trabajo es una arquitectura híbrida con funciones sustituibles. La arquitectura concreta, el protocolo y la modalidad de alojamiento están pendientes de evaluación. Esta entrega desarrolla las fases 1 y 2 del plan: dependencias, poderes y alternativas.

La independencia buscada debe permitir continuar sin el operador original, no simplemente cambiar una pantalla o descargar un archivo. La experiencia ordinaria debe seguir siendo la de una aplicación sencilla: alta, acceso y uso, con servicios predeterminados y ajustes opcionales.

La separación funcional no exige contratar muchos servicios, desplegar un servidor por función ni que todos los proveedores puedan hacer de todo. Un operador puede ofrecer un paquete completo; la cuestión es qué partes pueden sustituirse y bajo qué autoridad.

## 2. Tres tipos de separación

- Lógica: datos e interfaces permiten separar funciones, aunque las ejecute una misma aplicación.
- Operativa: las funciones se pueden ejecutar en instalaciones diferentes.
- Institucional: distintas entidades las controlan, sin compartir necesariamente administradores, infraestructura o financiación.

La primera es necesaria para sustituir componentes; no demuestra las otras dos. Dos marcas que dependen del mismo control o de una base de datos exclusiva no constituyen alternativas independientes. A la inversa, separar cada función desde el inicio puede multiplicar fallos, comunicaciones y soporte sin aportar independencia proporcional.

## 3. Mapa de funciones y límites de autoridad propuestos

| Función | Responsabilidad | Autoridad necesaria | Poder que conviene impedir |
| --- | --- | --- | --- |
| Identidad y localización de servicios | Reconocer una identidad estable y averiguar dónde recibe servicio | Verificar cambios autorizados de claves y ubicación | Que el alojamiento sea el único autorizado a permitir la salida |
| Acceso y dispositivos | Inicio de sesión, sesiones y revocación | Autorizar acciones ordinarias del titular | Que una sesión robada pueda apropiarse inmediatamente de toda la identidad |
| Recuperación | Restablecer autoridad tras pérdida o incidente | Aplicar el procedimiento de recuperación acordado | Recuperación secreta o arbitraria por un único intermediario |
| Repositorio personal | Conservar perfil, publicaciones y referencias a relaciones | Aceptar cambios autorizados y servir versiones vigentes | Apropiarse de identidad o convertir contenidos privados en públicos |
| Archivos multimedia | Conservar y entregar fotos, vídeos y otros adjuntos | Aplicar permisos y política de conservación | Que perder un servidor deje solo enlaces a archivos desaparecidos |
| Copia independiente | Recuperar datos y estado necesario después de un fallo | Custodiar copias y permitir restauración autorizada | Confundir réplica inmediata con copia resistente a borrados maliciosos |
| Entrega y distribución | Transportar actualizaciones y localizar contenido | Servir contenido público o autorizado | Convertirse en registro exclusivo de identidad o único acceso a la red |
| Búsqueda y recomendaciones | Encontrar y ordenar lo que se puede ver | Indexar datos permitidos y aplicar preferencias | Modificar el original o saltarse permisos |
| Comunidad | Admisión, roles, organización, normas y decisiones locales | Administrar participación e historial comunitario según sus reglas | Que expulsar de una comunidad extinga la identidad de la persona |
| Moderación del servicio | Proteger y administrar el servicio que presta | Rechazar alojamiento o entrega dentro de su ámbito | Presentar una decisión local como orden universal sin competencia para ello |
| Aplicación | Mostrar la experiencia y recoger decisiones | Actuar con permisos limitados | Convertirse en único custodio de credenciales, datos o funciones esenciales |
| Gobierno común | Mantener reglas, especificaciones y procedimiento de evolución | Competencias expresas definidas por la Constitución | Control ilimitado de identidades, cuentas o servicios |

Este cuadro es una propuesta de competencias, no una afirmación de que estén técnicamente garantizadas. Si un servidor conserva claves suficientes o texto privado legible, puede abusar de ese acceso. El cifrado, las firmas, la revocación, la separación de credenciales y los recursos de gobierno deben concretar los límites.

## 4. El núcleo que merece mayor protección

### Identidad persistente

Debe distinguirse de nombre visible, credenciales y alojamiento. Cambiar de nombre no debería destruir relaciones; cambiar alojamiento no debería crear una persona nueva. Un nombre bajo el dominio del proveedor puede seguir dependiendo de ese dominio aunque exista identidad canónica separada.

La capa que informa de cambios de proveedor es crítica. Distribuir datos y conservar un registro de identidad controlado unilateralmente por el operador dejaría un poder central decisivo. Deben compararse autoridad del titular, delegación recuperable, historial verificable de cambios, disponibilidad del directorio y alternativas de resolución. Copiar un directorio no elimina por sí solo el poder de quien autoriza sus cambios.

### Recuperación sencilla con poder limitado

No se propone pedir al usuario que gestione claves ni elija un comité al registrarse. Debe diseñarse un procedimiento predeterminado comprensible, y después evaluar qué combinación de dispositivos, custodios o medios independientes permite soportar pérdidas y ataques.

Existe una tensión no resuelta: si todo el acceso y la recuperación dependen de la empresa desaparecida, la identidad no es independiente; si la única alternativa es conservar para siempre un secreto irrecuperable, trasladamos el riesgo al usuario. No se puede prometer resolver simultáneamente todos los casos sin un modelo de confianza explícito.

### Datos propios, relaciones y estado compartido

El repositorio personal conserva publicaciones propias y referencias a relaciones. No es autoridad exclusiva sobre el consentimiento de otra persona, la membresía de una comunidad o las sanciones que esta administra.

Hay que clasificar cada dato por autoridad: unilateral del titular, bilateral, comunitaria o derivada. Sin esa distinción, «llevarse los datos» puede convertirse en llevarse permisos que ya no existen o borrar consecuencias de decisiones válidas de otros.

### Copia y restauración

La copia debe incluir lo necesario para recuperar publicaciones y adjuntos, y tener una vía de acceso que no dependa exclusivamente del proveedor que debe sustituir. Una copia bajo la misma cuenta administrativa y el mismo punto de recuperación aporta menos independencia.

Un respaldo cifrado no sirve si la única clave desaparece con el origen. Además, replicar inmediatamente todo cambio puede reproducir un borrado malicioso: conservación de versiones y retirada de contenido requieren políticas distintas y compatibles.

## 5. Qué conviene agrupar en la experiencia ordinaria

Propuesta: un paquete predeterminado integra acceso, alojamiento, archivos y funcionamiento básico de entrega. El usuario recibe una cuenta, sin elegir infraestructura. La copia independiente y el procedimiento de recuperación deben formar parte del diseño del paquete, no quedar como tareas avanzadas.

Recomendaciones, búsqueda, aplicación y almacenamiento adicional son candidatos a sustitución separada, cuando las pruebas justifiquen su viabilidad. El acceso cronológico al contenido seguido no debe requerir un recomendador comercial concreto, aunque seguirá necesitando componentes de entrega y lectura disponibles.

No se recomienda crear doce mercados de proveedores. La primera independencia útil podría ofrecerse mediante cambio del paquete de alojamiento completo, con algunas funciones opcionales separadas. Debe compararse con una división más fina antes de decidir.

## 6. Publicaciones públicas y privadas

Los distribuidores de contenido público pueden mantener índices y copias autorizadas. Los datos privados, intereses privados y contenidos comunitarios restringidos no deben difundirse indiscriminadamente por el mismo mecanismo.

El servicio responsable debe comprobar permisos; ocultar botones no es control de acceso. Si se adopta cifrado de extremo a extremo, cambian búsqueda, moderación, recuperación y administración de miembros. No se considera decidido por esta entrega.

La retirada de un miembro impide accesos futuros conforme al modelo elegido, pero no borra lo que ya pudo copiar. Ninguna propuesta debe prometer deshacer conocimiento previo ni borrar todas las copias externas.

## 7. Servidores voluntarios, alojamiento propio y servicios de pago

Son modalidades de prestación, no arquitecturas completas. Pueden coexistir en un modelo híbrido si cumplen los contratos técnicos y de servicio correspondientes.

- Voluntarios: posibles aportantes de distribución pública, capacidad o alojamiento gestionado. Deben asumir compromisos explícitos; el voluntariado no garantiza continuidad ni significa ausencia de costes.
- Autoalojamiento: opción para personas o entidades que quieran y puedan administrarlo. No debe ser condición para tener derechos ni convertir el ordenador personal en el único lugar donde existe una publicación.
- Pago: puede financiar alojamiento, recuperación, copias o funciones adicionales. El traslado no debe bloquearse por perder una suscripción; hay que prever aviso, transición y política de conservación, sin prometer alojamiento gratuito indefinido.
- Servicio predeterminado financiado: facilita entrada, pero puede concentrar usuarios. Debe evaluarse quién paga sus costes, qué capacidad incluye y cómo se evita convertirlo en punto irremplazable.

No se elige aquí proveedor gratuito, anuncios ni cuotas. La sostenibilidad se analiza junto con el coste real de las garantías.

## 8. Tres candidatas a comparar

| Candidata | Organización | Ventaja | Dependencia o coste principal |
| --- | --- | --- | --- |
| A. Servicio integrado portable | Una instalación presta la experiencia completa; software, datos e identidad permiten una continuación independiente | Menor complejidad inicial | Es preciso demostrar una segunda instalación y continuidad sin el operador original; exportar no basta |
| B. Paquetes de alojamiento sustituibles | Varios operadores pueden ofrecer la misma red; identidad y recuperación no quedan cautivas del alojamiento; extras separables | Equilibrio entre sencillez e independencia | Cambio de ubicación, permisos y estado compartido entre operadores |
| C. Servicios muy descompuestos | Identidad, repositorio, archivos, entrega e índices tienen proveedores separados | Mayor libertad potencial por función | Más dependencias simultáneas, fallos parciales, soporte y coordinación de seguridad |

Preferencia provisional de esta entrega: evaluar B como candidata principal, A como alternativa de menor complejidad y C como límite de modularidad útil. La selección tecnológica permanece abierta.

## 9. Escenarios de fallo y resultado esperado

| Situación | Respuesta que se debe diseñar y probar |
| --- | --- |
| Cierra el operador inicial | Otro operador puede prestar el servicio a identidades y datos recuperables sin permiso del desaparecido |
| Cae el alojamiento de una persona | Copia y procedimiento permiten continuar; la conmutación automática no se promete sin comprobar autoridad y consistencia |
| El alojamiento no coopera | El titular dispone de autoridad independiente para cambiar destino y de copia recuperable |
| Falla un recomendador | Se mantiene una vía básica de lectura; no se pierde contenido ni identidad |
| Falla el distribuidor dominante | Hay ruta alternativa que funciona a escala definida; no basta una API sin operadores |
| Cierra una aplicación | Otra puede acceder a datos y funciones básicas sin credenciales cautivas de la anterior |
| Se roba un dispositivo | Se revoca su autoridad y se aplica recuperación, sin admitir cambios críticos solo por poseer una sesión |
| Desaparece el alojamiento de una comunidad | Su continuidad depende de autoridad y copias comunitarias propias, sin apropiarse de cuentas personales |
| Se adquiere la entidad principal | Se examina qué poderes obtiene el comprador y qué continuidad independiente existe |

No todos los fallos se resuelven con la misma técnica. Recuperar después de una caída, tolerarla sin interrupción y resistir a un operador malicioso son niveles distintos de garantía y coste.

## 10. Dependencias externas que deben permanecer visibles

Dominios, resolución de nombres, proveedores de infraestructura, correo de recuperación, distribución de aplicaciones, notificaciones móviles y pagos pueden constituir puntos de concentración. Tener varios operadores no los elimina automáticamente.

Propuesta: identificar cada dependencia, alcance de daño y alternativa práctica. No intentar reemplazar todo Internet. Priorizar que ninguna dependencia evitable concentre simultáneamente identidad, datos y autorización de salida.

La gobernanza común también puede ser capturada. Debe decidirse quién modifica las reglas y qué significa continuar sin su aprobación. La firma de datos acredita procedencia bajo ciertas condiciones; no resuelve por sí sola la legitimidad de todas las decisiones de gobierno.

## 11. Antecedentes consultados

- [Estructura de AT Protocol](https://atproto.com/guides/the-at-stack): distingue alojamiento personal, relays y servicios de presentación; también enumera amplias funciones que en la práctica agrupa el alojamiento. Sirve para examinar concentración dentro de un diseño modular, no como elección de protocolo.
- [FAQ de Solid](https://solidproject.org/faq): distingue proveedor de identidad y almacenamiento, que pueden coincidir o separarse. Separación conceptual no prueba recuperación independiente de toda identidad.
- [Persistencia en IPFS](https://docs.ipfs.tech/concepts/persistence/): la persistencia requiere conservar contenido en nodos; los servicios de pinning pueden prestar esa función. Distribución no implica conservación automática ni gratuita.

Las recomendaciones del documento son análisis de diseño propio. No son prestaciones acreditadas por estos proyectos. No se han realizado pruebas de arquitectura ni presupuestado operación.

## 12. Siguiente entrega

Comparar A y B mediante los mismos recorridos de alta, publicación pública, publicación privada, recuperación y salida. Identificar la pieza mínima de autoridad independiente y el coste de mantenerla. Describir para cada opción qué datos guarda cada participante, qué puede leer y qué ocurre si desaparece.

Antes de elegir protocolo quedan especialmente abiertas: identidad y recuperación, autoridad de comunidades, modelo de datos privados y alcance de distribución. La transferencia de entrada continúa aplazada.
