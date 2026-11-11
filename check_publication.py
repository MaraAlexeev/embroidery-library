"""Verify the exact reviewed public file set and byte hashes; never upload anything."""
from pathlib import Path, PurePosixPath
import hashlib, json, sys

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'PUBLIC_FILES.json').read_text())
expected = manifest['files']
errors = []
actual = set()
for path in root.rglob('*'):
    rel = path.relative_to(root).as_posix()
    if rel == '.git' or rel.startswith('.git/'):
        continue
    if path.is_symlink():
        errors.append('Symlink is not allowed: ' + rel)
    elif path.is_file() and rel != 'PUBLIC_FILES.json':
        actual.add(rel)
for rel, sha in expected.items():
    p = PurePosixPath(rel)
    if p.is_absolute() or '..' in p.parts:
        errors.append('Invalid manifest path: ' + rel)
        continue
    path = root / rel
    if path.is_file() and not path.is_symlink():
        if hashlib.sha256(path.read_bytes()).hexdigest() != sha:
            errors.append('Changed since review: ' + rel)
for rel in sorted(actual - set(expected)):
    errors.append('Unlisted file: ' + rel)
for rel in sorted(set(expected) - actual):
    errors.append('Missing file: ' + rel)
if errors:
    print('Publication check failed:\n' + '\n'.join(errors))
    sys.exit(1)
print('Verified ' + str(len(expected)) + ' reviewed files; no extra files or changed bytes.')
