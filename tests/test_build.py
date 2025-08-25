import os
import shutil
import tempfile
import importlib.util
from cpybuild.tasks import build

def test_is_valid_identifier():
    # Should match valid Python identifiers
    assert build.is_valid_identifier('foo')
    assert build.is_valid_identifier('foo_bar')
    assert build.is_valid_identifier('_foo123')
    # Should not match invalid identifiers
    assert not build.is_valid_identifier('1foo')
    assert not build.is_valid_identifier('foo-bar')
    assert not build.is_valid_identifier('foo.bar')
    assert not build.is_valid_identifier('foo bar')

def test_check_module_parts():
    assert build.check_module_parts(['foo', 'bar']) == []
    assert build.check_module_parts(['foo', '1bar']) == ['1bar']
    assert build.check_module_parts(['foo-bar', 'baz']) == ['foo-bar']
    assert build.check_module_parts(['foo', 'bar-baz']) == ['bar-baz']

def test_build_skips_invalid(tmp_path, monkeypatch):
    # Setup a fake src/ tree
    src = tmp_path / 'src'
    src.mkdir()
    (src / 'validpkg').mkdir()
    (src / 'validpkg' / 'validmod.py').write_text('def foo(): return 42')
    (src / 'invalid-pkg').mkdir()
    (src / 'invalid-pkg' / 'mod.py').write_text('def bar(): return 99')
    (src / 'validpkg' / '1badmod.py').write_text('def bad(): return 0')
    # Write config
    config = tmp_path / 'cpybuild.yaml'
    config.write_text('sources:\n  - src/**/*.py\noutput: build/')
    # Patch cwd and env
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv('CPYBUILD_LOC', str(tmp_path / 'build'))
    # Patch build print to capture output
    import io, sys
    out = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = out
    build.run()
    sys.stdout = sys_stdout
    output = out.getvalue()
    assert 'Skipping' in output or 'ERROR' in output
    assert 'invalid-pkg' in output or '1badmod' in output
    # Only valid module should be built
    build_dir = tmp_path / 'build' / 'validpkg'
    assert build_dir.exists()
    assert any(f.name.startswith('validmod') for f in build_dir.iterdir())
