
import logging
from argument_mining_framework.loader import Module

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def process_pipeline(input_data: str) -> None:
    """Process input data through the entire argument mining pipeline."""

    # Initialize components
    modules = {
        'turninator': Module('turninator'),
        'segmenter': Module('segmenter'),
        'propositionalizer': Module('propositionalizer'),
        'argument_relation': Module('argument_relation', "dialogpt", "vanilla"),
        'hypothesis': Module('hypothesis', "roberta", "vanilla"),
        'scheme': Module('scheme', "roberta", "vanilla"), 
        'visualiser': Module('visualiser')
    }

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

    process_pipeline(input_data)


if __name__ == "__main__":
    main()
