---
title: Arquitectura 02 — Comparación de operación integrada y alojamiento sustituible
lang: es-ES
license: CC-BY-SA-4.0
date: 2026-10-22
status: Análisis de diseño; recomendación provisional, sin implementación ni pruebas
---

# Comparación de arquitecturas A y B

## 1. Definición precisa

Ambas candidatas aspiran a conservar identidad, publicaciones y relaciones, ofrecer una experiencia sencilla y permitir continuidad sin el operador inicial. Se comparan por organización, no por calidad desigual de sus garantías.

**A. Operación integrada con continuidad independiente:** una instalación lógica presta habitualmente toda la red. Puede tener muchos servidores físicos y réplicas. Se prepara una implementación alternativa capaz de continuar el servicio y recuperar cuentas, pero la operación entre proveedores independientes no constituye su funcionamiento ordinario. La sustitución individual del alojamiento requiere conexión adicional con la instalación principal o una transición del conjunto. Código abierto y exportación no bastan para resolver esa dificultad.

**B. Varios alojamientos dentro de la misma red:** distintos operadores pueden alojar cuentas simultáneamente. Las personas de distintos alojamientos siguen participando en las mismas conversaciones y comunidades. Identidad y cambios de ubicación tienen mecanismos independientes del permiso del proveedor saliente. El paquete predeterminado oculta la infraestructura, sin impedir elegir otro después.

B implica comunicación interna entre operadores de nuestra red. No exige compatibilidad con redes sociales ajenas. Ambas candidatas admiten servicios predeterminados y funciones opcionales sustituibles.

## 2. Alta y experiencia ordinaria

En A la aplicación crea la cuenta en el servicio integrado. En B crea la cuenta en un paquete predeterminado, elegido por la política del servicio, sin presentar un selector de servidores. Esa política debe documentar financiación y concentración; no se propone reparto aleatorio ni asignación a voluntarios sin garantías.

En ambos modelos se registra una identidad estable y se prepara un procedimiento de recuperación comprensible. El alta no pide contratar almacenamiento, elegir algoritmos ni gestionar claves. La información esencial sobre custodia debe ser accesible sin convertirla en un cuestionario.

**Resultado:** A puede simplificar la operación inicial. B puede tener la misma sencillez visible, pero exige más trabajo interno y soporte. La diferencia de infraestructura no tiene por qué convertirse en diferencia de pasos para el usuario.

## 3. Publicación pública

En A el servicio integrado conserva la publicación y actualiza sus índices y vistas. En B el alojamiento conserva el original autorizado y comunica la actualización a los componentes que atienden a lectores y comunidades. Los índices y las copias de distribución no se convierten por ello en autoridad para modificar el original.

B necesita versiones, revocación de credenciales, orden de cambios y manejo de mensajes repetidos o retrasados. Debe distinguir aceptación de la publicación por el alojamiento, entrega a destinatarios y aparición en índices; no prometer que ocurren simultáneamente.

**Resultado:** A dispone de coordinación interna más simple. B añade fallos parciales y actualización diferida. Debe comprobarse que ese retraso no degrade conversaciones ni produzca estados engañosos.

## 4. Publicación restringida y comunidad

En A el mismo entorno puede comprobar membresía, servir la publicación y actualizar permisos, aunque debe aplicar controles reales y limitar administradores. En B hay varios operadores que pueden intervenir en la sesión y entrega: la decisión de acceso debe apoyarse en una autoridad comunitaria identificable y vigente, no en una copia indefinida de un permiso antiguo.

Una opción para estudiar es alojar el servicio de cada comunidad en un operador definido y permitir que miembros de cualquier alojamiento accedan a él. Esto concentra la coordinación de esa comunidad sin concentrar toda la red. No se considera decidido si allí reside también cada original o solo estado compartido y referencias; hay que evitar dos autoridades contradictorias para la misma publicación.

La comunidad necesita una identidad y continuidad propias, separadas de la cuenta de quien la fundó. Sus reglas determinan administradores y cambios de alojamiento, sin crear por ello un sistema de migración colectiva de usuarios.

**Resultado:** permisos privados son una de las pruebas decisivas de B. Su compatibilidad con cifrado, recuperación y moderación debe examinarse antes de elegir protocolo.

## 5. Cambio voluntario de proveedor

En A una exportación permite conservar datos; mantener toda la actividad desde un alojamiento individual distinto exige un mecanismo adicional. Si la alternativa permanece conectada y participa ordinariamente, el modelo evoluciona hacia B para esas funciones. Si exige trasladar toda la instalación, la independencia de la persona queda condicionada a una decisión colectiva u operativa ajena.

En B el destino prepara datos y archivos, comprueba integridad y recibe autoridad autorizada. Se actualiza la ubicación vigente sin cambiar la identidad. Las referencias a seguidores y comunidades se mantienen, pero se vuelven a comprobar permisos sujetos a autoridades ajenas. Debe poder reanudarse un traslado interrumpido.

**Resultado:** B encaja mejor con el derecho individual de sustituir alojamiento sin abandonar nuestra red. No implica traslado instantáneo ni ausencia de costes.

## 6. Desaparición o negativa del proveedor

Ninguna candidata recupera datos que solo existían en el proveedor desaparecido. Ambas necesitan copias y autoridad de recuperación independientes. Un contrato de salida es insuficiente frente a una entidad que ya no existe.

En A, la reconstrucción del servicio puede necesitar una cantidad grande de estado y coordinación. Si una entidad central controla recuperación y localización, su caída puede afectar a todo el conjunto. A también puede incorporar separación institucional de esa autoridad; hacerlo reduce parte de su sencillez operativa.

En B la recuperación puede limitarse a las cuentas afectadas, siempre que el resto de componentes siga funcionando y admita el cambio autorizado. No se deduce que todos los fallos queden aislados: un directorio común o distribuidor dominante puede afectar a muchos alojamientos a la vez.

**Resultado:** B distribuye ciertos fallos, pero necesita un mapa explícito de dependencias comunes. Cifrar un respaldo no basta si su única clave depende del origen.

## 7. Pérdida o robo de acceso

Ambos modelos requieren recuperación y revocación; la distribución no resuelve por sí sola ninguna. Conviene separar autoridad ordinaria de publicación y autoridad para cambios críticos. Deben compararse métodos que sean automáticos en el uso normal y comprensibles al necesitar ayuda.

No se prescribe todavía un número de custodios ni un algoritmo. Debe evaluarse colusión, recuperación fraudulenta, indisponibilidad de custodios y desaparición del operador. Dividir autoridad añade independencia, pero también coordinación y coste.

**Resultado:** el mecanismo de recuperación es una decisión estructural pendiente. No puede relegarse a una función de soporte posterior al desarrollo.

## 8. Datos y autoridad por participante en la candidata B

| Participante | Custodia posible | Acceso que requiere estudiar | Autoridad propuesta |
| --- | --- | --- | --- |
| Alojamiento de la persona | Perfil, publicaciones, archivos y preferencias | Públicos; privados según cifrado y permisos aún no elegidos | Operación del servicio y cambios ordinarios autorizados; no veto exclusivo al traslado |
| Servicio de comunidad | Miembros, roles, normas, decisiones y estado de conversaciones | Datos de gestión y contenido necesario según modelo | Participación local, sin apropiarse de identidades personales |
| Distribuidor público | Copias e índices públicos | Contenido público y metadatos necesarios | Entrega; no cambio de autoría ni acceso privado implícito |
| Buscador o recomendador | Índices y preferencias autorizadas | Mínimo necesario para su función | Selección y orden, no creación de permisos |
| Custodia independiente de respaldo | Copias restaurables | Preferentemente contenido cifrado; claves y metadatos pendientes de diseño | Conservación y restauración autorizada, no publicación |
| Mecanismo de identidad y recuperación | Ubicaciones y cambios de autoridad verificables | Metadatos mínimos; evitar unir seudónimos innecesariamente | Validación del cambio conforme a reglas; no modificación arbitraria por alojamiento |

La tabla no afirma que cifrar todo sea compatible con todas las funciones. Los metadatos también pueden revelar relaciones y requieren análisis propio.

## 9. Complejidad y coste cualitativo

| Aspecto | A | B |
| --- | --- | --- |
| Operación inicial | Menos coordinación entre entidades | Exige coordinación entre alojamientos |
| Cambio individual manteniendo actividad | Necesita ampliar el modelo integrado | Parte del funcionamiento previsto |
| Permisos y consistencia | Más sencillos dentro del servicio | Requieren tratamiento de retrasos y autoridad remota |
| Soporte | Un responsable inmediato | Necesita diagnóstico compartido y responsable visible |
| Copias y recuperación independientes | Necesarias si se exige continuidad real | También necesarias; no vienen dadas por tener varios operadores |
| Riesgo de concentración | Directo en el operador | Puede reaparecer en proveedor predeterminado o servicios comunes |
| Coste económico | No estimado | No estimado; mayor complejidad no determina por sí sola coste por usuario |

No hay presupuestos ni mediciones. La siguiente evaluación debe usar escenarios de volumen, medios, actividad y disponibilidad antes de asignar cifras.

## 10. Recomendación provisional

Continuar con B como candidata principal: paquetes completos de alojamiento sustituibles, servicios de comunidad con autoridad delimitada y funciones de descubrimiento separables. Mantener A como referencia de menor complejidad para medir qué ganamos con cada separación.

Evitar por ahora descomponer todas las funciones en proveedores distintos. Exigir, antes de dar por acreditada independencia, una prueba con dos operadores bajo administración separada y un traslado que conserve actividad sin cooperación del origen.

Esta variante y sus mecanismos concretos requieren validación.

## 11. Cuentas huérfanas

Se estudia una marca visible de cuenta «huérfana» cuando su titular no pueda recuperarla. La función requiere criterios y procedimiento antes de su activación.

No equiparar imposibilidad de recuperación con inactividad, suspensión, fallecimiento o caída del alojamiento. Una imposibilidad definitiva rara vez se puede demostrar solo por ausencia de actividad; deben definirse evidencias y competencia para declarar el estado.

Preguntas pendientes: quién solicita y quién declara; qué pruebas sirven sin exponer información sensible; cómo evitar marcas maliciosas; propagación del estado; posibilidad de revisión si reaparece el titular; contenido visible y conservación; relación con una cuenta nueva y prueba de continuidad.

Una marca no debe transferir la identidad, liberar automáticamente su nombre ni autorizar a otra persona a publicar en su lugar. No se presupone que el estado deba ser irreversible. Su finalidad propuesta es informar de una falta de control recuperable, no resolver por sí mismo custodia, sucesión o eliminación.

## 12. Próximo trabajo

Examinar variantes del núcleo de identidad, localización y recuperación, con reglas de confianza y fallos concretos, manteniendo un único recorrido sencillo de alta. Definir después la relación entre originales personales y conversaciones comunitarias. Son las incertidumbres que pueden cambiar la elección de arquitectura.

Este documento es razonamiento de diseño propio. No acredita capacidades de un producto externo ni resultados de pruebas.
