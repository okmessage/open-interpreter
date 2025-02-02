import argparse
import inquirer
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

def cli(interpreter):
  """
  Takes an instance of interpreter.
  Modifies it according to command line flags, then runs chat.
  """

  # Load values from .env file with the new names
  AUTO_RUN = os.getenv('INTERPRETER_CLI_AUTO_RUN', 'False') == 'True'
  FAST_MODE = os.getenv('INTERPRETER_CLI_FAST_MODE', 'False') == 'True'
  LOCAL_RUN = os.getenv('INTERPRETER_CLI_LOCAL_RUN', 'False') == 'True'
  DEBUG = os.getenv('INTERPRETER_CLI_DEBUG', 'False') == 'True'
  USE_AZURE = os.getenv('INTERPRETER_CLI_USE_AZURE', 'False') == 'True'

  # Setup CLI
  parser = argparse.ArgumentParser(description='Chat with Open Interpreter.')
  
  parser.add_argument('-y',
                      '--yes',
                      action='store_true',
                      default=AUTO_RUN,
                      help='execute code without user confirmation')
  parser.add_argument('-f',
                      '--fast',
                      action='store_true',
                      default=FAST_MODE,
                      help='use gpt-3.5-turbo instead of gpt-4')
  parser.add_argument('-l',
                      '--local',
                      action='store_true',
                      default=LOCAL_RUN,
                      help='run fully local with code-llama')
  parser.add_argument('-d',
                      '--debug',
                      action='store_true',
                      default=DEBUG,
                      help='prints extra information')
  
  parser.add_argument('--model',
                      type=str,
                      help='HuggingFace repo id',
                      default="",
                      required=False)
  
  parser.add_argument('--use-azure',
                      action='store_true',
                      default=USE_AZURE,
                      help='use Azure OpenAI Services')
  
  args = parser.parse_args()


  # Modify interpreter according to command line flags
  if args.yes:
    interpreter.auto_run = True
  if args.fast:
    interpreter.model = "gpt-3.5-turbo"
  if args.local:


    
    # Temporarily, for backwards (behavioral) compatability, we've moved this part of llama_2.py here.
    # This way, when folks hit interpreter --local, they get the same experience as before.
    from rich import print
    from rich.markdown import Markdown
    import inquirer
    
    print('', Markdown("**Open Interpreter** will use `Code Llama` for local execution. Use your arrow keys to set up the model."), '')
        
    models = {
        '7B': 'TheBloke/CodeLlama-7B-Instruct-GGUF',
        '13B': 'TheBloke/CodeLlama-13B-Instruct-GGUF',
        '34B': 'TheBloke/CodeLlama-34B-Instruct-GGUF'
    }
    
    parameter_choices = list(models.keys())
    questions = [inquirer.List('param', message="Parameter count (smaller is faster, larger is more capable)", choices=parameter_choices)]
    answers = inquirer.prompt(questions)
    chosen_param = answers['param']

    # THIS is more in line with the future. You just say the model you want by name:
    interpreter.model = models[chosen_param]
    interpreter.local = True

  
  if args.debug:
    interpreter.debug_mode = True
  if args.use_azure:
    interpreter.use_azure = True
    interpreter.local = False
  if args.model != "":
    interpreter.model = args.model
    interpreter.local = True

  # Run the chat method
  interpreter.chat()
