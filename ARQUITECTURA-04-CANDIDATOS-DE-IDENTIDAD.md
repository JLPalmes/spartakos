---
title: Spartakos — Comparación de mecanismos de identidad para el laboratorio
lang: es-ES
license: CC-BY-SA-4.0
date: 2026-10-27
version: 0.1
status: Investigación documental y recomendación de laboratorio; sin integración ni arquitectura adoptada
---

# Identidad que sobreviva al alojamiento

## 1. Resultado de la comparación

Se propone **KERI/KERIpy como primer candidato de laboratorio para estudiar continuidad de control**, y PLC como contraste de directorio central si hace falta aislar ese compromiso. Es una selección provisional para medir fallos y costes, no una decisión de producción. Ningún candidato ha superado todavía los casos estructurales de Spartakos.

La razón de priorizar KERI es su separación entre identificador, evolución de claves y evidencias conservadas por otros participantes. Deben ensayarse disponibilidad, recuperación y detección de conflictos; no se deduce que funcione sin infraestructura o sin confianza. PLC ofrece un contraste útil, pero no basta para cerrar la independencia de una autoridad común. Esta valoración es una inferencia de diseño, apoyada en las fuentes de las secciones siguientes.

El barrido cubre nueve alternativas o familias relevantes. No pretende enumerar todos los métodos DID ni comparar todas las funciones sociales de sus ecosistemas. La unidad comparada es el control de identidad y su localización, no una red social completa.

## 2. Criterios y etiquetas de evidencia

Una candidata debe permitir probar: identidad persistente, cambio de ubicación sin permiso exclusivo del alojamiento, separación de claves ordinarias y control crítico, recuperación con medios suficientes, rechazo o detección de autoridad anterior, continuidad sin un directorio único y operación asumible para voluntarios.

**Documentado** significa que la fuente define una propiedad. **Observado** significa que se leyó un manifiesto, licencia o referencia Git. **Pendiente** significa que falta ejecutar o verificar la integración. Ninguna propiedad documental se contabiliza como prueba funcional superada. «No demostrado» no significa que ningún desarrollo futuro pueda resolverlo.

## 3. Comparación de familias

| Familia | Qué aporta | Dependencia o problema que debe resolverse | Papel en el ensayo |
| --- | --- | --- | --- |
| `did:key` | Identificador derivado de una clave, resolución determinista | El método no permite actualizar ni desactivar ese DID; no aporta el ciclo de recuperación requerido | Referencia mínima, no identidad principal |
| Nostr, protocolo básico | Eventos firmados vinculados a una clave pública y circulación por relays | NIP-01 no define por sí solo continuidad de la misma identidad al sustituir una clave perdida o robada | Contraste de publicación independiente del relay |
| `did:web` | Resolución sencilla mediante dominio y HTTPS | Control del dominio, DNS y alojamiento del documento; no da continuidad independiente de ese dominio | Contraste de dependencia web |
| PLC | Historial firmado, rotación y reglas de recuperación | Directorio central que recibe y valida cambios | Contraste de independencia de alojamiento con autoridad común |
| PKARR | Localización mediante registros firmados en DHT o relays | Republicación, registros efímeros y ciclo de control/recuperación no demostrado para Spartakos | Candidato de localización, no solución completa de identidad |
| `did:dht` | Documento DID en registros mutables firmados de Mainline DHT | Clave de identidad no rotatable dentro del mismo identificador; retención y recuperación | Contraste de directorio distribuido con clave raíz rígida |
| `did:webvh` | Historial verificable, SCID y mecanismos opcionales de portabilidad y testigos | El cambio de dominio puede cambiar la cadena DID; localizar la historia vigente requiere una ruta disponible | Alternativa de historial web a estudiar |
| KERI | Identificador y evolución verificable de claves; testigos y observadores | Configuración, disponibilidad y reconciliación de conflictos; no hay garantía universal por añadir testigos | Primer candidato de continuidad de control |
| ION/Sidetree | Cambios y recuperación con orden determinado por anclaje | Red de anclaje y almacenamiento asociado; esfuerzo operativo aún no medido | Reserva, no primera instalación |

Las fuentes primarias que sustentan cada fila se explicitan a continuación. La idoneidad y la prioridad de ensayo son conclusiones de Spartakos, no afirmaciones de los proyectos.

## 4. Propiedades documentadas y límites relevantes

### Claves y dominios: tres contrastes simples

`did:key` no ofrece actualización o desactivación del identificador en su propio método. Su sencillez sirve para representar material de verificación, pero no cubre nuestra continuidad de cuenta. [Especificación del método](https://w3c-ccg.github.io/did-key-spec/).

NIP-01 vincula eventos a una clave pública y define su intercambio con relays; no contiene un procedimiento general de recuperación que conserve el mismo identificador tras sustituir esa clave. Esta limitación se refiere al protocolo básico revisado, no a todas las propuestas del ecosistema. [NIP-01](https://github.com/nostr-protocol/nips/blob/master/01.md).

`did:web` deriva la localización del documento del dominio y la ruta contenidos en el DID. Cambiar el servidor conservando el dominio no prueba continuidad cuando desaparece el control de ese dominio. [Especificación](https://w3c-ccg.github.io/did-method-web/).

### PLC: un límite concreto y comprobable

La especificación usa un directorio central y claves de rotación ordenadas por prioridad. Una clave superior puede invalidar operaciones de otra inferior dentro de la ventana documentada de 72 horas. El historial público de operaciones conserva metadatos: esto merece una revisión de vigilancia y vinculación de seudónimos. No se publicarán alias reales en el laboratorio. [Especificación PLC](https://github.com/did-method-plc/did-method-plc/blob/main/website/spec/v0.1/did-plc.md).

El repositorio ofrece biblioteca y servidor TypeScript. Su README declara licencia dual MIT/Apache-2.0; el archivo LICENSE y los manifiestos leídos en la revisión inventariada distinguen ese marco de la declaración MIT de paquetes concretos. No debe interpretarse `NOASSERTION` de la API de metadatos como ausencia de licencia. [Repositorio](https://github.com/did-method-plc/did-method-plc).

### DHT: localización distribuida no equivale a recuperación

PKARR documenta registros firmados, republicación por caducidad, límite de tamaño y relays HTTP para navegadores. Permite estudiar sustitución de servicios de localización. No se ha demostrado con ello recuperación de una cuenta con identidad estable tras perder o comprometer su clave de control. [README y licencia MIT](https://github.com/pubky/pkarr), [diseño](https://github.com/pubky/pkarr/tree/main/design).

La especificación `did:dht` revisada se presenta como borrador de implementación. Su clave de identidad no es rotatable en el mismo DID; la rotación hacia otro DID no debe contarse como identidad textual invariable. La retención exige republicación. [Especificación fuente](https://github.com/decentralized-identity/did-dht/blob/main/spec/spec.md), [implementación Go y licencia Apache-2.0](https://github.com/decentralized-identity/did-dht).

### Historial web y continuidad de localización

La especificación `did:webvh` v1.0 contempla SCID, historial, portabilidad opcional desde la creación y testigos. La identidad textual puede cambiar al mover dominio/ruta aunque se conserve el SCID. Se requiere comprobar cómo un lector del identificador antiguo descubre el destino si el origen desaparece; no basta demostrar integridad de un archivo ya encontrado. [Especificación v1.0](https://identity.foundation/didwebvh/v1.0/).

El proyecto Python leído declara versión de paquete 1.0.1, pero su README aún dice implementar la especificación 0.4. Puede ser documentación desactualizada; no se ha resuelto mediante pruebas de conformidad. No equiparar el número del paquete con el de la especificación. [Implementación inventariada](https://github.com/decentralized-identity/didwebvh-py).

### KERI: candidata que exige un ensayo de fallos

KERI describe evolución de claves, testigos y observadores de historiales; distingue detección de duplicidad de confianza en un estado. No se debe simplificar a «una mayoría de servidores resuelve todo». Los testigos de eventos tampoco son automáticamente custodios de claves de recuperación. [Especificación KERI](https://trustoverip.github.io/kswg-keri-specification/).

KERIpy es una implementación Python con licencia Apache-2.0. Se verificó una etiqueta numérica 1.3.6 y su commit, cuyo manifiesto declara Python >=3.12.2. La rama HEAD observada declara 2.1.0-dev1 y otros requisitos; no se usará automáticamente como versión estable. Una etiqueta numérica no acredita auditoría, compatibilidad ni ausencia de vulnerabilidades. [Repositorio](https://github.com/WebOfTrust/keripy), [manifiesto de la etiqueta candidata](https://github.com/WebOfTrust/keripy/blob/4ce4cc79e06653f77342be1bf604086b89b1f090/setup.py).

### Anclaje distribuido

Sidetree define operaciones y orden mediante un sistema de anclaje; ION lo aplica sobre Bitcoin y utiliza almacenamiento de lotes asociado. Evitar un directorio único traslada dependencias, no elimina infraestructura. El coste y esfuerzo de mantenerla no se han medido para voluntarios de Spartakos. Se pospone como primera instalación, sin descartarlo por principio. [Sidetree](https://identity.foundation/sidetree/spec/), [ION](https://github.com/decentralized-identity/ion).

## 5. Inventario reproducible, sin instalación

El [inventario JSON](investigacion/identidad-candidatos-2026-10-27.json) conserva siete repositorios, sus HEAD observados, licencias declaradas, estado de archivo y referencias por SHA. Se consultaron metadatos públicos, `git ls-remote`, licencias y manifiestos. Un repositorio no archivado no demuestra mantenimiento suficiente. No se ejecutaron scripts ni se instalaron dependencias de esos proyectos.

| Candidata de implementación | Referencia observada | Requisito o cautela comprobada |
| --- | --- | --- |
| KERIpy, etiqueta para evaluar | `1.3.6` → `4ce4cc79e06653f77342be1bf604086b89b1f090` | `setup.py`: Python >=3.12.2; falta cerrar dependencias transitivas e instalación aislada |
| KERIpy, HEAD de contraste | `a6866a31e5b41b5d404d74554d5616ef66dba873` | Versión de desarrollo; no sustituye silenciosamente la etiqueta |
| PLC | `a2f0bdc41bd99a85796f77813108272257507b61` | Manifiestos: Node >=22.18; `.nvmrc` indica 24; servidor depende de `pg`; no se ha arrancado directorio |
| didwebvh-py | `914df0146c8d2b88633156557a509fc9a76c8796` | Licencia Apache-2.0; compatibilidad de especificación pendiente de resolver |

Estas referencias se fijan para reproducir la investigación; no constituyen un conjunto de dependencias aprobado. La revisión de avisos de seguridad, integridad de paquetes y recursos de operación precede a la instalación. El entorno local observado ofrece Python 3.14.7 y Node 22.23.4; esa coincidencia parcial de versión no demuestra que ninguna candidata pueda ejecutarse sin ajustes.

## 6. Próximo bloque ejecutable propuesto

1. Preparar un directorio de laboratorio independiente del simulador y de todos los datos del usuario. Fijar KERIpy 1.3.6 por commit y resolver sus dependencias sin actualizar Python global ni modificar el cliente social.
2. Usar las herramientas y configuración de referencia de la biblioteca para identidades sintéticas. No fijar todavía un umbral propio de Spartakos ni crear un mecanismo de recuperación nuevo.
3. Verificar persistencia, rotación y rechazo de operaciones sin autoridad antes de introducir dos alojamientos. El fallo de este paso impide presentar traslado soberano.
4. Aplicar T02–T07 del ensayo individual, registrando qué permite continuar al caer un proceso y qué deja de funcionar. No llamar caída de un directorio a detener solo una réplica de consulta.
5. Solo después probar datos y referencias de perfil entre A y B. Las programaciones copiadas permanecen inactivas; no se promete reanudación entre proveedores sin demostrar un único ejecutor.

No se ha ejecutado este bloque. La independencia institucional de los operadores, el coste de testigos y la recuperación sin medios suficientes siguen siendo cuestiones abiertas. La elección definitiva se tomará con resultados de fallos y operación, no con la cantidad de propiedades declaradas en una especificación.

## 7. Actualización del laboratorio — 27 de octubre

Después del inventario se ha ejecutado el [primer laboratorio aislado](laboratorio-identidad/README.md): cinco pruebas locales superadas con revisión y dependencias fijadas. Se completan las comprobaciones iniciales de persistencia y autoridad; no se ha ejecutado el traslado ni el ensayo con testigos. La auditoría de dependencias y la verificación de la firma de la distribución nativa siguen pendientes; el ensayo no constituye aprobación para producción.

## 8. Límite observado de los recibos — 27 de octubre

El [ensayo de recibos y discrepancias](laboratorio-identidad/README.md) añade siete pruebas superadas. Con un umbral sintético de dos de tres, faltar un recibo permite aceptar; faltar dos lo impide. Duplicar recibos o suplirlos con firmas ajenas no satisface el umbral. No se han arrancado servidores ni provocado fallos de red.

Dos verificadores aislados aceptan ramas distintas si el titular y un testigo compartido firman ambas; detectan la discrepancia al recibir la otra rama y mantienen su estado anterior. No hay convergencia automática demostrada. La evaluación de KERI continúa condicionada a contraste entre fuentes, operación de testigos y gestión de conflictos; no se eleva una mayoría de firmas a garantía general de consenso.

## 9. Transporte real y límite del servicio de recibos — 27 de octubre

Dos escenarios con procesos y HTTP locales verifican cierre normal y caída abrupta, persistencia del testigo, bloqueo sin recibos suficientes, reenvío explícito y rotación posterior. Una tercera prueba reproduce H01: ReceiptEnd firma el recibo de una interacción cuya firma de autor es inválida, aunque el evento no conste en su historial aceptado; el verificador completo sí lo rechaza. Véanse [resultados y límites](laboratorio-identidad/README.md).

KERI continúa como candidata de investigación. El endpoint de esta revisión no queda aprobado para producción; el hallazgo exige revisar la implementación y el límite de validación, sin deducir que se haya roto la autoridad del titular. No se sustituye el componente ni se inventa un protocolo propio. La consulta OSV de 34 versiones PyPI no devuelve avisos, con el alcance limitado indicado en el laboratorio.
