from core.service import GeneratorService


def main():
    options = GeneratorService.get_options()
    GeneratorService(options).generate()

