from pathlib import Path
import runpy


server_path = Path(__file__).with_name("server.py")
runpy.run_path(server_path, run_name="__main__")