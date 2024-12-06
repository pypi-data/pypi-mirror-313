import logging

import os
import argparse
import sys
import uuid
from dataclasses import dataclass
from cltl.dialogue_evaluation.metrics.utterance_likelihood import MLM

from cltl.combot.event.emissor import AnnotationEvent
from cltl.combot.infra.time_util import timestamp_now
from emissor.representation.scenario import Mention, TextSignal, Annotation, class_type
from emissor.persistence import ScenarioStorage
import cltl.dialogue_evaluation.utils.scenario_check as check
from emissor.persistence.persistence import ScenarioController
from emissor.processing.api import SignalProcessor
from emissor.representation.scenario import Modality, Signal
logger = logging.getLogger(__name__)

@dataclass

class Likelihood:
    score: float
    model: str
    max: float


@dataclass
class LikelihoodEvent(AnnotationEvent[Annotation[Likelihood]]):
    @classmethod
    def create_text_mention(cls, text_signal: TextSignal, llh: Likelihood , source: str):
        return cls(class_type(cls), [LikelihoodEvent.to_mention(text_signal, llh, source)])

    @staticmethod
    def to_mention(text_signal: TextSignal, llh: Likelihood, source: str) -> Mention:
        """
        Create Mention with annotations.
        """
        segment = text_signal.ruler
        annotation = Annotation("Likelihood", llh, source, timestamp_now())

        return Mention(str(uuid.uuid4()), [segment], [annotation])

class LikelihoodAnnotator (SignalProcessor):

    def __init__(self, model: str, model_name: str, max_content: int, top_results: int):
        """ an evaluator that will use reference metrics to approximate the quality of a conversation, across turns.
        params
        returns: None
        """
        self._classifier = MLM(path=model, top_results=top_results)
            #LikelihoodEvaluator(model=model, max_context=max_content, len_top_tokens=top_tokens)
        self._model_name = model_name
        self._max_context = max_content
        self._max_text_length=514
        self._context = ""


    def process_signal(self, scenario: ScenarioController, signal: Signal):
        if not signal.modality == Modality.TEXT:
            return
        mention = self.annotate(signal)
        signal.mentions.append(mention)

    def annotate(self, textSignal):
        utterance = textSignal.text
        if len(utterance)> self._max_text_length:
            utterance=utterance[:self._max_text_length]
        likelihood, expected_target, max_likelihood = self._classifier.sentence_likelihood(self._context, utterance)
        mention = LikelihoodEvent.to_mention(textSignal, likelihood, self._model_name)
        ### Update the context
        self._context += utterance
        if len(self._context)> self._max_context:
            self._context=self._context[:self._max_context]

        return mention

def main(emissor_path:str, scenario:str, model_path="google-bert/bert-base-multilingual-cased", model_name="mBERT", max_context=300, len_top_tokens=20):
    scenario_path = os.path.join(emissor_path, scenario)
    has_scenario, has_text, has_image, has_rdf = check.check_scenario_data(scenario_path, scenario)
    check_message = "Scenario folder:" + emissor_path + "\n"
    check_message += "\tScenario JSON:" + str(has_scenario) + "\n"
    check_message += "\tText JSON:" + str(has_text) + "\n"
    check_message += "\tImage JSON:" + str(has_image) + "\n"
    check_message += "\tRDF :" + str(has_rdf) + "\n"
    print(check_message)
    if not has_scenario:
        print("No scenario JSON found. Skipping:", scenario_path)
    elif not has_text:
        print("No text JSON found. Skipping:", scenario_path)
    else:
        annotator = LikelihoodAnnotator(model=model_path, model_name=model_name, max_content=max_context, top_results=len_top_tokens)
        scenario_path = os.path.join(emissor_path, scenario)
        print(scenario_path)
        print("model_path", model_path)
        print("model_name", model_name)
        print("context_threshold", max_context)
        print("top_results", len_top_tokens)
        scenario_storage = ScenarioStorage(emissor_path)
        scenario_ctrl = scenario_storage.load_scenario(scenario)
        signals = scenario_ctrl.get_signals(Modality.TEXT)
        for signal in signals:
            annotator.process_signal(scenario=scenario_ctrl, signal=signal)
        #### Save the modified scenario to emissor
        scenario_storage.save_scenario(scenario_ctrl)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Statistical evaluation emissor scenario')
    parser.add_argument('--emissor-path', type=str, required=False, help="Path to the emissor folder", default='')
    parser.add_argument('--scenario', type=str, required=False, help="Identifier of the scenario", default='')
    parser.add_argument('--model_path', type=str, required=False, help="Path to the model or huggingface URL", default="google-bert/bert-base-multilingual-cased")
    parser.add_argument('--model_name', type=str, required=False, help="Model name for annotation in emissor", default="mBERT")
    parser.add_argument('--context', type=int, required=False, help="Maximum character length of the context" , default=300)
    parser.add_argument('--top_results', type=int, required=False, help="Maximum number of MASKED results considered" , default=20)
    args, _ = parser.parse_known_args()
    print('Input arguments', sys.argv)

    emissor_path = "/Users/piek/Desktop/d-Leolani/leolani-mmai-parent/cltl-leolani-app/py-app/storage/emissor"
    scenario="68bdf6e8-88da-4735-8264-37166b7b930f"
    scenario="12f5c2a5-5955-40b2-9e11-45572cd26c75"

    main(emissor_path=emissor_path,
         scenario=scenario,
         model_path=args.model_path,
         model_name = args.model_name,
         max_context=args.context,
         len_top_tokens=args.top_results)
    # main(emissor_path=args.emissor_path,
    #      scenario=args.scenario,
    #      model_path=args.model_path,
    #      model_name = args.model_name,
    #      max_context=args.context,
    #      len_top_tokens=args.top_results)
