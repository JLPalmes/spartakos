---
title: Spartakos — Primer ensayo de traslado individual entre alojamientos
lang: es-ES
license: CC-BY-SA-4.0
date: 2026-10-27
version: 0.1
status: Protocolo de ensayo preparado; sin ejecutar ni adoptar arquitectura de producción
---

# Traslado individual con pérdida del alojamiento de origen

## 1. Pregunta y resultado esperado

Determinar si una persona puede cambiar de alojamiento sin cambiar su identidad ni romper las referencias a sus aportaciones y relaciones, incluso cuando el proveedor de origen deja de cooperar. El traslado es individual. No requiere que los contactos se trasladen ni que configuren sus clientes para cada cambio.

Este ensayo acota los casos E08–E10 del [programa estructural](ENSAYO-01-COMPONENTES-Y-VALIDACION.md), usando el [contrato de datos y autoridad](CONTRATO-DE-DATOS-Y-AUTORIDAD.md). No sustituye los ensayos de cifrado, recuperación de dispositivos y navegador. El simulador social actual sigue siendo de un solo servidor: su exportación no constituye un perfil portable de producción ni debe reutilizarse como prueba de autoridad.

Se deben informar dos resultados separados:

- **Independencia de alojamiento:** cambiar de A a B sin que A autorice o ejecute la salida en ese momento, siempre que existan previamente datos y medios de control independientes.
- **Independencia de la autoridad común:** poder resolver y modificar el destino cuando desaparece la autoridad principal de identidad. Consultar una copia antigua sin poder aceptar cambios nuevos no supera esta condición.

Una prueba con identidades ficticias y autorizaciones simuladas solo valida la organización del flujo; no demuestra ninguna de las dos garantías de control real. Los resultados deben indicar qué verificador auténtico se utilizó o declarar esa parte no ejecutada.

## 2. Alcance mínimo y exclusiones

Primera secuencia: perfil sintético, aportaciones públicas propias y referencias a interlocutores que permanecen en sus alojamientos. IDs estables y versiones se conservan; no se publican de nuevo las aportaciones para simular una recuperación. Una referencia a otra persona no equivale a importar su contenido o consentimiento.

Segunda secuencia: transporte del estado privado propio estrictamente necesario —borradores y preferencias— sin ampliar permisos. El destino no adquiere acceso al historial comunitario por recibir una copia de datos. Lectura y participación dependen de la autoridad comunitaria vigente. No presentar estos archivos como cifrados frente al proveedor si el mecanismo de ensayo no lo proporciona.

Quedan fuera: traslado colectivo, migración desde redes externas, descubrimiento global, reputación, pagos, anuncios, acreditación de servicios, recuperación sin medios previos y disponibilidad frente a la pérdida de toda la máquina. No se incorpora esta prueba a la interfaz social antes de demostrar el flujo y revisar sus límites.

## 3. Topología y separación de autoridad

| Participante | Función | Lo que no debe controlar por sí solo |
| --- | --- | --- |
| Alojamiento A | Estado inicial y atención del origen | Único permiso para salir o única copia recuperable |
| Alojamiento B | Preparación del destino y recepción autorizada | Apropiarse de una identidad al recibir un archivo |
| Cliente de la persona | Solicitar y confirmar el traslado, conservar medios independientes | Delegar silenciosamente su control al destino |
| Mecanismo de identidad R | Resolver control vigente y destino mediante un componente existente | Confundir réplicas de consulta con autoridades alternativas de escritura |
| Respaldo C | Inventario restaurable preparado antes del corte | Dar autoridad de identidad por poseer una copia de contenido |
| Servicio comunitario Q | Mantener roles y audiencia para las pruebas restringidas | Conceder acceso nuevo por el simple traslado personal |

A, B, R y C utilizan procesos, directorios y credenciales de laboratorio separados. Compartir ordenador se declara como límite. La primera prueba no despliega servicios públicos ni registra identidades en directorios de terceros. Un observador sintético permanece en su alojamiento para comprobar referencias sin migrar con la persona.

Q puede residir inicialmente junto a A, pero ese caso debe distinguirse: perder A puede dejar inaccesible esa comunidad aunque el perfil personal se recupere en B. El ensayo no afirma continuidad comunitaria sin respaldo y autoridad comunitarios independientes.

## 4. Condiciones previas a escribir la integración

1. Inventariar los componentes existentes candidatos del programa estructural: versión fija, licencia, instalación local, mantenimiento, persistencia, operaciones de traslado y límites de autoridad. Las referencias anteriores son candidatas documentales y deben verificarse de nuevo antes de usarse.
2. Seleccionar una integración de laboratorio capaz de validar el control de identidad y cambios de ubicación. Si falta ese componente, limitar el trabajo a un arnés de flujo expresamente simulado y declarar E08–E10 pendientes. No inventar un protocolo criptográfico o consenso para superar la falta.
3. Definir cómo comprobar que una operación es vigente y qué sucede ante dos cambios incompatibles. El criterio no puede ser únicamente la fecha aportada por un cliente o un contador elegido por un alojamiento hostil.
4. Preparar datos sintéticos e inventario de referencia antes del corte. Separar comprobación de integridad de comprobación de autoría y autoridad: un hash no acredita las dos últimas.
5. Delimitar qué controles dependen de R y qué recurso independiente permite recuperarlos. No llamar independiente a un respaldo cuyo único acceso o única clave exige contactar con A.

Estas condiciones no eligen todavía el componente de identidad ni un formato definitivo. La selección debe volver con evidencia y compromisos de independencia concretos. No se instalan dependencias ni se compromete el almacenamiento del simulador social como parte de este documento.

## 5. Estado lógico del traslado

| Estado observado | Evidencia exigida | Fallo que debe hacerse visible |
| --- | --- | --- |
| Preparación en B | Inventario recibido y comprobado; B aún no es autoridad de escritura | Datos incompletos, formato no compatible o falta de control válido |
| Cambio solicitado | Operación autorizada por el mecanismo elegido, con referencia verificable | R no disponible o autorización insuficiente; no afirmar traslado completo |
| Cambio confirmado | R reconoce el destino vigente y la regla de autoridad de escritura | Destinos contradictorios o vista obsoleta; no aceptar ambos silenciosamente |
| Comprobación del destino | El observador resuelve la misma identidad y encuentra las referencias previstas | Identidad nueva, objetos duplicados, referencias rotas o pérdida declarada |
| Cierre | Resultado e incidencias registrados, con alcance de los datos conservados | No prometer borrar el origen o copias externas sin evidencia |

Estos estados sirven para observar el ensayo; no constituyen un nuevo protocolo. La activación y la invalidez del antiguo emisor deben derivarse del mecanismo existente que se pruebe. Ante interrupción se reanuda desde evidencia persistida, sin generar otra identidad o repetir envíos. Si el componente no permite resolver de forma segura una bifurcación, el ensayo falla en ese punto.

Las programaciones, avisos y borradores usados no se ejecutan por el mero hecho de copiarse. El ensayo inicial deja inactivos los envíos pendientes del archivo y declara que la reanudación automática entre proveedores no está implementada. La posterior experiencia de activación necesita garantizar un único ejecutor antes de ofrecer continuidad de programación.

## 6. Casos reproducibles

| Caso | Acción | Comprobación y resultado esperado |
| --- | --- | --- |
| T01 — Línea base | Publicar datos sintéticos en A y registrar referencias desde el observador | Inventario de identidad, IDs y versiones, relaciones declaradas y audiencias; sin usar nombres mostrados como identidad |
| T02 — Traslado cooperante | Preparar B y confirmar el cambio conforme al componente | La identidad se conserva; el observador sigue referencias sin trasladarse; la escritura posterior tiene una autoridad vigente |
| T03 — Origen indisponible | Con medios y respaldo ya preparados, detener A antes de solicitar la salida | B puede recibir el control autorizado sin petición exitosa a A; las ausencias del respaldo se informan, no se inventan |
| T04 — Copia sin autoridad | Intentar activar en B el mismo inventario sin los medios de control requeridos | Se deniega apropiarse de la identidad aunque el contenido sea íntegro |
| T05 — Interrupción y repetición | Detener B en cada etapa y repetir la solicitud al recuperarlo | No se crea otra identidad ni se duplican objetos o envíos; la etapa recuperada se justifica con estado persistente |
| T06 — Autoridad anterior | A vuelve e intenta escribir, o entrega una operación antigua | Rechazo o conflicto explícito según el mecanismo; no aceptación silenciosa de dos autoridades |
| T07 — Directorio principal caído | Detener la autoridad principal R y ensayar consulta y cambio de ubicación por separado | Registrar si solo queda lectura obsoleta, si existe autoridad alternativa o si el cambio resulta imposible |
| T08 — Privacidad | Incluir borradores propios y referencias comunitarias restringidas | No se publica el texto privado, no se copian cuerpos ajenos ni se renuevan permisos; Q sigue siendo quien valida participación |
| T09 — Retiradas y referencias utilizadas | Restaurar datos con marcadores y borradores ya consumidos | No reaparece el cuerpo retirado ni se repiten respuesta, edición, aviso o programación |
| T10 — Datos faltantes y corrupción | Omitir un objeto y alterar otro respecto al inventario | Se informa de lo incompleto o inválido y no se presenta el traslado como restauración íntegra |

T03 se repite con respaldo y medios de control disponibles, y después sin alguno de ellos. El segundo resultado no debe inventar recuperación: informa qué capacidad falta. Las operaciones que impliquen borrar contenidos del escenario se prueban con copias sintéticas desechables, nunca con datos del usuario.

## 7. Evidencia que debe conservarse

Informe reproducible con versiones y licencias, topología, directorios y funciones, pasos de corte y recuperación, respuestas observadas, inventarios saneados y errores. Registrar también volumen de datos, duración por etapa, consumo de recursos y pasos manuales como observaciones, sin convertir una ejecución en promesa de rendimiento o coste para operadores voluntarios.

Separar fechas del reloj de prueba de tiempo real de ejecución. No publicar claves, tokens, estados criptográficos ni inventarios reales de usuarios. Las trazas públicas no incorporan topología privada o identificadores personales. El informe debe permitir repetir un fallo con fixtures sintéticos, sin exponer credenciales.

El resultado se añade como suite estructural independiente de las pruebas del simulador social. No aumenta retroactivamente el cumplimiento de E01–E15 ni de A01–A148 por compartir nombres o criterios.

## 8. Puertas de decisión

- Si falla el traslado aun con el origen cooperando, corregir o descartar la integración antes de añadir interfaz social.
- Si funciona sin A, pero depende de una única autoridad R para aceptar cambios, presentar el resultado como independencia del alojamiento con dependencia común de identidad. No dar por satisfecha la resistencia a censura o desaparición de R.
- Si no se pueden rechazar escrituras del origen antiguo, detener el ensayo de autoridad; copiar datos no solventa ese fallo.
- Si los costes o pasos de operación son excesivos, registrar el esfuerzo antes de pedir servicios voluntarios. No delegar decisiones técnicas repetidas en cada persona que se registre o se traslade.

La decisión de aceptar provisionalmente una dependencia común necesita revisión de producto y gobierno. No se presume aprobada por el éxito de un laboratorio. El primer trabajo ejecutable posterior a este protocolo es el inventario verificable y la comparación de componentes de identidad; después puede construirse el arnés aislado con la garantía exacta declarada.
