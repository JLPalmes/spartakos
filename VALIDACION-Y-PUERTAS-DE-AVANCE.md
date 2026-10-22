---
title: Spartakos — Validación y puertas de avance
lang: es-ES
license: CC-BY-SA-4.0
version: 0.1
date: 2026-10-22
status: Protocolo preparado; pruebas con participantes y sistema no ejecutadas
---

# Validación y puertas de avance

## 1. Secuencia y evidencia

La especificación permite preparar pruebas, pero no demuestra experiencia, seguridad ni sostenibilidad. Cada sesión o ensayo registrará versión, entorno, tarea, resultado, ayuda recibida, fallo y cambio propuesto. No usar retención o tiempo de pantalla como objetivo aislado: comprobar utilidad y control de la atención.

| Puerta | Evidencia requerida | Qué impide avanzar |
| --- | --- | --- |
| P0. Coherencia funcional | Revisión de requisitos, permisos y recomendaciones | Contradicciones con soberanía, gratuidad o unanimidad |
| P1. Comprensión | Prototipo descartable y tareas observadas | Confundir público/restringido/cifrado; no poder salir sin ayuda |
| P2. Viabilidad estructural | Laboratorio reproducible de identidad, recuperación, permisos y copias | Dependencia del origen hostil o publicación no autorizada |
| P3. Desarrollo abierto | Licencias, repositorio y contribución realmente disponibles | Derechos no aclarados o ausencia de canal atendido |
| P4. Piloto limitado | Operadores comprometidos y alcance de seguridad explícito | Recursos no cubiertos, soporte ausente o garantías ficticias |
| P5. Apertura distribuida | Continuidad independiente, revisión de seguridad y responsabilidad | Concentración no declarada o base gratuita inviable |

P3 debe cumplirse antes de iniciar desarrollo compartido, incluido un laboratorio que se publique o reciba contribuciones. El orden de las puertas representa dependencias, no una excusa para desarrollar en secreto hasta el piloto. Los esquemas de experiencia pueden elaborarse con herramientas descartables sin elegir el sistema definitivo.

## 2. Guion de experiencia individual

Propuesta: primera ronda pequeña y diversa, por ejemplo seis a ocho participantes con distinta experiencia técnica. Es una búsqueda cualitativa de problemas, no una muestra representativa ni validación estadística. No reclutar ni grabar sin consentimiento. No pedir exportaciones personales para una primera prueba: usar material ficticio identificado.

| Tarea | Situación | Evidencia de utilidad o fallo |
| --- | --- | --- |
| V01. Llegada | Sin contactos ni archivo importado | Encuentra algo útil sin escoger nodo ni algoritmo |
| V02. Privacidad | Publicar en comunidad privada y explicar quién puede leer | Distingue miembros, operador y otros usuarios |
| V03. Interés | Guardar una idea con la que discrepa | Comprende que guardar no expresa acuerdo público |
| V04. Interacción | Comparar acuerdo graduado y ausencia de reacciones rápidas | Comprensión, utilidad y presión percibida; orden alternado |
| V05. Historial | Importación ficticia con contactos ausentes | Distingue archivo, referencias de origen y personas activas |
| V06. Retorno | Segunda sesión sin avisos insistentes | Recupera una utilidad concreta; explica qué faltó si no vuelve |
| V07. Continuidad | Alojamiento indisponible, traslado guiado | Identidad conservada, datos recuperables y pérdidas entendidas |
| V08. Apertura | Administrador propone hacer pública una comunidad | Entiende unanimidad e historial; rechazo conserva privacidad |
| V09. Salida | Exportar y cancelar servicio opcional | No necesita pagar ni negociar con el proveedor |

Primero observar sin intervenir; después preguntar qué esperaba la persona. Registrar ayudas como tales. Una tarea completada tras explicación del facilitador no demuestra que el recorrido sea autónomo. Todo error de audiencia que exponga contenido bloquea esa variante hasta corregirla y volver a comprobarla.

## 3. Comparación equivalente

Seleccionar herramientas que ya resuelvan la tarea concreta, a partir de la [revisión comparada](REVISION-COMPARADA-E-INCENTIVOS.md): alojamiento federado, identidad portable, comunidades y archivo personal. No enfrentar una maqueta ideal de Spartakos a una instalación mal configurada del otro producto. Documentar versiones, configuración, ayuda y limitaciones equivalentes. Si una herramienta no ofrece la función, registrar ausencia sin convertirla en fracaso general del producto.

La superioridad solo se afirma para tareas y condiciones observadas. Si Spartakos añade configuración, dependencia de autoridad o carga operativa sin utilidad apreciable, simplificar o reconsiderar la arquitectura.

## 4. Laboratorio y datos de importación

Ejecutar E01–E15 del [ensayo estructural](ENSAYO-01-COMPONENTES-Y-VALIDACION.md) después de P0/P1 para las reglas que condicionan sus pruebas. Fijar versiones y entorno, conservar instrucciones reproducibles, excluir secretos y registrar resultados negativos. Ensayar fallos y recuperación, no únicamente el recorrido cooperativo.

Importación: corpus sintético para estructura y archivos reales voluntariamente aportados para cobertura. Obtener consentimiento, limitar acceso, definir eliminación y no incluir archivos personales en repositorio. Informar por categoría: detectado, importado, omitido, ilegible y recuperable mediante otra vía. Un ensayo con un archivo no acredita compatibilidad con todas las exportaciones de la plataforma.

## 5. Operación y acreditación

Aplicar el [programa de operadores](OPERACION-Y-VOLUNTARIADO.md), simular salida del mayor aportante y comprobar que sus recursos no estaban contados varias veces. Para acreditación, ensayar RC01–RC12 con identidades ficticias: denuncia infundada, conflicto de interés, financiación duplicada, caída del emisor y recurso estimado. No publicar acusaciones contra entidades reales para probar el procedimiento.

## 6. Estado de resultados

Esta versión no añade pruebas ejecutadas a la matriz A01–A148. V01–V09 y las puertas P0–P5 son guiones complementarios; no representan nuevas capacidades implementadas. Las comprobaciones editoriales de enlaces, identificadores e idioma se informan por separado de las pruebas de producto.

## 7. Comprobaciones locales posteriores

La [maqueta y su informe](RESULTADOS-DEL-PROTOTIPO.md) aportan diez pruebas automáticas de un modelo descartable y recorridos comprobados en navegador. V01–V09 no se consideran realizados con participantes y ninguna puerta de seguridad o distribución queda superada por ello.
