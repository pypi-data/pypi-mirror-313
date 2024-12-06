import os
import shutil
import questionary

from core.schemas import ComponentType, GeneratorServiceOptions
from core.constants import prompts, source_code_root_dir
from core.utils import log, stop_app


class GeneratorService:
    """Service for code generation"""
    def __init__(self, options: GeneratorServiceOptions):
        self.options = options

    @staticmethod
    def get_options() -> GeneratorServiceOptions | None:
        """Requests data from the user"""
        answers = {}
        GeneratorService.ask_prompts(answers, prompts['base'], 'base')
        GeneratorService.ask_prompts(answers, prompts[answers['base']['component_type'].lower()], answers['base']['component_type'].lower())
        
        return GeneratorServiceOptions(**answers)
    
    @staticmethod
    def ask_prompts(answers: dict[str, str], prompts: dict[str, questionary.Question], prefix: str):
        for key, prompt in prompts.items():
            if (answer := prompt.ask()) is not None:
                if answers.get(prefix):
                    answers[prefix][key] = answer
                else:
                    answers[prefix] = {key: answer}
            else:
                stop_app()
    
    def generate(self):
        """Directly generation, depends on the arguments passed to the constructor"""
        source_code_path = os.path.join(source_code_root_dir, self.options.base.api_type.value, self.options.base.component_type.value)
        res_dir_path = f'./{self.options.base.name}'
        log(f'Copying the template')
        try:
            shutil.copytree(source_code_path, res_dir_path)
        except Exception as e:
            log(f'Error copying the template: {e}', is_error=True)
            
        for root, _, files in os.walk(res_dir_path):
            for file in files:
                self._format_file(os.path.join(root, file))
                
        if self.options.base.component_type == ComponentType.PROJECT and self.options.project.generate_venv:
            log(f'Generating a virtual environment')
            self._generate_venv()
            
    def _format_file(self, path: str):
        try:
            if os.path.isfile(path):
                with open(path, 'r') as file:
                    content = file.read()
                    formatted_content = content.replace('{name}', self.options.base.name.lower()).replace('{capitalized_name}', self.options.base.name.capitalize())
                    with open(path, 'w') as file:
                        file.write(formatted_content)
        except Exception as e:
            log(f'Error formatting the file {path}: {e}', is_error=True)
        
    def _generate_venv(self):
        try:
            venv_path = os.path.join(self.options.base.name, '.venv')
            os.system(f'python -m venv {venv_path}')
            pip_executable = os.path.join(venv_path, 'Scripts', 'pip')
            os.system(f'{pip_executable} install -r {self.options.base.name}/requirements.txt')
        except Exception as e:
            log(f'Error generating a virtual environment: {e}', is_error=True)
