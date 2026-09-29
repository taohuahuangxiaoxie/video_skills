"""Verify or install this local skill bundle; dry-run unless --apply is supplied."""
import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- comfyui-skills:begin -->'
END = '<!-- comfyui-skills:end -->'

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def safe_join(base, rel):
    path = base / rel
    if Path(rel).is_absolute() or '..' in Path(rel).parts:
        raise ValueError(f'Invalid relative path: {rel}')
    if path.is_symlink() or any(p.is_symlink() for p in path.parents):
        raise ValueError(f'Refusing symlink destination: {path}')
    if not path.resolve().is_relative_to(base.resolve()):
        raise ValueError(f'Path escapes destination: {path}')
    return path

def verify(manifest):
    for package in manifest['packages']:
        base = safe_join(ROOT, package['path'])
        for rel, sha in package['files'].items():
            p = safe_join(base, rel)
            if not p.is_file() or digest(p) != sha:
                raise ValueError(f'Missing or changed package file: {p}')
        actual = {p.relative_to(base).as_posix() for p in base.rglob('*')
                  if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'}
        if actual != set(package['files']):
            raise ValueError(f'Unexpected package files: {package["name"]}')
    return {p['name']: p for p in manifest['packages']}

def rules_text(target):
    old = target.read_text(encoding='utf-8-sig') if target.exists() else ''
    block = START+'\n'+(ROOT/'preferences/AGENTS.fragment.md').read_text(encoding='utf-8').strip()+'\n'+END
    if START in old or END in old:
        if old.count(START) != 1 or old.count(END) != 1 or old.index(END) < old.index(START):
            raise ValueError('Malformed managed rules block; review AGENTS.md manually.')
        a,b = old.index(START), old.index(END)+len(END)
        return old[:a]+block+old[b:]
    return old.rstrip()+'\n\n'+block+'\n'

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['verify','install','list','refresh'])
    p.add_argument('--profile', default='studio')
    p.add_argument('--skill', action='append', default=[], help='Top-level package name; repeatable; adds dependencies')
    p.add_argument('--dest', type=Path, default=Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex')))/'skills')
    p.add_argument('--with-rules', action='store_true')
    p.add_argument('--rules-target', type=Path)
    p.add_argument('--apply', action='store_true')
    p.add_argument('--replace', action='store_true', help='Back up and overwrite conflicting files; never delete unrelated files')
    a = p.parse_args()
    manifest = json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
    if a.command == 'refresh':
        for package in manifest['packages']:
            base = safe_join(ROOT, package['path'])
            if not (base/'SKILL.md').is_file(): raise FileNotFoundError(base/'SKILL.md')
            files={}
            for f in sorted(base.rglob('*')):
                if f.is_file() and '__pycache__' not in f.parts and f.suffix != '.pyc':
                    rel=f.relative_to(base).as_posix()
                    safe_join(base,rel)
                    files[rel]=digest(f)
            package['files']=files
            package['skill_entries']=sum(x.endswith('SKILL.md') for x in files)
        if a.apply:
            (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
        print(json.dumps({'manifest_refreshed':a.apply,'packages':len(manifest['packages'])}));return
    packages = verify(manifest)
    if a.command in ('verify','list'):
        print(json.dumps({'verified_packages':len(packages),'skill_entries':sum(x['skill_entries'] for x in packages.values()),'profiles':manifest['profiles']},ensure_ascii=False,indent=2));return
    chosen = set(a.skill or manifest['profiles'].get(a.profile, []))
    if not chosen: p.error('Unknown or empty profile')
    pending = list(chosen)
    while pending:
        name = pending.pop()
        if name not in packages: p.error(f'Unknown package: {name}')
        for dep in packages[name]['dependencies']:
            if dep not in chosen: chosen.add(dep);pending.append(dep)
    dest = a.dest.expanduser().absolute()
    if dest.resolve().is_relative_to(ROOT) or ROOT.is_relative_to(dest.resolve()):
        p.error('Install destination must be separate from this bundle')
    changes=[];conflicts=[];unchanged=0
    for name in sorted(chosen):
        package=packages[name]
        for rel,sha in package['files'].items():
            target=safe_join(dest, name+'/'+rel)
            if target.exists() and not target.is_file(): raise ValueError(f'Not a file: {target}')
            if target.exists() and digest(target)==sha: unchanged+=1;continue
            if target.exists(): conflicts.append(str(target))
            changes.append((ROOT/package['path']/rel,target,None))
    if a.with_rules:
        target=(a.rules_target or dest.parent/'AGENTS.md').expanduser().absolute()
        safe_join(target.parent,target.name)
        new=rules_text(target)
        if not target.exists() or target.read_text(encoding='utf-8-sig')!=new:
            changes.append((None,target,new))
    summary={'packages':sorted(chosen),'changed_files':len(changes),'unchanged_files':unchanged,'conflicts':conflicts,'applied':False}
    if not a.apply:
        print(json.dumps(summary,ensure_ascii=False,indent=2));return
    if conflicts and not a.replace:
        raise FileExistsError('Existing skill files differ. Review dry-run; use --replace to back up and update them.')
    backup=dest.parent/'skill-migration-backups'/datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    entries=[]
    for i,(source,target,content) in enumerate(changes):
        backup_file=None
        if target.exists():
            backup.mkdir(parents=True,exist_ok=True)
            backup_file=backup/f'{i:04d}_{target.name}'
            shutil.copy2(target,backup_file)
        target.parent.mkdir(parents=True,exist_ok=True)
        if source: shutil.copy2(source,target)
        else: target.write_text(content,encoding='utf-8',newline='\n')
        expected=digest(source) if source else hashlib.sha256(content.encode('utf-8')).hexdigest()
        if digest(target)!=expected: raise RuntimeError(f'Write verification failed: {target}')
        entries.append({'target':str(target),'backup':str(backup_file) if backup_file else None,'sha256':digest(target)})
    if entries:
        backup.mkdir(parents=True,exist_ok=True)
        (backup/'install-report.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2),encoding='utf-8')
    summary.update(applied=True,report=str(backup/'install-report.json') if entries else None)
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
