import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


sessionizer = load('sessionizer', ROOT / 'bin/tmux-sessionizer')


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='work-env-install-')
        self.home = Path(self.temp.name)
        self.env = dict(os.environ, HOME=str(self.home))

    def tearDown(self):
        self.temp.cleanup()

    def run_install(self, *args, check=True):
        return subprocess.run([str(ROOT / 'install'), *map(str, args)], env=self.env,
                              capture_output=True, text=True, check=check)

    def backup(self):
        return next((self.home / '.local/state/work-dev-env/backups').iterdir())

    def test_preview_changes_nothing(self):
        self.run_install('--dry-run')
        self.assertEqual(list(self.home.iterdir()), [])

    def test_restore_files_directories_symlinks_and_absent_targets(self):
        config = self.home / '.config'
        (config / 'nvim').mkdir(parents=True)
        (config / 'nvim/init.lua').write_text('original')
        (config / 'tmux').mkdir()
        (config / 'tmux/tmux.conf').write_text('previous')
        (config / 'alacritty').mkdir()
        (config / 'alacritty/alacritty.toml').symlink_to('/missing-original-target')
        self.run_install()
        backup = self.backup()
        self.assertIn('Already installed', self.run_install().stdout)
        self.assertEqual(len(list(backup.parent.iterdir())), 1)
        self.run_install('--dry-run', '--restore', backup)
        self.assertTrue((config / 'nvim').is_symlink())
        self.run_install('--restore', backup)
        self.assertEqual((config / 'nvim/init.lua').read_text(), 'original')
        self.assertEqual((config / 'tmux/tmux.conf').read_text(), 'previous')
        self.assertEqual(os.readlink(config / 'alacritty/alacritty.toml'), '/missing-original-target')
        self.assertFalse(os.path.lexists(self.home / '.local/bin/ts'))

    def test_restore_refuses_changed_targets(self):
        self.run_install()
        target = self.home / '.local/bin/ts'
        target.unlink()
        target.write_text('local changes')
        result = self.run_install('--restore', self.backup(), check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(target.read_text(), 'local changes')


class SessionizerTests(unittest.TestCase):
    def test_same_names_do_not_collide(self):
        self.assertNotEqual(sessionizer.session_name(Path('/a/project')),
                            sessionizer.session_name(Path('/b/project')))
        self.assertEqual(sessionizer.session_name(Path('/a/project')),
                         sessionizer.session_name(Path('/a/project')))

    def test_search_depth_hidden_and_missing_roots(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ('a/b/c', '.hidden/x', 'node_modules/x'):
                (root / name).mkdir(parents=True)
            result = sessionizer.projects({'search_paths': [tmp, tmp + '/missing'], 'max_depth': 2})
            self.assertEqual(result, [str(root / 'a'), str(root / 'a/b')])

    def test_cancel_does_not_create_sessions(self):
        completed = subprocess.CompletedProcess([], 0, stdout='existing\n')
        cancelled = subprocess.CompletedProcess([], 130, stdout='')
        with patch('sys.argv', ['ts']), patch.object(sessionizer.shutil, 'which', return_value='/bin/tool'), \
             patch.object(sessionizer, 'tmux', return_value=completed), \
             patch.object(sessionizer.subprocess, 'run', return_value=cancelled), \
             patch.object(sessionizer, 'open_project') as opened:
            sessionizer.main()
            opened.assert_not_called()

    def test_existing_session_does_not_rehydrate(self):
        with patch.object(sessionizer, 'tmux', return_value=subprocess.CompletedProcess([], 0, stdout='')) as call:
            sessionizer.open_project(Path('/project with spaces'))
            self.assertEqual(call.call_count, 1)

    def test_restore_finishes_before_project_creation(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            snapshot = home / '.local/state/work-dev-env/resurrect/last'
            snapshot.parent.mkdir(parents=True)
            snapshot.write_text('saved session')
            calls = []
            restored = False

            def fake_tmux(*args, check=True):
                nonlocal restored
                calls.append(args)
                code, out = 0, ''
                if args[0] == 'has-session':
                    code = 0 if restored else 1
                elif args[0] == 'list-sessions':
                    code = 1
                elif args[0] == 'show-option':
                    restored, out = True, '1\n'
                return subprocess.CompletedProcess(args, code, stdout=out)

            with patch.object(sessionizer, 'tmux', side_effect=fake_tmux), \
                 patch.object(sessionizer.Path, 'home', return_value=home):
                sessionizer.open_project(home)
            created = [args for args in calls if args[0] == 'new-session']
            self.assertEqual(len(created), 1)
            self.assertTrue(created[0][3].startswith('work-startup-'))
            self.assertFalse(any('editor' in args for args in calls))
            self.assertEqual(calls[-1][0], 'kill-session')

    def test_direct_directory_uses_argv_and_attaches(self):
        with tempfile.TemporaryDirectory(prefix="space and 'quote ") as tmp:
            with patch('sys.argv', ['ts', tmp]), patch.object(sessionizer.shutil, 'which', return_value='/bin/tool'), \
                 patch.object(sessionizer, 'open_project', return_value='chosen') as opened, \
                 patch.dict(os.environ, {}, clear=True), patch.object(sessionizer.os, 'execvp') as execute:
                sessionizer.main()
                opened.assert_called_once_with(Path(tmp).resolve())
                execute.assert_called_once_with('tmux', ['tmux', 'attach-session', '-t', '=chosen'])

    def test_inside_tmux_switches(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch('sys.argv', ['ts', tmp]), patch.object(sessionizer.shutil, 'which', return_value='/bin/tool'), \
                 patch.object(sessionizer, 'open_project', return_value='chosen'), \
                 patch.dict(os.environ, {'TMUX': 'active'}), patch.object(sessionizer.os, 'execvp') as execute:
                sessionizer.main()
                self.assertEqual(execute.call_args.args[1][1], 'switch-client')


if __name__ == '__main__':
    unittest.main()
