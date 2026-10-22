---
title: Spartakos — Síntesis y revisión funcional
lang: es-ES
license: CC-BY-SA-4.0
version: 0.1
date: 2026-10-22
status: Primera pasada funcional y maqueta local; pendiente de validación con participantes
---

# Síntesis funcional

## 1. Recorrido de lectura

| Bloque | Documento | Resultado de diseño |
| --- | --- | --- |
| Identidad y relaciones | [01](FUNCIONAL-01-IDENTIDAD-PERFIL-Y-RELACIONES.md) | Seudónimo, perfil mínimo y relaciones sin amistad obligatoria |
| Interacción | [02](FUNCIONAL-02-INTERACCION-UTIL.md) | Acuerdo, interés y seguimiento separados; utilidad sin dependencia |
| Publicación | [03](FUNCIONAL-03-PUBLICACIONES-Y-CONVERSACIONES.md) | Audiencias, hilos, versiones y retirada sin viralidad impuesta |
| Comunidades | [04](FUNCIONAL-04-COMUNIDADES-Y-PERMISOS.md) | Plantillas simples, competencias y unanimidad para abrir privadas |
| Inicio y descubrimiento | [05](FUNCIONAL-05-INICIO-BUSQUEDA-Y-DESCUBRIMIENTO.md) | Cronología, exploración explicada y cobertura honesta de búsqueda |
| Intereses y reputación | [06](FUNCIONAL-06-INTERESES-Y-REPUTACION.md) | Declaración personal y evidencia contextual sin puntos |
| Protección y recursos | [07](FUNCIONAL-07-MODERACION-Y-RECURSOS.md) | Denuncia separada de desacuerdo; decisiones acotadas y revisables |
| Base gratuita y servicios | [08](FUNCIONAL-08-BASE-GRATUITA-Y-SERVICIOS.md) | Derechos básicos sin pago y recursos finitos explícitos |
| Continuidad personal | [09](FUNCIONAL-09-ENTRADA-RECUPERACION-Y-SALIDA.md) | Entrada, importación, recuperación, traslado y salida sencillos |
| Continuidad colectiva y gobierno | [10](FUNCIONAL-10-CONTINUIDAD-Y-GOBIERNO.md) | Iniciativa sin propiedad, administración sustituible y derechos comunes |

Son propuestas funcionales, con reglas ya establecidas y alternativas pendientes señaladas en cada bloque. Primera pasada completa no significa pantallas validadas, sistema electoral resuelto ni especificación técnica lista para implementar.

## 2. Coherencia entre bloques

- **Perfil y audiencia:** un nombre mínimo visible en intervenciones no vuelve públicas las publicaciones restringidas. Un perfil no listado tampoco garantiza ocultar participación pública.
- **Seguir y acceder:** seguir no concede lectura privada. Ser miembro no obliga a seguir ni recibir todos los avisos.
- **Interés y recomendación:** guardar es privado. Elegir temas puede orientar descubrimiento explicado; el guardado no autoriza por sí solo aprendizaje o acceso de terceros.
- **Acuerdo y reconocimiento:** coincidir no acredita verdad, competencia o reputación. Una edición no transfiere automáticamente el acuerdo a otro texto.
- **Reputación y permisos:** reconocimiento no concede moderación, voto ni prioridad automática. Controles contra abuso no son clasificación personal oculta.
- **Privado y cifrado:** el control de acceso del piloto y E2EE son modos distintos. Historial, búsqueda, denuncias y recuperación deben respetar esa diferencia.
- **Fundación y continuidad:** quien inicia no adquiere propiedad colectiva. Sustituir administración requiere autoridad y procedimiento, no apropiación por el más activo.
- **Unanimidad y contenido:** unanimidad para abrir la comunidad es obligatoria aunque se preserve pasado; no publica automáticamente aportaciones antiguas de terceros.
- **Salida y recursos:** cambiar proveedor conserva derechos y referencias conforme a pruebas; no promete capacidad gratuita infinita ni recepción universal por todos los nodos.
- **Apertura de código y operación:** desarrollo abierto no equivale a abrir inmediatamente un servicio público ni demostrar independencia institucional.

## 3. Decisiones funcionales prioritarias

| Pendiente | Recomendación provisional | Qué condiciona |
| --- | --- | --- |
| Nombre localizable y menciones | Referencia sencilla que preserve continuidad; comparar opciones sin imponer dominio propio | Identidad y búsqueda |
| Perfil totalmente reservado | Probar con uso exclusivo en comunidades privadas | Descubrimiento y exposición de metadatos |
| Audiencias personales elegidas | Añadir solo si no basta comunidad restringida y existe recorrido simple | Editor, cifrado y grupos |
| Historial de comunidad | Regla visible por espacio; distinción entre control de acceso y cifrado | Membresía y claves |
| Ediciones anteriores | Marca y contexto cuando proceda, con purga de datos sensibles | Réplicas, evidencia y privacidad |
| «Coincido» y expresión afectiva | Probar graduación y variante sin reacciones rápidas | Comprensión y presión social |
| Reconocimientos de terceros | Comparar con perfil autodeclarado y selección de aportaciones | Utilidad y coste de moderación |
| Censo de unanimidad y gobierno | Procedimiento verificable sin manipular membresía ni retener datos innecesarios | Autoridad comunitaria |
| Cuenta huérfana | Estado revisable con evidencia, separado de pérdida de archivos | Recuperación y representación pública |
| Capacidad base | Medir y publicar compromisos reales antes de prometer cuotas | Voluntariado y sostenibilidad |

No es necesario decidir colores, nombres finales de botones o bibliotecas para resolver estos asuntos. Sí son necesarios ejemplos de uso y revisión de reglas antes de congelar arquitectura.

## 4. Secuencia posterior

1. Revisar principios y decisiones funcionales de mayor impacto.
2. Probar recorridos con esquemas de pantalla o prototipo descartable, sin presumir validación por escribirlos.
3. Actualizar arquitectura a partir de esos resultados.
4. Resolver licencia inicial y preparar desarrollo abierto.
5. Ejecutar ensayos técnicos para las incertidumbres concretas, con criterios ya definidos.

La selección documental de OpenMLS y DID PLC permanece como antecedente provisional. No se ejecuta el laboratorio ni se adoptan componentes antes de completar la revisión funcional correspondiente.

## 5. Alcance de validación actual

Se ha comprobado coherencia documental, enlaces e identificación de requisitos. También existe una [maqueta descartable comprobada localmente](RESULTADOS-DEL-PROTOTIPO.md). No se han probado recorridos con participantes, implementado funciones de red, medido capacidad ni obtenido revisión de seguridad. La matriz distingue criterios definidos de resultados ejecutados. Las cuestiones pendientes no se consideran aprobadas por ausencia de observaciones.

## 6. Recomendaciones desarrolladas

La [resolución propuesta de pendientes](RESOLUCION-DE-PENDIENTES.md) concreta referencias y perfiles, interacción comparada, historial y censo de unanimidad. Los guiones V01–V09 de [validación](VALIDACION-Y-PUERTAS-DE-AVANCE.md) permiten contrastarlos con participantes. Las recomendaciones no reemplazan esta revisión ni constituyen resultados de pruebas.
