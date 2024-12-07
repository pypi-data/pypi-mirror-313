#   Copyright 2024 Miguel Loureiro

#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at

#       http://www.apache.org/licenses/LICENSE-2.0

#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
This module contains classes to help users simulate dynamical systems modelled in Simulink.

Classes
-------
Sim
    Run a simulation in Simulink.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matlab.engine

class Sim(object):
    """
    Simulator class.

    This class can be used to simulate Simulink models and save the results to a file. \
    Several simulation settings can be changed by the user, such as the final simulation \
    time, the minimum and maximum time steps, and whether to use a fixed-step or a \
    variable-step solver. \
    Controllers, state estimators, parameter-varying systems and noise generation are also supported. 

    Parameters
    ----------
    model_name : str
        Name of the Simulink model. No need to include the extension.

    model_path : str
        Path to the model.

    measured_variables : list[str]
        List containing the names of every measured variable. 
        These must correspond to Simulink "To Workspace" block names.

    controlled_variables : list[str], optional
        List containing the names of every controlled variable. 
        These must correspond to Simulink "Constant" block names.

    controller : any, optional
        Control system (class). Must have a 'Ts' attribute (sampling time).
        Its __call__ method should receive measurements or state estimates as inputs, \
        as well as reference signals (optional), and return an array of control actions.

    state_estimator : any, optional
        State estimator (class). Its __call__ method should receive measurements, and \
        return an array of state estimates to be fed to the controller.

    varying_parameters : dict[str, np.ndarray], optional
        A dictionary containing the names of time-varying parameters and \
        their respective arrays of values. The names must correspond to those \
        of Simulink "Constant" blocks.

    reference_signals : np.ndarray, optional
        An (n, t) array of reference signals, where n is the number of reference \
        signals, and t is the number of time steps specified for this simulation.

    reference_lookahead : int, default=1
        Parameter that controls how many future reference values are passed to the controller.

    stop_time : int | float, default=10.0
        Simulation stop time.

    time_step : int | float, default=0.001
        Simulation time step. Will be interpreted as a fixed time step if \
        a fixed-step solver is specified, and as the minimum time step if \
        a variable-step solver is selected.

    max_step : int | float, default=0.01
        Maximum allowable time step for variable-step simulations.
        Ignored if a fixed-step solver is selected.

    solver_type : {"var_step", "fixed_step"}, str, default="var_step"
        Solver type.

    Methods
    -------
    run()
        Run a simulation.

    plot(variable: str, reference_index: int | None=None, height: float=10.0, width: float=10.0, title: str="Results")
        Plot simulation results.

    save(file_path: str, format: str="csv")
        Save simulation results to a file.

    disconnect()
        End Matlab engine session.

    set_controller(new_controller: any)
        Change the controller.

    set_state_estimator(new_state_estimator: any)
        Change the state estimator

    Raises
    ------
    ValueError
        If 'solver_type' is neither 'var_step' nor 'fixed_step'.

    Warning
    -------
    The model's solver type definitions must be compatible with those specified when \
    instatiating the class (i.e. fixed- or variable-step solvers must also be specified \
    in the Simulink model).
    """

    def __init__(self,
                 model_name: str, 
                 model_path: str,
                 measured_variables: list[str],
                 controlled_variables: list[str] | None=None,
                 controller: any=None,
                 state_estimator: any=None,
                 varying_parameters: dict[str, np.ndarray] | None=None,
                 reference_signals: np.ndarray | None=None,
                 reference_lookahead: int=1,
                 noise_signals: dict[str, np.ndarray] | None=None,
                 stop_time: int | float=10.0,
                 time_step: int | float=0.001,
                 max_step: int | float=0.01,
                 solver_type: str="var_step") -> None:
        
        self._model_name = model_name;
        self._model_path = model_path;
        self._measurements = measured_variables;
        self._control_vars = controlled_variables;
        self._controller = controller;
        self._state_estimator = state_estimator;
        self._varying_params = varying_parameters;
        self._refs = reference_signals;
        self._lookahead = reference_lookahead;
        self._noise = noise_signals;

        if(solver_type == "var_step"):

            self._step_type = "MinStep";
        
        elif(solver_type == "fixed_step"):

            self._step_type = "FixedStep";
        
        else:

            raise ValueError("Please choose either a fixed-step or a variable-step solver.");

        self._settings = {"StopTime": stop_time, self._step_type: time_step};

        if(solver_type == "var_step"):

            self._settings["MaxStep"] = max_step;

        self._eng = matlab.engine.start_matlab();
        self._sim_data = None;

        #TODO: Add variable step solver option (if var_step=True [default], "time_step" is assigned to the MinStep setting)

        return;

    def run(self) -> pd.DataFrame:
        """
        Run a simulation.

        This method can be used to run a complete simulation of a Simulink model.

        Returns
        -------
        results : pd.DataFrame
            Simulation results.
        """

        self._reset();
        self._config_sim();
        self._check_controller();

        time_index = 0;
        measurement_data = {var: 0 for var in self._measurements};

        for var in self._measurements:
            
            self._eng.eval(f"{var} = out.{var};", nargout=0);
            measurement_data[var] = self._eng.workspace[f"{var}"];
            
            if(self._noise is not None):

                if(var in self._noise.keys()):
                    
                    measurement_data[var] += self._noise[var][time_index];

        if(self._varying_params is not None):

            for name, value in self._varying_params.items():

                self._eng.eval(f"set_param('{self._model_name}/{name}', 'Value', '{value[time_index]}')", nargout=0);

        if(self._controller is None):

            next_sample = self._settings["FixedStep"];
            #next_sample = self._settings["StopTime"] + self._settings["FixedStep"]; #! Change this -> fixed step only.

        else:

            next_sample = self._controller.Ts; #! Controller must have a Ts attribute or property.

        measurement_vals = np.array([val for val in measurement_data.values()]);

        if(self._state_estimator is not None):

            controller_inputs = self._state_estimator(measurement_vals); #! State estimator must override the call method.

        else:

            controller_inputs = measurement_vals;

        if(self._refs is not None):

            control_actions = self._controller(controller_inputs, self._refs[:, time_index:time_index+self._lookahead]); #! Controller must override the call method.
        
        else:

            control_actions = self._controller(controller_inputs);

        if(self._control_vars is not None):

            for control_var, u in zip(self._control_vars, control_actions):

                self._eng.eval(f"set_param('{self._model_name}/{control_var}', 'Value', '{u.item()}')", nargout=0); #! Controllers must return an array!

        time_index += 1;

        while(self._eng.eval(f"get_param('{self._model_name}', 'SimulationStatus');", nargout=1) != "stopped"):

            #print(time_index);

            if(self._varying_params is not None):

                for name, value in self._varying_params.items():

                    self._eng.eval(f"set_param('{self._model_name}/{name}', 'Value', '{value[time_index]}')", nargout=0);

            if(self._eng.eval(f"get_param('{self._model_name}', 'SimulationTime')", nargout=1) >= next_sample and self._control_vars is not None):

                #TODO: Add logs or progress bar to report on simulation progress.

                for var in self._measurements:

                    self._eng.eval(f"{var} = out.{var}(length(out.{var}));", nargout=0);
                    measurement_data[var] = self._eng.workspace[f"{var}"];
                
                    if(self._noise is not None):

                        if(var in self._noise.keys()):
                    
                            measurement_data[var] += self._noise[var][time_index];

                if(self._state_estimator is not None):

                    controller_inputs = self._state_estimator(measurement_vals); #! State estimator must override the call method.

                else:

                    controller_inputs = measurement_vals;

                if(self._refs is not None):

                    control_actions = self._controller(controller_inputs, self._refs[:, time_index:time_index+self._lookahead]); #! Controller must override the call method.
        
                else:

                    control_actions = self._controller(controller_inputs);

                for control_var, u in zip(self._control_vars, control_actions):

                    self._eng.eval(f"set_param('{self._model_name}/{control_var}', 'Value', '{u.item()}')", nargout=0);

                next_sample += self._controller.Ts; #! Controller must have a Ts attribute or property.

            self._eng.eval(f"set_param('{self._model_name}', 'SimulationCommand', 'continue', 'SimulationCommand', 'pause')", nargout=0);
            time_index += 1;

        vars_list = self._measurements; #+ self._control_vars;

        for var in vars_list:

            self._eng.eval(f"{var} = out.{var};", nargout=0);

        final_data = {var: np.ravel(np.asarray(self._eng.workspace[f"{var}"])) for var in vars_list};

        self._eng.eval("t = out.tout;", nargout=0);
        final_data["t"] = np.ravel(np.asarray(self._eng.workspace["t"]));

        self._sim_data = pd.DataFrame(final_data);

        return self._sim_data;

    def plot(self, variable: str, reference_index: int | None=None, height: float=10.0, width: float=10.0, title: str="Results") -> None:
        """
        Plot simulation results.

        This method can be used to visualise simulation results.

        Parameters
        ----------
        variable : str
            Variable to plot (could be a controlled variable).

        reference_index : int | None, optional
            Index of the reference signal to plot (starts from zero).

        height : float, default=10.0
            Figure height.

        width : float, default=10.0
            Figure width.

        title : str, default="Results"
            Plot title.
        """

        fig, ax = plt.subplots();
        fig.set_size_inches(width, height);

        if(reference_index is not None and self._refs is not None):
            
            ax.plot(self._sim_data["t"], self._refs[reference_index], label="Reference");
        
        ax.plot(self._sim_data["t"], self._sim_data[variable], label=variable);
        ax.set_title(title);
        ax.set_xlabel("t (s)");
        ax.set_ylabel(variable);
        ax.grid(visible=True);
        xfactor = 1.0005;
        yfactor = 1.05;

        if(reference_index is not None):

            minlim = np.fmin(self._sim_data[variable].min(), self._refs[reference_index].min());
            maxlim = np.fmax(self._sim_data[variable].max(), self._refs[reference_index].max());
        
        else:

            minlim = self._sim_data[variable].min();
            maxlim = self._sim_data[variable].max();

        plt.xlim([self._sim_data["t"].min() * xfactor, self._sim_data["t"].max() * xfactor]);
        plt.ylim([minlim * yfactor, maxlim * yfactor]);
        plt.legend();
        plt.show();

        return;

    def save(self, file_path: str, format: str="csv") -> None:
        """
        Save simulation results to a file.

        This method can be used to save simulation results to a file. \
        CSV, pickle, parquet, and feather files are supported.

        Parameters
        ----------
        file_path : str
            Path to the file where the results should be stored.

        format : {"csv", "pickle", "parquet", "feather"}, str, default="csv"
            File format.

        Raises
        ------
        ValueError
            If an unsupported file format is specified.
        """

        supported_formats = ["csv", "pickle", "parquet", "feather"];
        
        if(format not in supported_formats):

            raise ValueError("Format not supported.");
    
        string = f"{file_path}.{format}";

        if(format == "csv"):

            self._sim_data.to_csv(string, index=False);

        elif(format == "pickle"):

            self._sim_data.to_pickle(string);

        elif(format == "parquet"):

            self._sim_data.to_parquet(string);

        else:

            self._sim_data.to_feather(string);

        return;

    def disconnect(self) -> None:
        """
        Exits the Matlab Engine.

        This method must be called whenever the user does not intend to run more simulations using a class instance.
        """

        self._eng.quit();
    
        return;

    def set_controller(self, new_controller: any) -> None:
        """
        Change the system's controller.

        This method can be used to change the system's controller either before or after \
        a simulation has been run. This can be useful to run multiple simulations with different \
        controllers (e.g. for tuning purposes).
        Note that changing controllers while the simulation is running is not supported.

        Parameters
        ----------
        new_controller : any
            New controller.
        """

        self._controller = new_controller;

        return;

    def set_state_estimator(self, new_state_estimator: any) -> None:
        """
        Change the system's state estimator.

        This method can be used to change the system's state estimator either before or after \
        a simulation has been run. This can be useful to run multiple simulations with different \
        state estimators (e.g. for tuning purposes).
        Note that changing state estimators while the simulation is running is not supported.

        Parameters
        ----------
        new_state_estimator : any
            New state estimator.
        """

        self._state_estimator = new_state_estimator;

        return;

    def _config_sim(self) -> None:
        """
        Configure simulation settings.
        """

        self._eng.eval(f"model = '{self._model_path}';", nargout=0);
        self._eng.eval("load_system(model);", nargout=0);

        for (parameter, value) in self._settings.items():

            self._eng.eval("set_param('{}', '{}', '{}');".format(self._model_name, parameter, value), nargout=0);

        self._eng.eval("set_param('{}', 'SimulationCommand', 'start', 'SimulationCommand', 'pause');".format(self._model_name), nargout=0);

        return;

    def _reset(self) -> None:
        """
        Reset simulation data.
        """

        self._sim_data = None;

        return;

    def _check_controller(self) -> None:
        """
        Use dummy controller for open-loop simulations.
        """

        if(self._controller is None and self._refs is not None and self._control_vars is not None and len(self._control_vars) == self._refs.shape[0]):

            self._controller = _dummy_controller(self._settings[self._step_type]);

        return;

#class RLSim(object):

#    def __init__(self) -> None:

#        return;

class _dummy_controller(object):
    """
    Create a dummy controller for open-loop simulations.
    """

    def __init__(self, time_step: float) -> None:

        self.Ts = time_step;

        return;

    def __call__(self, inputs: np.ndarray, refs: np.ndarray=np.array([0])) -> np.ndarray:

        return refs;