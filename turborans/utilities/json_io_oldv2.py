import os
import json
from bayes_opt.logger import JSONLogger
from collections import defaultdict
import logging


class newJSONLogger(JSONLogger):
    """JSONLogger subclass that appends to an existing log file instead of overwriting it.
    
    In bayes_opt v2.x, JSONLogger.__init__ accepts a `reset` parameter.
    Passing reset=False makes it append to any existing file, which is the
    behaviour the original newJSONLogger was trying to achieve by bypassing
    the parent __init__ entirely.
    """
    def __init__(self, path):
        path = path if path.endswith(".json") else path + ".json"
        # reset=False → append to existing file (preserves history across calls)
        super().__init__(path=path, reset=False)


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
