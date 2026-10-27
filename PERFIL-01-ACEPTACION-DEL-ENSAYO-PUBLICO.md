---
title: Spartakos — Aceptación y estados del ensayo de perfil público
lang: es-ES
license: CC-BY-SA-4.0
date: 2026-10-27
version: 0.1
status: Cierre de alcance experimental y propuestas de integración; sin aprobación de producción
---

# Perfil público mínimo: qué se acepta y cómo se informa

## 1. Decisión de alcance

El laboratorio permite continuar con un banco experimental de entrega de datos públicos verificados. No permite ofrecer todavía una función de traslado completo ni aprobar KERI para producción. El perfil se conserva y verifica desde servicios distintos; el control de sus revisiones sigue en el titular y los proveedores de entrega no reciben sus claves.

Las 53 comprobaciones ejecutadas incluyen identidad, recibos, persistencia, conflictos, perfil y entrega. No son 53 casos de producto superados; una reproduce H01, que permanece abierto en la implementación fijada. Los quince casos E y diez casos T siguen sin completarse. Véanse [balance](BALANCE-01-IDENTIDAD-Y-TRASLADO.md) y [laboratorio reproducible](laboratorio-identidad/README.md).

Esta especificación ordena el alcance ya observado y propone su integración posterior. No añade pantallas al simulador, permisos de escritura a proveedores, reglas de consenso ni una arquitectura definitiva.

## 2. Criterios y evidencia disponible

«Demostrado en el ensayo» siempre incluye los límites de los escenarios sintéticos locales. No implica seguridad general o ausencia de defectos.

| Criterio | Resultado y evidencia | Límite que debe mantenerse explícito |
| --- | --- | --- |
| P01 — Identidad esperada independiente | El verificador rechaza otra identidad aunque su historia esté firmada válidamente; suite HTTP de perfil | La identidad esperada la proporciona el coordinador; no se ha probado su descubrimiento seguro por una persona nueva |
| P02 — Correspondencia del cuerpo | Se rechaza el contenido alterado sin anclaje aceptado; suites de perfil y HTTP | Esquema mínimo experimental y bytes del fixture, sin formato de perfil interoperable aprobado |
| P03 — Autoridad de revisión | La clave ajena y la anterior tras rotar no autorizan el cambio; suite de perfil | No hay delegación de escritura, recuperación de cuenta ni cliente final |
| P04 — Historial frente a cabeza local | Se distingue la copia anterior cuando la vista conoce otra revisión; suite de perfil | Una vista atrasada puede considerar cabeza a una copia antigua; actualidad global desconocida |
| P05 — Proveedor autorizado antes de red | Dirección conocida sin autorización se rechaza antes de HTTP; suite de entrega autorizada | Rol agent usado para entrega en este arnés, no mapa definitivo de permisos |
| P06 — Recuperación con origen apagado | B entrega el perfil y sus referencias verificables tras comprobar que A no responde; suites HTTP y entrega autorizada | Copia preparada previamente y distribución explícita de mensajes; no pérdida de toda la máquina |
| P07 — Regreso del origen | A no recupera el rol por anunciar dirección y su copia anterior es histórica en una vista actualizada | A no tenía clave del titular ni permiso de editar; no se prueba revocación de escritura delegada |
| P08 — Persistencia | Cuerpo y vínculo se reabren entre procesos; suites de estado, HTTP y estados parciales | Sin corrupción, restauración del dispositivo o fallo durante transacción |
| P09 — Incompletitud visible | Solo revocación deja cero proveedores, solo autorización deja dos, ningún cambio conserva A; suite de estados parciales | Comprobado por aserciones del arnés; aún no es una representación de interfaz ni sincronización automática |
| P10 — Reanudación y repetición | Se conserva la vista parcial tras salida abrupta posterior a commits; completar mensajes dos veces deja B y un solo cuerpo guardado | No prueba atomicidad de dos declaraciones ni deduplicación general de objetos sociales |
| P11 — Conflicto duradero | El registro local conserva bloqueo tras reiniciar y caducar la cola; suite de estado de perfil | Limitado a ramas sn=1 sin rotación/testigos/delegación; intervalo entre KERI y SQLite sin probar |
| P12 — Actualidad y dependencias | Se conserva expresamente la ausencia de prueba de actualidad global | Es un límite declarado, no una garantía de detección de toda actualización o conflicto |

Pruebas fuente: [perfil](laboratorio-identidad/keri_profiles.py), [estado persistido](laboratorio-identidad/keri_profile_state.py), [entrega HTTP](laboratorio-identidad/keri_profile_http.py), [resolución autorizada](laboratorio-identidad/keri_authorized_delivery.py) y [estados parciales](laboratorio-identidad/keri_partial_delivery.py). Las rutas enlazan código ejecutable; esta tabla no sustituye repetirlo en el entorno fijado.

## 3. Dimensiones independientes de estado

No se propone un único indicador verde que mezcle integridad, permiso y actualidad. El futuro resultado de consulta deberá conservar por separado:

| Dimensión | Estados que deben distinguirse | Deducción que no se permite |
| --- | --- | --- |
| Cuerpo | Ausente, recibido sin verificar, verificado para una revisión | Recibir bytes no acredita autor ni versión |
| Historia conocida | Sin anclaje validado, revisión histórica, cabeza en la vista | Cabeza local no acredita última revisión global |
| Servicio | Sin autorización conocida, autorizado en la vista, revocado en la vista | Una URL firmada por el proveedor no concede rol; revocar un rol no borra sus copias |
| Entrega | Sin destino autorizado, destinos disponibles, error de conexión | Error de red no prueba revocación; cero destinos no elimina el perfil guardado |
| Conflicto | Evidencia registrada, evidencia no registrada con cobertura limitada | Ausencia de registro no demuestra ausencia de contradicción |
| Actualidad | Sin prueba suficiente, evidencia de actualización conocida | El silencio de un proveedor no confirma que no haya cambios |

No hay un procedimiento general de «actualidad confirmada» implementado. Tampoco se propone uno por elegir la fecha mayor de una declaración. Los casos de igual fecha con resultados distintos entre observadores ya están documentados.

## 4. Comportamiento de integración propuesto

Estas reglas son propuestas para el siguiente arnés y el cliente posterior, no funciones ya presentes en el simulador.

- Una copia verificada podrá conservarse para lectura, indicando su condición histórica o la limitación de actualización cuando corresponda. No se borrará por una interrupción de red.
- Si existe un anclaje posterior conocido pero falta su cuerpo, se informará de esa ausencia. Mostrar la copia anterior no deberá presentarse como restauración íntegra de la nueva.
- Un servicio sin autorización en la vista no se consultará a través del flujo autorizado. La disponibilidad de una copia por otra vía no le concede autorización.
- Un conflicto registrado impedirá presentar como confirmada una revisión o un cambio sensible. Se conserva evidencia y no se elige automáticamente la rama que contestó primero.
- Un conflicto no se resolverá por caducar una cola ni por reiniciar. La ausencia de bloqueo tampoco será autorización automática para una acción sensible.
- El estado parcial se conservará y se reintentará su actualización mediante el mecanismo que llegue a integrarse. No se pedirá al usuario escoger un proveedor o resolver fechas para salir del paso.

La creación de una revisión por el titular y su recepción por terceros son hechos distintos. La incertidumbre de distribución no debe convertirse por sí sola en una prohibición general de preparar o firmar datos propios; la confirmación de efectos compartidos requiere reglas específicas todavía pendientes. No se añade aquí una nueva política de publicación desconectada.

## 5. Qué sigue bloqueado para producción

H01 y su adaptador experimental, concurrencia, cortes entre almacenes, pérdida de claves o registro de conflictos, recuperación general, navegador, dispositivos, distribución y autenticidad del cliente, privacidad comunitaria, costes de operación y difusión independiente de declaraciones. La firma de la distribución nativa sigue sin verificar y la consulta de avisos de dependencias no es una auditoría.

Los servicios comparten máquina y administrador; no demuestran independencia institucional ni resistencia a vigilancia o censura. No se contacta con terceros ni se despliega un servicio público para cerrar estos puntos.

Para continuar investigando en local no hace falta elegir todavía umbral de testigos, árbitro, proveedor obligatorio o mecanismo de recuperación. Adoptar cualquiera de esos compromisos sí requiere una decisión de arquitectura explícita.

## 6. Próximo ensayo: inventario público y referencias

El siguiente bloque ampliará el objeto de copia, manteniendo las garantías acotadas:

1. Preparar un inventario sintético de perfil y aportaciones públicas propias, con IDs, revisiones y huellas. El inventario deberá tener autoridad verificable del titular, no solo hashes.
2. Mantener un observador con referencias ya guardadas que no se traslada ni cambia manualmente sus IDs al pasar de A a B.
3. Recuperar desde B con A apagado, preservando referencias y versiones. Probar un objeto omitido, otro alterado y un marcador de retirada sin resucitar su cuerpo.
4. Repetir la recepción y reiniciar para detectar duplicación o pérdida de estado. Declarar por separado qué fases dependen aún del coordinador y del componente.
5. Publicar el balance de los casos T afectados sin dar por completos privacidad, relaciones, recuperación o independencia de autoridad común.

La primera ampliación no transportará historial comunitario, borradores, contactos reales ni envíos programados. Migrar desde redes externas seguirá siendo otro trabajo: el ensayo de proveedores internos no lo sustituye. El formato inicial será de laboratorio; no comprometerá el almacenamiento del simulador ni una API pública estable.
