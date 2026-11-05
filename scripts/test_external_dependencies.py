"""Offline checks for the official-provider packaging boundary."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import manage


class ExternalDependencyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.patcher = patch.object(manage, 'ROOT', self.root)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)
        self.manifest = {
            'packages': [{'name': 'xyq-project-workflow', 'path': 'skills/xyq-project-workflow',
                          'dependencies': [], 'external_dependencies': ['pippit-official']}],
            'profiles': {'xyq': ['xyq-project-workflow']},
            'external_dependencies': [{'name': 'pippit-official'}],
        }
        self.write('skills/xyq-project-workflow/SKILL.md',
                   '---\nname: xyq-project-workflow\ndescription: Personal defaults.\n---\n')

    def write(self, rel, content):
        target = self.root/rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding='utf-8')

    def test_personal_wrapper_and_online_metadata_are_allowed(self):
        self.write('docs/dependencies.md', 'Download xyq-skill from https://github.com/Pippit-dev/cli')
        manage.check_external_only(self.manifest)

    def test_official_manifest_package_is_rejected(self):
        self.manifest['packages'].append({'name': 'xyq-skill', 'path': 'skills/renamed', 'dependencies': []})
        with self.assertRaisesRegex(ValueError, 'external-only'):
            manage.check_external_only(self.manifest)

    def test_unregistered_official_directory_is_rejected(self):
        self.write('skills/xyq-nest-skill/commands/doc.md', 'An accidentally copied provider file.')
        with self.assertRaisesRegex(ValueError, 'external-only'):
            manage.check_external_only(self.manifest)

    def test_renamed_official_skill_is_rejected(self):
        for name in manage.OFFICIAL_XYQ_SKILLS:
            with self.subTest(name=name):
                self.write('skills/renamed/SKILL.md', f'---\nname: "{name}"\ndescription: Provider.\n---\n')
                with self.assertRaisesRegex(ValueError, 'renamed copies'):
                    manage.check_external_only(self.manifest)

    def test_official_binary_is_rejected(self):
        self.write('tools/pippit-tool-cli.exe', 'binary placeholder')
        with self.assertRaisesRegex(ValueError, 'binary is external-only'):
            manage.check_external_only(self.manifest)

    def test_unknown_external_dependency_is_rejected(self):
        self.manifest['external_dependencies'] = []
        with self.assertRaisesRegex(ValueError, 'Unknown external dependency'):
            manage.check_external_only(self.manifest)

    def test_cli_cache_outside_bundle_is_ignored(self):
        self.write('node_modules/@pippit-dev/cli/skills/xyq-skill/SKILL.md',
                   '---\nname: xyq-skill\n---\n')
        manage.check_external_only(self.manifest)


if __name__ == '__main__':
    unittest.main()
