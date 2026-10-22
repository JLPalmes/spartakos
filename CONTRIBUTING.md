---
title: Spartakos — Guía inicial de contribución
lang: es-ES
license: CC-BY-SA-4.0
version: 0.1
date: 2026-10-22
status: Guía inicial de contribución bajo licencias adoptadas
---

# Contribuir a Spartakos

Spartakos está en especificación y prototipo descartable. No hay servicio de producción ni componente de privacidad listo para uso real. El destino público es [JLPalmes/spartakos](https://github.com/JLPalmes/spartakos). Las licencias se describen en [LICENCIAS.md](LICENCIAS.md); el estado operativo de la apertura consta en [preparación de apertura](PREPARACION-DE-APERTURA.md).

## Dónde empezar

Leer el [índice](README.md), los requisitos R01–R14 de la [especificación](ESPECIFICACION.md) y el bloque funcional relacionado con el cambio. Distinguir requisito confirmado, recomendación y duda pendiente. Una propuesta de arquitectura no debe presentarse como función operativa.

Tareas iniciales acotadas:

- Revisar lenguaje y comprensión de audiencias del prototipo, sin datos reales.
- Comprobar navegación por teclado, foco, ampliación y lectura asistida; registrar entorno y fallos.
- Proponer escenarios adversos para consentimiento, censo y continuidad.
- Preparar ejemplos sintéticos de exportación con procedencia e integridad explícitas.
- Revisar el contrato de autoridad antes de elegir protocolos o bases de datos.

## Presentar un cambio

Explicar el problema concreto, comportamiento anterior y propuesto, requisito afectado, validación y límites. Si cambia una regla de privacidad, autoridad o gobierno, acompañarlo de una propuesta de decisión y consecuencias; no introducirlo como detalle de interfaz.

Mantener cambios acotados y revisables. No mezclar un arreglo de navegación con una nueva política de datos. Si una propuesta amplía el alcance, actualizar descripción y pruebas para reflejar su resultado final.

La coordinación del repositorio organiza el trabajo técnico; no obtiene por ello propiedad sobre comunidades o identidades de una futura red. Las reglas constitucionales no se cambian mediante una aprobación de código.

## Comprobaciones disponibles

La [guía del prototipo](prototipo/README.md) describe cómo abrirlo y ejecutar sus pruebas sin dependencias externas. Sus diez pruebas locales no verifican seguridad ni los 148 criterios de producto. Registrar qué se ejecutó y qué no; no escribir «todo probado» después de una comprobación parcial.

Documentación y metadatos de revisión en español de España (`es-ES`), conservando otro idioma en pasajes deliberadamente escritos en él. No añadir datos personales, contraseñas, exportaciones reales, claves, registros de comunidades ni direcciones de contacto privadas a los ejemplos o pruebas.

## Derechos y participación

La contribución conserva su autoría y se incorpora bajo la licencia aplicable al material, conforme a LICENCIAS.md. No se exige cesión exclusiva al promotor por defecto. Declarar procedencia y avisos de código o materiales ajenos. Al proponer su incorporación, indica que dispones de derechos suficientes para ofrecerla bajo esa licencia. La accesibilidad pública de una obra ajena no basta para incorporarla.

Las discrepancias razonadas forman parte de la revisión. No se admite acoso, amenazas ni divulgación de datos privados. La coordinación inicial y sus límites se identifican en GOVERNANCE.md y CODE_OF_CONDUCT.md; no se presupone un comité independiente ya constituido.
