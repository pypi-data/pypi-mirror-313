from click.testing import CliRunner
from douglog.douglog import dlog

#  ──────────────────────────────────────────────────────────────────────────

def test_delete():
    runner = CliRunner()
    result = runner.invoke(dlog, ['delete', 'teaching'])
    print(result.output)
    result = runner.invoke(dlog, ['delete', 'teaching', '-l', '1701375780.md'])
    print(result.output)
    result = runner.invoke(dlog, ['delete', 'teaching', '-l', '1701375781.md'])
    print(result.output)
