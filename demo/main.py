# here importing the stackoverflow auto search module
from module.main import StackOverflow

# here we writing the command to run test file.
# example: python test.py
#          python module/main.py
command = "python test.py"

search = StackOverflow(cmd=command,AutoSearch=True)
# if AutoSearch is false we need to assign
search = StackOverflow(cmd=command,AutoSearch=False)
search.__start__()