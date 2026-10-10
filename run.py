import importlib.util
import runpy
import subprocess
import sys
from pathlib import Path

project_dir = Path(__file__).resolve().parent
required_modules = ("fastapi", "uvicorn", "ruff")
if any(importlib.util.find_spec(module) is None for module in required_modules):
	print(
		"Project dependencies are missing. Installing dependencies...",
	)
	install_result = subprocess.run(
		[
			sys.executable,
			"-m",
			"pip",
			"install",
			"-r",
			str(project_dir / "requirements.txt"),
			"-r",
			str(project_dir / "requirements-dev.txt"),
		],
		cwd=project_dir,
		check=False,
	)
	if install_result.returncode:
		raise SystemExit(install_result.returncode)

lint_result = subprocess.run(
	[sys.executable, "-m", "ruff", "check", str(project_dir)],
	cwd=project_dir,
	check=False,
)
if lint_result.returncode:
	raise SystemExit(lint_result.returncode)

server_path = project_dir / "server.py"
runpy.run_path(server_path, run_name="__main__")