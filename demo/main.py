# here importing the stackoverflow auto search module
from module.main import StackOverflow

# here we writing the command to run test file.
# example: python test.py
#          python module/main.py
command = "node test.js"

# if AutoSearch is false we need to assign
search = StackOverflow(cmd=command, AutoSearch=True, language="javascript", Limit=10)
