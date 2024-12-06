from click.testing import CliRunner
from douglog.douglog import dlog

#  ──────────────────────────────────────────────────────────────────────────

def test_git():
    runner = CliRunner()
    result = runner.invoke(dlog, ['git', 'add', '-A'])
    print(result.output)
