from src.loader.task_loader import load_amf_component
from utils.visualise2 import JsonToSvgConverter



def process_pipeline(input_data):
    """Process input data through the entire pipeline."""
    # Initialize components
    turninator = load_amf_component('turninator')()
    segmenter = load_amf_component('segmenter')()
    propositionalizer = load_amf_component('propositionalizer')()    
    argument_relation = load_amf_component('argument_relation', "dialogpt", "vanila")

    # Step 1: Turninator
    turninator_output = turninator.get_turns(input_data, True)
    print(f'Turninator output: {turninator_output}')

    # Step 2: Segmenter
    segmenter_output = segmenter.get_segments(turninator_output)
    print(f'Segmenter output: {segmenter_output}')

    # Step 3: Propositionalizer
    propositionalizer_output = propositionalizer.get_propositions(segmenter_output)
    print(f'Propositionalizer output: {propositionalizer_output}')

    # Step 4: Argument Relation Prediction
    argument_map_output = argument_relation.get_argument_map(propositionalizer_output)
    print(f'Argument relation prediction output: {argument_map_output}')

    # Additional Analysis
    print("Get all claims:")
    print(argument_relation.get_all_claims(argument_map_output))
    print("===============================================")

    print("Get evidence for claim:")
    print(argument_relation.get_evidence_for_claim(
        "But this isn’t the time for vaccine nationalism", argument_map_output))
    print("===============================================")

    print("Visualise the argument map")

    # Initialize the converter and perform the conversion
    url = 'http://ws.arg.tech/t/json-svg'
    converter = JsonToSvgConverter(url)
    json_data = argument_map_output['AIF']
    svg_output = converter.convert(json_data)
    if svg_output:
        converter.visualize_svg(svg_output)

def main():
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

    process_pipeline(input_data)

if __name__ == "__main__":
    main()
