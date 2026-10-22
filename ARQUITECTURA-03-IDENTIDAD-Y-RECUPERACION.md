---
title: Arquitectura 03 — Identidad, localización y recuperación
lang: es-ES
license: CC-BY-SA-4.0
date: 2026-10-22
status: Alternativas y recomendación provisional; sin protocolo elegido ni pruebas
---

# Identidad, localización y recuperación

## 1. Cuatro problemas distintos

Identidad: reconocer la continuidad de una cuenta. Autenticación: demostrar autoridad para una acción. Localización: encontrar sus servicios vigentes. Recuperación: restablecer autoridad después de perder los medios ordinarios.

El nombre visible no tiene por qué ser único; el identificador interno sí debe distinguir cuentas. No se requiere identidad civil ni una única identidad por persona. Los seudónimos no deben vincularse públicamente por compartir recuperación.

La separación conceptual no obliga a mostrar cuatro servicios al usuario ni a desplegarlos por separado. El recorrido normal sigue siendo registrarse y entrar, con mecanismos predeterminados comprensibles.

## 2. Alternativas de autoridad

| Alternativa | Ventaja | Compromiso |
| --- | --- | --- |
| Alojamiento controla cambios y recuperación | Integración sencilla y soporte único | Su desaparición o negativa puede bloquear la salida |
| Titular conserva el único secreto de control | Evita autorización de intermediarios si el secreto sigue disponible | Perderlo puede hacer irrecuperable la cuenta; robo puede transferir el control |
| Entidad de identidad independiente del alojamiento | Permite cambiar alojamiento sin su permiso | Crea otra autoridad crítica y necesita continuidad propia |
| Autoridad distribuida mediante reglas y varias evidencias o custodios | Puede impedir apropiación unilateral y tolerar algunos fallos | Más coste, coordinación, colusión posible y riesgo de bloqueo por falta de participantes |

La comparación no asigna superioridad absoluta. La elección depende del nivel de fallo y adversario que deba soportarse, del coste y de la experiencia conseguida.

## 3. Propuesta preferente para estudiar

Combinar control ordinario sencillo del titular y sus dispositivos con recuperación asistida cuya autoridad no resida exclusivamente en el alojamiento. El paquete inicial incluye estos medios sin un cuestionario técnico.

Hay que distinguir dos grados de independencia: separarse del alojamiento y resistir la desaparición de la entidad de identidad. La primera puede conseguirse con una autoridad independiente; la segunda exige mecanismos adicionales verificables. No describir el sistema como plenamente descentralizado por alcanzar solo la primera.

Separar credenciales ordinarias de autorización de cambios críticos, limitar las delegaciones del proveedor y registrar cambios verificables. No fijar todavía un esquema de umbrales o número de custodios: sus fallos deben modelarse antes. Separar permisos de software no impide que una misma entidad se apropie del conjunto si custodia todo el material secreto.

No exigir como condición básica un documento de identidad, una cuenta de una gran plataforma ni personas de confianza. Pueden excluir a usuarios o crear dependencias ajenas. Tampoco tomar por suficiente una fotografía de un documento para demostrar titularidad de un seudónimo.

## 4. Procedimiento de recuperación propuesto

1. Intentar recuperar con un medio ordinario ya autorizado.
2. Si no existe, abrir una solicitud asistida y evaluar evidencias previamente establecidas, sin inventar criterios caso por caso.
3. Diferenciar solicitud, recuperación autorizada y conflicto sobre la titularidad. Una denuncia no bloquea ni transfiere una cuenta automáticamente.
4. Aplicar avisos por medios disponibles y, cuando proceda, un plazo antes de acciones irreversibles. La duración depende del tipo de riesgo; no hay un plazo universal decidido.
5. Autorizar nuevas credenciales, revocar las comprometidas y comprobar restauración de datos.

El titular legítimo puede no tener un teléfono antiguo, un correo disponible ni contactos colaboradores. Debe evaluarse qué combinaciones tolera el diseño, sin prometer recuperación cuando ya no existe evidencia suficiente.

En un robo activo, esperar puede agravar el daño; una paralización preventiva requiere reglas y pruebas suficientes para evitar que se use como ataque. Los avisos y plazos son controles complementarios, no pruebas de titularidad ni garantías frente a un custodio con autoridad total.

## 5. Localizar sin conceder poder ilimitado

La red debe conocer el alojamiento vigente y poder comprobar que el cambio fue autorizado. Una copia de un directorio no garantiza por sí sola integridad, actualidad ni capacidad de aceptar cambios sin el directorio original.

Deben probarse cambios incompatibles, información antigua, operadores desconectados y censura de una actualización válida. Fijar cómo se determina la versión vigente y qué se hace durante una disputa antes de diseñar automatismos de traslado.

El nombre público y la localización interna no deberían depender necesariamente de comprar un dominio. Si se ofrece nombre bajo un dominio del operador, explicar qué conserva la persona al irse y qué referencia pública cambia.

## 6. Recuperar identidad no recupera todos los secretos

Restablecer credenciales permite volver a actuar, pero no descifra automáticamente un respaldo privado. Si solo queda una copia cifrada y se ha perdido todo medio de descifrado, el historial privado puede resultar irrecuperable aunque la cuenta vuelva a funcionar.

La recuperación de claves de contenido plantea una decisión propia: incluirlas en recuperación asistida aumenta disponibilidad, pero también capacidad de acceso de terceros. No afirmar a la vez inaccesibilidad absoluta para intermediarios y recuperación universal sin un mecanismo coherente.

## 7. Autenticación cómoda y dependencia externa

Se pueden evaluar passkeys y otros medios de acceso sin elegirlos todavía. WebAuthn define credenciales ligadas a una entidad de confianza de la aplicación; no proporciona por sí solo una identidad universal portable. El cambio de proveedor debe contemplar el alcance de esas credenciales, nuevos registros y desaparición del dominio inicial.

Los medios sincronizados pueden facilitar recuperar un dispositivo y, a la vez, depender de un proveedor de sincronización. No confundir varias copias bajo una sola cuenta externa con independencia de esa cuenta.

## 8. Cuenta huérfana: propuesta pendiente

Se estudia hacer visible la imposibilidad de recuperación por el titular. Deben distinguirse cuenta inactiva, servicio inaccesible, recuperación en curso, titularidad en disputa y cuenta declarada huérfana mediante procedimiento definido.

No deducir orfandad de un tiempo sin publicar, correos sin respuesta o un proveedor caído. Tampoco usar el estado para anunciar fallecimiento. Debe decidirse quién puede declarar, con qué evidencia, cómo recurrir y cómo retirar la marca si aparece un medio válido de recuperación.

La orfandad no transfiere titularidad ni libera automáticamente identificadores. El perfil puede mantener una indicación comprensible y el historial permitido, pero no debe exhibir detalles sensibles de la recuperación. El texto concreto y la conservación se estudiarán después.

## 9. Escenarios que decidirán la viabilidad

| Escenario | Comprobación necesaria |
| --- | --- |
| Pérdida del teléfono con otro medio válido | Recuperación sencilla y revocación del perdido |
| Desaparición del alojamiento | Cambio autorizado sin su cooperación y acceso a respaldo |
| Desaparición del servicio de identidad | Localización y cambios posibles por una vía independiente, o dependencia reconocida explícitamente |
| Correo robado | Que no baste por sí solo para apropiarse de toda la identidad |
| Custodio malicioso | Qué puede hacer unilateralmente y qué evidencia deja; no prometer prevenirlo si tiene autoridad suficiente |
| Pérdida de todos los medios suficientes | Denegar apropiación sin evidencia y estudiar estado huérfano |
| Cambio de dominio de acceso | Nuevo acceso sin depender de una credencial válida solo para el dominio desaparecido |
| Recuperación de identidad con claves privadas perdidas | Separar cuenta recuperada y contenido no descifrable |

No se han ejecutado estas pruebas. La siguiente etapa debe comparar configuraciones concretas de autoridad independiente y distribuida, con fallos tolerados y coste estimado, antes de fijar un mecanismo.

## 10. Antecedentes documentales

- [Recuperación en AT Protocol](https://atproto.com/guides/account-recovery): distingue claves para firmar datos y autorizar cambios de identidad; documenta registro previo de una clave propia para independencia del alojamiento. Es un antecedente, no nuestra solución elegida.
- [WebAuthn](https://www.w3.org/TR/webauthn-3/): especifica credenciales de autenticación con alcance a una entidad de confianza. No debe extrapolarse a portabilidad automática entre dominios.

Las alternativas restantes son propuestas de diseño sujetas a validación.
