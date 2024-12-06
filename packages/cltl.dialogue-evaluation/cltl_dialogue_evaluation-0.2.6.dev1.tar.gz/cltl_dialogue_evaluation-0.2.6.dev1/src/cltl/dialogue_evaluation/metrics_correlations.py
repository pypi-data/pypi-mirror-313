import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import argparse
import sys
import os
from pathlib import Path
from cltl.dialogue_evaluation.utils.constants import GRAPH_METRICS, LIKELIHOOD_METRICS, HUMAN_METRICS

from cltl.dialogue_evaluation.api import BasicCorrelator

class Correlator(BasicCorrelator):
    def __init__(self):
        """Creates an evaluator that will use graph metrics to approximate the quality of a conversation, across turns.
        params
        returns: None
        """
        super(Correlator, self).__init__()
        self._log.debug(f"Correlator ready")

    def correlate_metrics_single_scenario(self, scenario, metrics):
        # Read data from human annotations, automatic and likelihood
        convo_df = self.read_evaluations(scenario, metrics)
        # convo_df = convo_df.set_index('Turn')
        convo_df['Conversation'] = scenario.stem
        conversation_id = f"{convo_df['Conversation'].values[0]}"

        # Compute correlations
        corr_df = convo_df.corr(method='pearson', numeric_only=True)
        # Plot per scenario
        evaluation_path = os.path.join(scenario, "evaluation")
        self.plot_correlations(corr_df, None, conversation_id, evaluation_path)
        csv_file = os.path.join(evaluation_path, conversation_id+"_correlations.csv")
        corr_df.to_csv(csv_file)
        return corr_df

    def correlate_metrics(self, scenarios_path, scenario_selected, metrics):
        scenarios_paths = sorted([path for path in scenarios_path.iterdir()
                                  if path.is_dir() and path.stem not in ['.idea', 'plots']])

        corr_dfs = []
        for scenario in scenarios_paths:
            if scenario_selected and not scenario_selected==scenario.stem:
                print(scenario_selected, " is not this scenario", scenario.stem)
                continue
            else:
                print('Getting correlations for', scenario)
            # Read data from human annotations, automatic and likelihood
            corr_df = self.correlate_metrics_single_scenario(scenario, metrics)
            corr_dfs.append(corr_df)
        # Average conversations
        if len(corr_dfs)>1:
            avg_df = pd.concat(corr_dfs).groupby(level=0).mean(numeric_only=True)
            avg_df = avg_df.reindex(sorted(avg_df.columns), axis=1)
            self.plot_correlations(avg_df, None, '', scenarios_path)

    @staticmethod
    def read_evaluations(scenario, metrics):
        print(f"Correlations on {scenario.stem}")
        evaluation_folder = os.path.join(scenario, "evaluation")
        print('evaluation_folder', evaluation_folder)
        # Read evaluations
        evaluations = []
        for file in ['graph_evaluation.csv', 'likelihood_evaluation_USR_context300.csv',
                     f'{scenario.stem}_manual_evaluation.csv']:
            try:
                file_path = os.path.join(evaluation_folder, file)
                df = pd.read_csv(file_path, header=0, index_col='Turn')
            except:
                try:
                    df = pd.read_csv(file_path, header=0, index_col='Turn', sep=';')
                except:
                    print(f"Could not load {scenario}")
                    df = pd.DataFrame()
                    # continue

            columns_to_keep = [c for c in metrics if c in df.columns]
            df = df[columns_to_keep]
            evaluations.append(df)

        # Merge and select
        full_df = pd.concat(evaluations, axis=1)

        # rename
        # full_df.rename(columns={'System llh': 'AUTOMATIC - System llh', 'MLM llh': 'AUTOMATIC - MLM llh',
        #                         'USR DLcontext': 'AUTOMATIC - USR DLcontext', 'USR DLfact': 'AUTOMATIC - USR DLfact'},
        #                inplace=True)
        #New columns: Turn	Speaker	Cue	Response	Context	MLM response	System llh	MLM llh
        full_df.rename(columns={'System llh': 'AUTOMATIC - System llh', 'MLM llh': 'AUTOMATIC - MLM llh'},
                       inplace=True)
        full_df.rename(columns={'Overall Human Rating': 'HUMAN - Overall Human Rating',
                                'Interesting': 'HUMAN - Interesting', 'Engaging': 'HUMAN - Engaging',
                                'Specific': 'HUMAN - Specific', 'Relevant': 'HUMAN - Relevant',
                                'Correct': 'HUMAN - Correct',
                                'Semantically Appropriate': 'HUMAN - Semantically Appropriate',
                                'Understandable': 'HUMAN - Understandable',
                                'Fluent': 'HUMAN - Fluent'}, inplace=True)

        return full_df

    @staticmethod
    def plot_correlations(df_to_plot, mask, scenario, evaluation_folder):
        # Plot
        plt.figure()
        plt.xticks(fontsize=3)
        plt.yticks(fontsize=3)

        g = sns.heatmap(df_to_plot, mask=mask, annot=False, fmt=".2f",
                        cmap="YlGnBu", cbar_kws={"shrink": .3, "location": "top"},
                        cbar=True, center=0,
                        square=True)

        # Save
        plot_file = os.path.join(evaluation_folder, scenario+"_correlations_heatmap.png")
        g.figure.savefig(plot_file, dpi=300, transparent=False, bbox_inches='tight')
        plt.close()
        print(f"\tSaved to file: {plot_file}")


def main(emissor_path:str, scenario:str, graph_evalation, llh_evalation, manual_evaluation):
    metrics= None
    if graph_evalation:
        metrics += GRAPH_METRICS
    if llh_evalation:
        metrics += LIKELIHOOD_METRICS
    if manual_evaluation:
        metrics += HUMAN_METRICS
    correlator = Correlator()

    emissor_path = Path("../../../examples/data/emissor")
    scenario = "d5a6bc60-c19b-4c08-aee5-b4dd1c65c64d"
    scenario_path = os.path.join(emissor_path, scenario)
    print(scenario_path)

    correlator.correlate_metrics(emissor_path, scenario,
                                 metrics=GRAPH_METRICS + LIKELIHOOD_METRICS + HUMAN_METRICS)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Statistical evaluation emissor scenario')
    parser.add_argument('--emissor-path', type=str, required=False, help="Path to the emissor folder", default='')
    parser.add_argument('--scenario', type=str, required=False, help="Identifier of the scenario", default='')
    parser.add_argument('--graph_evaluation', type=str, required=False, help="Path to the graph evaluation file", default='')
    parser.add_argument('--graph_metrics', type=str, required=False, help="Path to the graph evaluation file", default='')
    parser.add_argument('--llh_evaluation', type=str, required=False, help="Path to the llh evaluation file", default='')
    parser.add_argument('--manual_evaluation', type=str, required=False, help="Path to the manual evaluation file", default='')
    args, _ = parser.parse_known_args()
    print('Input arguments', sys.argv)

    main(emissor_path=args.emissor_path,
         scenario=args.scenario,
         graph_evalation=args.graph_evaluation,
         llh_evalation=args.llh_evaluation,
         manual_evaluation=args.manual_evaluation)