---
title: Plan de trabajo — estructura e independencia de la red
lang: es-ES
license: CC-BY-SA-4.0
date: 2026-10-22
status: Propuesta de trabajo; sin arquitectura elegida
---

# Plan de trabajo

## Estado y alcance

Disponible un [simulador local con cuatro cuentas simultáneas](simulacion/README.md), servidor persistente y permisos por sesión. Hay catorce pruebas HTTP superadas además de las diez pruebas de la maqueta anterior. No se ha adoptado una arquitectura distribuida de producción ni ejecutado el laboratorio estructural E01–E15.

Disponible una [maqueta descartable de experiencia](prototipo/README.md), con diez pruebas locales del modelo superadas y comprobaciones en navegador. El [informe](RESULTADOS-DEL-PROTOTIPO.md) documenta alcance y defectos corregidos. No hay aplicación de red, pruebas con participantes ni laboratorio estructural ejecutado. Se ha preparado el [paquete de apertura](PREPARACION-DE-APERTURA.md).

Se ha preparado una [propuesta de resolución de todos los pendientes Q01–Q29](RESOLUCION-DE-PENDIENTES.md), con procedimientos de acreditación, fichas de compromiso operativo y guiones de validación. No se han obtenido adhesiones, ejecutado pruebas de producto ni adoptado decisiones de gobierno. Las [puertas de avance](VALIDACION-Y-PUERTAS-DE-AVANCE.md) distinguen lo preparado de la evidencia necesaria.

El mecanismo candidato de [reciprocidad y acreditación](RECIPROCIDAD-ACREDITACION-Y-RECURSOS.md) está desarrollado hasta procedimientos y escenarios; autoridad, ámbito, proporcionalidad y condiciones de adopción permanecen pendientes. No hay obligaciones de reciprocidad activadas ni acreditadores designados.

La primera pasada de los diez bloques funcionales está completada documentalmente. La [síntesis funcional](REVISION-FUNCIONAL.md) organiza la revisión y las decisiones pendientes. La selección técnica y el laboratorio siguen aplazados hasta revisar los comportamientos que condicionan arquitectura.

La [especificación integral v0.20](ESPECIFICACION.md) está disponible para revisión, con anexos de aceptación, decisiones y antecedentes. El desarrollo de la red está pendiente. El repositorio de referencia es [JLPalmes/spartakos](https://github.com/JLPalmes/spartakos), con [licencias adoptadas](LICENCIAS.md) y guías de colaboración desde esta etapa.

La base de servicio se apoya en iniciativas voluntarias gratuitas y distribuidas; los servicios comerciales añaden prestaciones opcionales. La arquitectura híbrida con funciones sustituibles es la hipótesis de trabajo.

El análisis comienza por estructura y distribución del poder. La transferencia de datos se concreta sobre el modelo de destino y se comprueba antes de cerrar la arquitectura. La especificación vigente prevalece sobre los borradores exploratorios.

Análisis disponibles: [funciones y poder](ARQUITECTURA-01-FUNCIONES-Y-PODER.md), [comparación de arquitecturas](ARQUITECTURA-02-COMPARACION-A-B.md) e [identidad y recuperación](ARQUITECTURA-03-IDENTIDAD-Y-RECUPERACION.md).

## Base confirmada

- Buscar la mayor independencia práctica posible, considerando descentralización y alternativas.
- Soberanía sobre identidad y publicaciones, portabilidad y derecho a irse.
- Experiencia sencilla para usuarios individuales, sin configuración ni decisiones continuas obligatorias.
- Migración de entrada desde redes populares, conservando historial y medios para recuperar contactos; no se requiere interoperabilidad con ellas.
- Comunidades con permisos, libertad algorítmica, reputación temática discreta, intereses privados y públicos, pluralidad de proveedores y una Constitución.
- Migración colectiva descartada.

El orden de análisis no elimina requisitos ni determina su prioridad de implementación.

## Fase 1. Definir la independencia

Identificar de quién y de qué depende una persona: operador de la red, alojamiento, identidad, recuperación, distribución, búsqueda, aplicación, financiación y gobierno. Separar continuidad de servicio, control de decisiones y custodia de información.

Resultado: mapa de dependencias y situaciones que el diseño debe soportar. Ejemplos: cierre o adquisición del operador, desaparición de un nodo, proveedor que no coopera, pérdida de acceso, subida de precios y concentración en buscadores o distribuidores.

## Fase 2. Comparar modelos completos de red

Evaluar con el mismo conjunto de funciones y escenarios:

1. Operador único con código abierto, garantías de salida y gobierno independiente.
2. Red común operada por una cooperativa o entidad con poder limitado; distinguir este gobierno de la arquitectura técnica.
3. Servidores autónomos que participan en una misma red, con cuentas alojadas en ellos.
4. Servicios separados y sustituibles: identidad, almacenamiento personal, distribución, búsqueda y presentación.
5. Red entre dispositivos con nodos de apoyo, voluntarios o comerciales.
6. Arquitectura híbrida: experiencia gestionada sencilla con alternativas independientes realmente operativas.

No son casillas mutuamente excluyentes: autoalojamiento y pago son modalidades de provisión; gobierno y distribución técnica son ejes distintos.

Resultado: dos o tres candidatas coherentes, con diagrama, recorrido de alta, responsables, dependencias críticas, capacidades y limitaciones. No elegir un protocolo por afinidad ideológica ni sumar componentes sin definir cómo funcionan juntos.

## Fase 3. Comprobar viabilidad y costes

Para cada candidata: disponibilidad con el usuario desconectado, dispositivos móviles, latencia, almacenamiento y medios, recuperación, permisos privados, moderación, actualización y retirada, abuso, mantenimiento y financiación.

Estimar costes por escenarios declarados de uso y volumen. Distinguir coste de desarrollo del coste recurrente y quién lo asume. El voluntariado no se considera capacidad garantizada ni ausencia de costes. No exigir un servidor propio para disfrutar de derechos básicos.

Resultado: comparación de riesgos y costes, y lista de pruebas necesarias para resolver incertidumbres relevantes. Sin puntuaciones numéricas inventadas.

## Fase 4. Propuesta arquitectónica razonada

Presentar una candidata preferida y alternativa, explicando sacrificios, dependencias que permanecen y evolución posible. Definir interfaces abiertas, autoridad sobre identidad, custodia, recuperación, copias y sustitución de servicios.

Resultado: decisión explícita, con razones y asuntos pendientes. Si la primera versión tiene infraestructura concentrada, explicar qué permitirá sustituirla y cómo se verificará; no prometer descentralización futura sin mecanismos.

## Fase 5. Gobierno y Constitución

Delimitar poderes de personas, comunidades, proveedores y entidad común; financiación, cambios de reglas, recursos, conflictos y prevención de captura. La Constitución debe reflejar garantías realizables y los mecanismos para exigirlas. Las restricciones constitucionales se consideran desde fases anteriores para que no queden subordinadas a una arquitectura ya cerrada.

Resultado: marco de gobierno y borrador constitucional discutible, no aprobado por defecto.

## Fase 6. Producto sobre esa estructura

Definir comunidades y permisos, identidad visible, publicaciones, algoritmos, reputación e intereses con una experiencia inicial simple. Después concretar migración de entrada y salida sobre los datos y servicios elegidos.

Resultado: recorridos de uso, valores predeterminados y requisitos funcionales, con detalle avanzado opcional.

## Fase 7. Validación y primera implementación

Probar primero las incertidumbres que podrían invalidar la propuesta, incluida recuperación y cambio de proveedor. Preparar un prototipo de experiencia antes de comprometer el desarrollo completo.

Resultado: evidencia de viabilidad, alcance de primera versión y hoja de ruta. No comienza la construcción de la aplicación en las fases de investigación.

## Disciplina de trabajo

Cada entrega distingue requisito confirmado, alternativa, recomendación, decisión y duda pendiente. Las comparaciones separan capacidades documentadas, resultados de pruebas e hipótesis sobre adopción. Las decisiones se presentan con alternativas, consecuencias y evidencia.
