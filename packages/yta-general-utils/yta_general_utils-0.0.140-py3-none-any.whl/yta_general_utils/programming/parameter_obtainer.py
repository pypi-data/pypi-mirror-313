import inspect


class ParameterObtainer:
    """
    Class to interact with python methods and classes to obtain
    the parameters those method have. This is usefull for dynamic
    functionality that need to fill or check if the required
    parameters are passed or not.
    """
    @staticmethod
    def get_parameters_from_method(method, params_to_ignore: list[str] = ['self', 'cls', 'args', 'kwargs']):
        """
        This methods returns the existing parameters in the provided
        'method' that are not in the 'params_to_ignore' list. These
        parameters will be categorized in 'mandatory' and 'optional'.
        The 'optional' values are those that have None as default 
        value.

        The 'method' parameter must be a real python method to be able
        to inspect it.
        """
        parameters = {
            'mandatory': [],
            'optional': []
        }

        params = inspect.signature(method).parameters.values()
        for parameter in params:
            if params_to_ignore is not None and parameter.name in params_to_ignore:
                continue
            
            # If parameter is set as None, it is optional
            if parameter.default is parameter.empty:
                parameters['mandatory'].append(parameter.name)
            else:
                parameters['optional'].append(parameter.name)

        return parameters
