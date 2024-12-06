import os
import argparse
import sys
import cltl.dialogue_evaluation.utils.scenario_check as check
import pandas as pd
from emissor.persistence import ScenarioStorage
from emissor.representation.scenario import Modality

import cltl.dialogue_evaluation.utils.text_signal as text_util
from cltl.dialogue_evaluation.api import BasicEvaluator


class ManualEvaluator(BasicEvaluator):
    def __init__(self):
        """Creates an evaluator that will create placeholders for manual evaluation
        params
        returns: None
        """
        super(ManualEvaluator, self).__init__()

        self._log.debug(f"Manual Evaluator ready")

    def evaluate_conversation(self, scenario_folder, scenario_id, metrics_to_plot=None):
        ### Create the scenario folder, the json files and a scenarioStorage and scenario in memory
        scenario_storage = ScenarioStorage(scenario_folder)
        scenario_ctrl = scenario_storage.load_scenario(scenario_id)
        signals = scenario_ctrl.get_signals(Modality.TEXT)
        ids, turns, speakers = text_util.get_utterances_with_context_from_signals(signals)

        print('SCENARIO_FOLDER:', scenario_folder)
        print('Nr of turns:', len(turns), ' extracted from scenario: ', scenario_id)
        print('Speakers:', speakers)

        # Get likelihood scored
        speaker_turns = {k: [] for k in speakers}

        df = self._calculate_metrics(turns, speaker_turns)

        # Save
        evaluation_folder = os.path.join(scenario_folder, scenario_id, 'evaluation')
        if not os.path.exists(evaluation_folder):
            os.mkdir(evaluation_folder)
        self._save(df, evaluation_folder, scenario_id)
        self._create_dialogue_summary_file(evaluation_folder, scenario_id)
        #
        # if metrics_to_plot:
        #     self.plot_metrics_progression(metrics_to_plot, [full_df], evaluation_folder)

    @staticmethod
    def _calculate_metrics(turns, speaker_turns):
        # Iterate turns
        print(f"\tPlaceholders for manual scores")
        rows = []
        for index, turn in enumerate(turns):
            context = turn[0]
            target = turn[1]
            cue = turn[2]
            speaker = turn[3]
            rows.append({"Turn": index, "Speaker": speaker, "Response": target, "Reference Response": "",
                         "Overall Human Rating": '', "Interesting": '', "Engaging": '', "Specific": '', "Relevant": '',
                         "Correct": '', "Semantically Appropriate": '', "Understandable": '', "Fluent": ''})
            # rows.append({"Turn": index, "Speaker": speaker, "Cue": cue, "Response": target, "Reference Response": "", "Context": context,
            #              "Overall Human Rating": '', "Interesting": '', "Engaging": '', "Specific": '', "Relevant": '',
            #              "Correct": '', "Semantically Appropriate": '', "Understandable": '', "Fluent": ''})

            if speaker:
                speaker_turns[speaker].append(index)

        return pd.DataFrame(rows)

    def _save(self, df, evaluation_folder, scenario_id):
        file_name =  scenario_id+"_manual_evaluation.csv"
        file = os.path.join(evaluation_folder, file_name)
        df.to_csv(file, sep=";", index=False)

    def _create_dialogue_summary_file(self, evaluation_folder, scenario_id):
        file_name =  scenario_id+"_dialogue_summary.txt"
        file = os.path.join(evaluation_folder, file_name)
       # Create an empty file for the dialogue summary
        with open(file, 'w') as fp:
            pass

    def get_score(self, value):
        score = 0
        if not value == 'nan' and not value == '-':
            if type(value == 'str'):
                score = float(value)
            else:
                score = value
        else:
            print(type(value))
        return score


    def get_manual_evaluation_overview(self, scenario_folder):
        stat_dict = {}

        storage = ScenarioStorage(scenario_folder)
        scenarios = list(storage.list_scenarios())
        print("Processing scenarios: ", scenarios)
        columns = ["Label"]

        for scenario in scenarios:
           # if not scenario=='7ed0b885-c7b9-452a-bf8d-65a4d44409aa' and not scenario=='e7f18940-d085-4dde-a56e-9604fd22e601':
           #     continue
            columns.append(scenario)
           # csv_path = scenario_folder+"/"+scenario+"/"+"evaluation/"+scenario+"_manual_evaluation.csv"
            csv_path = scenario_folder+"/"+scenario+"/"+"evaluation/"+scenario+"_manual_evaluation.csv"
            print('Reading', csv_path)
            try:
                df = pd.read_csv(csv_path)
            except:
                df = pd.read_csv(csv_path, sep=";")
            print(df.info())
            overall = 0;
            interesting = 0
            engaging = 0
            specific = 0
            relevant = 0
            correct = 0;
            appropriate = 0
            understandable = 0
            fluent = 0
            agent = 'LEOLANI'
            agent_turns =0
            for index in df.index:
                if not df['Speaker'][index]==agent:
                    #### Skipping the speaker
                    continue

                scored = False
                if df["Overall Human Rating"][index]:
                    score = self.get_score(df["Overall Human Rating"][index])
                    if score>0:
                        overall += score
                        scored = True
                if df["Interesting"][index]:
                    score = self.get_score( df["Interesting"][index])
                    if score > 0:
                        interesting += score
                        scored = True
                if df["Engaging"][index]:
                    score = self.get_score(df["Engaging"][index])
                    if score>0:
                        engaging += score
                        scored = True
                if df["Specific"][index]:
                    score = self.get_score( df["Specific"][index])
                    if score>0:
                        specific += score
                        scored = True
                if df["Relevant"][index]:
                    score = self.get_score(df["Relevant"][index])
                    if score>0:
                        relevant += score
                        scored = True
                if df["Correct"][index]:
                    score = self.get_score(df["Correct"][index])
                    if score>0:
                        correct += score
                        scored = True
                if df["Semantically Appropriate"][index]:
                    score = self.get_score(df["Semantically Appropriate"][index])
                    if score>0:
                        appropriate += score
                        scored = True
                if df["Understandable"][index]:
                    score = self.get_score(df["Understandable"][index])
                    if score>0:
                        understandable += score
                        scored = True
                if df["Fluent"][index]:
                    score = self.get_score(df["Fluent"][index])
                    if score>0:
                        fluent += score
                        scored = True
                if scored:
                    agent_turns += 1
            #### After for loop
            if agent_turns>0:
                row = {"Overall_Rating":overall/agent_turns,"Interesting": interesting/agent_turns,
                       "Engaging": engaging/agent_turns,"Specific": specific/agent_turns,"Relevant": relevant/agent_turns,
                       "Correct": correct/agent_turns,"Semantically_Appropriate":appropriate/agent_turns,
                       "Understandable":understandable/agent_turns,"Fluent":fluent/agent_turns}
                #print(scenario, row)
                stat_dict[scenario] = row
            #break
        return stat_dict, columns

    def save_manual_evaluations(self, scenario_folder, stat_dict, columns):
        #  Rows:
        rows = ["Overall_Rating","Interesting","Engaging","Specific","Relevant","Correct","Semantically_Appropriate","Understandable","Fluent"]
        dfall = pd.DataFrame(columns=columns)
        turn_row = {'Label': 'Turns'}
        image_row = {'Label': 'Images'}
        storage = ScenarioStorage(scenario_folder)
        scenarios = list(storage.list_scenarios())
        for scenario in scenarios:
            scenario_ctrl = storage.load_scenario(scenario)
            text_signals = scenario_ctrl.get_signals(Modality.TEXT)
            image_signals = scenario_ctrl.get_signals(Modality.IMAGE)
            turn_row.update({scenario: len(text_signals)})
            image_row.update({scenario: len(image_signals)})

        dfall = dfall.append(turn_row, ignore_index=True)
        dfall = dfall.append(image_row, ignore_index=True)

        for label in rows:
            row = {'Label': label}
            for scenario in scenarios:
               # print(label, scenario)
                if scenario in stat_dict.keys():
                    count_dict = stat_dict.get(scenario)
                    if label in count_dict.keys():
                        count = count_dict[label]
                    else:
                        count = 0
                else:
                   # print("cannot find scenario for label", label, scenario)
                    count = 0
                row.update({scenario: count})
            #print("added the row",row)
            dfall = dfall.append(row, ignore_index=True)

        file_path = scenario_folder + "/" + "manual_evaluation_overview.csv"
        print("Saving overview to:", file_path)
        dfall.to_csv(file_path)




    def server_submission(self, submission_path):
          for scenario in os.listdir(submission_path):
              scenario_path = os.path.join(submission_path, scenario)
              if os.path.isdir(scenario_path):
                  has_scenario, has_text, has_image, has_rdf = check.check_scenario_data(scenario_path, scenario)
                  check_message = "Scenario folder:" + scenario_path + "\n"
                  check_message += "\tScenario JSON:" + str(has_scenario) + "\n"
                  check_message += "\tText JSON:" + str(has_text) + "\n"
                  check_message += "\tImage JSON:" + str(has_image) + "\n"
                  check_message += "\tRDF :" + str(has_rdf) + "\n"
                  print(check_message)
                  if not has_scenario:
                      print("No scenario JSON file found. Aborting.")
                  elif not has_text:
                      print("No text JSON file found. Aborting.")
                  else:
                        self.evaluate_conversation(submission_path, scenario)


    def process_all_scenarios(self, emissor:str, scenarios:[]):
        for scenario in scenarios:
            if not scenario.startswith("."):
                scenario_path = os.path.join(emissor, scenario)
                has_scenario, has_text, has_image, has_rdf = check.check_scenario_data(scenario_path, scenario)
                check_message = "Scenario:" + scenario + "\n"
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
                    self.evaluate_conversation(emissor, scenario)

def main(emissor_path:str, scenario:str):
    evaluator = ManualEvaluator()

   # emissor_path = "/Users/piek/Desktop/t-MA-Combots-2024/assignments/assignment-1/leolani_local/emissor"
   # scenario=""
    folders = []
    if not scenario:
        folders = os.listdir(emissor_path)
    else:
        folders = [scenario]
    evaluator.process_all_scenarios(emissor_path, folders)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Statistical evaluation emissor scenario')
    parser.add_argument('--emissor-path', type=str, required=False, help="Path to the emissor folder", default='')
    parser.add_argument('--scenario', type=str, required=False, help="Identifier of the scenario", default='')
    args, _ = parser.parse_known_args()
    print('Input arguments', sys.argv)

    main(emissor_path=args.emissor_path,
         scenario=args.scenario)
