import json
import logging
import os

import pandas as pd
import numpy as np
import random

from bayes_opt import BayesianOptimization
from bayes_opt import acquisition

from sklearn.gaussian_process.kernels import Matern

from scipy.stats import qmc

from turborans.utilities.json_io import load_json, write_json, newJSONLogger, load_history_loss_log
from turborans.utilities.kernel import derive_length_scales, get_optimizer
from turborans.utilities.control import reset
from turborans.utilities.checks import validate_settings


def _load_logs(optimizer, log_path):
    """Reads a history.json file (one JSON object per line) and registers
    each point with the optimizer. Replaces the removed bayes_opt.load_logs."""
    with open(log_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            params = entry.get("params", {})
            target = entry.get("target", None)
            if params and target is not None:
                try:
                    optimizer.register(params=params, target=target)
                except Exception:
                    pass  # Skip duplicate points silently


def _make_acquisition(kind, kappa, xi):
    """Returns the appropriate acquisition function object.
    Replaces the removed UtilityFunction class."""
    kind = kind.lower()
    if kind == "ucb":
        return acquisition.UpperConfidenceBound(kappa=kappa)
    elif kind == "ei":
        return acquisition.ExpectedImprovement(xi=xi)
    elif kind == "poi":
        return acquisition.ProbabilityOfImprovement(xi=xi)
    else:
        raise ValueError(f"Unknown acquisition kind: '{kind}'. Use 'ucb', 'ei', or 'poi'.")


class optimizer():
    """ Main turbo-RANS optimizer object.
    This optimizer object is designed to be the primary I/O for turbo-RANS. The json_mode setting is important; it indicates
    a global mode for this object. If this object is acting in json_mode = False, then it is designed to not save progress
    and simply run within a single python script. json_mode = True is recommended for the majority of applications, where
    saving progress is important. 
    

    Attributes
    ----------
    settings : dict
        a dictionary of settings for the optimizer.
        settings and current defaults:
                'force_restart': False,
                'start_with_defaults_if_given': True,
                'json_mode': True,
                'n_samples': 10,
                'random_state': None,
                'bo_utility_kind': 'ucb',
                'bo_kappa': 2.0,
                'bo_xi': 0.1,
                'kernel_relative_lengthscale': 0.1,
                'kernel_relative_lengthscale_bounds': [1E-2,1E1],
                'kernel_nu': 5/2

    coeffs : dict
        coefficient dictionary
    directory : str
        location for any file I/O
    default_coeffs_given : boolean
        flag to indicate whether or not default coefficients are provided in coeffs
    bayesian_optimizer : bayesian_optimization library object
    mode : str
        current mode for next recommendation, 'default_coefficient', 'sampling_paramerers', or 'bayesian_optimization'
    iter : int
        current optimization iteration number, equal to number of points in history
    samples : array
        sobol-sequence generated samples
    samples_generated: boolean
        flag to indicate whether sobol samples have been generated
    database : dict
        valid only for json_mode: False, dictionary containing information for summary at end of optimization
    database_created : boolean
        flag to indicate whether database has been generated
    
    Methods
    -------
    suggest(mode = None)
        gives the next suggestion. Mode is inferred if mode == None. If you attempt to set mode to bayesian_optimization with,
        insufficient points available, an error will be thrown.
    register_score(score, coefficients = None)
        registers the score with the underlying bayesian_optimization object. If coefficients = None, the coefficients in suggestion.json 
        are used as the coefficients. This means that in non-json mode, the coefficients argument must be provided.
    """
    settings = {
                'force_restart': False,
                'start_with_defaults_if_given': True,
                'json_mode': True,
                'n_samples': 10,
                'random_state': None,
                'bo_utility_kind': 'ucb',
                'bo_kappa': 2.0,
                'bo_xi': 0.1,
                'kernel_relative_lengthscale': 0.1,
                'kernel_relative_lengthscale_bounds': [1E-2,1E1],
                'kernel_nu': 5/2
                }

    def __init__(self,
                 coeffs = None, 
                 turborans_directory=os.getcwd(), 
                 settings = 'default'):
        """
        Parameters
        ----------
        coeffs : dict, optional
            coefficient dictionary, containing bounds and defaults. e.g.
            {
                "default": {
                    "x": -0.5,
                    "y": 2
                },
                "bounds": {
                    "x": [
                        -1,
                        1
                    ],
                    "y": [
                        -10,
                        10
                    ]
                }
            }
            If coeffs is not given or coeffs = None, the coefficients are read from coefficients.json (this required json_mode = True). 
            coeffs can be specified in either json_mode = True or False. The coefficients.json file will only be read
            if coeffs = None, and json_mode = True.
        turborans_directory : str, optional
            directory for file I/O. If not given, the current directory will be used.
        
        settings : str or dict, optional
            if not given, or equal to 'default', default settings will be used. If you wish to change the settings, you must supply a dict
            with the settings that should be changed. If a settings.json file exists in the directory, this argument will be ignored.
            Default settings:
                    {
                        'force_restart': False,
                        'start_with_defaults_if_given': True,
                        'json_mode': True,
                        'n_samples': 10,
                        'random_state': None,
                        'bo_utility_kind': 'ucb',
                        'bo_kappa': 2.0,
                        'bo_xi': 0.1,
                        'kernel_relative_lengthscale': 0.1,
                        'kernel_relative_lengthscale_bounds': [1E-2,1E1],
                        'kernel_nu': 5/2
                    }
        """
        
        self.coeffs = coeffs
        self.directory = turborans_directory

        # Attempt to find settings.json file. If not found, update any non-default settings supplied in the init argument.
        if os.path.exists(os.path.join(self.directory,"settings.json")):
            json_settings = load_json(self.directory, "settings.json")
            self.settings.update(json_settings)
        else:
            if settings != 'default':
                self.settings.update(settings)

        # Check if settings are valid.
        validate_settings(self)

        # If we're in json_mode, look for coefficients.json if coeffs are not provided in init argument.
        # If they are provided, write them to a json file.
        if self.settings['json_mode']:
            if self.coeffs is None:
                self.coeffs = load_json(self.directory, "coefficients.json")
            else:
                write_json(self.directory, self.coeffs, "coefficients.json")
            write_json(self.directory, self.settings, "settings.json")
        
        if 'default' in self.coeffs:
            self.default_coeffs_given = True
        else: 
            self.default_coeffs_given = False

        # Reset optimizer if force_restart is True.
        if self.settings['force_restart']: 
            reset(self.directory)

        # Get bayesian_optimizer based on current settings.
        if not self.settings['json_mode']:
            self._get_bayesian_optimizer()
                    
        self.samples_generated = False
        self.database_created = False

    def _condition_bayesian_optimizer(self):
        """Conditions the bayesian optimizer on history.json if we're in json_mode."""
        history_path = os.path.join(self.directory, "history.json")
        if os.path.exists(history_path):
            try:
                _load_logs(self.bayesian_optimizer, history_path)
            except Exception:
                raise LookupError(
                    f'Could not load history from {history_path}, even though it exists.\n'
                    f'The number of coefficients might have changed.'
                )
        else:
            logging.info(f'No history file exists at {history_path}, assumed to be starting fresh')
    
    def _infer_current_iteration(self):
        """Infer the current iteration number based on the number of registered points."""
        iter = len(self.bayesian_optimizer._space)
        self.iter = iter
        return iter
    
    def _set_mode(self, mode=None):
        """Set the optimizer mode based on iteration number."""
        self._infer_current_iteration()
        if mode is None:
            if self.iter == 0:
                if self.default_coeffs_given and self.settings['start_with_defaults_if_given']:
                    self.mode = 'default_coefficient'
                else:
                    self.mode = 'sampling_parameters'
            elif self.iter <= self.settings['n_samples']:
                self.mode = 'sampling_parameters'
            else:
                self.mode = 'bayesian_optimization'
        else:
            self.mode = mode

    def _generate_samples(self, n_samples):
        """Generates sobol-sequence samples for each coefficient."""
        qrng = qmc.Sobol(d=len(self.coeffs['bounds'].keys()), seed=self.settings['random_state'])
        self.samples = qrng.random(n=2**(int(np.log2(n_samples))+1))
        for i, bounds in enumerate(self.coeffs['bounds'].values()):
            self.samples[:,i] = bounds[0] + self.samples[:,i]*(bounds[1]-bounds[0])
        self.samples_generated = True

    def _suggest_default(self):
        """Returns the default coefficients provided."""
        return self.coeffs['default']
           
    def _suggest_sample(self, index):
        """Returns a sobol-sequence sample for each coefficient."""
        if index >= len(self.samples):
            logging.info(f'Generating more samples, since index {index} is beyond len(samples) = {len(self.samples)}')
            self._generate_samples(len(self.samples)+1)
        suggestion = dict(zip(self.coeffs['bounds'].keys(), self.samples[index]))
        return suggestion

    def _suggest_bayesian_optimization(self):
        """Suggests a point using the bayesian optimizer."""
        if self.iter < 5: 
            raise ValueError("Bayesian optimizer should not be run without at least 5 initial samples")

        acq_function = _make_acquisition(
            kind=self.settings['bo_utility_kind'],
            kappa=self.settings['bo_kappa'],
            xi=self.settings['bo_xi'],
        )
        return self.bayesian_optimizer.suggest(acq_function)

    def suggest(self, mode=None):
        """Primary suggestion I/O method."""
        if self.settings['json_mode']:
            return self._suggest_to_json(mode)
        else: 
            return self._suggest(mode)
        
    def _suggest_to_json(self, mode):
        """Writes suggestion to suggestion.json."""
        self._get_bayesian_optimizer()
        suggestion = self._suggest(mode)
        logging.info(f'Suggesting to json')
        write_json(self.directory, suggestion, "suggestion.json")
        write_json(self.directory, {"mode": self.mode}, "mode.json")
        return suggestion
        
    def _suggest(self, mode):
        """Core suggestion method."""
        self._set_mode(mode)
        logging.info(f'Suggesting new value, current mode: {self.mode}')

        if self.mode == 'default_coefficient':
            return self._suggest_default()
        elif self.mode == 'sampling_parameters':
            if not self.samples_generated:
                self._generate_samples(self.settings['n_samples'])
            return self._suggest_sample(self.iter)
        else:
            return self._suggest_bayesian_optimization()

    def register_score(self, score, coefficients=None):
        """Primary score registration I/O method."""
        if coefficients is None:
            if not self.settings['json_mode']:
                raise ValueError('You must provide a corresponding suggestion to be registered, unless turbo-RANS is in json_mode')
            else:
                suggestion = load_json(self.directory, "suggestion.json")
                self._register_score_json(score, suggestion)
        else:
            if self.settings['json_mode']:
                self._register_score_json(score, coefficients)
            else:
                self._register_score(score, coefficients)
                self._update_database(score, coefficients)

    def _register_score_json(self, score, suggestion):
        """Registers the score and appends the result to history.json manually.
        subscribe/Events have been removed in bayes_opt v3.x, so we write the
        log entry directly after registering."""
        self._get_bayesian_optimizer()
        history_path = os.path.join(self.directory, "history.json")
        if not os.path.exists(history_path):
            logging.info(f'No history file exists at {history_path}, creating and registering first point')
        logging.info(f'Registering score in {history_path}')
        try:
            self._register_score(score, suggestion)
        except Exception:
            suggestion = {k: v + random.uniform(0.0000001, 0.000001) for k, v in suggestion.items()}
            logging.warning('Could not register score, maybe a duplicate point. Adding small random value to search point.')
            self._register_score(score, suggestion)

        # Manually append to history.json (replaces the old subscribe/Events pattern)
        entry = {"target": score, "params": suggestion}
        with open(history_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def _register_score(self, score, suggestion):
        """Registers the score in the bayesian_optimizer object."""
        self.bayesian_optimizer.register(params=suggestion, target=score)

    def _update_database(self, score, coefficients):
        """Updates a database tracking optimization info. Only valid for json_mode = False."""
        if self.settings['json_mode'] is True:
            raise ValueError("update_database should only be used for non-json mode")

        if not self.database_created:
            self.database = {'iteration': [], 'mode': [], 'target': []}
            [self.database.update({key: []}) for key in coefficients.keys()]
            self.database_created = True
        self.database['iteration'].append(self.iter)
        self.database['mode'].append(self.mode)
        [self.database[key].append(value) for key, value in coefficients.items()]
        self.database['target'].append(score)

    def _get_bayesian_optimizer(self):
        self.bayesian_optimizer = get_optimizer(
            coeff_bounds=self.coeffs['bounds'],
            relative_lengthscale=self.settings['kernel_relative_lengthscale'],
            relative_lengthscale_bounds=self.settings['kernel_relative_lengthscale_bounds'],
            nu=self.settings['kernel_nu'],
            random_state=self.settings['random_state']
        )
        self._condition_bayesian_optimizer()
