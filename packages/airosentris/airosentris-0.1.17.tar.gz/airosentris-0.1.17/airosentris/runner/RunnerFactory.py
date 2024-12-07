import os
import importlib
from importlib.util import find_spec

from airosentris.runner.RunnerRegistry import RunnerRegistry


class RunnerFactory:
    _runners_loaded = False

    @classmethod
    def _load_runners(cls, runner_path='airosentris.algorithm'):
        """Private method to load runners dynamically."""
        if cls._runners_loaded:
            return

        # Locate the base directory of the runner module
        spec = find_spec(runner_path)
        if not spec or not spec.submodule_search_locations:
            raise ModuleNotFoundError(f"Cannot locate module: {runner_path}")

        base_path = spec.submodule_search_locations[0]

        # Walk through the base directory
        for root, _, files in os.walk(base_path):
            for file in files:
                if file.endswith("Runner.py"):
                    # Construct the module path
                    relative_path = os.path.relpath(root, base_path)
                    module_name = (
                        f"{runner_path}.{relative_path.replace(os.sep, '.')}.{file[:-3]}"
                        if relative_path != "."
                        else f"{runner_path}.{file[:-3]}"
                    )
                    runner_class_name = file.replace(".py", "")  # Class name matches the file name

                    try:
                        # Import the module and get the runner class
                        module = importlib.import_module(module_name)
                        runner_class = getattr(module, runner_class_name)
                        RunnerRegistry.register_runner(runner_class_name.lower(), runner_class)

                    except (ImportError, AttributeError) as e:
                        print(f"Error loading runner {runner_class_name} from {module_name}: {e}")

        cls._runners_loaded = True

    @staticmethod
    def get_runner(runner_type):
        """Get a runner by name, loading runners if necessary."""
        RunnerFactory._load_runners()
        return RunnerRegistry.get_runner(runner_type)
