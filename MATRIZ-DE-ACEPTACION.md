---
title: Spartakos — Matriz de aceptación
lang: es-ES
license: CC-BY-SA-4.0
version: 0.16
date: 2026-10-22
status: Pruebas especificadas; ninguna ejecutada
---

# Matriz de aceptación

Todas las filas tienen estado inicial **no ejecutada**. Fases según ESPECIFICACION.md. Una prueba adelantada verifica diseño; la fase indicada exige su aceptación. Si el alcance cambia, registrar decisión, no borrar el requisito original.

| Prueba | Requisito | Fase límite | Escenario y resultado exigido |
| --- | --- | --- | --- |
| A01 | R01, R02 | F1 | Cambiar alojamiento sin cooperación del origen: misma identidad y referencias; autoridad anterior no acepta cambios como vigente |
| A02 | R01, R02 | F1 | Destruir el alojamiento de ensayo: restaurar autoridad, publicaciones y adjuntos conforme a RPO/RTO ensayados |
| A03 | R01, R02 | F1 | Interrumpir traslado en cada paso: reanudar sin doble autoridad ni pérdida silenciosa |
| A04 | R01, R02 | F1 | Proponer cambios críticos incompatibles: rechazar conflicto o entrar en estado seguro documentado |
| A05 | R01 | F1 | Robar una sesión ordinaria: no basta para apropiación irreversible sin controles críticos previstos |
| A06 | R01, R02 | F1 | Perder correo o dispositivo: recuperar con medios suficientes restantes; declarar el caso no recuperable si falta evidencia |
| A07 | R01, R02 | F5 | Perder servicio común de identidad: demostrar continuidad o limitar garantías públicas explícitamente |
| A08 | R01 | F3 | Descargar exportación y leerla con herramienta independiente: manifiesto, textos y archivos accesibles |
| A09 | R01 | F3 | Exportación ordinaria: no contiene secretos activos ni claves de administración |
| A10 | R01 | F3 | Cambiar nombre visible: permanecen relaciones y referencias a objetos |
| A11 | R01, R04 | F2 | Dos seudónimos de la misma persona: recuperación o interfaz no los vincula públicamente |
| A12 | R01, R04 | F3 | Solicitud maliciosa de recuperación: no transfiere ni bloquea cuenta automáticamente |
| A13 | R01 | F3 | Recuperar identidad con claves de contenido perdidas: informar de contenido no descifrable; no afirmar restauración completa |
| A14 | R01 | F3 | Marca huérfana experimental: no se activa por inactividad; requiere procedimiento; admite revisión y no libera identidad |
| A15 | R03 | F3 | Cuenta gratuita: alta, publicación, permisos, cronología, recuperación, respaldo y salida funcionan sin pago ni anuncios |
| A16 | R02, R03 | F5 | Instalación por operador independiente: participa con otro nodo sin administración común ni servicio comercial obligatorio |
| A17 | R02, R03 | F5 | Cierre de nodo voluntario: aviso cuando sea posible y continuidad desde respaldo; documentar pérdida de cambios dentro del RPO |
| A18 | R03 | F3 | Cuota agotada: aviso, lectura y exportación disponibles; no borrado inesperado para forzar pago |
| A19 | R03 | F5 | Capacidad de altas agotada: espera o alternativa válida; no ocultar falta de recursos |
| A20 | R03 | F5 | Directorio recomienda operadores por política pública, sin preferencia comprada |
| A21 | R03, R09 | F6 | Cancelar servicio comercial: conserva derechos básicos y permite transición de capacidad |
| A22 | R04 | F2 | Prueba no técnica de alta/publicación/comunidad: medir autonomía con criterio y muestra definidos |
| A23 | R04 | F2 | Alta no exige elegir nodo, custodios, algoritmo ni modelo de almacenamiento |
| A24 | R04 | F3 | Interrupción móvil durante publicación/importación: conserva borrador y reanuda sin duplicación |
| A25 | R04 | F3 | Teclado y lector de pantalla: completar funciones básicas; registrar incumplimientos WCAG |
| A26 | R04 | F3 | Estado de envío distingue aceptado, pendiente y error sin jerga ni confirmación falsa |
| A27 | R05 | F3 | Importar origen textual validado: comparar manifiesto, hilos disponibles y archivos recibidos |
| A28 | R05 | F3 | Importar origen fotográfico validado: abrir medios propios sin depender del origen |
| A29 | R05 | F3 | Archivo dividido/incompleto: detectar partes faltantes o declarar incertidumbre; no afirmar integridad |
| A30 | R05 | F3 | Repetir importación: ningún duplicado de objetos o relaciones por reintento |
| A31 | R05 | F3 | Publicación similar en dos redes: preservar procedencias y conversaciones, sin fusión destructiva |
| A32 | R05 | F3 | Coincidencia solo de nombres: no restablecer relación como identidad verificada |
| A33 | R05 | F3 | Contacto llega después: coincidencia según preferencias, sin cuenta ficticia ni amistad unilateral |
| A34 | R05 | F3 | Contacto bloqueado importado: no sugerencia ni interacción reactivada automáticamente |
| A35 | R05 | F3 | Archivo manipulado: no convertir datos subidos en prueba de control del origen |
| A36 | R05 | F3 | Mensajes privados y audiencias inciertas: no publicación automática; la importación restante continúa |
| A37 | R05 | F3 | Contenido histórico: fechas y origen visibles; no notificaciones masivas ni reputación local fabricada |
| A38 | R05 | F3 | Archivo hostil: no ejecución, escape de rutas, agotamiento ilimitado ni solicitudes a infraestructura privada |
| A39 | R05 | F3 | Temporales: comprobar caducidad y borrado conforme a política; reintento explícito si hace falta retención |
| A40 | R06 | F1 | Leer contenido privado sin permiso: denegación en servicio y archivos, no solo en interfaz |
| A41 | R06 | F1 | Revocar membresía y desconectar nodo: no conceder lecturas nuevas con permisos no verificables |
| A42 | R06 | F3 | Plantillas pública/editorial/privada: comprobar leer, comentar y publicar con cada rol |
| A43 | R06, R13 | F3 | Intentar cambiar privada a pública sin unanimidad expresa: impedirlo aunque se preserve historial; silencio e inactividad no cuentan como consentimiento |
| A44 | R06 | F3 | Títulos, miembros, miniaturas y notificaciones privados: no filtración a visitante o índice público |
| A45 | R06 | F3 | Expulsión comunitaria: limita participación local sin destruir identidad de red |
| A46 | R06, R01 | F3 | Autor retira cuerpo comunitario: la comunidad no lo reescribe como autor; respuestas conservan referencia sin reproducción indebida |
| A47 | R06 | F5 | Sustituir administración/alojamiento comunitario: autoridad y permisos preservados según procedimiento, sin mover cuentas personales |
| A48 | R07 | F3 | Cronología funciona sin recomendador externo y no exige pago |
| A49 | R07 | F6 | Caída/revocación de algoritmo externo: regreso comprensible a cronología, sin pérdida de contenido |
| A50 | R07 | F6 | Recomendador solicita datos excesivos: permisos mínimos aplicados y revocables |
| A51 | R07 | F3 | Orden comunitario frente a inicio personal: ambos ámbitos visibles y ninguna anulación de acceso |
| A52 | R07 | F6 | Recomendación: explicación disponible; promociones comerciales diferenciadas |
| A53 | R08 | F3 | Interés privado no aparece en perfil, moderación ni recomendaciones públicas por error |
| A54 | R08 | F5 | Especialidad autodeclarada distinguible de reconocimiento con evidencia |
| A55 | R08 | F5 | Reputación: sin nota universal, ranking de personas ni avisos para aumentarla |
| A56 | R08 | F5 | Reconocimiento portable: conserva emisor/contexto; no concede privilegios automáticos en otra comunidad |
| A57 | R08 | F5 | Emisión recíproca masiva: límites y revisión sin transformar controles en puntuación personal opaca |
| A58 | R09 | F6 | Publicidad desactivada: servicio básico funcional y sin represalia |
| A59 | R09 | F6 | Activar/revocar publicidad: beneficio, datos y consecuencias claros; intereses privados excluidos |
| A60 | R09, R10 | F5 | Donación o servicio contratado: no compra voto, reputación ni excepción de moderación |
| A61 | R10 | F3 | Denuncia y recurso: motivo, autoridad, alcance y estado accesibles sin revelar evidencia sensible |
| A62 | R10 | F5 | Bloqueo de nodo: procedimiento y efectos documentados; no apropiación de identidades |
| A63 | R10 | F4 | Decisión técnica y reforma constitucional: procedimientos separados y publicados |
| A64 | R10 | F5 | Representación: no activar votación vinculante sin censo, resistencia a abuso y sustitución definidos |
| A65 | R10 | F5 | Incidente urgente: medida limitada, registro y revisión; no poder de emergencia indefinido |
| A66 | R11 | F4 | Instalación desde copia limpia por tercero con documentación, configuración de ejemplo y dependencias disponibles |
| A67 | R11 | F4 | Revisión de repositorio e historial: sin secretos, datos de usuarios ni artefactos sensibles |
| A68 | R11 | F0 | Repositorio abierto, licencia aprobada y guía mínima de contribución antes del desarrollo público; no esperar al piloto; revisar compatibilidad de dependencias en cada incorporación |
| A69 | R11 | F4 | Contribución externa de ensayo: guía, revisión, pruebas y autoridad de aceptación funcionan |
| A70 | R11 | F0 | Canal privado de vulnerabilidades y etiquetado experimental desde la apertura; política de versiones mantenidas antes de releases operativas |
| A71 | R02, R03 | F5 | Caída de distribuidor principal: ruta alternativa ensayada para alcance declarado |
| A72 | R01, R06 | F3 | Retirada con eventos desordenados: no resucitar versión retirada; medir pendientes y caducidad de respaldo |
| A73 | R03, R04 | F3 | Ensayo de carga: publicar entorno, mezcla y errores; no extrapolar escala masiva |
| A74 | R01, R03 | F5 | Respaldo bajo operador independiente: restauración no depende de claves inaccesibles del origen |
| A75 | R01, R02 | F5 | Inventariar registros, proxies, copias y terceros: minimizar IP, relaciones y contenido; comprobar caducidad por categoría |
| A76 | R01, R04 | F5 | Notificaciones, vistas previas y errores: no filtrar texto privado, ubicación de medios ni vinculación entre seudónimos |
| A77 | R02, R04 | F5 | Acceso en Tor Browser y sin tienda: funciones básicas utilizables con controles de abuso proporcionados; sin garantía de anonimato absoluto |
| A78 | R01, R02 | F5 | Bloquear dominio principal en ensayo: verificar alternativa autenticada y continuidad de identidad sin enviar credenciales a espejos no confiables |
| A79 | R01, R10 | F5 | Simular requerimiento externo: validación, alcance, registro restringido, revisión y comunicación según procedimiento aplicable |
| A80 | R01, R02 | F1 | Revisar contenido restringido frente a acceso al servidor: límites explícitos y decisión de E2EE; no ofrecer protección de alto riesgo sin evaluación y pruebas específicas |
| A81 | R01, R06 | F1 | Ensayo de cifrado mixto: nodos de entrega y respaldo no reciben claves de contenido por ejercer su rol; separar públicos, restringidos y cifrados |
| A82 | R01, R06 | F1 | Alta/expulsión con dispositivos desconectados: nuevas claves aplicadas; nuevo miembro sin historial anterior por defecto; expulsado sin mensajes futuros tras revocación efectiva |
| A83 | R01 | F1 | Recuperar cuenta sin claves históricas: no descifrar ni incorporar silenciosamente dispositivos en grupos; informar de pérdida parcial |
| A84 | R01, R06 | F1 | Búsqueda, notificaciones y adjuntos cifrados: no filtrar texto ni claves a índices/servicios externos |
| A85 | R01, R10 | F1 | Denuncia en grupo cifrado: compartir solo selección autorizada y contexto señalado; no acceso general del operador al historial |
| A86 | R01, R02 | F1 | Revisar cliente web alterado y sustitución de claves: declarar límites, controles y necesidad de distribución verificable; no atribuir seguridad global solo a MLS |
| A87 | R12 | F2 | Comprensión de interacción: distinguir acuerdo, interés y seguimiento sin atribuir al interés privado adhesión pública |
| A88 | R08, R12 | F3 | Guardar interés: no notificar al autor, publicar marcador ni derivar reputación o autorización publicitaria |
| A89 | R06, R12 | F3 | Señal de acuerdo en espacio restringido: no revelar contenido ni participantes fuera de su audiencia |
| A90 | R07, R12 | F3 | Reacciones o falta de reacción: sin prioridad automática, penalización, contador competitivo ni presión para corresponder |
| A91 | R04, R12 | F2 | Lectura y salida: conservar posición, puntos de parada y control de avisos sin rachas ni reproducción forzada |
| A92 | R09, R12 | F6 | Proveedor de anuncios o recomendaciones: no eludir autonomía de atención ni usar intereses privados sin autorización |
| A93 | R13 | F3 | Consulta de apertura: censo verificable sin exclusiones para eludir consentimiento; unanimidad no publica automáticamente aportaciones de antiguos integrantes |
| A94 | R14 | F3 | Ausencia o retirada del promotor/administrador: procedimiento de sustitución y continuidad verificable, sin apropiación por fundador, operador o miembro más activo |
| A95 | R01, R04 | F2 | Perfil mínimo: alta y participación sin foto, biografía, intereses o contactos importados |
| A96 | R01 | F2 | Seudónimos separados: no vinculación pública por dispositivo o recuperación compartida |
| A97 | R01, R04 | F2 | Nombre cambiado o repetido: referencias continuas y desambiguación sin exponer datos privados |
| A98 | R04, R06 | F2 | Seguir, pertenecer y acceder: comprensión de diferencias sin conceder permisos implícitos |
| A99 | R06 | F2 | Crear comunidad mediante plantilla: no configurar matriz completa; permisos de lectura/comentario/tema inequívocos |
| A100 | R06, R13 | F2 | Consulta de apertura incompleta: comunidad sigue privada aunque solo se pretenda abrir contenido futuro |
| A101 | R06, R14 | F2 | Sustitución de administración: recorrido comprensible y ausencia de propiedad perpetua del creador |
| A102 | R04, R12 | F2 | Primera entrada sin seguimientos: búsqueda y exploración útiles sin personalización obligatoria |
| A103 | R07, R12 | F2 | Novedades y conversación intensa: conservar posición, no reinyectar por respuestas ni reacciones |
| A104 | R02, R07 | F2 | Búsqueda parcial o caída: distinguir falta de resultados y falta de cobertura; no derivar consultas privadas silenciosamente |
| A105 | R01, R07 | F2 | Consultas y perfil: no notificar visitas/búsquedas ni convertir lectura sensible en rasgo público |
| A106 | R04, R12 | F2 | Avisos agrupados y resúmenes opcionales: sin campaña de reactivación por inactividad |
| A107 | R08 | F2 | Interés, especialidad declarada y reconocimiento: etiquetas comprendidas y ausencia sin penalización |
| A108 | R08, R12 | F2 | Reconocimiento recibido: no publicación automática en perfil ni aviso de recompensa o pérdida de posición |
| A109 | R06, R08 | F3 | Reconocimiento privado: no divulgar comunidad, miembros ni contenido por aceptación unilateral del receptor |
| A110 | R08 | F3 | Atribución errónea o retirada: ocultar/impugnar sin humillación ni reescribir autoría |
| A111 | R08, R12 | F2 | Reputación sin puntos: comparar utilidad con selección personal de aportaciones y sin reconocimientos externos |
| A112 | R06, R10 | F2 | Denuncia frente a desacuerdo: no exigir terminología jurídica ni tratar cantidad de reportes como prueba |
| A113 | R01, R10 | F3 | Recurso con moderador implicado: derivación o límite de independencia declarados |
| A114 | R01, R10 | F3 | Evidencia y comunicación: expediente restringido separado de decisión comunicable y exportación pública |
| A115 | R03, R09 | F2 | Cuota gratuita agotada: alternativas comprensibles y derechos básicos, sin pago como única salida presentada |
| A116 | R03, R09 | F3 | Cancelación comercial: revocar datos y explicar transición sin borrado inmediato ni privilegios persistentes |
| A117 | R03, R14 | F3 | Cambio de operador voluntario: revocar acceso anterior y comprobar continuidad de servicio y autoridad |
| A118 | R01, R05 | F2 | Entrada con datos externos: resumen claro sin preguntas por elemento ni exposición de aportaciones ajenas |
| A119 | R01, R05 | F3 | Reversión de importación publicada: distinguir lote propio y respuestas locales ajenas |
| A120 | R01 | F2 | Cuenta huérfana frente a pérdida de archivo: no confundir titular recuperado sin historial con falta de control |
| A121 | R01, R04 | F2 | Salida y eliminación: exportación sin baja obligatoria ni formularios de retención emocional |
| A122 | R10, R14 | F3 | Comunidad cerrada o administración ausente: procedimiento y límites, sin adjudicarla por actividad o financiación |
| A123 | R03, R10 | F5 | Gobierno y recursos: contribución económica no compra voto; representación requiere censo validado |
| A124 | R01, R12 | F2 | Edición sustancial y retirada sensible: no atribuir apoyo al texto nuevo ni perpetuar datos purgados mediante versiones visibles |
| A125 | R04, R05 | F2 | Primera y segunda sesión sin contactos: observar utilidad concreta y razón de regreso intencional sin exigir reclutamiento |
| A126 | R01, R05 | F2 | Historial importado: comparar recuperación de una aportación con gestión manual de exportación; registrar ayuda y pérdidas |
| A127 | R04, R12 | F2 | Contraste con referente existente: misma tarea y condiciones documentadas; medir utilidad, autonomía y esfuerzo sin objetivos de uso compulsivo |
| A128 | R03 | F0 | Catálogo voluntario: cada rol explicita tarea, alcance, recursos, acceso, apoyo, exclusiones y retirada |
| A129 | R03, R14 | F3 | Ensayo de contribución voluntaria con relevo: medir instalación, mantenimiento, incidentes, coste y salida segura |
| A130 | R03, R10 | F5 | Bienes comunes: identidad, respaldo y soporte con responsables, capacidad y continuidad comprometidos; no contar simpatía como provisión |
| A131 | R03, R08 | F2 | Reconocimiento a contribución: opcional y sin puntos sociales, votos adicionales ni propiedad sobre cuentas |
| A132 | R04, R05 | F2 | Transición gradual individual: probar y traer parte del historial sin cerrar origen, asumir exclusividad o configurar interoperabilidad |
| A133 | R03, R09 | F2 | Reciprocidad candidata: dos clientes compatibles conservan permisos equivalentes sin imposición de publicidad ajena |
| A134 | R03, R09 | F2 | Capacidad compartida: no duplicar íntegramente compromisos de operador entre beneficiarios |
| A135 | R09, R10 | F2 | Distinguir firma de compromiso, evidencia de pago y prestación real; no presentar una como prueba de las otras |
| A136 | R09, R10 | F2 | Emisor sin mandato o fuera de alcance: no habilitar prestaciones solo por verificar firma |
| A137 | R01, R09 | F2 | Estado de acreditación inaccesible o caducado: política explícita; no pérdida de identidad ni bloqueo de salida |
| A138 | R09 | F2 | Publicidad local fuera de mecanismo: documentar límite de control y alcance de investigación, no afirmar detección universal |
| A139 | R09, R10 | F2 | Captura manipulada o denuncia masiva: contraste y contradicción, sin sanción por número de reportes |
| A140 | R01, R09 | F2 | Evidencia de campaña: minimizar datos de denunciantes y terceros, sin monitorizar pantallas por defecto |
| A141 | R09, R10 | F2 | Acreditador vinculado al investigado: conflicto visible y derivación o límite de independencia declarado |
| A142 | R09, R10 | F2 | Informes contradictorios: procedimiento revisable, sin votos de denunciantes ni financiación como criterio de verdad |
| A143 | R01, R09 | F2 | Revocar mandato o clave: revisar alcance sin declarar falsas automáticamente todas las acreditaciones históricas |
| A144 | R03, R09 | F3 | Retirada del principal aportante: transición de capacidad y continuidad personal, sin expropiación de cuentas |
| A145 | R01, R09 | F2 | Consultas de estado: evitar seguimiento individual de uso por el acreditador y documentar validez de caché |
| A146 | R03, R10 | F0 | Alcance de reciprocidad formalmente decidido antes de imponer cuotas, umbrales o rechazo obligatorio |
| A147 | R10, R11 | F0 | Compatibilidad de licencia y condiciones de recursos: revisión antes de adoptar restricciones de oferta |
| A148 | R09, R12 | F2 | Contribución publicitaria: no exime de autonomía de atención ni compra reputación, alcance o autoridad |

Las pruebas A133–A148 corresponden a un mecanismo candidato de reciprocidad. Su adopción y configuración requieren resolver las decisiones Q23–Q29; definirlas no activa obligaciones o sanciones. Las fases indican el momento de evaluación si la propuesta se incorpora al alcance.

## Registro de ejecución

Por prueba: fecha, versión, entorno, datos sintéticos o consentimiento, pasos, resultado observado, evidencia, responsable y defectos. «No aplicable» exige motivo y revisión; no sustituye un requisito incómodo. Los casos de seguridad y fallo estructural bloquean su fase mientras no se resuelvan o cambie explícitamente el alcance aprobado.
