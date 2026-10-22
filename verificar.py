# SPDX-License-Identifier: AGPL-3.0-or-later
"""Comprobaciones editoriales y de licencias; no prueba la seguridad de la red."""
from hashlib import sha256
from pathlib import Path
import re
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent
errors = []
documents = sorted(ROOT.rglob('*.md'))
for path in documents:
    if '.git' in path.relative_to(ROOT).parts:
        continue
    text = path.read_text(encoding='utf-8')
    parts = text.split('---', 2)
    if not text.startswith('---\n') or len(parts) < 3:
        errors.append(f'{path.relative_to(ROOT)}: faltan metadatos')
        continue
    if 'lang: es-ES' not in parts[1]:
        errors.append(f'{path.relative_to(ROOT)}: falta idioma es-ES')
    if 'license: CC-BY-SA-4.0' not in parts[1]:
        errors.append(f'{path.relative_to(ROOT)}: falta licencia de documentación')
    for target in re.findall(r'\]\(([^)]+)\)', text):
        if target.startswith(('https://', 'http://', '#')):
            continue
        local = path.parent / unquote(target.split('#')[0])
        if not local.exists():
            errors.append(f'{path.relative_to(ROOT)}: enlace roto a {target}')

matrix = (ROOT / 'MATRIZ-DE-ACEPTACION.md').read_text(encoding='utf-8')
ids = re.findall(r'^\| (A\d+) \|', matrix, re.M)
if len(ids) != 148 or set(ids) != {f'A{i:02}' for i in range(1, 149)}:
    errors.append('La matriz no contiene A01–A148 una sola vez')

hashes = {
    'AGPL-3.0-or-later.txt': 'd8a6cc31abc16b6748c7a21f21611f5a1ec33f67d22ca23d7da1c19b95496bee',
    'Apache-2.0.txt': 'cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30',
    'CC-BY-SA-4.0.txt': '28a9529c7d0bb4dc51f4bf5c116a3d16ef247a052f7591466768ddf563fd1cf5',
}
for filename, expected in hashes.items():
    path = ROOT / 'LICENSES' / filename
    if not path.exists() or sha256(path.read_bytes()).hexdigest() != expected:
        errors.append(f'LICENSES/{filename}: no coincide con la copia canónica registrada')
if (ROOT / 'LICENSE').read_bytes() != (ROOT / 'LICENSES' / 'AGPL-3.0-or-later.txt').read_bytes():
    errors.append('LICENSE y su copia AGPL difieren')

for path in (ROOT / 'prototipo').iterdir():
    if path.suffix in {'.mjs', '.html', '.css'}:
        if 'SPDX-License-Identifier: AGPL-3.0-or-later' not in path.read_text(encoding='utf-8')[:200]:
            errors.append(f'{path.relative_to(ROOT)}: falta identificador SPDX')
if '<html lang="es-ES">' not in (ROOT / 'prototipo' / 'index.html').read_text(encoding='utf-8'):
    errors.append('El prototipo no declara idioma es-ES')

if errors:
    for error in errors:
        print(error)
    raise SystemExit(1)
print(f'Correcto: {len(documents)} documentos; idioma es-ES; enlaces locales; licencias; criterios A01–A148.')
print('Estas comprobaciones no ejecutan los 148 criterios de producto ni validan seguridad.')
