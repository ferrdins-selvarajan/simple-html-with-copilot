import importlib.util
import runpy
import subprocess
import sys
from pathlib import Path

project_dir = Path(__file__).resolve().parent
if importlib.util.find_spec("ruff") is None:
	print(
		"Ruff is not installed. Run `python -m pip install -r requirements-dev.txt`.",
		file=sys.stderr,
	)
	raise SystemExit(1)

lint_result = subprocess.run(
	[sys.executable, "-m", "ruff", "check", str(project_dir)],
	cwd=project_dir,
	check=False,
)
if lint_result.returncode:
	raise SystemExit(lint_result.returncode)

server_path = project_dir / "server.py"
runpy.run_path(server_path, run_name="__main__")