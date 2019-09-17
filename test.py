import appscript
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
window = appscript.app("Terminal")
window.do_script(f"cd {script_dir}; python gui.py")
