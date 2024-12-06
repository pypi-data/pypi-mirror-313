import os
import json
from datetime import date
from emissor.persistence import ScenarioStorage
from emissor.representation.scenario import Modality
import datasets
import cltl.dialogue_evaluation.utils.text_signal as text_util
from cltl.dialogue_evaluation.api import BasicEvaluator
import numpy as np
import pandas as pd

#https://github.com/huggingface/evaluate
#https://huggingface.co/spaces/evaluate-metric/bleu
#https://huggingface.co/docs/datasets/metrics
NLG_METRICS = ['rouge', 'blue', 'sacrebleu', 'bleurt', 'meteor', 'google_bleu', 'bertscore', "all"]


class ReferenceEvaluator(BasicEvaluator):
    def __init__(self):
        """Creates an evaluator that will use reference metrics to approximate the quality of a conversation, across turns.
        params
        returns: None
        """
        super(ReferenceEvaluator, self).__init__()
        self._log.debug(f"Reference Evaluator ready")

    def apply_metrics(self, metrics_to_plot, references, predictions):
        results =[]
        for metric in metrics_to_plot:
            if not metric in NLG_METRICS:
                print('Unknown metrics: %s. Please provide one of the following: %s', metric, NLG_METRICS)

            if metric=="blue" or metric=="all":
                try:
                    print("blue")
                    evaluator = datasets.load_metric("bleu")
                    _predictions = [i.split() for i in predictions]
                    _references = [[i.split()] for i in references]
                   # print('_predictions', _predictions)
                   # print('_references', _references)
                    result = evaluator.compute(predictions=_predictions, references=_references)
                    result['precisions'] = np.average(result['precisions'])
                    result['metric']='blue'
                   # print('Result', result)
                    results.append(result)
                except Exception as e:
                    # By this way we can know about the type of error occurring
                    print("The error is: ", e)
                    pass

            #install the following dependencies ['absl', 'nltk', 'rouge_score']
            if metric=="rouge" or metric=="all":
                try:
                    print("rouge")
                    evaluator = datasets.load_metric("rouge")
                   # evaluator = evaluate.load("rouge")
                    result = evaluator.compute(predictions=predictions, references=references)
                    result = {key: value.mid.fmeasure * 100 for key, value in result.items()}
                    result = {k: round(v, 4) for k, v in result.items()}
                    result['metric']='rouge'

                  #  print(result)
                    results.append(result)
                except Exception as e:
                    # By this way we can know about the type of error occurring
                    print("The error is: ", e)
                    pass

            if metric=="meteor" or metric=="all":
                try:
                    print("meteor")
                    evaluator = datasets.load_metric("meteor")
                    result = evaluator.compute(predictions=predictions, references=references)
                    result['metric']='meteor'

                  #  print(result)
                    results.append(result)
                except Exception as e:
                    # By this way we can know about the type of error occurring
                    print("The error is: ", e)
                    pass

            if metric=="bertscore" or metric=="all":
                #https://arxiv.org/abs/1904.09675
                try:
                    print("bertscore")
                    evaluator = datasets.load_metric("bertscore")
                    result = evaluator.compute(predictions=predictions, references=references, lang="en", model_type="distilbert-base-uncased")
                    result['precision'] = round(np.average(result['precision']),4)
                    result['recall'] = round(np.average(result['recall']), 4)
                    result['f1'] = round(np.average(result['f1']), 4)
                    result['metric']='bertscore'
                  #  print(result)
                    results.append(result)
                except Exception as e:
                    # By this way we can know about the type of error occurring
                    print("The error is: ", e)
                    pass

            # install the following  pip install sacrebleu
            if metric=="sacrebleu" or metric=="all":
                print("sacrebleu")
                print("NOT IMPLEMENTED")
                #evaluator = datasets.load_metric("sacrebleu")
                #result = evaluator.compute(predictions=predictions, references=references)
                #print(result)
                #results.append(result)

            #install the following  https://github.com/google-research/bleurt
            if metric=="bleurt" or metric=="all":
                print("bleurt")
                print("NOT IMPLEMENTED")
               # evaluator = datasets.load_metric("bleurt")
               # result = evaluator.compute(predictions=predictions, references=references)
               # print(result)
               # results.append(result)

            if metric=="google_bleu" or metric=="all":
                print("google_bleu")
                print("NOT IMPLEMENTED")
                # evaluator = datasets.load_metric("google_bleu")
                # result = evaluator.compute(predictions=predictions, references=references)
                # print(result)
                # results.append(result)
            #https://github.com/neulab/BARTScore
        return results

    def evaluate_conversation_single_scenario_csv(self, csv_name, csv_file, metrics_to_plot):
        results ={}
        results["Description"]="EMSISSOR dialogue conversation by turns"
        results["File"]= csv_name
        results["date"]=  str(date.today())
        try:
          #  df = pd.read_csv(csv_file, sep=';')
            df = pd.read_excel(csv_file)
            results["System utterances"] = int((df['Speaker']=='LEOLANI').count()),
           # print(df.head())
            eval_refs =[]
            eval_preds =[]
            for index, row in df.iterrows():
                if pd.notnull(row["Reference Response"]) & pd.notnull(row["Response"]):
                    eval_preds.append(row['Response'])
                    eval_refs.append(row['Reference Response'])

            results["Reference utterances"] = len(eval_refs)
            results["Scores"] = []
            if len(eval_refs)>0:
                print('references', len(eval_refs))
                print('predictions', len(eval_preds))
                scores = self.apply_metrics(metrics_to_plot,references=eval_refs ,predictions=eval_preds )
                results["Scores"]=scores
                #print(scores)
              #Overall Human Rating	Interesting	Engaging	Specific	Relevant	Correct	Semantically Appropriate	Understandable	Fluent
           # mean = df.mean(axis=1, skipna=True)
           # results['Manual']=mean
            human_overall = df['Overall Human Rating'].mean(axis=0, skipna=True)
            human_interesting = df['Interesting'].mean(axis=0, skipna=True)
            human_engaging = df['Engaging'].mean(axis=0, skipna=True)
            human_specific = df['Specific'].mean(axis=0, skipna=True)
            human_relevant = df['Relevant'].mean(axis=0, skipna=True)
            human_correct = df['Correct'].mean(axis=0, skipna=True)
            human_seman_appr = df['Semantically Appropriate'].mean(axis=0, skipna=True)
            human_understandable = df['Understandable'].mean(axis=0, skipna=True)
            human_fluent = df['Fluent'].mean(axis=0, skipna=True)
            human_scores = {"Evaluated_responses" : str(df['Overall Human Rating'].count()),
                            "human_overall" : human_overall,
                            'human_interesting' : human_interesting,
                            'human_engaging' : human_engaging,
                            'human_specific' : human_specific,
                            'human_relevant' : human_relevant,
                            'human_correct' : human_correct,
                            'human_seman_appr' : human_seman_appr,
                            'human_undestandable' : human_understandable,
                            'human_fluent' : human_fluent}
            print(human_scores)
            results["manual"]=human_scores


        except Exception as e:
            print('Error reading', csv_file)
            results['Error']=str(e)
            print(e)
        return results

    def evaluate_conversation_two_scenarios(self, ref_scenario_folder,
                              sys_scenario_folder,
                              ref_scenario_id,
                              sys_scenario_id, metrics_to_plot=None):
        # Get the scenario folder, the json files and a scenarioStorage and scenario in memory
        # For both the reference scenario with the gold data (human-human conversation) and the system scenario
        # We expect the system to respond to the gold history for each turn of one of the interlocutors

        ref_scenario_storage = ScenarioStorage(ref_scenario_folder)
        ref_scenario_ctrl = ref_scenario_storage.load_scenario(ref_scenario_id)
        ref_signals = ref_scenario_ctrl.get_signals(Modality.TEXT)
        ref_ids, ref_utt, ref_speakers = text_util.get_utterances_with_context_from_signals(ref_signals, max_context=0)

        print('Reference SCENARIO_FOLDER:', ref_scenario_folder)
        print('Nr of reference utterances:', len(ref_utt), ' extracted from reference scenario: ', ref_scenario_id)
        print('Reference Speakers:', ref_speakers)

        sys_scenario_storage = ScenarioStorage(sys_scenario_folder)
        sys_scenario_ctrl = sys_scenario_storage.load_scenario(sys_scenario_id)
        sys_signals = sys_scenario_ctrl.get_signals(Modality.TEXT)
        sys_ids, sys_utt, sys_speakers = text_util.get_utterances_with_context_from_signals(sys_signals, max_context=0)


        print('System SCENARIO_FOLDER:', sys_scenario_folder)
        print('Nr of system utterances:', len(sys_utt), ' extracted from reference scenario: ', sys_scenario_id)
        print('system Speakers:', sys_speakers)
        references = text_util.get_texts_from_utterances(sys_utt)
        predictions = text_util.get_texts_from_utterances(ref_utt)

        print('Applying the following metrics',metrics_to_plot)

        results ={}
        results["Description"]="EMSISSOR dialogue conversation by turns"
        results["Reference scenario"]= ref_scenario_id
        results["Reference speakers"]= str(ref_speakers)
        results["Reference utterances"] = len(ref_utt)
        results["System scenario"]= sys_scenario_id
        results["System speakers"]= str(sys_speakers)
        results["System utterances"] = len(sys_utt)
        results["date"]=  str(date.today())
        results["Scores"]=self.apply_metrics(metrics_to_plot, references, predictions)
        # for metric in metrics_to_plot:
        #     if not metric in NLG_METRICS:
        #         print('Unknown metrics: %s. Please provide one of the following: %s', metric, NLG_METRICS)
        #
        #     if metric=="blue" or metric=="all":
        #         try:
        #             print("blue")
        #             evaluator = datasets.load_metric("bleu")
        #             _predictions = [i.split() for i in predictions]
        #             _references = [[i.split()] for i in references]
        #            # print('predictions', _predictions)
        #            # print('references', _references)
        #             result = evaluator.compute(predictions=_predictions, references=_references)
        #             result['precisions'] = np.average(result['precisions'])
        #             result['metric']='blue'
        #            # print('Result', result)
        #             results["Scores"].append(result)
        #         except Exception as e:
        #             # By this way we can know about the type of error occurring
        #             print("The error is: ", e)
        #             pass
        #
        #     #install the following dependencies ['absl', 'nltk', 'rouge_score']
        #     if metric=="rouge" or metric=="all":
        #         try:
        #             print("rouge")
        #             evaluator = datasets.load_metric("rouge")
        #            # evaluator = evaluate.load("rouge")
        #             result = evaluator.compute(predictions=predictions, references=references)
        #             result = {key: value.mid.fmeasure * 100 for key, value in result.items()}
        #             result = {k: round(v, 4) for k, v in result.items()}
        #             result['metric']='rouge'
        #
        #           #  print(result)
        #             results["Scores"].append(result)
        #         except Exception as e:
        #             # By this way we can know about the type of error occurring
        #             print("The error is: ", e)
        #             pass
        #
        #     if metric=="meteor" or metric=="all":
        #         try:
        #             print("meteor")
        #             evaluator = datasets.load_metric("meteor")
        #             result = evaluator.compute(predictions=predictions, references=references)
        #             result['metric']='meteor'
        #
        #            # print(result)
        #             results["Scores"].append(result)
        #         except Exception as e:
        #             # By this way we can know about the type of error occurring
        #             print("The error is: ", e)
        #             pass
        #
        #     if metric=="bertscore" or metric=="all":
        #         #https://arxiv.org/abs/1904.09675
        #         try:
        #             print("bertscore")
        #             evaluator = datasets.load_metric("bertscore")
        #             result = evaluator.compute(predictions=predictions, references=references, lang="en", model_type="distilbert-base-uncased")
        #             result['precision'] = round(np.average(result['precision']),4)
        #             result['recall'] = round(np.average(result['recall']), 4)
        #             result['f1'] = round(np.average(result['f1']), 4)
        #             result['metric']='bertscore'
        #           #  print(result)
        #             results["Scores"].append(result)
        #         except Exception as e:
        #             # By this way we can know about the type of error occurring
        #             print("The error is: ", e)
        #             pass
        #
        #     # install the following  pip install sacrebleu
        #     if metric=="sacrebleu" or metric=="all":
        #         print("sacrebleu")
        #         print("NOT IMPLEMENTED")
        #         #evaluator = datasets.load_metric("sacrebleu")
        #         #result = evaluator.compute(predictions=predictions, references=references)
        #         #print(result)
        #         #results["Scores"].append(result)
        #
        #     #install the following  https://github.com/google-research/bleurt
        #     if metric=="bleurt" or metric=="all":
        #         print("bleurt")
        #         print("NOT IMPLEMENTED")
        #        # evaluator = datasets.load_metric("bleurt")
        #        # result = evaluator.compute(predictions=predictions, references=references)
        #        # print(result)
        #        # results["Scores"].append(result)
        #
        #     if metric=="google_bleu" or metric=="all":
        #         print("google_bleu")
        #         print("NOT IMPLEMENTED")
        #         # evaluator = datasets.load_metric("google_bleu")
        #         # result = evaluator.compute(predictions=predictions, references=references)
        #         # print(result)
        #         # results["Scores"].append(result)
        #
        #     #https://github.com/neulab/BARTScore

        #
        # # Save
        evaluation_folder_path = os.path.join(sys_scenario_folder, sys_scenario_id, 'evaluation')
        ##evaluation_folder = os.path.(evaluation_folder_path)
        if not os.path.exists(evaluation_folder_path):
            os.mkdir(evaluation_folder_path)
        self._save(results, evaluation_folder_path)
        # #
#        if metrics_to_plot:
#             self.plot_metrics_progression(metrics_to_plot, [df], evaluation_folder)

    @staticmethod
    def _calculate_metrics(model_mlm, turns, speaker_mlm_scores, speaker_mlm_max_scores, speaker_turns):
        # Iterate turns
        print(f"\n\tCalculating likelihood scores")
        rows = []
        for index, turn in enumerate(turns):
            print(f"\t\tProcessing turn {index}/{len(turns)}")
            context = turn[0]
            target = turn[1]
            cue = turn[2]
            speaker = turn[3]
            llh, best_sentence, max_score = model_mlm.sentence_likelihood(context, target)
            rows.append({"Turn": index, "Speaker": speaker, "Cue": cue, "Response": target, "Context": context,
                         "MLM response": best_sentence, "System llh": llh, "MLM llh": max_score})

            if speaker:
                speaker_turns[speaker].append(index)
                speaker_mlm_scores[speaker].append(llh)
                speaker_mlm_max_scores[speaker].append(max_score)

        return pd.DataFrame(rows)

    def _save(self, results, evaluation_folder):
        file_path = os.path.join(evaluation_folder, "reference_evaluation.json")
        file = open(file_path, "w")
        json.dump(results, file, indent=4)
        file.close()

