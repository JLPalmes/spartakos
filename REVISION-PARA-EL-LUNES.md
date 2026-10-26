---
title: Spartakos — Revisión de continuidad para el lunes 26 de octubre
lang: es-ES
license: CC-BY-SA-4.0
date: 2026-10-24
status: Registro de trabajo en curso; no aprobación ni versión de producción
---

# Revisión de continuidad

La revisión prevista es el lunes 26 de octubre de 2026. Este registro reúne resultados, límites y propuestas para facilitar la revisión conjunta. No sustituye la especificación ni la matriz de aceptación.

## Estado vigente antes de la revisión

- Funcionalidad disponible: borradores privados con papelera, edición con versión, retirada del cuerpo, citas y tres niveles, programación, Me gusta con cortes horarios y rescate local al perder permisos o membresía.
- Validación vigente: 91 pruebas automáticas superadas y recorridos sintéticos registrados; 49 documentos verificados. Los recuentos menores de los bloques anteriores son resultados históricos.
- Estadísticas: catálogo propuesto, sin aprobar ni implementar. La identidad distribuida, migración real y operación con proveedores siguen fuera del simulador.
- Preparación: seguir la [guía de revisión](GUIA-REVISION-PROTOTIPO.md) con un escenario separado. Antes de recargar un cliente abierto para cargar la versión actual, copiar el texto local que no se haya guardado.
- Rama de #2 sin integrar en main. No hay despliegue público ni nueva captación. Los datos del laboratorio del usuario se mantienen separados de los ensayos.

## Estado de partida

- Rama de trabajo: `prototipo-segunda-revision`; propuesta pública [#2](https://github.com/JLPalmes/spartakos/pull/2), sin integrar en main.
- Laboratorio local: `http://127.0.0.1:8787`; acceso libre con cuentas ficticias, no autenticación de producción.
- Última batería ejecutada al inicio de este bloque: 75 pruebas automáticas superadas; la matriz completa de producto sigue sin ejecutarse.
- Borradores recuperables implementados para publicaciones iniciales, con guardado explícito, versiones y copias ante conflictos.
- Estadísticas personales, comunitarias y globales documentadas como propuesta N11; sin captación nueva ni implementación.

## Orden de trabajo

1. Completar la gestión reversible de borradores y comprobar persistencia, privacidad y conflictos.
2. Desarrollar edición y retirada de publicaciones, preservando autoría, contexto de respuestas y restricciones de audiencia. Distinguir la retirada del cuerpo de una garantía de borrado de copias externas.
3. Revisar consistencia de editor, citas, avisos, programaciones y borradores después de los cambios.
4. Concretar el catálogo y permisos de estadísticas sin inventar seguimiento de lecturas, métricas globales exhaustivas ni clasificaciones de personas.
5. Consolidar resultados, límites, comprobaciones y propuestas pendientes para revisión.

## Límites de este trabajo

Conservar los datos locales existentes y separar los escenarios sintéticos. No publicar datos de ensayo del usuario. No integrar la rama principal, desplegar un servicio público ni contactar con terceros. No dar por aprobadas alternativas pendientes. Cualquier continuación debe inspeccionar los cambios presentes antes de editar y preservar el trabajo previo.

## Resultados acumulados

### Bloque 1 — 23 de octubre: gestión reversible de borradores

Implementada papelera privada y persistente, con restauración de contenido y estado anterior. Mover una referencia no retira publicaciones ni cancela programaciones; restaurarla no ejecuta de nuevo el envío. Se comprueban propiedad y versión. No hay borrado definitivo ni vaciado automático.

Comprobaciones: 78 pruebas automáticas superadas y recorrido de navegador con datos sintéticos. Se conservaron los datos locales del laboratorio. Se incorporan también las notas de estadísticas N11 y su desarrollo funcional, todavía sin implementación.

### Bloque 2 — 24 de octubre: edición propia y retirada del cuerpo

Implementada edición con versión, autoría y permisos, sin cambio de audiencia o contexto. Respuestas, citas y Me gusta anteriores conservan su referencia; se advierte sobre versiones anteriores y no se renueva automáticamente la aprobación. La retirada vacía el cuerpo activo, deja marcador y conserva respuestas ajenas. Las citas no muestran el cuerpo retirado y las programaciones que lo necesitan quedan bloqueadas. El autor puede retirar su propio texto tras perder acceso, sin recibir historial ajeno.

Comprobaciones: 88 pruebas automáticas superadas; edición y referencias anteriores comprobadas con dos clientes; vista sintética de marcador y cita retirada comprobada en navegador. No se modificaron publicaciones del laboratorio del usuario durante esas pruebas. Límites: sin borrado garantizado de copias/respaldos, historial público de cuerpos anteriores o moderación por terceros.

### Bloque 3 — 24 de octubre: consistencia de operaciones

Añadidos tres escenarios sintéticos de regresión: un borrador conserva estado y privacidad cuando se retira su fuente citada; una retirada obsoleta no borra una edición vigente; restaurar una referencia privada ya utilizada no reactiva el cuerpo retirado. Recuperar el estado serializado mantiene estos resultados. Batería completa: **91 pruebas superadas**, incluidos los 33 ensayos HTTP anteriores. Verificación documental y diferencias sin errores.

No se han modificado datos del laboratorio, comportamiento de producción ni configuración del servidor. Los controles de accesibilidad y el rescate persistente de ediciones siguen pendientes; no se presentan como verificados en este bloque. Los cambios se conservan en la rama de la propuesta #2, sin integrar en main.

### Bloque 4 — 24 de octubre: catálogo propuesto de estadísticas

El [diseño de estadísticas](DISENO-ESTADISTICAS.md) concreta fuentes, audiencias, actualización y conservación de una primera fase de gestión de recursos y pendientes. Propone excluir recuentos de comportamiento en grupos, sin atribuir anonimato a un umbral numérico. El panel público se limita como candidato a declaraciones voluntarias y fechadas de servicios, con cobertura y caducidad explícitas; no mide por sí mismo disponibilidad ni capacidad global.

Diez casos de aceptación documentales quedan pendientes de ejecución si se aprueba desarrollar el catálogo. No se ha añadido captación, implementación ni acceso a datos del laboratorio. Verificación editorial de 48 documentos y diferencias sin errores; la batería funcional vigente sigue siendo de 91 pruebas, sin repetirla por este cambio exclusivamente documental. Catálogo enlazado en la documentación de la rama de #2 para revisión, no decisión ratificada.

### Bloque 5 — 25 de octubre: controles del editor y pérdida de permisos

Ajuste local del cliente: cuando el autor conserva lectura pero pierde permiso de edición, el texto que estaba editando se presenta como rescate local de solo lectura, en lugar de ofrecer Guardar edición. La conservación no publica, no persiste el texto por sí misma ni recupera permisos. El mensaje de rescate también se aplica a retirada o pérdida de acceso. Se añaden identificadores estables a los controles de edición y retorno del foco al botón Editar publicación tras guardar o cancelar.

Comprobaciones realizadas: sintaxis del cliente correcta, batería completa de **91 pruebas superadas**, metadatos y enlaces de 48 documentos y diferencias sin errores. Estas pruebas de dominio y HTTP no validan el foco del navegador. El recorrido visual, los conflictos entre pestañas y teclado/lector de pantalla siguen pendientes: el canal del navegador dejó de responder antes de abrir el escenario sintético. No se modificaron datos del usuario ni se reinició su servidor.

**Comprobación posterior — 25 de octubre:** recuperado el navegador, se ejecutó el recorrido con datos sintéticos en un servidor separado. Guardar y cancelar devuelven el foco a Editar publicación. Dos pestañas de Bruno comprobaron el rechazo de una edición obsoleta, conservando su texto y mostrando la versión nueva. Al reducir Alicia el permiso de Bruno a lectura, su edición abierta apareció como rescate de solo lectura, sin Guardar edición y sin cambiar el cuerpo publicado. Se comprobó la propiedad `readOnly` del control. No se ha realizado evaluación con lector de pantalla ni auditoría completa de accesibilidad.

**Estado de publicación:** bloque incorporado a la rama de la propuesta #2 junto con esta evidencia. Los cambios permanecen en `prototipo-segunda-revision`, sin integrar en main. La copia local debe verificarse contra el remoto después de publicar; no descartar commits locales sin comprobar igualdad de contenido.

### Bloque 6 — 25 de octubre: rescate tras pérdida de membresía

Al perder acceso completo a una comunidad, la edición local ya conservada necesita un recorrido visible. Se añade aviso y botón para abrir Mi cuenta cuando existe texto propio en edición fuera de los espacios accesibles. Si el editor enfocado desaparece, el foco pasa al acceso al rescate; en una reducción de permisos con lectura, pasa al campo rescatado. Abrir el recorrido enfoca el texto local de solo lectura. No se publica ni guarda automáticamente, ni se recupera acceso al historial ajeno.

Recorrido sintético comprobado en servidor separado: Bruno publicó y dejó una edición abierta; Alicia le retiró la membresía. Desapareció el historial de comunidad, apareció el aviso con foco y Mi cuenta mostró únicamente la aportación propia y su edición local, con `readOnly` verificado. Se conservan los controles de retirada del texto propio ya existentes, sin ejecutarlos en este recorrido. La batería completa mantiene **91 pruebas superadas**; sintaxis, 48 documentos es-ES y diferencias correctos. No se accedió a datos del laboratorio del usuario. El bloque se incorpora a la rama de #2 para revisión, sin integrar en main.

### Bloque 7 — 25 de octubre: guion de revisión y límites de sesión

Preparada la [guía de revisión](GUIA-REVISION-PROTOTIPO.md), con recorrido por espacios, interacciones, conversaciones, borradores, programación, versiones y pérdida de permisos. Distingue persistencia del servidor de texto en memoria y orienta a usar un escenario separado. La inspección del cliente confirma que entrar en una cuenta reinicia los editores locales; la exportación no incluye texto que nunca se envió. No se añade aviso de salida, guardado automático ni promesa de recuperación tras cerrar sesión.

Cambio exclusivamente documental: verificación editorial de 49 documentos y diferencias sin errores. La batería funcional vigente sigue en **91 pruebas superadas**, sin repetirla por esta guía. El guion es para revisión, no una nueva acta de pruebas ni aprobación de estadísticas. Documentación incorporada a la rama de la propuesta #2, sin integrar en main.

### Bloque 8 — 25 de octubre: coherencia del cierre

Contrastados guía, informe y estado del cliente. Los 91 casos declarados coinciden con la batería vigente registrada; no se repiten pruebas de comportamiento sin cambio de código. Se añade una síntesis actual para distinguir resultados históricos y una instrucción de recarga que protege el texto local sin guardar. Verificación editorial de 49 documentos y diferencias sin errores. No hay nuevas funciones ni cambios de datos. Ajuste documental conservado en un commit local de la rama de #2, pendiente de publicación: el control de permisos del navegador agotó su tiempo de espera. No es una denegación ni un cambio del estado de los bloques ya publicados.

### Consolidación previa a la revisión — noche del 25 de octubre

No se inicia otro desarrollo. El cliente y las pruebas publicados siguen siendo los de la rama de #2; los últimos cambios pendientes son exclusivamente documentales. El navegador sigue sin conexión en esta comprobación, por lo que no se atribuye publicación al ajuste local. No se han modificado credenciales, desplegado servicios públicos ni integrado cambios en main.

Para la revisión quedan estas decisiones y comprobaciones:

- Valorar el recorrido de la guía y decidir si la experiencia permite otra prueba con participantes antes de integrar #2.
- Revisar el catálogo de estadísticas; sigue sin aprobación, implementación ni captación añadida.
- Priorizar respuestas recuperables y ediciones persistentes: actualmente solo los borradores de publicaciones iniciales tienen guardado explícito.
- Definir política de retención y copias; retirada del cuerpo activo no equivale a borrar respaldos o referencias privadas independientes.
- Planificar evaluación de accesibilidad, seguridad y matriz completa de producto; las 91 pruebas de laboratorio no las sustituyen.
- Mantener fuera de las garantías del prototipo la identidad distribuida, migración real, recuperación de cuentas y operación entre proveedores.

### Siguiente paso

Publicar los ajustes documentales locales cuando vuelva el acceso al navegador, comprobando igualdad de contenido antes de alinear referencias. Al llegar al lunes, confirmar este estado y detener los bloques autónomos. No ampliar alcance ni repetir recorridos ya registrados sin motivo; cualquier bloqueo de publicación debe quedar explícito para la revisión.

### Disciplina de continuidad

Inspeccionar rama, cambios locales y propuesta de revisión antes de continuar. La automatización no confirma por sí misma nuevas decisiones de producto. No empezar otro bloque tras el lunes 26; consolidar los resultados y límites. Registrar aquí las pruebas reales y el estado de publicación de cada bloque.
