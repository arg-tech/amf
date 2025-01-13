import os
import sys
import yaml
import logging
import importlib.util

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class ModuleLoader:
    def __init__(self, modules_directory):
        self.modules_directory = modules_directory
        self.modules_metadata = self._load_modules_metadata()

    def _load_modules_metadata(self):
        modules_metadata = {}

        for module_name in os.listdir(self.modules_directory):
            module_path = os.path.join(self.modules_directory, module_name)

            if os.path.isdir(module_path):
                metadata_file = os.path.join(module_path, 'metadata.yaml')

                if os.path.isfile(metadata_file):
                    with open(metadata_file, 'r') as f:
                        try:
                            metadata = yaml.safe_load(f)
                            model_name = metadata.get('Name')
                            variant_list = metadata.get('Variants', [])
                            modules_metadata[model_name] = {
                                'metadata': metadata,
                                'variants': variant_list,
                                'module_path': module_path
                            }
                        except yaml.YAMLError as e:
                            logger.error(f"Error reading {metadata_file}: {e}")
                else:
                    logger.warning(f"Metadata file not found in {module_name}")

        return modules_metadata
    def load_module(self, model_name, variant, version=None):
        try:
            module_info = self.modules_metadata[model_name]

            # Create a check for the variant with an optional version
            variant_info = next((v for v in module_info['variants'] if v['name'] == variant and (v['version'] == version or v['version'] is None)), None)

            if variant_info is None:
                raise ValueError(f"Variant '{variant}' with version '{version}' not found for model '{model_name}'.")

            module_path = module_info['module_path']
            predictor_file = os.path.join(module_path, 'predictor.py')

            # Add the parent directory of the 'modules' folder to sys.path
            sys.path.append(os.path.dirname(os.path.dirname(module_path)))

            # Load the module using importlib
            spec = importlib.util.spec_from_file_location('predictor', predictor_file)
            predictor_module = importlib.util.module_from_spec(spec)
            sys.modules['predictor'] = predictor_module
            spec.loader.exec_module(predictor_module)

            predictor_class = getattr(predictor_module, 'Predictor')

            return predictor_class(variant, version)

        except KeyError:
            logger.error(f"Model '{model_name}' not found in modules metadata.")
            raise
        except ImportError as e:
            logger.error(f"Failed to import module from path '{module_path}'. Error: {e}")
            raise
        except AttributeError:
            logger.error(f"Class 'Predictor' not found in module '{module_path}'.")
            raise

    def load_module22(self, model_name, variant_name, variant_version):
        try:
            module_info = self.modules_metadata[model_name]

            # Check if the variant with the specified version exists
            variant_found = False
            for variant in module_info['variants']:
                if variant['name'] == variant_name and variant.get('version') == variant_version:
                    variant_found = True
                    break
            
            if not variant_found:
                raise ValueError(f"Variant '{variant_name}' with version '{variant_version}' not found for model '{model_name}'.")

            module_path = module_info['module_path']
            predictor_file = os.path.join(module_path, 'predictor.py')

            # Add the parent directory of the 'modules' folder to sys.path
            sys.path.append(os.path.dirname(os.path.dirname(module_path)))

            # Load the module using importlib
            spec = importlib.util.spec_from_file_location('predictor', predictor_file)
            predictor_module = importlib.util.module_from_spec(spec)
            sys.modules['predictor'] = predictor_module
            spec.loader.exec_module(predictor_module)

            predictor_class = getattr(predictor_module, 'Predictor')

            return predictor_class(variant_name)

        except KeyError:
            logger.error(f"Model '{model_name}' not found in modules metadata.")
            raise
        except ImportError as e:
            logger.error(f"Failed to import module from path '{module_path}'. Error: {e}")
            raise
        except AttributeError:
            logger.error(f"Class 'Predictor' not found in module '{module_path}'.")
            raise

    def print_metadata(self):
        logger.info("Modules Metadata:")
        for model_name, info in self.modules_metadata.items():
            logger.info(f"\nModel Name: {model_name}")
            logger.info(f"Metadata:\n  Name: {info['metadata']['Name']}\n  Date: {info['metadata']['Date']}")
            logger.info(f"  Originator: {info['metadata']['Originator']}")
            logger.info(f"  License: {info['metadata']['License']}")
            logger.info(f"  Variants:")
            for variant in info['variants']:
                # Check if the variant is a dictionary or a string
                if isinstance(variant, dict):
                    logger.info(f"    - Name: {variant.get('name')}, Version: {variant.get('version')}")
                else:
                    logger.info(f"    - Name: {variant}, Version: N/A")  # Handle cases where variant is a string without version
            logger.info(f"  Requires: {info['metadata']['Requires']}")
            logger.info(f"  Outputs: {info['metadata']['Outputs']}")
            logger.info(f"Module Path: {info['module_path']}")


# Example usage
if __name__ == "__main__":
    loader = ModuleLoader(modules_directory='amf/src/argument_mining_framework/modules')
    
    loader.print_metadata()
    
    try:
        model_name = 'sequence_classifier'  # Replace with the actual model name
        variant_name = "dialogpt"  # Use the variant name as a string
        variant_version = "vanilla" # Specify the version
        module_instance = loader.load_module(model_name, variant_name, variant_version)
        print(f"Loaded module: {module_instance}")
        
    except Exception as e:
        logger.error(f"An error occurred while loading the module: {e}")
