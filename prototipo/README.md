---
title: Spartakos — Prototipo descartable de experiencia
lang: es-ES
license: CC-BY-SA-4.0
version: 0.1
date: 2026-10-22
status: Maqueta local; sin red, seguridad ni validación con participantes
---

# Prototipo de experiencia

Sirve para inspeccionar navegación, audiencias, interés privado, importación ficticia y unanimidad. No inicia la implementación de la red ni adopta protocolos o componentes de producción. No contiene cuentas reales, cifrado, persistencia, autenticación ni comunicación entre nodos. Los roles se simulan desde la misma pantalla para comprobar reglas; un producto real no permitiría consentir en nombre de otra persona.

## Abrir y comprobar

Desde la raíz del proyecto, servir solo en la máquina local:

```sh
python3 -m http.server 8765 --bind 127.0.0.1 --directory prototipo
```

Abrir `http://127.0.0.1:8765`. No requiere instalar dependencias ni conectar servicios externos. Recargar restablece el estado. No introducir información personal: es una maqueta de diseño.

Pruebas del modelo de simulación:

```sh
node --test prototipo/modelo.test.mjs
```

Estas pruebas comprueban reglas del modelo local, no los criterios A01–A148 de una aplicación operativa. Tampoco prueban seguridad, control real de acceso ni comprensión de los participantes.

## Tareas disponibles

1. Llegar sin contactos y encontrar una conversación útil.
2. Publicar con audiencia explícita; comprobar su indicación y ubicación.
3. Guardar interés sin acuerdo público ni cambio de permisos.
4. Importar repetidamente un archivo ficticio sin fabricar contactos activos.
5. Proponer apertura; probar mayoría insuficiente, negativa y unanimidad.
6. Simular una baja durante la propuesta y comprobar que no elude la protección.
7. Exportar las acciones ficticias de la sesión.

El control de acceso se representa solo mediante estados. Cualquier persona con acceso a la maqueta puede inspeccionar todos sus datos ficticios. El modelo adopta una protección conservadora para bajas durante apertura; la revisión del censo de una comunidad real exigiría historia de membresía, expedientes y política adoptada.
