---
title: Spartakos — Identidad, perfil y relaciones
lang: es-ES
license: CC-BY-SA-4.0
version: 0.1
date: 2026-10-22
status: Diseño funcional propuesto; alternativas y decisiones pendientes identificadas
---

# Identidad, perfil y relaciones

## 1. Objetivo y criterio de diseño

Permitir entrar, ser reconocido y relacionarse sin obligar a comprender infraestructura ni revelar identidad civil. Este bloque define comportamiento antes de seleccionar mecanismos técnicos. Se propone, no se da por aprobado, el diseño siguiente.

El recorrido básico requiere un nombre de uso y un medio de acceso. Los demás datos pueden completarse después. La cuenta resulta utilizable sin foto, biografía, lista de intereses, contactos importados ni decisiones sobre reputación.

## 2. Qué representa una cuenta

Propuesta: una cuenta personal corresponde a una identidad de participación, no a una identidad civil verificada. Admite seudónimo. Una persona puede mantener identidades separadas para contextos distintos; no se muestran como vinculadas por compartir dispositivo o recuperación.

Separar identidades protege contextos, pero no debe permitir fabricar reputación, votos o apoyos. La resistencia a abuso y la legitimidad del voto se diseñan aparte: no se resolverán imponiendo exposición pública de identidades ni suponiendo que una cuenta equivale a una persona única.

Una entidad o colectivo necesita administración delegada y sucesión de responsables. No conviene simularlo compartiendo la contraseña de una cuenta personal. Propuesta: perfil de entidad administrable desde cuentas personales con permisos explícitos; su inclusión en primera versión queda pendiente del análisis de comunidades. No se obliga a elegir tipo de cuenta al registrarse.

Automatizaciones, cuando se admitan, tienen identidad y atribución visibles, permisos limitados y ninguna apariencia obligatoria de persona humana. No se consideran prioritarias para la primera experiencia.

## 3. Identidad estable, nombre y perfil

| Elemento | Función | Comportamiento propuesto |
| --- | --- | --- |
| Identidad estable | Continuidad de cuenta, relaciones y publicaciones | Se conserva al cambiar nombre o alojamiento; sin códigos técnicos en uso ordinario |
| Nombre mostrado | Cómo desea presentarse la persona | No necesita ser único; admite seudónimo y cambios |
| Referencia para localizar y mencionar | Encontrar la cuenta correcta | Debe desambiguar sin exigir conocer el proveedor; formato pendiente de resolver |
| Perfil | Presentación pública o restringida | Datos opcionales, audiencia comprensible y cambios revisables |

No elegir todavía un nombre de usuario único global: su asignación, recuperación y posible captura pueden introducir autoridad central. Comparar referencia global, referencia asociada a un espacio de nombres y enlaces estables, con ejemplos de búsqueda, dictado y cambio de proveedor. Esta es una decisión funcional que condiciona arquitectura.

Cambiar nombre no rompe menciones ni referencias. Evitar un historial público obligatorio de nombres anteriores, que puede revelar contextos que la persona necesita abandonar. Una medida contra suplantación no debe crear exposición indiscriminada. Los nombres y avatares parecidos requieren desambiguación y denuncia, no confianza automática.

## 4. Perfil inicial y visibilidad

Datos iniciales visibles propuestos: nombre de uso, avatar opcional y una referencia mínima a la cuenta. Biografía, enlaces y especialidades se añaden voluntariamente. No mostrar correo, teléfono, medios de recuperación, última conexión, localización o lista de dispositivos.

Propuesta para simplificar: perfil público mínimo, con publicaciones inicialmente limitadas hasta elegir audiencia en el editor; no hacer pasar perfil mínimo visible por contenido privado. Ofrecer después una opción de perfil no listado con explicación de sus límites. La existencia de interacciones públicas puede revelar una cuenta no listada.

Esta propuesta precisa la formulación general anterior de «audiencia privada»: no significa que el nombre necesario para intervenir públicamente permanezca secreto. El modo de perfil totalmente reservado debe estudiarse con comunidades privadas antes de fijar su alcance.

No mostrar listas de seguidores/seguidos públicamente por defecto. Permitir a la persona consultar sus propias relaciones y gestionar descubrimiento sin exponer automáticamente un grafo público. Los recuentos no son necesarios en la vista inicial ni determinan reputación.

## 5. Relaciones mínimas

| Acción | Qué expresa | Qué no concede |
| --- | --- | --- |
| Seguir | Querer recibir publicaciones accesibles de una cuenta | Acceso a publicaciones restringidas ni derecho a escribirle |
| Aprobar seguidor | Admitir una relación de seguimiento controlada | Amistad universal ni acceso a cualquier comunidad |
| Pertenecer a comunidad | Participar según rol y reglas | Seguimiento mutuo automático |
| Silenciar | Reducir contenido o avisos para quien lo activa | Sanción pública ni cambio de derechos del silenciado |
| Bloquear | Evitar interacción directa y sugerencias en nuestros servicios | Impedir toda lectura externa de contenido público |
| Guardar | Conservar una referencia privada | Reconocimiento público o copia publicable |

No introducir por defecto «amistad» como segunda relación paralela al seguimiento. Si el análisis de audiencias descubre necesidad de relación recíproca, justificarla antes de añadir otro concepto. Una etiqueta privada de contactos puede servir para organizar personas sin imponer reciprocidad.

Seguir no requiere preguntas adicionales cuando la cuenta acepta seguidores; si requiere aprobación, se muestra una solicitud pendiente y se evitan solicitudes repetidas. Retirar seguimiento no se anuncia como evento social. Las notificaciones no deben presionar para corresponder.

El bloqueo desactiva interacciones directas controladas por el servicio y evita recomendaciones. En espacios compartidos debe ofrecer colapso de contenido y límites claros; no garantizar que dos participantes nunca coincidirán ni anular funciones moderadoras necesarias. La revisión de bloqueos entre moderadores y miembros corresponde al bloque de comunidades.

## 6. Descubrimiento y continuidad

Buscar por nombre, referencia o enlace. Distinguir coincidencia de nombre y cuenta conocida. Las sugerencias no se basan en subir agenda o vincular otras plataformas de forma obligatoria. No anunciar visitas al perfil ni quién buscó a quién.

Conservar relaciones al trasladar alojamiento dentro de Spartakos; no pedir a contactos que acepten de nuevo una persona cuya identidad no ha cambiado. Solicitudes pendientes, bloqueos y silencios también se conservan según sus autoridades y privacidad.

Vincular una cuenta externa es opcional y separado de permitir que antiguos contactos la encuentren. Un importador no activa descubrimiento público universal. Se propone una acción clara de reencuentro sobre cuentas externas verificadas, sin configurar cada relación.

## 7. Señales de confianza y estados

No utilizar un distintivo ambiguo de «verificado». Si existe una comprobación, indicar qué acredita: control de un dominio, cuenta externa o representación de entidad. No acredita honestidad, conocimiento ni seguridad de todas sus publicaciones. No vender un distintivo que se confunda con reputación.

El usuario ve estados relevantes para interactuar: solicitud pendiente, cuenta trasladada cuando corresponda, servicio temporalmente inaccesible o cuenta huérfana declarada mediante procedimiento. No convertir cada incidencia técnica en etiqueta pública permanente.

La inactividad no se señala como defecto ni genera presión. La orfandad no transfiere identidad. La retirada o eliminación tiene tratamiento separado de suspensión y no libera automáticamente identificadores para suplantación.

## 8. Recorridos y casos difíciles

- Una persona se registra con seudónimo, publica y sigue sin completar perfil: debe funcionar.
- Dos cuentas comparten nombre: buscar o mencionar exige distinguirlas sin revelar datos privados.
- Se cambia nombre y nodo: relaciones y referencias permanecen; no se publica por defecto un historial de identidades anteriores.
- Una persona usa dos contextos: no hay vínculo público por compartir acceso o dispositivo.
- Una cuenta con seguidores aprobados participa públicamente: esa intervención es pública; aprobar seguidores no cambia la audiencia del espacio.
- Dos personas bloqueadas coinciden en comunidad: límites explicados y acceso a moderación sin prometer invisibilidad absoluta.
- Se administra una entidad: delegación revocable sin compartir credenciales personales.
- Un antiguo contacto migra: correspondencia fiable y descubrimiento autorizado; no se fabrican amistad o usuarios activos.

## 9. Decisiones pendientes de revisión funcional

1. Referencia legible para menciones y búsqueda: facilidad, unicidad y dependencia de autoridad.
2. Perfil público mínimo frente a perfil completamente reservado y acceso desde comunidades privadas.
3. Necesidad de relación recíproca más allá del seguimiento y membresía.
4. Perfiles de entidades en primera versión y diferencias con comunidades.
5. Límites del bloqueo en espacios moderados compartidos.

Las propuestas permiten evaluar recorridos sin elegir bibliotecas, protocolos o proveedores. La continuación funcional debe tratar publicaciones, audiencias y conversaciones, y volver sobre estas decisiones cuando sus consecuencias estén claras.
