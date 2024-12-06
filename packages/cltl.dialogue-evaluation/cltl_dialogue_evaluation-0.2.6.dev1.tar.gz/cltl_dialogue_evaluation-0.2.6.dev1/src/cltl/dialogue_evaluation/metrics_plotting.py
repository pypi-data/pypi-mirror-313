import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from cltl.dialogue_evaluation.api import BasicPlotter
from cltl.dialogue_evaluation.utils.constants import GRAPH_METRICS


class Plotter(BasicPlotter):
    def __init__(self):
        """Creates an evaluator that will use graph metrics to approximate the quality of a conversation, across turns.
        params
        returns: None
        """
        super(Plotter, self).__init__()
        self._log.debug(f"Plotter ready")

    def plot_conversations(self, scenarios_path, metrics):
        scenarios_paths = sorted([path for path in scenarios_path.iterdir()
                                  if path.is_dir() and path.stem not in ['.idea', 'plots']])

        # Plot metrics progression per conversation
        for metric in metrics:
            metric_df = pd.DataFrame()

            # Read data
            for scenario in scenarios_paths:
                filename = 'graph_evaluation.csv' if metric in GRAPH_METRICS else 'likelihood_evaluation_context300.csv'
                convo_df = pd.read_csv(scenario / 'evaluation' / filename, header=0)
                convo_df = convo_df.set_index('Turn')
                convo_df['Conversation'] = scenario.stem
                conversation_id = f"{convo_df['Conversation'].values[0]}"

                # Add into a dataframe
                if len(metric_df) == 0:
                    metric_df[conversation_id] = convo_df[metric]
                else:
                    metric_df = pd.concat([metric_df, convo_df[metric]], axis=1)
                    metric_df.rename(columns={metric: conversation_id}, inplace=True)

            # Cutoff and plot
            self.plot_progression(metric_df, metric, scenarios_path)

    @staticmethod
    def plot_progression(df_to_plot, xlabel, evaluation_folder):
        # Re-structure
        df_to_plot = df_to_plot.reset_index().melt('Turn', var_name='cols', value_name=xlabel)

        # Plot
        g = sns.relplot(x="Turn", y=xlabel, hue='cols', data=df_to_plot, kind='line')
        ax = plt.gca()
        plt.xlim(0)
        plt.xticks(ax.get_xticks()[::5], rotation=45)

        # Save
        plot_file = evaluation_folder / f"{xlabel}.png"
        print(plot_file)
        g.figure.savefig(plot_file, dpi=300, bbox_inches='tight')
