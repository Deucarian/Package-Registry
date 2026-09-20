"""Translate shared changes without replacing host-specific configuration or history."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import PurePosixPath

from package_sync_projection import Projection, TranslationNeedsReview, merge_independent_changes


@dataclass(frozen=True)
class Blob:
    mode: str
    data: bytes


def host_owned(name):
    path = PurePosixPath(name)
    return (path.parts[0] in ('.github', '.git') or name == 'bitbucket-pipelines.yml'
            or name.lower().endswith(('.md', '.md.meta'))
            or path.name.lower().startswith(('license', 'notice', 'copyright')))


def validate_path(name):
    path = PurePosixPath(name)
    if (not name or path.is_absolute() or '\\' in name or '\x00' in name
            or any(part.lower() in ('.git', '..', '.') for part in path.parts)):
        raise TranslationNeedsReview('Unsafe repository path')


def projection_for(profile, github_tree):
    rules = dict(profile['packageIds'])
    rules.update(profile['namespaceOverrides'])
    rules.update({'Deucarian': 'Simultria', 'deucarian': 'simultria', 'DEUCARIAN': 'SIMULTRIA'})
    for name, slug in profile['repositories'].items():
        for source, destination in (
            (f'https://raw.githubusercontent.com/Deucarian/{name}/',
             f'https://api.bitbucket.org/2.0/repositories/simultria/{slug}/src/'),
            (f'https://github.com/Deucarian/{name}/blob/', f'https://bitbucket.org/simultria/{slug}/src/'),
            (f'https://github.com/Deucarian/{name}/tree/', f'https://bitbucket.org/simultria/{slug}/src/'),
            (f'https://github.com/Deucarian/{name}', f'https://bitbucket.org/simultria/{slug}'),
            (f'git@github.com:Deucarian/{name}', f'git@bitbucket.org:simultria/{slug}'),
        ):
            rules[source] = destination
    forward = Projection(rules, {})
    identifiers = set(profile['packageIds']) | set(profile['namespaceOverrides'])
    for name, blob in github_tree.items():
        if host_owned(name):
            continue
        text = blob.data.decode('utf-8', errors='ignore')
        identifiers.update(re.findall(r'\bDeucarian[A-Za-z_0-9.]*(?:[A-Za-z_0-9])', text))
        identifiers.update(re.findall(r'\bDeucarian[A-Za-z_0-9.]*', name))
    inverse = {}
    collisions = set()
    for source in sorted(identifiers):
        if source in ('Deucarian', 'deucarian', 'DEUCARIAN'):
            continue
        destination = forward.forward(source)
        if destination in inverse and inverse[destination] != source:
            collisions.add(destination)
        inverse[destination] = source
    for source, destination in rules.items():
        if source.startswith(('https://', 'git@')):
            if destination in inverse and inverse[destination] != source:
                collisions.add(destination)
            inverse[destination] = source
    for destination in collisions:
        inverse.pop(destination, None)
    return Projection(rules, inverse)


def translate_tree(github_baseline, bitbucket_baseline, bitbucket_incoming, profile):
    projection = projection_for(profile, github_baseline)
    paths = {}
    for source in github_baseline:
        destination = source if host_owned(source) else projection.forward(source)
        if destination in paths:
            raise TranslationNeedsReview('Translated paths collide')
        paths[destination] = source
    result = dict(github_baseline)
    changed = []
    for name in sorted(set(bitbucket_baseline) | set(bitbucket_incoming)):
        validate_path(name)
        old, new = bitbucket_baseline.get(name), bitbucket_incoming.get(name)
        if old == new or host_owned(name):
            continue
        source = paths.get(name)
        if source is None:
            if old is not None:
                raise TranslationNeedsReview(f'{name}: host-only file changed')
            source = projection.reverse_insert(name)
            validate_path(source)
            if source in result or host_owned(source):
                raise TranslationNeedsReview(f'{name}: new path collides with host content')
        original = github_baseline.get(source)
        if any(blob and blob.mode not in ('100644', '100755') for blob in (old, new, original)):
            raise TranslationNeedsReview(f'{name}: symlinks and submodules require review')
        if new is None:
            if original is None:
                raise TranslationNeedsReview(f'{name}: no corresponding source to delete')
            # A deletion must not discard local, host-specific content.
            try:
                exact = projection.forward(original.data.decode('utf-8')).encode('utf-8') == old.data
            except UnicodeDecodeError:
                exact = original.data == old.data
            if not exact:
                raise TranslationNeedsReview(f'{name}: deletion would discard host-specific content')
            result.pop(source)
        elif original is None:
            if b'\0' in new.data:
                result[source] = new
            else:
                try:
                    data = projection.reverse_insert(new.data.decode('utf-8')).encode('utf-8')
                except UnicodeDecodeError:
                    data = new.data
                if b'\0' not in data:
                    try:
                        if projection.forward(data.decode('utf-8')).encode('utf-8') != new.data:
                            raise TranslationNeedsReview(f'{name}: new content failed round-trip check')
                    except UnicodeDecodeError:
                        pass
                result[source] = Blob(new.mode, data)
        elif old is None:
            raise TranslationNeedsReview(f'{name}: upstream addition collides with existing source')
        else:
            result[source] = translate_blob(original, old, new, projection)
        changed.append(source)
    return result, changed


def translate_blob(original, old, new, projection):
    if old.mode != original.mode and old.mode != new.mode:
        raise TranslationNeedsReview('Conflicting host-specific file mode')
    mode = original.mode if old.mode == new.mode else new.mode
    if b'\0' in original.data + old.data + new.data:
        if original.data != old.data:
            raise TranslationNeedsReview('Host-specific binary content changed')
        return Blob(mode, new.data)
    try:
        data = projection.reverse_change(original.data.decode('utf-8'), new.data.decode('utf-8'),
                                         old.data.decode('utf-8')).encode('utf-8')
    except UnicodeDecodeError:
        if original.data != old.data:
            raise TranslationNeedsReview('Host-specific non-UTF8 content changed')
        data = new.data
    return Blob(mode, data)


def merge_trees(current, baseline, incoming):
    result = dict(current)
    for name in sorted(set(baseline) | set(incoming)):
        before, after, local = baseline.get(name), incoming.get(name), current.get(name)
        if before == after:
            continue
        if local == before or local == after:
            if after is None:
                result.pop(name, None)
            else:
                result[name] = after
            continue
        if not all((before, after, local)):
            raise TranslationNeedsReview(f'{name}: add/delete conflict')
        if before.mode != after.mode and local.mode not in (before.mode, after.mode):
            raise TranslationNeedsReview(f'{name}: mode conflict')
        if b'\0' in before.data + after.data + local.data:
            raise TranslationNeedsReview(f'{name}: binary conflict')
        result[name] = Blob(local.mode if before.mode == after.mode else after.mode,
                            merge_independent_changes(local.data, before.data, after.data))
    return result
