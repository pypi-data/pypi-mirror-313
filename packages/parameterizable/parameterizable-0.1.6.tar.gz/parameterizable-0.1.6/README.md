# parameterizable

Parameter manipulation for Python classes.

## What Is It?

`parameterizable` provides the functionality for work with parameterizable 
classes: those that have (hyper) parameters which define object's configuration,
but not its internal contents or data. Such parameters are typically
passed to the .__init__() method.

## Usage
Inherit from `parameterizable.ParameterizableClass` class and define methods 
`.get_params()` and `.get_default_params()`. 

## Key Classes, Functions, and Constants

* `ParameterizableClass` - a base class for parameterizable objects.

## How To Get It?

The source code is hosted on GitHub at:
[https://github.com/pythagoras-dev/parameterizable](https://github.com/pythagoras-dev/parameterizable) 

Binary installers for the latest released version are available at the Python package index at:
[https://pypi.org/project/parameterizable](https://pypi.org/project/parameterizable)

        pip install parameterizable

## Dependencies

* [pytest](https://pytest.org)

## Key Contacts

* [Vlad (Volodymyr) Pavlov](https://www.linkedin.com/in/vlpavlov/)