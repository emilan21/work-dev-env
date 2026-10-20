#!/usr/bin/env python3
"""Verify config and save/restore using only a disposable tmux server and state."""
import os
import platform
import json
from pathlib import Path
import subprocess
import tempfile
import time

root = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='work-tmux-') as tmp:
    socket = str(Path(tmp) / 'socket')
    env = os.environ.copy()
    env.pop('TMUX', None)
    env.pop('TMUX_PANE', None)

    def tmux(*args, check=True):
        return subprocess.run(['tmux', '-S', socket, *args], env=env, capture_output=True, text=True, check=check)

    try:
        tmux('-f', str(root / 'config/tmux/tmux.conf'), 'new-session', '-d', '-s', 'test-save', '-c', tmp)
        errors = tmux('show-messages', check=False).stdout
        assert 'unknown command' not in errors and 'invalid option' not in errors, errors
        pid = tmux('display-message', '-p', '#{pid}').stdout.strip()
        env['TMUX'] = f'{socket},{pid},0'
        assert tmux('show-option', '-gv', 'prefix').stdout.strip() == 'C-a'
        for key, value in {'@resurrect-default-processes': 'nvim', '@resurrect-processes': 'nvim',
                           '@resurrect-capture-pane-contents': 'off', '@continuum-save-interval': '15',
                           '@continuum-boot': 'off', '@continuum-restore': 'on'}.items():
            assert tmux('show-option', '-gv', key).stdout.strip() == value, key
        # Disable auto restore in this test server and give the startup task time to exit.
        tmux('set-option', '-g', '@continuum-restore', 'off')
        time.sleep(1.2)
        tmux('set-option', '-g', '@resurrect-dir', str(Path(tmp) / 'snapshots'))
        tmux('split-window', '-h', '-t', 'test-save:', '-c', tmp)
        tmux('new-window', '-d', '-t', 'test-save:', '-n', 'terminal', '-c', tmp)
        save = tmux('show-option', '-gv', '@resurrect-save-script-path').stdout.strip()
        restore = tmux('show-option', '-gv', '@resurrect-restore-script-path').stdout.strip()
        assert Path(save).is_file(), 'Run ./bootstrap in this HOME first'
        # Preserve the server while removing the saved session.
        tmux('new-session', '-d', '-s', 'keepalive', '-c', tmp)
        subprocess.run([save], env=env, check=True, capture_output=True)
        snapshot = Path(tmp) / 'snapshots/last'
        assert snapshot.exists(), 'Snapshot not created'
        tmux('kill-session', '-t', '=test-save')
        subprocess.run([restore], env=env, check=True, capture_output=True)
        tmux('has-session', '-t', '=test-save')
        assert len(tmux('list-windows', '-t', 'test-save', '-F', '#W').stdout.splitlines()) == 2
        assert tmux('list-panes', '-t', 'test-save:1', '-F', '#{pane_id}').stdout.count('\n') == 2
        if platform.system() == 'Darwin':
            # A macOS runner has no other tmux servers, so exercise continuum's
            # real cold-start path as well as resurrect's manual restore.
            tmux('kill-server')
            env.pop('TMUX', None)
            config = Path(tmp) / 'restart.conf'
            config.write_text('source-file ' + json.dumps(str(root / 'config/tmux/tmux.conf'))
                              + '\nset -g @resurrect-dir ' + json.dumps(str(Path(tmp) / 'snapshots')) + '\n')
            tmux('-f', str(config), 'new-session', '-d', '-s', 'startup', '-c', tmp)
            deadline = time.monotonic() + 20
            while tmux('show-option', '-gqv', '@work-restore-done', check=False).stdout.strip() != '1':
                if time.monotonic() > deadline:
                    raise AssertionError('Cold-start automatic restore did not complete')
                time.sleep(0.1)
            tmux('has-session', '-t', '=test-save')
            print('macOS cold-start automatic restore passed.')
        print('Isolated tmux configuration and save/restore passed.')
    finally:
        tmux('kill-server', check=False)
