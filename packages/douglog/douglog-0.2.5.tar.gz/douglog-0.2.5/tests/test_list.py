from click.testing import CliRunner
from douglog.douglog import dlog

#  ──────────────────────────────────────────────────────────────────────────

def test_list():
    runner = CliRunner()
    result = runner.invoke(dlog, ['list', '--logs'])
    print(result.output)
