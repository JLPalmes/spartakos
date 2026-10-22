---
title: Spartakos — Documentación del proyecto
lang: es-ES
license: CC-BY-SA-4.0
date: 2026-10-22
---

# Spartakos

Nombre provisional de la red: **Spartakos**.

Proyecto en fase de especificación y prototipo descartable. Existe una maqueta local con datos ficticios; todavía no existe una aplicación de red operativa.

La orientación confirmada es una base gratuita sostenida por iniciativas voluntarias distribuidas, con servicios comerciales opcionales no imprescindibles. Experiencia sencilla, identidad y publicaciones bajo control de sus titulares y derecho efectivo a cambiar de proveedor.

## Código y colaboración abiertos

Repositorio de referencia: [JLPalmes/spartakos](https://github.com/JLPalmes/spartakos). Licencias adoptadas: AGPL-3.0-or-later para servicio y prototipo, Apache-2.0 para futuras bibliotecas independientes con aviso expreso y CC-BY-SA-4.0 para documentación original. Véase el [mapa de licencias](LICENCIAS.md).

Para participar: [guía de contribución](CONTRIBUTING.md), [coordinación inicial](GOVERNANCE.md), [conducta](CODE_OF_CONDUCT.md) y [seguridad de esta etapa](SECURITY.md).

## Abrir el prototipo y comprobar la copia

Requisitos: Python 3 y Node.js 22 o posterior. No hay dependencias de terceros que instalar. Desde la raíz de una copia del repositorio:

```sh
python3 verificar.py
node --test prototipo/modelo.test.mjs
python3 -m http.server 8765 --bind 127.0.0.1 --directory prototipo
```

Abrir `http://127.0.0.1:8765`. Los datos son ficticios y se borran al recargar; no introducir información personal. Estas comprobaciones no prueban seguridad ni una red distribuida.

## Lectura principal

1. [Especificación integral v0.19](ESPECIFICACION.md): primera pasada funcional y contraste comparado; reciprocidad y acreditación como mecanismos candidatos.
2. [Decisiones, dudas y riesgos](DECISIONES-Y-DUDAS.md): qué está confirmado, qué se propone y qué exige ensayo.
3. [Matriz de aceptación](MATRIZ-DE-ACEPTACION.md): 148 pruebas especificadas, ninguna ejecutada; incluye escenarios condicionados a adoptar reciprocidad.
4. [Antecedentes y lecciones](ANTECEDENTES-Y-LECCIONES.md): fuentes, cobertura y límites de la investigación.
5. [Vigilancia y resistencia a la censura](VIGILANCIA-Y-CENSURA.md): modelo de amenazas, medidas y límites.
6. [Modelo mixto de privacidad](MODELO-MIXTO-DE-PRIVACIDAD.md): contenido público, espacios cifrados, claves y recuperación.
7. [Primer ensayo estructural](ENSAYO-01-COMPONENTES-Y-VALIDACION.md): componentes candidatos, 15 casos reproducibles y criterios de descarte; no ejecutado.
8. [Identidad, perfil y relaciones](FUNCIONAL-01-IDENTIDAD-PERFIL-Y-RELACIONES.md): primer bloque de diseño funcional, con alternativas pendientes.
9. [Interacción útil y autonomía de atención](FUNCIONAL-02-INTERACCION-UTIL.md): acuerdo, interés privado y seguimiento sin diseño orientado a dependencia.
10. [Publicaciones, audiencias y conversaciones](FUNCIONAL-03-PUBLICACIONES-Y-CONVERSACIONES.md): editor, respuestas, difusión, edición y retirada.
11. [Comunidades y permisos](FUNCIONAL-04-COMUNIDADES-Y-PERMISOS.md): plantillas, roles, participación, moderación local y continuidad.
12. [Inicio, búsqueda y descubrimiento](FUNCIONAL-05-INICIO-BUSQUEDA-Y-DESCUBRIMIENTO.md): lectura, exploración, privacidad de consultas y avisos útiles.
13. [Intereses y reputación](FUNCIONAL-06-INTERESES-Y-REPUTACION.md): presentación personal y evidencia contextual sin puntuación.
14. [Moderación y recursos](FUNCIONAL-07-MODERACION-Y-RECURSOS.md): protección, denuncias y decisiones revisables.
15. [Base gratuita y servicios](FUNCIONAL-08-BASE-GRATUITA-Y-SERVICIOS.md): cuotas, operadores voluntarios y extras opcionales.
16. [Entrada, recuperación y salida](FUNCIONAL-09-ENTRADA-RECUPERACION-Y-SALIDA.md): recorridos individuales de continuidad.
17. [Continuidad y gobierno](FUNCIONAL-10-CONTINUIDAD-Y-GOBIERNO.md): competencias, sustitución y unanimidad.
18. [Síntesis funcional](REVISION-FUNCIONAL.md): recorrido recomendado de revisión y decisiones abiertas.
19. [Revisión comparada e incentivos](REVISION-COMPARADA-E-INCENTIVOS.md): ventajas potenciales, precedentes, carencias de migración y propuesta para servicios voluntarios.
20. [Reciprocidad de servicios](PROPUESTA-RECIPROCIDAD-DE-SERVICIOS.md): contribución a infraestructura común como posible condición de ofertas comerciales e institucionales; propuesta no adoptada.
21. [Acreditación y recursos](RECIPROCIDAD-ACREDITACION-Y-RECURSOS.md): responsabilidades, credenciales, denuncias, revisión y decisiones pendientes.

Los documentos de análisis conservan los antecedentes técnicos. La especificación vigente define el alcance del proyecto.

## Prototipo y comprobaciones

La [maqueta de experiencia](prototipo/README.md) permite probar recorridos con datos ficticios. Se han superado diez pruebas del modelo local y comprobado en navegador publicación restringida, interés privado, importación ficticia y unanimidad. El [informe de resultados](RESULTADOS-DEL-PROTOTIPO.md) distingue estas comprobaciones de las pruebas de producto, que siguen sin ejecutarse.

El [contrato preliminar de datos y autoridad](CONTRATO-DE-DATOS-Y-AUTORIDAD.md) fija separaciones antes de elegir componentes. El [paquete de apertura](PREPARACION-DE-APERTURA.md) documenta el repositorio y las licencias adoptadas, y las condiciones de contribución.

## Continuación preparada

La [resolución propuesta de los 29 pendientes](RESOLUCION-DE-PENDIENTES.md) concreta recomendaciones, alternativas y dependencias. Se complementa con el [gobierno de la acreditación](GOBIERNO-DE-LA-ACREDITACION.md), el [programa de operadores voluntarios](OPERACION-Y-VOLUNTARIADO.md) y el [protocolo de validación](VALIDACION-Y-PUERTAS-DE-AVANCE.md). Son propuestas listas para revisar, sin ratificación implícita.

La continuación exige evidencia: participantes para probar recorridos, archivos consentidos para importación, operadores comprometidos y ensayos técnicos. Las licencias iniciales y el destino público están adoptados. La autoridad de gobierno de la red, los operadores y la validación siguen pendientes. No se ha iniciado la implementación de la red; la maqueta es descartable.
