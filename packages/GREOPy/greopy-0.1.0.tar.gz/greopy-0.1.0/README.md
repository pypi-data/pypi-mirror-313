# General Relativistic Emitter-Observer problem Python algorithm (GREOPy)

## What GREOPy does

GREOPy is a Python library for calculating relativistic light rays sent by an emitter to a receiver in the presence of a gravitational field.
The emitter and receiver can move along arbitrary curves and the gravitational field can be described by a rotating, non-accelerating central mass.

This package is specifically dedicated for work in (relativistic) geodesy.
In classical geodesy, either a light signal's travel time or its bending angle (deviation from a straight line) is usually neglected because of the Earth's weak gravitational field and short light travel distance.
While these deviations and resulting observable uncertainties might be overshadowed by other effects with state-of-the-art measurement accuracies, they might become relevant in the future where these accuracies increase.
GREOPy builds a basis for quantifying what impact these deviations have on the subsequent observable error.

## How to install GREOPy

To install this package run:

`python -m pip install GREOPy`

## Get started using GREOPy

Two curves and the underlying spacetime structure are needed to calculate light signals between the curves.
Assume `emission_curve` and `reception_curve` contain the coordinates and four-velocity tangent vector of each point along the respective curve in spacetime.
Also assume that `config` contains information on the spacetime structure.
Then calling the `eop_solver` function calculates for each point along the emission curve the corresponding unique light signal propagating to the reception curve:

```python
from greopy.emitter_observer_problem import eop_solver

light_rays = eop_solver(config, emission_curve_reduced, receiver_curve_data)
```

The resulting `light_rays` contains the coordinates and four-velocity tangent vector of each point along the light signal curve in spacetime.
These results can be visualised by calling the `eop_plot` function:

```python
from greopy.emitter_observer_solution_plot import eop_plot

eop_plot(emission_curve, reception_curve, light_rays)
```

![Example result](doc/source/auto_tutorials/images/sphx_glr_plot_quickstart_tutorial_001.png)
*Image caption*

Please visit the [documentation](doc/source/index.rst) for more information about the package, including a more detailed [quickstart](doc/source/quickstart.rst) guide.

## Community

If you would like to contribute to this package, you can read about ideas [here](CONTRIBUTING.md).
Since this is a young package, detailed instructions on how to contribute are still a work in progress.

Please note that this package is released with a [Code of Conduct](CODE_OF_CONDUCT.md) and by participating in this project you agree to abide by its terms.

## License

License information will follow. 

## How to cite GREOPy

Citation information will follow.

## Acknowledgements

This project was funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) – Project-ID 434617780 – SFB 1464, and we acknowledge support by the DFG under Germany’s Excellence Strategy – EXC-2123 QuantumFrontiers – 390837967.

