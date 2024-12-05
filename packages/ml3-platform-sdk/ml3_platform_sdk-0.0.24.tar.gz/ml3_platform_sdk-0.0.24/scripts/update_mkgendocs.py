import importlib
import inspect
import os

import yaml


def find_classes_in_module(module_path):
    classes = []
    module_name = os.path.basename(module_path)[:-3]  # Remove '.py' extension
    try:
        import_name = module_path[:-3].replace('/', '.').replace('\\', '.')
        importlib.import_module("os")
        module = importlib.import_module(import_name)
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and (obj.__module__ == import_name):
                classes.append(obj)
    except Exception as e:
        print(f"Error importing module {module_name}: {str(e)}")
    return classes


if __name__ == "__main__":
    import sys
    # Add current directory to path to see ml3_platform_sdk
    sys.path.append(os.getcwd())
    repository_directory = "ml3_platform_sdk"
    config_file = 'mkgendocs.yml'

    python_files = list(map(
        lambda x: os.path.join(repository_directory, x),
        filter(
            lambda x: x.endswith('.py') and x != '__init__.py',
            os.listdir(repository_directory)
        )
    ))

    with open(config_file, 'r') as f:
        config = yaml.full_load(f)

    # clear pages
    config['pages'] = []

    for python_file in python_files:
        print(f'processing {python_file}')
        classes = find_classes_in_module(python_file)
        if len(classes) > 0:
            config['pages'].append(
                {
                    'page': f'{os.path.basename(python_file)[:-3]}.md',
                    'source': python_file,
                    'classes': list(map(lambda x: x.__name__, classes))
                }
            )
        if classes:
            print(f"Classes in module {python_file}:")
            for cls in classes:
                print(f"  {cls.__name__}")
    with open(config_file, 'w') as f:
        yaml.dump(config, f)
