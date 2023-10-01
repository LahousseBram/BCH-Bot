import sys, os, subprocess

print("test")
python_executable = sys.executable  # Get the path to the current Python interpreter
script_path = os.path.abspath(__file__)  # Get the absolute path of the current script
args = sys.argv  # Get the command-line arguments

# Use subprocess to start a new Python process with the same script and arguments
subprocess.Popen([python_executable, script_path] + args[1:])