import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
import argparse
import sys
from emissor.representation.scenario import Signal
from emissor.persistence import ScenarioStorage
from emissor.representation.scenario import Modality
import cltl.dialogue_evaluation.utils.text_signal as text_signal_util
import cltl.dialogue_evaluation.utils.image_signal as image_signal_util
import cltl.dialogue_evaluation.utils.scenario_check as check

class PlotSettings():
    _LLH_THRESHOLD = 0
    _SENTIMENT_THRESHOLD = 0
    _ANNOTATIONS =[]
    _START = 0
    _END = -1

## TEXT ONLY
def get_signal_rows(signals:[Signal], human, agent, settings: PlotSettings):
    data = []
    print('Nr of signals', len(signals))
    for i, signal in enumerate(signals):
        if i>= settings._START and (i<= settings._END or settings._END==-1):
            speaker = text_signal_util.get_speaker_from_text_signal(signal)
            if speaker.lower()=='speaker':
                speaker = human
            elif speaker.lower()=='agent':
                speaker = agent
            text = ''.join(signal.seq)
            score = 0
            score += text_signal_util.get_dact_feedback_score_from_text_signal(signal)
            if "sentiment" in settings._ANNOTATIONS:
                score += text_signal_util.get_sentiment_score_from_text_signal(signal)
            if "ekman" in settings._ANNOTATIONS:
                score += text_signal_util.get_ekman_feedback_score_from_text_signal(signal)
            if "go" in settings._ANNOTATIONS:
                score += text_signal_util.get_go_feedback_score_from_text_signal(signal)
            if "llh" in settings._ANNOTATIONS:
                score += text_signal_util.get_likelihood_from_text_signal(signal, settings._LLH_THRESHOLD)

            label = text_signal_util.make_annotation_label(signal, settings._SENTIMENT_THRESHOLD, settings._ANNOTATIONS)
            row = {'turn':i+1, 'utterance': text, 'score': score, "speaker": speaker, "type":signal.modality, "annotation": label}
            data.append(row)
    return data

def get_multimodal_signals(emissor_path, scenario):
    signalDict = {}
    sorted_signal_list = []
    scenario_storage = ScenarioStorage(emissor_path)
    scenario_ctrl = scenario_storage.load_scenario(scenario)
    text_signals = scenario_ctrl.get_signals(Modality.TEXT)
    image_signals =  scenario_ctrl.get_signals(Modality.IMAGE)
    for signal in text_signals+image_signals:
        time = signal.time.start
        if time in signalDict:
            signalDict[time].append(signal)
        else:
            signalDict[time] = [signal]

    times = list(signalDict.keys())
    times.sort()
    for time in times:
        signals = signalDict[time]
        for signal in signals:
            sorted_signal_list.append(signal)
    return sorted_signal_list

def get_multimodal_signal_rows(signals:[Signal], human, agent, settings: PlotSettings):
    data = []
    print('Nr of signals', len(signals))
    previous_image_label = ""
    previous_image_id = ""
    last_image_turn = 0
    margin = 2
    for i, signal in enumerate(signals):
        if i>= settings._START and (i<= settings._END or settings._END==-1):
            if signal.modality==Modality.TEXT:
                speaker = text_signal_util.get_speaker_from_text_signal(signal)
                if speaker.lower() == 'speaker':
                    speaker = human
                elif speaker.lower() == 'agent':
                    speaker = agent
                text = ''.join(signal.seq)
                score = 0
                score += text_signal_util.get_dact_feedback_score_from_text_signal(signal)
                if "sentiment" in settings._ANNOTATIONS:
                    score += text_signal_util.get_sentiment_score_from_text_signal(signal)
                if "ekman" in settings._ANNOTATIONS:
                    score += text_signal_util.get_ekman_feedback_score_from_text_signal(signal)
                if "go" in settings._ANNOTATIONS:
                    score += text_signal_util.get_go_feedback_score_from_text_signal(signal)
                if "llh" in settings._ANNOTATIONS:
                    score += text_signal_util.get_likelihood_from_text_signal(signal, settings._LLH_THRESHOLD)

                label = text_signal_util.make_annotation_label(signal, settings._SENTIMENT_THRESHOLD, settings._ANNOTATIONS)
                row = {'turn':i+margin, 'utterance': text, 'score': score, "speaker": speaker, "type":signal.modality, "annotation": label, "rotation": 70}
                data.append(row)
            elif signal.modality==Modality.IMAGE:
                score = 0
                score += image_signal_util.get_emotic_feedback_score_from_signal(signal)
                object, face, id, emotion = image_signal_util.make_annotation_label(signal)
                object_type = object
                if "-" in object:
                    object_type = object[:object.index("-")]
                if not id == previous_image_id:
                    row = {'turn':i+margin, 'utterance': id[:5], 'score': score, "speaker": "camera", "type":signal.modality, "annotation": face+";"+emotion+";"+object, "rotation": 70}
                elif not object_type==previous_image_label:
                    row = {'turn':i+margin, 'utterance': id[:5], 'score': score, "speaker": "camera", "type":signal.modality, "annotation": face+";"+emotion+";"+object, "rotation": 70}
                elif i+margin>last_image_turn:
                    row = {'turn':i+margin, 'utterance': id[:5], 'score': score, "speaker": "camera", "type":signal.modality, "annotation": emotion, "rotation": 70}
                previous_image_label = object_type
                previous_image_id = id
                last_image_turn = i+margin
                data.append(row)
    return data


def create_timeline_image(emissor_path, scenario, settings: PlotSettings):
    scenario_storage = ScenarioStorage(emissor_path)
    scenario_ctrl = scenario_storage.load_scenario(scenario)
    speaker = "No speaker"
    agent = "No agent"
    try:
        speaker = scenario_ctrl.scenario.context.speaker["name"] if "name" in scenario_ctrl.scenario.context.speaker else "No speaker"
    except:
        print("No speaker name in context")
    try:
        agent = scenario_ctrl.scenario.context.agent["name"] if "name" in scenario_ctrl.scenario.context.agent else "No agent"
    except:
        print("No agent name in context")
   # text_signals = scenario_ctrl.get_signals(Modality.TEXT)
   # rows = get_signal_rows(text_signals, speaker, agent, settings)
    signals = get_multimodal_signals(emissor_path, scenario)
    rows = get_multimodal_signal_rows(signals, speaker, agent, settings)

    plt.rcParams['figure.figsize'] = [len(rows), 5]
    df = pd.DataFrame(rows)
    #print(df.head())
    sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
 #   ax = sns.lineplot(x='turn', y='score', data=df, hue='speaker', style='annotation', markers=True, palette="bright", legend="brief")
    ax = sns.lineplot(x='turn', y='score', data=df, hue='speaker', style='speaker', markers=True, palette="bright", legend="brief")
    #palette = "flare/bright/deep/muted/colorblind/dark"
    for index, row in df.iterrows():
        x = row['turn']
        y = row['score']
        rotation = row['rotation']
        category = row['speaker']+":"
        words = row['utterance'].split(" ")
        for i, word in enumerate(words):
            if i==15:
                category += "..."
                break
            if i>0 and i%5==0:
                category+="\n"
            category +=word+" "
        annotations = row['annotation'].split(";")
        for i, annotation in enumerate(annotations):
            if i==0 or i%3==0:
                category+="\n"
            category += annotation+";"
        signalType = row['type']
        if signalType==Modality.TEXT:
            ax.text(x, y,
                    s=" " + str(category),
                    rotation=rotation,
                    horizontalalignment='left', size='small', color='black', verticalalignment='bottom',
                    linespacing=1.5)
        elif signalType==Modality.IMAGE:
            ax.text(x, y,
                    s=" " + str(category),
                    rotation=rotation,
                    horizontalalignment='right', size='small', color='blue', verticalalignment='top',
                    linespacing=1.5)

    ax.tick_params(axis='x', rotation=70)
    # Save the plot
    plt.legend(loc='lower right')
    plt.ylim(-5,5)

    evaluation_folder = os.path.join(emissor_path, scenario, "evaluation")
    if not os.path.exists(evaluation_folder):
        os.mkdir(evaluation_folder)
    name= scenario
    if settings._START>0:
        name += "_S"+ str(settings._START)
    if settings._END>-1:
        name += "_E"+str(settings._END)
    path =  os.path.join(evaluation_folder, name+"_plot.png")
   # plt.savefig(path, dpi=600)
    plt.savefig(path)
    plt.show()



def process_all_scenarios(emissor:str, scenarios:[], settings):
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
                    create_timeline_image(emissor_path=emissor, scenario=scenario, settings=settings)

def main(emissor_path:str, scenario:str, annotations:[], sentiment_threshold=0, llh_threshold=0, start=0, end=-1):
    settings = PlotSettings()
    if annotations:
        settings._ANNOTATIONS = annotations
    if sentiment_threshold > 0:
        settings._SENTIMENT_THRESHOLD = sentiment_threshold
    if llh_threshold > 0:
        settings._LLH_THRESHOLD = llh_threshold
    if start > 0:
        settings._START = start
    if end > -1:
        settings._END = end

    scenario_path = os.path.join(emissor_path, scenario)
    print(scenario_path)
    print("_ANNOTATIONS", settings._ANNOTATIONS)
    print("_SENTIMENT_THRESHOLD", settings._SENTIMENT_THRESHOLD)
    print("_LLH_THRESHOLD", settings._LLH_THRESHOLD)

    # DEBUG tests
    #settings._START = 0
    #settings._END = -1
    emissor_path = "/Users/piek/Desktop/d-Leolani/leolani-mmai-parent/cltl-leolani-app/py-app/storage/emissor"
    scenario="12f5c2a5-5955-40b2-9e11-45572cd26c75"
    scenario="96f97ec5-b25c-4991-af63-5eb4af05e3bf"
    scenario="415d481a-6a12-40ef-8675-cb8b1102bcd8"
    scenario="3598e3a7-ef15-4a3b-9ee2-3d410d5fb69a"
   # emissor_path = "/Users/piek/Desktop/t-MA-Combots-2024/code/ma-communicative-robots/interaction_analysis/emissor"
   # scenario="1abc01f0-b1d0-48f9-aafb-60214eaa4380"

    folders = []
    if not scenario:
        folders = os.listdir(emissor_path)
    else:
        folders = [scenario]
    process_all_scenarios(emissor_path, folders, settings)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Statistical evaluation emissor scenario')
    parser.add_argument('--emissor-path', type=str, required=False, help="Path to the emissor folder", default='')
    parser.add_argument('--scenario', type=str, required=False, help="Identifier of the scenario", default='')
    parser.add_argument('--sentiment_threshold', type=float, required=False, help="Threshold for dialogue_act, sentiment and emotion scores", default=0.5)
    parser.add_argument('--llh_threshold', type=float, required=False, help="Threshold below which likelihood becomes negative", default=0.3)
    parser.add_argument('--annotations', type=str, required=False, help="Annotations to be considered for scoring: 'go, sentiment, ekman, llh'" , default='go,sentiment,llh')
    parser.add_argument('--start', type=int, required=False, help="Starting signal for plotting" , default=0)
    parser.add_argument('--end', type=int, required=False, help="End signal for plotting, -1 means until the last signal" , default=-1)
    args, _ = parser.parse_known_args()
    print('Input arguments', sys.argv)

    main(emissor_path=args.emissor_path,
         scenario=args.scenario,
         annotations=args.annotations,
         llh_threshold=args.llh_threshold,
         sentiment_threshold=args.sentiment_threshold,
         start=args.start,
         end=args.end)