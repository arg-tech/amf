import json
from src.argument_relation.predictor import ArgumentRelationPredictor as ArgumentRelation
from src.turninator.turninator import Turninator
from src.segmenter.segmenter import Segmenter
from src.propositionaliser.propositionalizer import Propositionalizer

def main():
    # Initialize components
    turninator = Turninator()
    segmenter = Segmenter()
    propositionalizer = Propositionalizer()
    predictor = ArgumentRelation("dialogpt", "vanila")

    # Sample input data
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

    # Process input through each component
    turninator_output = turninator.turninator_default(input_data, True)
    print(f'Turninator output: {turninator_output}')

    segmenter_output = segmenter.segmenter_default(turninator_output)
    print(f'Segmenter output: {segmenter_output}')

    propositionalizer_output = propositionalizer.propositionalizer_default(segmenter_output)
    print(f'Propositionalizer output: {propositionalizer_output}')

    argument_map_output = predictor.argument_map(propositionalizer_output)
    print(f'Argument relation prediction output: {argument_map_output}')

if __name__ == "__main__":
    main()
