import pm4py
import pandas as pd
from math import log2, ceil, log10


def load_data(file_path):
    xes_file = pm4py.read_xes(file_path)
    return xes_file


def xes_to_df(event_log_xes):
    event_log_xes = pm4py.convert_to_dataframe(event_log_xes)
    event_log_xes = event_log_xes[['case:concept:name', 'concept:name', 'time:timestamp']]
    event_log_df = pm4py.format_dataframe(event_log_xes, case_id='case:concept:name', activity_key='concept:name',
                                          timestamp_key='time:timestamp')

    return event_log_df


def print_num_cases_and_num_trace_variants(event_log, event_log_name):
    number_cases_n = event_log['case:concept:name'].nunique()

    event_log_sorted = event_log.sort_values(by=['case:concept:name', 'time:timestamp'])
    trace_variants = event_log_sorted.groupby('case:concept:name')['concept:name'].apply(
        lambda x: ' -> '.join(x)).reset_index()
    trace_variants = trace_variants.rename(columns={"concept:name": "trace variant"})
    trace_variants_occurences = trace_variants['trace variant'].value_counts().reset_index()

    print(f"Number of cases for {event_log_name}: {number_cases_n}")
    print(f"Number of trace variants for {event_log_name}: {trace_variants_occurences.shape[0]}")
    print()


def zeta_tv(event_log):
    event_log_sorted = event_log.sort_values(by=['case:concept:name', 'time:timestamp'])
    trace_variants = event_log_sorted.groupby('case:concept:name')['concept:name'].apply(lambda x: '<' + ', '.join(x)
                                                                                                   + '>').reset_index()
    trace_variants_log = trace_variants.rename(columns={"concept:name": "specie"})
    trace_variants_log = trace_variants_log.drop(columns=['case:concept:name'])

    trace_variants_log = trace_variants_log['specie'].value_counts().reset_index()
    trace_variants_log.columns = ['specie', 'count']

    return trace_variants_log


def zeta_act(event_log):
    event_log = event_log.drop(columns=['case:concept:name', 'time:timestamp', '@@case_index', '@@index'])
    activities_log = event_log['concept:name'].value_counts().reset_index()
    activities_log.columns = ['specie', 'count']

    return activities_log


def zeta_df(event_log):
    event_log_sorted = event_log.sort_values(by=['case:concept:name', 'time:timestamp']).reset_index()
    event_log_sorted = event_log_sorted.drop(columns=['index'])
    directed_followed = []

    for i in range(event_log_sorted.shape[0]):
        if i < event_log_sorted.shape[0] - 1 and event_log_sorted['@@case_index'][i] == \
                event_log_sorted['@@case_index'][i + 1]:
            directed_followed.append((event_log_sorted['concept:name'][i], event_log_sorted['concept:name'][i + 1]))
        else:
            directed_followed.append((event_log_sorted['concept:name'][i], None))

    for i in range(event_log_sorted.shape[0]):
        if i == 0:
            directed_followed.append((None, event_log_sorted['concept:name'][i]))

        elif i > 0 and event_log_sorted['@@case_index'][i] != event_log_sorted['@@case_index'][i - 1]:
            directed_followed.append((None, event_log_sorted['concept:name'][i]))

    directed_followed_log = pd.DataFrame({'specie': directed_followed})
    directed_followed_log = directed_followed_log['specie'].value_counts().reset_index()
    directed_followed_log.columns = ['specie', 'count']

    return directed_followed_log


def zeta_t1(event_log):
    event_log_sorted = event_log.sort_values(by=['time:timestamp'])

    event_log_sorted['next_timestamp'] = event_log_sorted.groupby('case:concept:name')['time:timestamp'].shift(-1)
    event_log_sorted['duration'] = event_log_sorted['next_timestamp'] - event_log_sorted['time:timestamp']

    duration_lambda1_log = event_log_sorted.dropna(subset=['duration'])

    duration_lambda1_log['duration_min'] = duration_lambda1_log['duration'].apply(
        lambda x: ceil(x.total_seconds() / 60))
    duration_lambda1_log = duration_lambda1_log.drop(columns=['case:concept:name', 'time:timestamp',
                                                              'duration', '@@case_index', '@@index'])
    duration_lambda1_log = pd.DataFrame({'specie': duration_lambda1_log.apply(lambda row: (row['concept:name'],
                                                                                           row['duration_min']),
                                                                              axis=1)})
    duration_lambda1_log = duration_lambda1_log['specie'].value_counts().reset_index()

    return duration_lambda1_log


def zeta_t5(event_log):
    event_log_sorted = event_log.sort_values(by=['time:timestamp'])

    event_log_sorted['next_timestamp'] = event_log_sorted.groupby('case:concept:name')['time:timestamp'].shift(-1)
    event_log_sorted['duration'] = event_log_sorted['next_timestamp'] - event_log_sorted['time:timestamp']

    duration_lambda5_log = event_log_sorted.dropna(subset=['duration'])

    duration_lambda5_log['duration_min'] = duration_lambda5_log['duration'].apply(
        lambda x: 5 * ceil((x.total_seconds() / 60) / 5))
    duration_lambda5_log = duration_lambda5_log.drop(columns=['case:concept:name', 'time:timestamp',
                                                              'duration', '@@case_index', '@@index'])
    duration_lambda5_log = pd.DataFrame({'specie': duration_lambda5_log.apply(lambda row: (row['concept:name'],
                                                                                           row['duration_min']),
                                                                              axis=1)})
    duration_lambda5_log = duration_lambda5_log['specie'].value_counts().reset_index()

    return duration_lambda5_log


def zeta_t30(event_log):
    event_log_sorted = event_log.sort_values(by=['time:timestamp'])

    event_log_sorted['next_timestamp'] = event_log_sorted.groupby('case:concept:name')['time:timestamp'].shift(-1)
    event_log_sorted['duration'] = event_log_sorted['next_timestamp'] - event_log_sorted['time:timestamp']

    duration_lambda30_log = event_log_sorted.dropna(subset=['duration'])

    duration_lambda30_log['duration_min'] = duration_lambda30_log['duration'].apply(
        lambda x: 30 * ceil((x.total_seconds() / 60) / 30))
    duration_lambda30_log = duration_lambda30_log.drop(columns=['case:concept:name', 'time:timestamp',
                                                                'duration', '@@case_index', '@@index'])
    duration_lambda30_log = pd.DataFrame({'specie': duration_lambda30_log.apply(lambda row: (row['concept:name'],
                                                                                             row['duration_min']),
                                                                                axis=1)})
    duration_lambda30_log = duration_lambda30_log['specie'].value_counts().reset_index()

    return duration_lambda30_log


def zeta_te2(event_log):
    event_log_sorted = event_log.sort_values(by=['time:timestamp'])

    event_log_sorted['next_timestamp'] = event_log_sorted.groupby('case:concept:name')['time:timestamp'].shift(-1)

    event_log_sorted['duration'] = event_log_sorted['next_timestamp'] - event_log_sorted['time:timestamp']

    duration_te2_log = event_log_sorted.dropna(subset=['duration'])

    duration_te2_log['duration_te2'] = duration_te2_log['duration'].apply(
        lambda x: 2*ceil(log2(x.total_seconds() / 60)) if x.total_seconds() != 0 else 0)

    duration_te2_log = duration_te2_log.drop(columns=['case:concept:name', 'time:timestamp',
                                                              'duration', '@@case_index', '@@index'])
    duration_te2_log = pd.DataFrame({'specie': duration_te2_log.apply(lambda row: (row['concept:name'],
                                                                                           row['duration_te2']),
                                                                              axis=1)})

    duration_te2_log = duration_te2_log['specie'].value_counts().reset_index()

    return duration_te2_log


def calculate_S_obs(zeta_specie_count):
    return zeta_specie_count['count'].shape[0]


def calculate_Q1(zeta_specie_count):
    return zeta_specie_count[zeta_specie_count['count'] == 1].shape[0]


def calculate_Q2(zeta_specie_count):
    return zeta_specie_count[zeta_specie_count['count'] == 2].shape[0]


def calculate_S_est(zeta_specie_count):
    S_obs = calculate_S_obs(zeta_specie_count)
    Q1 = calculate_Q1(zeta_specie_count)
    Q2 = calculate_Q2(zeta_specie_count)
    t = zeta_specie_count['count'].sum()

    if Q2 > 0:
        S_est = S_obs + (1 - 1 / t) * ((Q1 ** 2) / (2 * Q2))

    else:
        S_est = S_obs + (1 - 1 / t) * (Q1 - (Q1 - 1)) / 2

    return int(S_est)


def calculate_Cov_obs(zeta_specie_count):
    Q1 = calculate_Q1(zeta_specie_count)
    Q2 = calculate_Q2(zeta_specie_count)
    n = zeta_specie_count['count'].sum()

    if Q1 == 0 and Q2 == 0:
        return 1.0

    cov_obs = (1 - 1 / n) - ((Q1 / n) * (((n - 1) * Q1) / ((n - 1) * Q1 + 2 * Q2)))

    return round(cov_obs, 3)


def calculate_Com_obs(zeta_specie_count):
    S_obs = calculate_S_obs(zeta_specie_count)
    S_est = calculate_S_est(zeta_specie_count)

    return round(S_obs / S_est, 3)


def calculate_lg(zeta_specie_count, g):
    n = 1050
    S_obs = calculate_S_obs(zeta_specie_count)
    S_est = calculate_S_est(zeta_specie_count)
    Q1 = calculate_Q1(zeta_specie_count)
    Q2 = calculate_Q2(zeta_specie_count)
    Com_obs = calculate_Com_obs(zeta_specie_count)

    if Q1 == 0 and Q2 == 0:
        return None

    denominator = 2 * Q2 / ((n - 1) * Q1 + 2 * Q2)
    denominator = log10(1 - denominator)

    if g > Com_obs:
        numerator = (n / (n - 1)) * (2 * Q2 / (Q1 ** 2)) * (g * S_est - S_obs)
        numerator = log10(1 - numerator)

        lg = numerator / denominator
        lg = int(ceil(lg))

    else:
        lg = None

    return lg


if __name__ == "__main__":
    # file_path_BPI_2012 = "C:/Users/bijao/PycharmProjects/Process_Mining_Project/BPI_Challenge_2012.xes"
    file_path_sepsis = "Sepsis Cases - Event Log.xes"

    # xes_file_BPI_2012 = load_data(file_path_BPI_2012)
    xes_file_sepsis = load_data(file_path_sepsis)

    # event_log_BPI_2012 = xes_to_df(xes_file_BPI_2012)
    event_log_sepsis = xes_to_df(xes_file_sepsis)

    # print_num_cases_and_num_trace_variants(event_log_BPI_2012, "BPI 2012")
    print_num_cases_and_num_trace_variants(event_log_sepsis, "Sepsis Cases")

    species_functions = [zeta_act, zeta_df, zeta_tv, zeta_t1, zeta_t5, zeta_t30, zeta_te2]
    measures_functions = [calculate_S_obs, calculate_S_est, calculate_Q1, calculate_Q2, calculate_Com_obs,
                          calculate_Cov_obs, calculate_lg]
    measures_names = ["S_obs", "S_est", "Q1", "Q2", "Com_obs", "Cov_obs", "l"]
    g_values = [0.8, 0.9, 0.95, 0.99]

    species_logs = {}
    species_measures = {}

    for func in species_functions:
        zeta_log = func(event_log_sepsis)
        species_logs[f"{func.__name__}"] = zeta_log
        species_measures[f"{func.__name__}"] = {}

        for name, measure in zip(measures_names, measures_functions):
            if measure != calculate_lg:
                species_measures[f"{func.__name__}"][f"{name}"] = measure(species_logs[f"{func.__name__}"])

            else:
                for g in g_values:
                    species_measures[f"{func.__name__}"][f"{name}_{g}"] = \
                        measure(species_logs[f"{func.__name__}"], g)

    results = pd.DataFrame.from_dict(species_measures, orient='index')
    print(results)

