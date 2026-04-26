import os
import json
from collections import defaultdict
import logging


class newJSONLogger:
    """Append-mode JSON logger for bayes_opt v3.x.

    In v3.x, JSONLogger and the Events/subscribe system have been removed.
    This class is now a plain helper that writes a JSON line to the history
    file. It is no longer used as a subscriber — bayes_io.py writes log
    entries directly after each register() call instead.
    
    Kept here for API compatibility in case it is referenced elsewhere.
    """
    def __init__(self, path):
        self._path = path if path.endswith(".json") else path + ".json"

    def log(self, target, params):
        """Append a single result entry to the log file."""
        entry = {"target": target, "params": params}
        with open(self._path, "a") as f:
            f.write(json.dumps(entry) + "\n")


def load_json(directory, filename):
    filename = os.path.join(directory, filename)
    with open(filename, "r") as j:
        data = json.load(j)
    return data


def write_json(directory, data, filename, append=False):
    filename = os.path.join(directory, filename)
    if append:
        with open(filename, "a") as outfile:
            outfile.write(json.dumps(data) + '\n')
    else:
        with open(filename, "w") as outfile:
            json.dump(data, outfile, indent=4)
    return filename


def load_history_line_by_line(directory, file):
    data = []
    filename = os.path.join(directory, file)
    with open(filename, "r") as j:
        for line in j:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data


def load_history_loss_log(directory, file):
    losses_dict = defaultdict(list)
    history = load_history_line_by_line(directory, file)
    keys = history[0].keys()
    for key in keys:
        if key == 'params':
            for param in history[0][key].keys():
                loss_list = [d[key][param] for d in history]
                losses_dict[param] = loss_list
        elif key == 'datetime':
            date_list = [d[key]['datetime'] for d in history]
            losses_dict[key] = date_list
        else:
            loss_list = [d[key] for d in history]
            losses_dict[key] = loss_list
    return losses_dict
