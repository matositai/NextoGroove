import os
import numpy as np
import pandas as pd
import math
from collections import defaultdict
from scipy import stats
import random
import threading
import queue
import time
import warnings
import mido
import numpy as np
import pandas as pd

def conditional_mean(series):
    zeros = (series == 0).sum()
    if zeros >= len(series) / 2:
        return 0
    else:
        return series.mean()



def get_midi_note():
    # --- CONFIGURATION ---
    VIRTUAL_PORT_NAME = "fromLivePort 2"  # Adjust this to match your loopMIDI port
    MINIMUM_ACCEPTED_VELOCITY = 0

    # --- LIST AVAILABLE OUTPUT PORTS ---
    print("Available MIDI Output Ports:")
    for name in mido.get_output_names():
        print(f" - {name}")

    # --- OPEN PORT AND LISTEN ---
    print(f"\nListening for MIDI notes from Ableton on port: {VIRTUAL_PORT_NAME}\n")

    inport = mido.open_input()
    msg = inport.receive()
    if ((msg.type == "note_on") and (msg.velocity > MINIMUM_ACCEPTED_VELOCITY)):
        return int(msg.note)
    else:
        return None

def find_bar(base_list):
    #Find the indices of the two 24s
    first_24 = base_list.index(24)
    second_24 = base_list.index(24, first_24 + 1)
    
    #Slice the list between the two 24s (exclusive)
    bar = base_list[first_24 + 1:second_24]
    
    print("Bar Found:", bar)
    return bar

def find_keynote_and_duration(bar):
    #Find the duration & keynote of a bar
    bar_duration = len(bar)
    bar_keynote, keynote_freq = stats.mode(np.array(bar), axis=None, keepdims=True)
    return bar_duration, bar_keynote

def get_density_class_and_component_count(note_density_to_component_count_recommendation, bar_duration):
    component_count_selected_df = note_density_to_component_count_recommendation.query(f'notes_per_bar_lower_bound <= {bar_duration} & notes_per_bar_upper_bound >= {bar_duration}')
    component_lower_bound = note_density_to_component_count_recommendation['components_lower_bound'].to_list()[0]
    component_upper_bound = note_density_to_component_count_recommendation['components_upper_bound'].to_list()[0]
    component_count_selection = random.randint(component_lower_bound, component_upper_bound)
    density_class_present = note_density_to_component_count_recommendation['density_class'].to_list()[0]
    return component_count_selection, density_class_present

def perform_score_based_recommendation(bar_keynote, density_class_present, component_count_selection, pooled_scoring_df):
    # Given pooled scoring dataframe, keynote & duration filter the pooled scoring matrix to find the possible actions to perform recommendation
    
    # filter pooled scoring df given density class & keynote
    pooled_scoring_df['Input_list'] = [[int(s) for s in e.split(',')] for e in pooled_scoring_df['Input'].to_list()]
    pooled_scoring_df_filtered = pooled_scoring_df.query(f'Density_Class == {density_class_present}')
    pooled_scoring_df_filtered['is_keynote_present'] = [1 if bar_keynote in e else 0 for e in pooled_scoring_df_filtered['Input_list'].to_list()]
    pooled_scoring_df_filtered_final = pooled_scoring_df_filtered.query('is_keynote_present == 1')
    
    # given the component count selection pick top k components that are not zero
    possible_actions_df = pooled_scoring_df_filtered_final[['Kick', 'Snare', 'Hihat', 'Tom', 'Cymbals']]
    k = component_count_selection
    #Convert row to dictionary
    row_dict = possible_actions_df.iloc[0].to_dict()
    #Filter non-zero items and sort by value (descending)
    non_zero_items = {k: v for k, v in row_dict.items() if v != 0}
    top_k_keys = sorted(non_zero_items, key=non_zero_items.get, reverse=True)[:k]
    #Create binary dictionary (1 for top k, 0 otherwise)
    binary_dict = {k: int(k in top_k_keys) for k in row_dict}

    return binary_dict

def map_names_to_cc_numbers(control_mappings, binary_dict):
    # Read cc numbers to name mappings
    num = control_mappings['cc_number'].to_list()
    nam = control_mappings['cc_name'].to_list()
    mapping = dict(zip(nam, num))
    # Apply mapping to keys
    final_dict = {mapping[k]: v for k, v in binary_dict.items()}
    return final_dict

def read_inputs():
    # Given the duration decide on the number of components
    note_density_to_component_count_recommendation = pd.read_csv('note_density_to_component_count_recommendation.csv', sep = ';', encoding = 'utf8')
    pooled_scoring_df = pd.read_csv('pooled_choice_ranks.csv', sep = ',', encoding = 'utf8')
    control_mappings = pd.read_csv('control_mappings.csv', sep = ';', encoding = 'utf8')
    return note_density_to_component_count_recommendation, pooled_scoring_df, control_mappings

def read_scoring_inputs():
    input_dir = 'C:/Users/User/NextoGroove/inputs/choice_ranks'
    os.chdir(input_dir)
    
    # Load all CSVs into one long DataFrame
    files = ['choice_ranks_1.csv', 'choice_ranks_2.csv']
    df_all = pd.concat([pd.read_csv(f, sep = ';', encoding = 'utf8') for f in files])
    return df_all

def perform_score_pooling(df_all):
    item_list = np.unique(df_all['Input'].to_numpy()).tolist()
    index_list = list(range(len(item_list)))
    mapping_dict = dict(zip(item_list, index_list))
    df_all['Input_index'] = df_all.Input.map(mapping_dict)
    inv_mapping_dict = dict(zip(index_list, item_list))

    pooled_scoring_df = df_all.groupby(['Input_index','Density_Class']).agg({'Kick' : conditional_mean, 
                                                                          'Snare' : conditional_mean, 
                                                                          'Hihat' : conditional_mean,
                                                                          'Tom' : conditional_mean,
                                                                          'Cymbals' : conditional_mean}).reset_index()

    pooled_scoring_df['Input'] = pooled_scoring_df.Input_index.map(inv_mapping_dict)

    return pooled_scoring_df

def write_scoring_output(pooled_scoring_df):
    output_dir = 'C:/Users/User/NextoGroove/inputs'
    os.chdir(output_dir)
    
    pooled_scoring_df.to_csv('pooled_choice_ranks.csv', index = False)
    return None

def run_pooled_scoring():
    df_all = read_scoring_inputs()
    pooled_scoring_df = perform_score_pooling(df_all)
    x = write_scoring_output(pooled_scoring_df)

def run_recommendation_algorithm(bar, note_density_to_component_count_recommendation, pooled_scoring_df, control_mappings):
    bar_duration, bar_keynote = find_keynote_and_duration(bar)
    component_count_selection, density_class_present = get_density_class_and_component_count(note_density_to_component_count_recommendation, bar_duration)
    binary_recommendation_dict = perform_score_based_recommendation(bar_keynote, density_class_present, component_count_selection, pooled_scoring_df)
    mapped_binary_recommendation_dict = map_names_to_cc_numbers(control_mappings, binary_recommendation_dict)
    return binary_recommendation_dict, mapped_binary_recommendation_dict, bar, bar_duration, bar_keynote, density_class_present

def producer_fn(q_out):
    # --- CREATE BUFFER ---
    buffer = []

    # --- OPEN MIDI CONNECTION & READ
    while True:
        value = get_midi_note()
        buffer.append(value)
        
        #Catch the 24s that signify the start and end of a bar
        if buffer.count(24) >= 2:
            idxs = [i for i, val in enumerate(buffer) if val == 24]
            last_start, last_end = idxs[-2], idxs[-1]
            between_24s = buffer[last_start + 1:last_end]

            if between_24s:
                print(f"[Producer] Sending: {between_24s}")
                q_out.put(between_24s)

            buffer = buffer[last_end:]  # truncate old part

        time.sleep(0.1)

def processor_fn(q_in, q_out, note_density_to_component_count_recommendation, pooled_scoring_df, control_mappings):
    while True:
        try:
            bar = q_in.get(timeout=1)
            binary_recommendation_dict, mapped_binary_recommendation_dict, bar, bar_duration, bar_keynote, density_class_present = run_recommendation_algorithm(bar, 
                                                                                                                                                                note_density_to_component_count_recommendation, 
                                                                                                                                                                pooled_scoring_df, 
                                                                                                                                                                control_mappings)
            print(f"[Processor] Processed: {bar} → {binary_recommendation_dict}")
            q_out.put(binary_recommendation_dict)
            q_in.task_done()
        except queue.Empty:
            time.sleep(0.05)

def start_pipeline(producer_fn, processor_fn,
                   poll_interval=0.1, max_qsize=10000):

    # Start by Performing the score pooling
    run_pooled_scoring()

    # Set the new input directory
    warnings.filterwarnings("ignore")
    input_dir = 'C:/Users/User/NextoGroove/inputs'
    os.chdir(input_dir)

    # Read the Inputs Needed For Recommendation
    note_density_to_component_count_recommendation, pooled_scoring_df, control_mappings = read_inputs()
    
    # Queues between stages
    q1 = queue.Queue(maxsize=max_qsize)
    q2 = queue.Queue(maxsize=max_qsize)

    # Launch threads with the queues
    threading.Thread(target=producer_fn, args=(q1,), daemon=True).start()
    threading.Thread(target=processor_fn, args=(q1, q2, note_density_to_component_count_recommendation, pooled_scoring_df, control_mappings), daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down.")

if __name__ == "__main__":
    start_pipeline(producer_fn, processor_fn, consumer_fn)