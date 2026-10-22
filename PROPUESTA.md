---
title: Spartakos — propuesta fundacional
lang: es-ES
license: CC-BY-SA-4.0
status: Borrador preliminar no validado, sustituido como punto de partida por el análisis de requisitos
---

# Spartakos

> Este documento se redactó antes del análisis comparado y no recoge decisiones acordadas. Para continuar el proyecto, consultar ANALISIS-01-SOBERANIA.md. Sus propuestas, prioridades y artículos constitucionales no se consideran aprobados.

Una red de comunidades donde cada persona conserva su identidad, puede decidir cómo participa y puede cambiar de proveedor sin perder su vida social digital.

## Constitución inicial

1. **Soberanía personal.** Cada persona controla su identidad y decide qué publica y con quién. Publicar no transfiere la titularidad del contenido al proveedor; las licencias de distribución deben ser explícitas y limitadas a su finalidad.
2. **Derecho a salir.** Toda persona puede exportar su perfil, publicaciones y preferencias en formatos documentados, y trasladar su identidad a otro proveedor compatible. La migración de relaciones debe respetar el consentimiento y la privacidad de terceros.
3. **Privacidad y consentimiento.** Los datos privados no se hacen públicos por un cambio de condiciones. Los intereses privados no se convierten en reputación pública ni se utilizan para publicidad sin una autorización específica.
4. **Libertad de elección.** Las personas pueden elegir proveedores y sistemas de recomendación. Siempre existe una vista cronológica de sus suscripciones, accesible y sin personalización obligatoria.
5. **Autonomía comunitaria.** Cada comunidad define su propósito, sus permisos y sus reglas dentro de los derechos comunes y de la legislación aplicable. Las restricciones relevantes se conocen antes de entrar.
6. **Debido proceso.** Las decisiones de moderación incluyen motivo, alcance y una vía de recurso. Las medidas urgentes de protección pueden preceder a la revisión, pero deben revisarse.
7. **Pluralidad sin competencia forzada.** No hay una puntuación universal del valor de una persona. Las señales de reputación tienen contexto, son comprensibles y pueden impugnarse.
8. **Transparencia económica.** La publicidad, los patrocinios y las contraprestaciones se identifican. Rechazar publicidad no elimina los derechos fundamentales del usuario.
9. **Interoperabilidad.** Los proveedores no deben crear obstáculos artificiales a la exportación, la migración o el uso de servicios compatibles.
10. **Poder limitado y revisable.** Los cambios constitucionales requieren una propuesta pública, deliberación y un procedimiento de aprobación previamente establecido. Ningún proveedor puede modificar unilateralmente estos derechos.

Esta Constitución expresa compromisos de diseño y gobernanza. Su aplicación requiere contratos, mecanismos técnicos, responsables y un procedimiento de resolución de conflictos. No sustituye la legislación aplicable.

## Experiencia de usuario

La entrada debe ser tan sencilla como en una red convencional: crear una cuenta, elegir intereses y encontrar una primera comunidad útil. La elección de infraestructura puede posponerse mediante un proveedor predeterminado claramente identificado y sustituible.

La soberanía debe manifestarse en acciones comprensibles: «Quién puede leer esto», «Por qué veo esto», «Cambiar mi inicio», «Exportar mis datos» y «Cambiar de proveedor». No debe exigir comprender claves, servidores o protocolos.

La identidad pública persistente debe separarse de las credenciales de acceso y del proveedor de alojamiento. La recuperación de cuenta y el traslado seguro son requisitos iniciales, no mejoras posteriores. Un identificador persistente puede tener costes de privacidad; deben contemplarse seudónimos e identidades separadas.

## Comunidades y permisos

La visibilidad del contenido y la capacidad de actuar son dimensiones independientes. Los permisos pueden concederse por rol y, cuando haga falta, por canal o publicación.

| Modalidad | Leer | Comentar | Publicar |
| --- | --- | --- | --- |
| Pública abierta | Cualquiera | Miembros | Miembros |
| Pública editorial | Cualquiera | Miembros autorizados | Autores autorizados |
| Pública de lectura | Cualquiera | Miembros | Equipo editorial |
| Privada | Miembros admitidos | Según rol | Según rol |
| Privada de difusión | Miembros admitidos | Desactivado o limitado | Equipo editorial |

Los roles iniciales son visitante, miembro, colaborador, moderador y administrador. Un rol no implica automáticamente acceso a todo el historial. El sistema debe explicar si el contenido público puede indexarse, si las invitaciones permiten descubrir la comunidad y qué ocurre con las publicaciones al abandonarla.

## Libertad algorítmica

Cada persona dispone de un inicio cronológico y puede activar recomendaciones por temas, diversidad de fuentes, cercanía social u otros criterios explícitos. Puede restablecer sus preferencias y consultar una explicación útil de cada recomendación.

Las comunidades pueden proponer un orden predeterminado para sus espacios y distinguir contenido destacado. Debe quedar clara la diferencia entre una selección editorial y una recomendación personal. El usuario mantiene el acceso a una vista cronológica del contenido que tiene permiso para ver.

Los algoritmos externos solo reciben los datos necesarios y autorizados. La libertad de elegir algoritmo no autoriza a eludir permisos de acceso ni reglas de moderación.

## Intereses y reputación

**Intereses privados:** temas que la persona quiere seguir o aprender, declarados y editables. No implican competencia y pueden mantenerse fuera del perfil público. Los intereses inferidos deben poder consultarse, corregirse y borrarse.

**Presentación pública:** especialidades e intereses que la persona decide mostrar. Una especialidad autodeclarada debe distinguirse de una señal respaldada por contribuciones o reconocimientos.

**Reputación contextual:** señales por tema y comunidad, basadas en aportaciones útiles y reconocimientos con contexto. Sin contador global, clasificaciones públicas, rachas ni avisos para incentivar su aumento. Su presentación debe favorecer información cualitativa y procedencia antes que cifras.

La reputación requiere defensas frente a grupos que se puntúan entre sí, acoso y cuentas artificiales. No debe convertirse por defecto en requisito de voz, visibilidad o acceso. El usuario puede ocultar reconocimientos en su perfil, pero no borrar las decisiones de moderación que una comunidad necesite conservar legítimamente.

## Importación y derecho a irse

La importación comienza con archivos que el usuario obtiene de otras redes y, cuando sea viable y esté autorizado, con sus interfaces oficiales. Antes de incorporar datos se muestra una previsualización con autoría, fechas, adjuntos y visibilidad.

No se promete importar relaciones, mensajes privados ni contenidos ajenos cuando no exista permiso o capacidad técnica. Los contactos encontrados se ofrecen como sugerencias; no se recrean seguimientos ni consentimientos de terceros automáticamente.

La exportación incluye contenido propio, perfil, archivos adjuntos, preferencias y relaciones exportables. Debe documentar qué no incluye y por qué. El cambio de proveedor necesita comprobarse mediante una migración real a una segunda implementación compatible.

La eliminación debe propagarse entre proveedores según reglas explícitas, con acuses y límites visibles. No se puede garantizar borrar capturas, copias externas o contenido ya distribuido a destinatarios fuera del control de la red.

## Proveedores y sostenibilidad

El modelo admite proveedores distintos para identidad, alojamiento, búsqueda, recomendaciones y otros servicios. La separación debe introducirse gradualmente: cada dependencia adicional añade costes de soporte, privacidad y coordinación.

Los ingresos pueden combinar suscripciones, cuotas comunitarias, servicios gestionados y publicidad voluntaria. Si una persona acepta anuncios, debe saber qué beneficio recibe, qué datos se utilizan y cómo revocar el acuerdo. Una primera opción a evaluar es publicidad contextual sin compartir el historial privado.

La identidad, la portabilidad y los permisos no deben depender de un proveedor publicitario. La independencia real exige formatos abiertos, pruebas de compatibilidad y alternativas operativas, además de declaraciones de principios.

## Gobernanza

Conviene separar tres ámbitos: la entidad que custodia la Constitución y la compatibilidad del protocolo, los proveedores que prestan servicios y las comunidades que gobiernan sus espacios.

Quedan por definir la representación de usuarios, comunidades y proveedores; el procedimiento de reforma; la financiación de los bienes comunes; las incompatibilidades; y la instancia de recurso. La descentralización técnica no resuelve por sí sola la concentración de poder.

## Primera versión

Empezar con una comunidad concreta que tenga una necesidad compartida. La hipótesis es que un espacio útil, comprensible y con control efectivo de permisos ofrece un motivo suficiente para regresar.

El alcance inicial incluye cuenta recuperable, perfil, publicaciones y comentarios, comunidades públicas y privadas, permisos por rol, inicio cronológico, preferencias temáticas explícitas, moderación con recurso e importación de un formato de archivo seleccionado tras comprobar su viabilidad.

La exportación completa y una prueba de traslado entre dos proveedores forman parte de la validación inicial. El mercado de algoritmos, la reputación automatizada y la publicidad con contraprestación quedan para fases posteriores.

## Hipótesis y validación

No se presupone una causa universal del escaso crecimiento de otras iniciativas. Antes de elegir protocolo o arquitectura debe contrastarse qué obstáculos afectan al público elegido: falta de contactos, dificultad de entrada, moderación, fiabilidad, sostenibilidad o ausencia de una razón para volver.

Las pruebas iniciales deben observar si una persona entra sin asistencia, comprende quién verá sus publicaciones, encuentra una conversación útil, configura su inicio y consigue exportar y trasladar su cuenta. Las métricas de comunidad deben medir utilidad y salud de las conversaciones, no solo tiempo de permanencia.

## Decisiones pendientes

- Público y primera comunidad a los que servir.
- Qué significa identidad soberana en el modelo de amenazas elegido y cómo se recupera.
- Protocolo existente o componentes propios, tras evaluar permisos, migración y moderación.
- Jurisdicción, entidad responsable y obligaciones de los proveedores.
- Costes de funcionamiento y disposición a pagar.
- Representación y procedimiento para aprobar la Constitución.
