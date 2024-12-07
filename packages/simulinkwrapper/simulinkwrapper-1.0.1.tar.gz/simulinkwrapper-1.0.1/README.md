# SimulinkWrapper
SimulinkWrapper is a simple Python wrapper around Simulink that allows one to simulate an existing model in Simulink from Python. This is particularly useful for control systems design and implementation, as the control algorithms can then be implemented in Python, while the plant model is run by Simulink. This way, custom control systems making use of powerful Python libraries (e.g. machine learning libraries) can be tested on Simulink models. This frees the designer from having to devise a way to model complicated systems in Python (e.g. using nonlinear state-space models).

Keep in mind that this package uses the [Matlab-Python engine](https://github.com/mathworks/matlab-engine-for-python) to communicate with Matlab. The engine will have to be installed manually, as the version to install depends on the Matlab version used to obtain the Simulink models and run the simulations.

# Installation

## Using pip
The package may be installed using pip:

```
pip install simulinkwrapper
```

## Using git
Alternatively, clone the repository:

```
git clone https://github.com/MiguelLoureiro98/simulinkwrapper.git
```

And then move into the cloned repository to install it locally:

```
cd simulinkwrapper
pip install .
```

Development dependencies can be installed by typing:

```
pip install .[dev]
```

# Documentation
A dedicated website hosting the documentation will be released soon.

# Licence
This project is licenced under the [Apache 2.0 Licence](LICENSE).
