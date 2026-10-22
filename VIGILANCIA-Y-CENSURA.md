---
title: Spartakos — Vigilancia y resistencia a la censura
lang: es-ES
license: CC-BY-SA-4.0
version: 0.1
date: 2026-10-22
status: Análisis y medidas propuestas; garantías pendientes de validación
---

# Vigilancia y resistencia a la censura

## 1. Objetivos diferentes

Proteger contenido privado, reducir identificación y seguimiento, preservar acceso al servicio y permitir continuidad ante retirada de infraestructura son objetivos distintos. Una red puede resistir el cierre de un servidor y seguir exponiendo relaciones, direcciones IP o contenidos legibles por sus operadores.

La descentralización aporta alternativas, pero también multiplica operadores que pueden observar datos o sufrir presión. No equivale a anonimato ni elimina la capacidad de un Estado de bloquear acceso a Internet, intervenir dispositivos o actuar sobre personas.

El modelo incluye observación de red, requerimientos a proveedores, incautación de nodos, infiltración de comunidades, captura de servicios de identidad, bloqueo DNS/IP y retirada de aplicaciones. La protección debe evaluarse frente a adversarios concretos, sin prometer invulnerabilidad.

## 2. Superficies y controles

| Superficie | Exposición | Medida propuesta | Límite |
| --- | --- | --- | --- |
| Tráfico de acceso | IP, horarios y volumen | Transporte cifrado y compatibilidad con herramientas de privacidad | Cifrado de transporte no oculta todos los metadatos |
| Nodo de alojamiento | Perfil, datos y registros que recibe | Minimización, separación de autoridad y controles de administración | Si conserva texto legible, puede acceder a él |
| Copias | Datos históricos y claves | Cifrado y recuperación separada; versiones y retención acotadas | Custodios con capacidad suficiente pueden acceder o coludirse |
| Identidad | Vinculación entre cuentas y servicios | Seudónimos separados y datos mínimos de resolución | Un identificador público persistente facilita correlación |
| Comunidad | Miembros, conversaciones y relaciones | Membresía oculta cuando corresponda; permisos; evaluar E2EE | Un miembro autorizado puede copiar o informar |
| Índices | Contenido público y grafo social | No indexar datos restringidos; opciones de descubrimiento | Publicar en abierto permite observación externa |
| Distribución | Dependencia de nodos, dominios o aplicaciones | Varios operadores y vías de acceso verificadas | Alternativas pueden compartir infraestructura o ser bloqueadas |

## 3. Base de protección incorporable al piloto

- No exigir nombre civil, teléfono o identidad de otra plataforma por defecto. Recuperación debe evitar que esta minimización haga imposible el uso ordinario.
- Evitar directorio público que relacione seudónimos, intereses privados, correos o medios de recuperación.
- No realizar conexiones directas entre dispositivos de participantes por defecto: evitar que leer o conversar revele mutuamente sus IP. P2P requiere análisis específico antes de activarse.
- Reducir registros con IP completa, identificadores persistentes y grafos de interacción. Separar seguridad, diagnóstico y métricas; documentar finalidad, duración y accesos. Los 30 días de registros ordinarios de la especificación no justifican conservar todo metadato durante ese plazo.
- Propuesta para ensayo: no persistir IP completa en registros de aplicación salvo necesidad de seguridad delimitada; cuando se necesite, ventana inicial de hasta 24 horas, con excepción documentada y revisión. Inventariar también proxy, infraestructura, copias y proveedores, que pueden conservar otros registros.
- No incluir texto privado en notificaciones externas, analítica, correo o informes de error por defecto. Revisar miniaturas, previsualizaciones y peticiones a servicios externos que revelen qué se está leyendo.
- Eliminar metadatos de localización de medios compartidos cuando proceda, con explicación y conservación privada del original solo si se ofrece explícitamente.

## 4. Cifrado y usos de riesgo elevado

La versión propuesta del piloto usa controles de acceso para comunidades restringidas y no promete E2EE. Por tanto, no debe presentarse como refugio seguro frente a un adversario capaz de acceder a servidores. La evaluación de E2EE pasa a ser una decisión arquitectónica temprana, aunque su implementación pueda quedar para una fase posterior.

Comparar grupos cifrados con mecanismos existentes revisados: incorporación y expulsión, verificación de miembros/dispositivos, búsqueda, copias, recuperación de claves y moderación. No implantar criptografía propia. La recuperación asistida de identidad no debe conceder silenciosamente lectura de todas las conversaciones cifradas anteriores.

El E2EE protege contenido en determinadas condiciones, pero no evita dispositivos comprometidos, copias por interlocutores ni todos los metadatos. EFF describe expresamente estas diferencias [V1].

## 5. Acceso frente a bloqueos

Proponer cliente web utilizable sin tienda de aplicaciones, software instalable por operadores independientes y varias vías de acceso documentadas. Evaluar diversidad efectiva de dominios, proveedores de infraestructura y administración; varias marcas sobre la misma dependencia no acreditan resistencia.

Ensayar compatibilidad con Tor Browser sin rastreadores, captchas excluyentes ni bloqueo indiscriminado por IP compartida. Aplicar controles contra abuso que no dependan solo de IP. Un servicio onion es candidato adicional, no requisito ya decidido; necesita operación y verificación propias.

Publicar endpoints alternativos autenticados mediante un mecanismo de confianza preestablecido. La firma prueba el origen del anuncio, no que el endpoint siga siendo seguro. No redirigir silenciosamente credenciales o contenido privado a supuestos espejos descubiertos por terceros.

Tor ofrece mecanismos frente a ciertos bloqueos; su documentación también reconoce límites frente a correlación de tráfico por adversarios con observación suficiente [V2]. No integrarlo como promesa de anonimato absoluto ni exigir configuración manual de red a todo usuario.

La recuperación debe funcionar sin depender exclusivamente del dominio bloqueado. Distinguir servicio caído, dirección bloqueada y cuenta comprometida. Si hay corte total de conectividad, conservar borradores locales cuando sea seguro; no prometer acceso remoto inexistente.

## 6. Presión institucional y procedimientos de retirada

Los operadores necesitan un procedimiento para verificar procedencia, competencia, alcance y datos solicitados de requerimientos recibidos, obtener revisión competente y limitar actuaciones al ámbito exigible. No prometer desobediencia universal, inmunidad por distribuir nodos ni acceso secreto para autoridades.

Registrar decisiones de forma restringida, permitir impugnación cuando proceda, informar a afectados cuando sea posible y publicar informes agregados de transparencia sin revelar datos sensibles o información cuya comunicación esté limitada. Una retirada o bloqueo debe identificar si nace de moderación comunitaria, política de alojamiento o requerimiento externo cuando sea comunicable.

Diseñar para conservar menos información innecesaria reduce exposición; no equivale a eliminar evidencia selectivamente tras recibir un requerimiento. La respuesta normativa depende de jurisdicción y requiere asesoramiento competente. La distribución geográfica aporta continuidad potencial, no exención de obligaciones.

## 7. Diagnóstico y riesgos para participantes

La red puede consultar evidencia pública y hacer pruebas controladas de bloqueo. No convertir clientes de personas en sondas de censura por defecto ni publicar diagnósticos de su conexión sin consentimiento específico. OONI documenta utilidad y riesgos de sus mediciones; observar un fallo no basta para atribuirlo a censura [V3].

Un nodo voluntario no debe anunciarse como resistente a incautación sin pruebas y capacidad de operación. El directorio de operadores debe equilibrar transparencia con minimización de datos personales innecesarios de voluntarios.

## 8. Criterios de validación y prioridades

Antes del lanzamiento público: inventario de metadatos y terceros, retirada de rastreadores, prueba de seudónimos separados, acceso sin tienda, ensayo Tor, procedimiento de requerimientos y comunicación honesta sobre privacidad del contenido restringido.

Antes de ofrecer protección de alto riesgo: revisión externa del modelo de amenazas, resolución de E2EE y recuperación, análisis de metadatos y pruebas de continuidad bajo bloqueo/incautación. La protección reforzada no debe depender exclusivamente de un servicio comercial.

Estas medidas amplían el programa de evaluación. No están implementadas ni ensayadas por existir este documento.

## Fuentes

- **V1.** [EFF: cifrado y sus límites](https://ssd.eff.org/module/what-should-i-know-about-encryption) y [metadatos](https://ssd.eff.org/glossary/metadata).
- **V2.** [Tor: ataques y límites](https://support.torproject.org/about-tor/security/attacks-on-onion-routing/) y [acceso desde regiones con censura](https://support.torproject.org/tor-browser/circumvention/connecting-from-censored-regions/).
- **V3.** [OONI: proyecto](https://ooni.org/about/) y [riesgos de medición](https://labs.ooni.io/about/risks/).
- [RFC 6973: consideraciones de privacidad](https://www.rfc-editor.org/info/rfc6973/). Referencia de análisis de protocolos; no certificación de Spartakos.
