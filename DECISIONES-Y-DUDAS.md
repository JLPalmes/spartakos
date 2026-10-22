---
title: Spartakos — Decisiones, dudas y riesgos
lang: es-ES
license: CC-BY-SA-4.0
version: 0.19
date: 2026-10-22
status: Registro para revisión; sin aprobación implícita
---

# Decisiones, dudas y riesgos

## 1. Base confirmada

Los requisitos R01–R14 están definidos en ESPECIFICACION.md. La base es gratuita, voluntaria y distribuida, con servicios comerciales no imprescindibles. La arquitectura híbrida es la hipótesis de trabajo; sus mecanismos concretos requieren validación.

R11 y D14 establecen código abierto y colaboración desde el inicio del desarrollo.

R12 establece utilidad sin dependencia emocional; R13 exige unanimidad expresa para pasar de privada a pública; R14 separa iniciativa promotora y propiedad, con continuidad y administración sustituible. La revisión funcional precede a adoptar componentes o ejecutar el laboratorio.

## 2. Propuestas cerradas para poder revisar el conjunto

| Decisión | Propuesta de esta versión | Motivo y consecuencia |
| --- | --- | --- |
| D01 | Red generalista, apertura limitada por capacidad | No imponer nicho no solicitado; validar con alcance operativo controlado |
| D02 | Varios nodos con paquetes completos sustituibles | Mantener experiencia sencilla y permitir salida individual |
| D03 | Alta con nodo predeterminado por política pública | Evitar selector técnico; vigilar concentración |
| D04 | Roles de nodo opcionales y aplicación modular | Permitir aportaciones pequeñas sin exigir infraestructura completa |
| D05 | Identidad y recuperación sin veto del alojamiento | Derecho a irse incluso si el origen no coopera |
| D06 | Autoridad de continuidad separada en piloto; independencia reforzada antes de apertura distribuida | No fingir descentralización por tener réplicas |
| D07 | Original comunitario alojado en servicio comunitario con copia de aportación propia | Coordinar permisos sin que comunidad pueda suplantar al autor |
| D08 | Contenido restringido con control de acceso, sin promesa inicial de E2EE | Ser explícitos sobre confianza en operadores; evitar contradicción con recuperación |
| D09 | Cronología predeterminada y descubrimiento opcional | Libertad sin configuraciones obligatorias |
| D10 | Reconocimientos cualitativos, sin puntuación universal | Reputación temática discreta y con contexto |
| D11 | Texto/imagen primero; vídeo intensivo y mensajería después | Ajustar coste y operación voluntaria |
| D12 | Primeros importadores de X e Instagram sujetos a prueba | Cubrir perfiles de origen distintos; no declarar compatibilidad por anticipado |
| D13 | Publicidad futura voluntaria y contextual como preferencia | No financiar derechos básicos mediante seguimiento obligatorio |
| D14 | Código abierto y contribuciones desde el inicio del desarrollo | Revisión temprana y desarrollo colectivo sin esperar al piloto operativo |
| D15 | Adoptadas AGPL-3.0-or-later para servicio/prototipo, Apache-2.0 para bibliotecas independientes con aviso y CC-BY-SA-4.0 para documentación | Textos completos y alcance en LICENCIAS.md; comprobar compatibilidad de cada incorporación |
| D16 | Piloto con adultos; política de edades públicas antes de F5 | Evitar admitir un público sin diseño y capacidad adecuados |
| D17 | Interés privado separado de acuerdo, seguimiento y reputación | Evitar inferencias de adhesión, presión y filtración |
| D18 | Reconocimiento de aportaciones sin puntos ni privilegios automáticos | Evidencia contextual, no clasificación universal |
| D19 | Inicio cronológico y exploración separada como propuesta | Elegir lectura sin configurar algoritmos |
| D20 | Continuidad bajo reglas verificables, sin propiedad del promotor | Sustitución de administración y alojamiento sin apropiación |

Las decisiones provisionales están sujetas a revisión; sus alternativas y consecuencias constan en la especificación y los análisis.

## 3. Dudas que no deben impedir la revisión del documento

| Duda | Recomendación actual | Cuándo debe resolverse |
| --- | --- | --- |
| Q01. Identidad y protocolo concreto | Comparar mecanismos existentes con pruebas de salida y recuperación; no crear criptografía propia | F1, antes de implementar persistencia definitiva |
| Q02. Autoridad independiente o distribuida | Separar alojamiento primero; ensayar custodia conjunta y continuidad real | F1; garantías reforzadas antes de F5 |
| Q03. Custodios independientes disponibles | No confundir varios responsables del fundador con entidades distintas | Antes de presentar independencia institucional |
| Q04. Cifrado de contenido privado | Controles claros y confianza declarada en piloto; E2EE requiere ensayo específico | Antes de anunciar E2EE o admitir usos que lo requieran |
| Q05. Recursos iniciales | Inventariar recursos voluntarios y compromisos; limitar altas | Antes de F3 con usuarios reales |
| Q06. Cuota gratuita común | Fijarla por capacidad y medición, con derechos de continuidad | Antes de F5 |
| Q07. Entidad de gobierno y responsabilidades | Definir identidad jurídica y acuerdos de operadores; no equivale a constituir ahora una entidad | Antes de apertura pública |
| Q08. Representación y censo | No activar voto constitucional vinculante sin modelo contra abuso | Antes de sustituir dirección fundacional |
| Q09. Marca huérfana | Estado revisable con procedimiento; no declaración por inactividad | Ensayo F3; revisar antes de visibilidad pública |
| Q10. Licencia inicial | Resuelta: D15 adoptada y textos completos incorporados; compatibilidad de futuras dependencias sigue en revisión | Revisar cada incorporación o cambio de alcance |
| Q11. Cobertura real de exportaciones | Ensayo con archivos consentidos y categorías explícitas | Antes de anunciar cada importador |
| Q12. Acceso a APIs | Solicitar solo si el producto y requisitos lo justifican | Antes de prometer transferencia directa |
| Q13. Preparación de apertura inicial | Licencias, destino JLPalmes/spartakos y guías adoptados; falta consolidar canal privado atendido y mantener publicación comprobada | Etapa de apertura, antes de recibir información sensible |
| Q14. Vigilancia gubernamental y censura | Minimizar metadatos y puntos de bloqueo; ensayar acceso alternativo; evaluar E2EE antes de ofrecer usos de alto riesgo | Modelo de amenazas en F1, base de protección antes de F5 |
| Q15. Modelo mixto | Evaluar E2EE para espacios privados; separar acceso restringido del piloto, identidad e historial cifrado; incluir confianza en el cliente web | Ensayo estructural F1; sin promesas de protección hasta revisión |
| Q16. Identidad localizable y perfil reservado | Resolver referencias legibles y visibilidad con recorridos privados y públicos | Revisión funcional antes de congelar arquitectura |
| Q17. Interacciones y reconocimientos | Comparar graduación de acuerdo y reconocimiento contextual con alternativas más simples | Prototipo funcional antes de implementación |
| Q18. Historial, versiones y audiencia | Distinguir privacidad, cifrado, nuevos miembros y retirada de datos sensibles | Revisión funcional y modelo de datos |
| Q19. Censo de unanimidad | Impedir apertura sin todos los consentimientos y manipulación mediante expulsiones | Antes de implementar cambios de visibilidad |
| Q20. Valor para llegar individualmente | Probar primera y segunda sesión útiles sin contactos presentes; distinguir archivo y actividad social | Antes de cerrar producto mínimo |
| Q21. Incentivos para operadores | Definir compromisos acotados, costes, apoyo y salida; medir disponibilidad real por rol | Antes de reclutar infraestructura y abrir altas |
| Q22. Ventaja frente a herramientas existentes | Comparar tareas equivalentes y coste de cambio; no deducir superioridad de la especificación | Revisión funcional y prototipo |
| Q23. Ámbito de reciprocidad | Distinguir reglas de recursos comunes, programa recomendado y participación general; propuesta aún no adoptada | Antes de condiciones obligatorias o implementación de rechazo |
| Q24. Sujetos y proporcionalidad | Definir categorías, umbrales y capacidad neta; no contar solo máquinas ni penalizar expresión individual | Antes de reclutar servicios bajo reciprocidad |
| Q25. Autoridad de acreditación | Comparar pluralidad bajo criterios comunes y resolver legitimidad, conflictos y sustitución | Antes de emitir credenciales con efectos públicos |
| Q26. Publicidad no identificada | Categorías y evidencia que distingan anuncio, patrocinio, promoción propia y opinión | Antes de resolver denuncias con consecuencias |
| Q27. Financiación de comprobadores | Evitar compra de aprobación, dependencia del investigado y selección del más permisivo | Antes de ofrecer verificación como servicio |
| Q28. Discrepancias y estados | Definir revisión, caducidad, revocación, periodos y caída del emisor sin atrapar personas | Antes de prestaciones condicionadas |
| Q29. Licencia y condiciones de servicio | No convertir reciprocidad en restricción incompatible de uso del código; revisar el encaje elegido | Antes de licencia y contratos definitivos |

El [mecanismo candidato de reciprocidad](RECIPROCIDAD-ACREDITACION-Y-RECURSOS.md) documenta funciones, afirmaciones verificables, procedimiento y doce escenarios. Las cuestiones Q23–Q29 permanecen pendientes; no hay acreditadores seleccionados ni capacidades certificadas.

Las 29 cuestiones disponen de [recomendación desarrollada y dependencia de cierre](RESOLUCION-DE-PENDIENTES.md). No se marcan como resueltas por disponer de una propuesta. El detalle funcional se conserva en [REVISION-FUNCIONAL.md](REVISION-FUNCIONAL.md); las condiciones de prueba están en [VALIDACION-Y-PUERTAS-DE-AVANCE.md](VALIDACION-Y-PUERTAS-DE-AVANCE.md).

## 4. Riesgos y respuesta

| Riesgo | Consecuencia | Control y señal de revisión |
| --- | --- | --- |
| K01. Dependencia del servicio de identidad | Operadores múltiples sin salida real | A07, modelo de autoridad y dependencia publicada |
| K02. Capacidad voluntaria insuficiente | Pérdidas, altas incumplidas y presión hacia pago | Cuotas, reserva, espera y coste medido; A15–A20 |
| K03. Recuperación fraudulenta | Apropiación de identidad y contenido | Separación de autoridad, evidencias y ensayos A05–A14 |
| K04. Custodios que desaparecen o coluden | Bloqueo o apropiación | Modelo de umbrales/fallos explícito; no prometer tolerancia no ensayada |
| K05. Privacidad rota entre nodos | Exposición de comunidades/intereses | A40–A44, revisión de metadatos y permisos |
| K06. Moderación sin recursos | Daño y abandono de participantes | Límites de altas, herramientas, carga observada y recursos de revisión |
| K07. Formatos externos cambian | Importadores incompletos | Versionado, inventario, corpus de prueba y compatibilidad anunciada por versión |
| K08. Apertura sin colaboradores | Mantenimiento sigue concentrado | Documentación, tareas accesibles y expectativas realistas |
| K09. Captura económica o institucional | Red abierta con gobierno dependiente | Separar contribución de voto, conflictos y cambios públicos |
| K10. Confusión entre respaldo y archivo eterno | Promesas incompatibles con retirada | Conservación explícita, restauración y borrado ensayados |
| K11. Exceso de separación técnica | Coste y soporte inviable | Módulos por nodo y contratos, sin servicio obligatorio por función |
| K12. Apariencia de independencia antes de existir | Pérdida de confianza | Etiquetas de etapa y puertas de F5 verificables |

## 5. Cuestiones prioritarias de revisión

La revisión debe resolver los siguientes puntos:

1. ¿La propuesta de paquetes gratuitos voluntarios, con límites de capacidad y respaldo básico incluido, expresa la base económica deseada?
2. ¿Es aceptable un piloto con autoridad de continuidad todavía concentrada y declarada, siempre que la apertura distribuida exija resolver su sustitución?
3. ¿Se acepta posponer E2EE, mensajería y vídeo intensivo sin presentar la privacidad del piloto como equivalente a E2EE?
4. ¿Encaja el gobierno por ámbitos y la separación de financiación y voto, pendiente de resolver su representación?
5. ¿Se mantienen las licencias como preferencia de revisión o se desea otra orientación antes de desarrollar?

Las cuestiones pendientes requieren resolución explícita en el registro de decisiones.

## 6. Evidencia local disponible

La [primera comprobación del prototipo](RESULTADOS-DEL-PROTOTIPO.md) registra diez pruebas del modelo descartable y recorridos observados en navegador. Q17, Q20 y Q22 siguen necesitando participantes; Q19 cuenta con casos locales de protección de unanimidad, sin implementación de autoridad real. Q10 y Q13 tienen un [paquete concreto de apertura](PREPARACION-DE-APERTURA.md), con licencias iniciales y destino público adoptados.
