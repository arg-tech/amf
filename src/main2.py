import logging
import sys
import os
from argument_mining_framework.loader import ModuleLoader

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_modules(loader: ModuleLoader) -> dict:
    """Initialize modules based on loaded metadata from ModuleLoader."""
    modules = {}
    for task_name, info in loader.modules_metadata.items():
        # Iterate through variants and load the specified version
        for variant_info in info['variants']:
            variant_name = variant_info['name']
            variant_version = variant_info.get('version')  # Use .get() to handle optional version
            
            # Load the module, allowing for None as a version
            modules[task_name] = loader.load_module(task_name, variant_name, variant_version)
            logging.info(f'Loaded {task_name} module: {variant_name} (version {variant_version})')
            break  # Load the first variant for now
    return modules

def process_pipeline(input_data: str, modules: dict) -> None:
    print("==================:", modules)
    """Process input data through the entire argument mining pipeline."""
    
    # Step 1: Turninator
    turninator_output = modules['turninator'].get_turns(input_data, True)
    logging.info('Turninator output: %s', turninator_output)

    # Step 2: Segmenter
    segmenter_output = modules['segmenter'].get_segments(turninator_output)
    logging.info('Segmenter output: %s', segmenter_output)

    # Step 3: Propositionalizer
    propositionalizer_output = modules['propositionalizer'].get_propositions(segmenter_output)
    logging.info('Propositionalizer output: %s', propositionalizer_output)

    # Step 4: Argument Relation Prediction
    argument_map_output = modules['argument_relation'].get_argument_map(propositionalizer_output)
    logging.info('Argument relation prediction output: %s', argument_map_output)

    # Additional Analysis
    claims = modules['argument_relation'].get_all_claims(argument_map_output)
    logging.info("Extracted claims: %s", claims)

    evidence = modules['argument_relation'].get_evidence_for_claim(
        "But this isn’t the time for vaccine nationalism", argument_map_output)
    logging.info("Evidence for claim: %s", evidence)

    # Hypothesis Prediction
    hypothesis_results = modules['hypothesis'].predict([
        "But this isn’t the time for vaccine nationalism",
        "Vaccine is useful to prevent infections."
    ])
    logging.info("Hypothesis prediction: %s", hypothesis_results)

    # Scheme Prediction
    scheme_results = modules['scheme'].predict([
        "But this isn’t the time for vaccine nationalism",
        "Vaccine is useful to prevent infections."
    ])
    logging.info("Scheme prediction: %s", scheme_results)

    # Visualize the argument map
    modules['visualiser'].visualise(argument_map_output)

def main() -> None:
    """Main function to run the argument mining pipeline."""
    input_data = (
        """Liam Halligan: Vaccines mark a major advance in human achievement since the """
        """enlightenment into the 19th Century and Britain’s been at the forefront of """
        """those achievements over the years and decades. But this isn’t the time for """
        """vaccine nationalism. I agree we should congratulate all the scientists, those """
        """in Belgium, the States, British scientists working in international teams here """
        """in the UK, with AstraZeneca.\n"""
        """Fiona Bruce: What about the logistical capabilities? They are obviously """
        """forefront now, now we’ve got a vaccine that’s been approved. It’s good -- I’m """
        """reassured that the British Army are going to be involved. They’re absolute world """
        """experts at rolling out things, complex logistic capabilities. This is probably """
        """going to be the biggest logistical exercise that our armed forces have undertaken """
        """since the Falklands War, which I’m old enough to remember, just about. So, as a """
        """neutral I’d like to see a lot of cross-party cooperation, and I’m encouraged with """
        """Sarah’s tone, everybody wants to see us getting on with it now. They don’t want """
        """to see competition on whose vaccine is best. There will be some instances where """
        """the Pfizer vaccine works better, another where you can’t have cold refrigeration, """
        """across the developing world as well, a cheaper vaccine like the AstraZeneca works """
        """better. Let’s keep our fingers crossed and hope we make a good job of this."""
    )

    # Load the ModuleLoader
    loader = ModuleLoader(modules_directory='amf/src/argument_mining_framework/modules')

    # Print metadata (optional)
    loader.print_metadata()

    # Initialize modules based on metadata
    modules = initialize_modules(loader)

    # Process the input data through the pipeline
    process_pipeline(input_data, modules)

if __name__ == "__main__":
    main()
