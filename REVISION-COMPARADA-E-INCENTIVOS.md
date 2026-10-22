---
title: Spartakos — Revisión comparada, migración e infraestructura voluntaria
lang: es-ES
license: CC-BY-SA-4.0
version: 0.1
date: 2026-10-22
status: Evaluación documental crítica; ventajas e incentivos sin validación de campo
---

# Revisión comparada e incentivos

## 1. Dictamen

Spartakos tiene una orientación coherente y diferencias de diseño potencialmente valiosas, pero todavía no ventajas operativas demostradas. La especificación combina soluciones conocidas con elecciones normativas propias. No se puede afirmar que haya resuelto un problema porque haya descrito la solución deseada y escrito su prueba de aceptación.

La suficiencia de los incentivos de migración y de aportación de infraestructura no está acreditada. El mayor déficit de adopción es el valor inmediato para una persona cuyos contactos no participan; el mayor déficit de oferta voluntaria es la carga previsible de operar, proteger y abandonar un servicio sin perjudicar a sus usuarios.

Recomendación: conservar los principios y completar la propuesta de valor individual y el contrato de colaboración voluntaria antes de fijar tecnología. No añadir funciones por acumulación para aparentar diferenciación.

## 2. Método y límites

Se compara cada propuesta con antecedentes en su función correspondiente: redes generales, comunidades, comunicación privada, datos personales y operación cooperativa. No se establece un ranking global entre productos de finalidades diferentes. Los orígenes de migración son distintos de los referentes de diseño.

Documentación oficial acredita mecanismos declarados; estudios originales aportan observaciones de poblaciones y periodos concretos. No se atribuye fracaso universal a una iniciativa ni se interpreta una correlación como causa suficiente. Tampoco se da por inexistente una función porque no se haya encontrado en esta revisión.

El estado actual de Spartakos es diseño documental: sin aplicación, migraciones ejecutadas, prueba con usuarios ni operadores reclutados. Esta asimetría de madurez cuenta en toda comparación.

## 3. Comparación por problema

| Problema | Antecedente contrastado | Propuesta de Spartakos | Evaluación crítica |
| --- | --- | --- | --- |
| Cuenta dependiente del alojamiento | Hubzilla documenta identidad nómada y clones; AT Protocol documenta cambio de alojamiento | Identidad persistente, copia y traslado sin permiso exclusivo del origen | No es novedad. La ventaja dependerá de continuidad, facilidad y recuperación efectivamente probadas |
| Traslado que pierde historial | Mastodon documenta límites de reimportación de publicaciones y medios | Conservar originales, adjuntos y referencias | Mejora potencial frente a ese límite, no superioridad demostrada frente a todas las redes |
| Datos y aplicación cautivos | Solid distingue proveedor de identidad y almacenamiento | Servicios sustituibles con experiencia integrada | Debemos demostrar que esa integración no exige configuración ni centraliza de nuevo autoridad |
| Algoritmo impuesto | Bluesky ofrece feeds de terceros y valores predeterminados | Cronología básica y descubrimiento opcional | Paridad conceptual; ventaja posible en comprensión y ausencia de presión, no en inventar la elección |
| Comunidades con roles | Lemmy y Discourse ofrecen espacios y administración; Discourse separa numerosos permisos por grupos | Plantillas y poderes delimitados | Función ampliamente ensayada. Hace falta probar sencillez y convivencia distribuida |
| Reputación que se vuelve escala de privilegios | Discourse documenta confianza y permisos; Stack Overflow vincula puntos con privilegios | Evidencia temática sin puntuación universal | Diferencia de objetivo. Puede reducir competición, pero también perder una señal útil: debe compararse con alternativas simples |
| Confidencialidad de grupos | Signal y Matrix tienen soluciones de cifrado y clientes operativos | Modelo mixto con cifrado todavía en evaluación | Desventaja de madurez. No existe aún una ventaja de protección frente a herramientas operativas |
| Autonomía y retirada de contenido | Manyverse reconoce límites de borrado en copias distribuidas | Retirada propagada y versiones con conservación acotada | Tratamiento necesario, pendiente de demostrar ante desconexión, archivos y respaldos |
| Continuidad del operador | Covenant de Mastodon exige backups, acceso de emergencia y aviso de cierre a servidores recomendados | Respaldo independiente, sustitución y autoridad separada | Parte de la respuesta ya existe como compromiso operativo; exigir más implica financiar y organizar más |
| Gobierno no corporativo | Social.coop documenta cooperación, aportaciones y grupos de trabajo | No propiedad del promotor y gobierno compartido | Hay precedentes. La especificación aún debe concretar censo, capacidad de sustitución y carga de participación |
| Costes de bienes comunes | Lemmy solicita apoyo recurrente; PeerTube presenta aportaciones diversas y donaciones | Base voluntaria y servicios comerciales no imprescindibles | Plausible como modelo, insuficiente como plan de provisión y continuidad |
| Arranque sin contactos | Bluesky usa colecciones de cuentas y feeds recomendados | Explorar y reencuentro diferido | El reencuentro no crea actividad presente; la selección inicial necesita personas, contenido y mantenimiento reales |

Fuentes: [Hubzilla](https://help.hubzilla.hu/en/basicconcepts.html), [AT Protocol](https://atproto.com/guides/account-migration), [Mastodon](https://docs.joinmastodon.org/user/moving/), [Solid](https://solidproject.org/faq), [feeds de Bluesky](https://bsky.social/about/blog/7-27-2023-custom-feeds), [Lemmy](https://join-lemmy.org/?lang=en), [Discourse](https://blog.discourse.org/2018/06/understanding-discourse-trust-levels/), [Stack Overflow](https://stackoverflow.com/help/whats-reputation), [Matrix](https://matrix.org/docs/matrix-concepts/end-to-end-encryption/), [Signal](https://signal.org/blog/phone-number-privacy-usernames/), [Manyverse](https://www.manyver.se/faq/permanence/), [Covenant](https://joinmastodon.org/covenant), [Social.coop](https://wiki.social.coop/wiki/Main_Page), [Lemmy: apoyo](https://join-lemmy.org/support), [PeerTube: contribuciones](https://joinpeertube.org/contribute), [starter packs](https://bsky.social/about/blog/06-26-2024-starter-packs).

Los bloques de revisión anteriores detallan Nostr, IndieWeb/POSSE, Friendica, Diaspora* y extensiones de identidad portable. Aportan precedentes de autoría, control del original y traslado, pero su cobertura no acredita superioridad global. El estudio de todos los derivados o iniciativas históricas no es exhaustivo; no se presenta como tal.

## 4. Dónde podría haber una ventaja clara

### 4.1 Una experiencia integrada coherente

La combinación más prometedora es: identidad portable, comunidades con garantías claras, historial utilizable e interacción sin competición, todo con configuración mínima. La ventaja sería completar recorridos mejor que combinar herramientas separadas. Esa afirmación necesita comparación de tareas y no puede deducirse de una lista más larga de funciones.

### 4.2 Autonomía de atención coherente en todo el producto

Interés privado, ausencia de puntuación personal y avisos centrados en utilidad ofrecen una dirección clara. Cambiar «me gusta» por «coincido» no basta: si se mantiene total destacado, recompensa, ranking o impulso de alcance, se reproduce el incentivo. Es una ventaja normativa defendible y una ventaja de experiencia todavía por probar.

La menor actividad visible no debe interpretarse automáticamente como fracaso. Hay que comprobar utilidad y regreso intencional, no maximizar sesiones. Al mismo tiempo, no confundir un producto vacío o confuso con serenidad: la autonomía necesita contenido útil y relaciones reales.

### 4.3 Garantías comunitarias explícitas

Unanimidad para abrir una comunidad privada, ausencia de propiedad del fundador y sustitución de administración son compromisos concretos. No se afirma que sean exclusivos. Su ventaja potencial es credibilidad si la interfaz y el gobierno los hacen exigibles.

La unanimidad también bloquea cambios cuando falta consentimiento; no se considera un fallo a corregir mediante una excepción. Debe existir continuidad privada viable y una nueva comunidad pública independiente como alternativa, sin apropiación de miembros o historial.

### 4.4 Continuidad que no depende del titular del servidor

Puede diferenciar si funciona incluso con operador inaccesible o no cooperante. Pero guardar copias no resuelve control de identidad ni financiación de restauración. La dependencia de directorio común sigue abierta; no hay problema resuelto mientras solo exista una réplica de lectura.

## 5. Problemas conocidos todavía abiertos

| Problema | Situación actual | Evidencia que falta |
| --- | --- | --- |
| Arranque social | Diseño de exploración y contactos pendientes | Personas encuentran actividad útil sin traer amigos ni organizar grupos |
| Recuperación soberana | Alternativas y límites documentados | Recuperar autoridad sin alojamiento ni apropiación por custodio |
| Continuidad de identidad común | Directorio y réplicas como candidatos | Cambios válidos tras caída o censura de autoridad común |
| Privacidad frente a operadores | Modelo mixto en estudio | Cliente, claves, archivo, metadatos y recuperación verificados |
| Sostenibilidad gratuita | Cuotas y fuentes posibles | Recursos comprometidos, coste medido y relevo real |
| Moderación distribuida | Procedimientos descritos | Personas disponibles, formación, carga y recursos de revisión |
| Importación completa | Vías documentadas | Corpus de exportaciones, pérdidas y recorrido sin asistencia |
| Gobierno representativo | Ámbitos propuestos | Censo, resistencia a abuso y legitimidad de sustitución |

Ninguno de estos problemas se declara solucionado por contar con un criterio de aceptación. Las pruebas de aceptación definidas no son resultados ejecutados.

## 6. Incentivos para llegar y para quedarse voluntariamente

### 6.1 Distinguir tres capas de valor

**Valor individual inmediato:** biblioteca recuperable de trayectoria propia, búsqueda y guardados privados, perfil estable y publicación legible. Debe servir antes de que los contactos estén aquí. El archivo es candidato a puerta de entrada, pero importarlo debe ser mucho más sencillo que gestionar carpetas externas; falta demostrarlo.

**Valor social presente:** conversaciones, respuestas y fuentes útiles disponibles desde el inicio. No basta con almacenar la referencia de contactos ausentes. Necesitamos disponibilidad editorial y de participación, sin exigir al recién llegado reclutar a nadie.

**Garantía futura:** derecho a irse, límites de poder y control de atención. Puede motivar confianza, pero rara vez sustituye por sí sola utilidad presente para quien está satisfecho con sus relaciones actuales. Es hipótesis de producto, no ley universal del comportamiento.

### 6.2 Diferencias entre personas

| Necesidad de llegada | Incentivo potencial | Déficit actual |
| --- | --- | --- |
| Buscar conversación útil y tranquila | Comunidades legibles, control de avisos y bajo coste de participación | No hay contenido ni respuesta disponibles todavía |
| Conservar trayectoria propia | Historial importado, referencias y salida | Importadores sin probar y organización por validar |
| Publicar conocimiento o recursos | Piezas desarrolladas, contexto y archivo estable | Audiencia inicial reducida y descubrimiento no probado |
| Mantener contactos personales | Reencuentro y continuidad de vínculos | Los contactos pueden no participar; una lista no los sustituye |
| Conservar gran audiencia profesional | Menor dependencia de plataforma | Ofrecemos menos alcance inicial y sin mecanismos de amplificación probados |
| Comunicación especialmente sensible | Cifrado y protección ante vigilancia | Sin garantías operativas acreditadas; no es promesa de captación válida aún |

Conclusión: incentivos plausibles para necesidades específicas; no suficientes demostrados para migración generalista masiva. Red generalista no obliga a captar a todo el mundo a la vez ni a especializar permanentemente el producto.

### 6.3 Migración gradual individual

No pedir cerrar la cuenta de origen, trasladar amigos en grupo ni elegir exclusividad. Permitir probar lectura, guardar contenido y traer parte del historial antes de decidir dónde publicar habitualmente. La llegada individual puede ser gradual y convivir con cuentas externas sin requerir interoperabilidad.

POSSE es un precedente de convivencia, pero su sindicación no se convierte en nuevo requisito de Spartakos [E08]. Enlazar un perfil o exportar contenido propio puede facilitar transición; no se añade ahora un sistema de publicación simultánea.

### 6.4 Evidencia empírica relevante y límites

Un estudio de adoptores académicos encontró que su conectividad interna no bastó para mantener la transición y observó asociaciones con interacción entre servidores y comunidades temáticas. No demuestra que toda migración fracase ni prescribe llegada colectiva. Sí impide asumir que contactos conservados equivalen a participación sostenida [E01].

La investigación sobre starter packs de Bluesky estudia beneficios y problemas de descubrimiento social a gran escala. Su resultado no se traslada automáticamente a nuestro producto: el objetivo aquí no es aumentar seguidores o reacciones. La lección a probar es reducir búsqueda inicial de fuentes útiles, con selección revisable y sin seguimiento masivo obligatorio [E02].

## 7. Incentivos para aportar servicios voluntarios

### 7.1 El vacío actual

La especificación describe lo que necesita de un operador con más claridad que lo que le ofrece. Para reclutar, la propuesta debe responder: qué aporta, para quién, cuánto trabajo y gasto acepta, qué apoyo obtiene y cómo puede dejarlo.

Los estudios de administradores de Mastodon documentan motivaciones comunitarias y de privacidad, junto con cargas de gobierno, moderación y recursos. Son evidencia de que la motivación existe y de que no basta para hacer sostenible cualquier compromiso; no estiman nuestra capacidad futura [E03, E04].

### 7.2 Perfiles de aportación

| Participante posible | Beneficio no coercitivo | Oferta de colaboración propuesta |
| --- | --- | --- |
| Asociación o entidad cívica | Cumplir misión y disponer de infraestructura social autónoma | Alojar capacidad acotada sin apropiarse de cuentas, con soporte y salida |
| Persona con conocimientos técnicos | Aprender, contribuir y usar un servicio útil | Tareas pequeñas, instalación repetible, límites y comunidad de apoyo |
| Entidad que aporta capacidad | Destinar recursos a un bien común con resultado verificable | Compromiso concreto de almacenamiento/entrega, costes visibles y reconocimiento institucional opcional |
| Moderador o facilitador | Cuidar un entorno relevante | Formación, respaldo, cobertura y rotación; no guardia ilimitada |
| Desarrollador, traductor o diseñador | Resolver problemas visibles y participar en proyecto abierto | Tareas delimitadas, revisión previsible y reconocimiento de autoría |
| Servicio comercial complementario | Actividad económica compatible con misión | Interfaces estables y competencia abierta; sin derecho exclusivo sobre base gratuita |

Reconocer una aportación al proyecto no implica otorgar puntos sociales, reputación temática o votos adicionales. La contribución no debe convertirse en jerarquía de personas ni en obligación de visibilidad pública.

### 7.3 Catálogo mínimo antes de reclutar

Ofrecer compromisos acotados, inicialmente en cuatro modalidades: alojamiento con capacidad declarada; respaldo cifrado sin claves de lectura por su rol; entrega de contenido público; tareas de soporte/documentación/moderación con turnos definidos. No todas las modalidades comparten exposición, obligaciones o conocimientos.

Para cada modalidad: tarea, capacidad, presupuesto propio máximo, tiempo estimado a medir, acceso necesario, exclusiones, formación, responsable de apoyo y procedimiento de salida. No pedir instalar un servidor completo para contribuir un recurso pequeño.

La separación técnica solo atrae aportantes si disminuye carga real. Si cada rol requiere administrar la pila entera, la modularidad no constituye incentivo.

### 7.4 Reducir sacrificios antes de prometer reconocimiento

Instalación repetible, actualización y reversión, prueba de restauración, alertas de bajo ruido, diagnóstico saneado, calendario de mantenimiento y ruta de relevo. Límites de altas y recursos bajo control operativo, sin conferir propiedad sobre cuentas. Un voluntario puede rechazar ampliar compromiso; eso no cancela lo ya acordado ni autoriza eliminar datos de improviso.

Apoyo común para incidentes, moderación y requerimientos; explicar capacidad real y responsabilidades sin prometer cobertura inexistente. Ningún voluntario se compromete implícitamente a disponibilidad permanente por instalar software. No reclutar a personas en entornos de riesgo sin explicar la exposición del rol.

Donaciones y reembolso de costes o apoyos documentados pueden sostener trabajo; no convierten el acceso básico en pago obligatorio. Social.coop muestra aportaciones económicas, trabajo y procedimientos de gasto, pero su modelo de cuotas no es el modelo de acceso propuesto para Spartakos [E05]. PeerTube ofrece varias formas de contribuir y pide apoyo económico; Lemmy explicita necesidad de apoyo recurrente [E06, E07]. La lección es organizar y financiar tareas, no copiar una obligación de pago.

### 7.5 Bienes comunes sin atractivo comercial directo

Identidad, recuperación, coordinación de incidentes y mantenimiento de contratos pueden resultar esenciales y poco atractivos para aportar aisladamente. No asumir que el mercado de extras los financiará. Hace falta identificar quién los sostiene y cómo se sustituyen antes de prometer continuidad.

Dos servidores subvencionados por una misma entidad tampoco garantizan independencia. Deben distinguirse diversidad de máquinas, administradores, financiación y autoridad. La fase de pruebas puede compartir origen, con límites declarados.

## 8. Mejoras recomendadas para la especificación

| Acción | Cambio propuesto | Prioridad |
| --- | --- | --- |
| C01 | Definir una utilidad individual de primera sesión y una de segunda sesión, sin contactos presentes | Antes de fijar producto mínimo |
| C02 | Plan editorial y de participación inicial con recursos comprometidos, sin exigir mudanzas colectivas | Antes de altas generales |
| C03 | Llegada gradual: probar, importar parcialmente y permanecer también fuera | Diseño funcional |
| C04 | Comparar recorridos con herramientas existentes, no solo promesas | Revisión funcional y prototipo |
| C05 | Catálogo de compromisos voluntarios con límites, apoyo y salida | Antes de reclutar infraestructura |
| C06 | Presupuesto de bienes comunes y responsables concretos | Antes de garantizar continuidad pública |
| C07 | Ensayar sustitución y recuperación con operador retirado | Antes de anunciar soberanía efectiva |
| C08 | Validar comprensión y presión social de interacción y reputación | Antes de adoptar esos mecanismos |

Las acciones son recomendaciones de esta revisión, no modificaciones automáticas de principios o nuevas obligaciones de usuarios. No se proponen incentivos adictivos, propiedad del fundador, publicidad obligatoria, migración colectiva ni puntos por voluntariado.

## 9. Programa de validación previo a desarrollo completo

**Usuarios individuales:** comparar un recorrido equivalente con la herramienta que ya usan o un referente funcional pertinente. Prototipo sin marca cuando sea útil; muestra diversa y pequeña al principio, sin presentar cifras como representativas. Medir tarea completada, ayuda requerida, valor percibido, razón para volver deliberadamente y capacidad de recuperar trabajo. No retención compulsiva.

**Historial y contactos:** pruebas separadas de archivo y utilidad social. Comprobar que el importador reduce trabajo respecto a gestionar la exportación por cuenta propia y que el descubrimiento ofrece contenido presente. No usar un contador restaurado como evidencia de contactos activos.

**Operadores voluntarios:** entrevistas primero, sin pedir compromisos ilimitados; después ensayo de tarea acotada con retirada incluida. Medir instalación, actualizaciones, incidentes, coste real, horas, llamadas de apoyo y motivos de abandono. Una declaración favorable a la misión no cuenta como servicio comprometido.

**Disponibilidad:** inventario por rol, capacidad y dependencia, con responsable de relevo. Antes de abrir altas, evidencia de funciones esenciales cubiertas y un plan de transición. No fijar una cifra universal de operadores antes de definir carga y tolerancia a fallos.

**Decisión:** continuar si existe ventaja verificable en tareas prioritarias y recursos sostenibles; ajustar diseño si la ventaja es pequeña o exige demasiada ayuda; reducir alcance o reconsiderar construcción propia si un proyecto existente cubre mejor el recorrido. No sostener una arquitectura solo porque ya se haya documentado extensamente.

No se ha contactado con participantes, reclutado operadores ni realizado estos ensayos. No hay evidencia actual para afirmar incentivos suficientes.

## 10. Fuentes empíricas y operativas

- **E01.** Wang, Koneru y Rajtmajer, [The Failed Migration of Academic Twitter](https://ojs.aaai.org/index.php/ICWSM/article/view/42757), publicación de 2026. Cohorte concreta observada durante un año; no tasa universal de fracaso.
- **E02.** Balduf y colaboradores, [Bootstrapping Social Networks: Lessons from Bluesky Starter Packs](https://arxiv.org/abs/2501.11605), 2025. Estudio de descubrimiento y actividad; no prueba de bienestar ni de adecuación a Spartakos.
- **E03.** Zhang y colaboradores, [Trouble in Paradise?](https://www.cs.ox.ac.uk/files/15025/Zhang_et_al_2024_Trouble_in_paradise.pdf), 2024. Entrevistas con 16 administradores; muestra cualitativa, no estimación representativa de toda la red.
- **E04.** Anaobi y colaboradores, [Will Admins Cope?](https://arxiv.org/abs/2302.05915), 2023. Estudia carga de moderación y recursos; no fija el coste de Spartakos.
- **E05.** Social.coop: [organización](https://wiki.social.coop/wiki/Main_Page), [estatutos](https://wiki.social.coop/wiki/Bylaws), [gastos](https://wiki.social.coop/wiki/Submitting_an_expense). Políticas operativas consultadas, no garantía de resultados de nuestro diseño.
- **E06.** [PeerTube: contribuciones](https://joinpeertube.org/contribute). Organización de aportaciones y financiación, sin equivalencia de costes entre vídeo y nuestra primera versión.
- **E07.** [Lemmy: apoyo al desarrollo](https://join-lemmy.org/support). Necesidad declarada de financiación recurrente; no se extrapolan importes.
- **E08.** [IndieWeb/POSSE](https://indieweb.org/POSSE). Precedente de convivencia; sindicación fuera del alcance de esta recomendación.

Fecha de revisión: 22 de octubre de 2026. Fuentes con años diferentes se interpretan en su contexto; los diseños propuestos son razonamiento propio.
