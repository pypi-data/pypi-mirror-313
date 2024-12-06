"""
    The 'inspect' module (native in python) is very interesting because
    it has some methods to check if a user defined function or things 
    like that.

    'f.__qualname__' is very interesting thing as it works
    with the full path, not as 'f.__name__' does, this is
    one example of it value when doing it from a local file:
    
    'Example.example.__qualname__'
    test_discord_video.<locals>.Example.example
    
    And yes, the 'example' is a @staticmethod defined in the
    Example class that is contained in the 'test_discord_video'
    file
"""
from yta_general_utils.programming.error_message import ErrorMessage
# from yta_general_utils.file.filename import filename_is_type
# from yta_general_utils.checker.type import variable_is_positive_number
# from yta_general_utils.file.checker import file_exists
# from yta_general_utils.checker.url import url_is_ok
from enum import Enum
from typing import Union

import numpy as np
import inspect
import re


# TODO: Remove commented methods in PythonValidator for the next version
class PythonValidator:
    """
    Class to simplify and encapsulate the functionality related with
    parameters and variables validation.

    This class has been created to simplify the way it work and 
    replace the old ParameterValidator that was using too many 
    different methods being imported and generating cyclic import
    issues.

    We have some equivalent methods that do not need to pass the class
    as a parameter, so we can only work with the class name and avoid
    imports that can cause issues.
    """

    @staticmethod
    def is_instance(element, cls: Union[str, type, list]):
        """
        Check if the provided 'element' is an instance of the provided
        class (or classes) 'cls'. An instance is not the same as a
        class. The 'cls' parameter can be the class or the string name
        of that class, or a list of them (even mixed).

        This method is useful if you want to check if it belongs to a
        class but without importing the class and passing it as a 
        parameter to avoid cyclic import issues.
        """
        if not PythonValidator.is_list(cls):
            cls = [cls]

        # TODO: I need to review this below when providing Unions or
        # strange things because of the 'validate_method_params'
        # method
        if any(not PythonValidator.is_string(cls_item) and not PythonValidator.is_a_class(cls_item) and cls_item is not None for cls_item in cls):
            classes_str = [cls_item.__str__() for cls_item in cls]
            #classes_str = ', '.join(cls)
            raise Exception(f'At least one of the provided "cls" parameters "{classes_str}" is not a string nor a class.')
        
        if PythonValidator.is_a_class(element):
            return False
        
        cls_class_items = tuple([cls_item for cls_item in cls if PythonValidator.is_a_class(cls_item)])
        cls_str_items = [cls_item for cls_item in cls if not PythonValidator.is_a_class(cls_item)]

        return isinstance(element, cls_class_items) or any(getattr(type(element), '__name__', None) == cls_item for cls_item in cls_str_items)
    
    @staticmethod
    def is_an_instance(element):
        """
        Check if the provided 'element' is an instance of any class.
        """
        return isinstance(element, object)
        # This below is just another alternative I want to keep
        return getattr(element, '__name__', None) is None
    
    @staticmethod
    def is_class(element, cls: Union[str, type]):
        """
        Check if the provided 'element' is the provided class 'cls'.
        A class is not the same as an instance of that class. The
        'cls' parameter can be the class or the string name of that
        class. 

        You can pass the string name of the class to avoid import in 
        the file where you are calling this method.
        """
        # TODO: Convert this to accept cls as array and check 
        # diferent classes
        if not PythonValidator.is_string(cls) and not PythonValidator.is_a_class(cls):
            raise Exception(f'The provided "cls" parameter "{str(cls)}" is not a string nor a class.')
        
        if PythonValidator.is_string(cls):
            return getattr(element, '__name__', None) is cls
        else:
            return PythonValidator.is_a_class(element) and element == cls

    @staticmethod
    def is_a_class(element):
        """
        Check if the provided 'element' is a class.
        """
        return isinstance(element, type)
        # This below is just another alternative I want to keep
        return getattr(element, '__name__', None) is not None
    
    @staticmethod
    def is_subclass(element: type, cls: Union[str, type]):
        """
        Check if the provided 'element' is a subclass of the provided
        class 'cls'. The 'cls' parameter can be the class or the
        string name of that class.

        You can pass the string name of the class to avoid import in 
        the file where you are calling this method.

        This method can return True if the provided 'element' is an
        instance or a class that inherits from Enum or YTAEnum class.
        Consider this above to check later if your 'element' is an
        instance or a class.
        """
        # TODO: Convert this to accept cls as array and check 
        # diferent classes
        if not PythonValidator.is_string(cls) and not PythonValidator.is_a_class(cls):
            raise Exception(f'The provided "cls" parameter "{str(cls)}" is not a string nor a class.')
        
        if not PythonValidator.is_a_class(element):
            # We want to know if it is a subclass, we don't
            # care if the provided one is an instance or a class,
            # so we try with both.
            if PythonValidator.is_an_instance(element):
                element = type(element)
            else:
                return False
            
        if PythonValidator.is_string(cls):
            return cls in [base_class.__name__ for base_class in element.__bases__]
        else: 
            issubclass(element, cls)

    @staticmethod
    def is_a_function(element):
        """
        Check if the provided 'element' is a function.
        """
        # TODO: Maybe inspect.isfunction(element) (?)
        return type(element).__name__ == 'function'
    
    @staticmethod
    def is_class_staticmethod(cls: type, method: 'function', method_name: str = None):
        """
        Check if the provided 'method' is an staticmethod (a
        function) defined in the also provided 'cls' class.

        If the 'method_name' parameter is provided, it will
        also check if the name of the provided 'method' is
        equal to the one provided in the 'method_name' param.
        """
        if not PythonValidator.is_a_class(cls):
            raise Exception('The provided "cls" parameter is not a class.')
        
        if not PythonValidator.is_a_function(method):
            raise Exception('The provided "method" parameter is not a function.')
        
        for function in inspect.getmembers(cls, predicate = inspect.isfunction):
            if function[0] == method.__name__:
                if method_name is None:
                    return True
                else:
                    return method.__name__ == method_name
            
        return False
    
    @staticmethod
    def is_list(element):
        """
        Check if the provided 'element' is a list.
        """
        return type(element) == list

    @staticmethod
    def is_tuple(element):
        """
        Check if the provided 'element' is a tuple.
        """
        return PythonValidator.is_instance(element, tuple)
    
    @staticmethod
    def is_string(element):
        """
        Check if the provided 'element' is a string (str).
        """
        return isinstance(element, str)
    
    @staticmethod
    def is_boolean(element):
        """
        Check if the provided 'element' is a boolean (bool).
        """
        return isinstance(element, bool)
    
    @staticmethod
    def is_number(element, do_accept_string_number: bool = False):
        """
        Check if the provided 'element' is a numeric value. If
        'do_accept_string_number' is True, it will try to parse
        the 'element' as a float if a string is provided.
        """
        return NumberValidator.is_number(element, do_accept_string_number)

    @staticmethod
    def is_numpy_array(element):
        """
        Check if the provided 'element' is an instance of the
        numpy array np.ndarray.
        """
        return PythonValidator.is_instance(element, np.ndarray)
    
    @staticmethod
    def is_enum(element: Union['YTAEnum', Enum]):
        """
        Check if the provided 'element' is a subclass of an Enum or
        a YTAEnum.

        This method can return True if the provided 'element' is an
        instance or a class that inherits from Enum or YTAEnum class.
        Consider this above to check later if your 'element' is an
        instance or a class.
        """
        # TODO: I think it is 'EnumMeta' not Enum
        return PythonValidator.is_subclass(element, 'YTAEnum') or PythonValidator.is_subclass(element, 'Enum')
    
    @staticmethod
    def is_enum_instance(element: Union['YTAEnum', Enum]):
        """
        Check if the provided 'element' is a Enum (it is a subclass
        of an Enum or a YTAEnum) and it is an instance.
        """
        return PythonValidator.is_enum(element) and PythonValidator.is_an_instance(element)
    
    @staticmethod
    def is_enum_class(element: Union['YTAEnum', Enum]):
        """
        Check if the provided 'element' is a Enum (it is a subclass
        of an Enum or a YTAEnum) and it is a class.
        """
        return PythonValidator.is_enum(element) and PythonValidator.is_a_class(element)
    
    @staticmethod
    def validate_method_params(method: 'function', params: list, params_to_ignore: list[str] = ['self', 'cls', 'args', 'kwargs']):
        """
        IMPORTANT! This method should be called on top of any method
        in which you want to validate if the provided parameters are
        valid, by providing the method (function) declaration and
        also the 'locals()' function executed as 'params' parameter.
        So, it should be called like this:

        PythonValidator.validate_method_params(function, locals())

        This method check the types of the params that the provided
        'method' has and validate if the provided values fit the
        specified types (according also to the default values). It
        will raise an Exception when any of the provided params (and
        not ignored) is not valid according to its type declaration.

        The provided 'params' must be a dict containing all the param
        names and values.

        This method is able to parse non-type declarations, as in
        "method(type)", single declarations, as in "method(type: str)"
        and Union declarations, as in
        "method(type: Union[str, MyClass])"

        The 'method' parameter must be a real python method to be able
        to inspect it.
        """
        if not PythonValidator.is_a_function(method):
            raise Exception('The provided "method" parameter is not a valid method (function).')

        # This below is like '<class 'package.of.class.name'> or '<class 'str'>
        SINGLE_TYPE_REGEX = r"<class '([^']+)'>"
        # This below is like 'Union['str', 'int', 'FfmpegHandler']
        UNION_TYPE_REGEX = r"typing\.Union\[\s*((?:[^,]+(?:\s*,\s*)?)+)\s*\]"
        # This below is to flag those params with no default value
        # because None can be a default value indicating that it is
        # an optional value
        NO_DEFAULT_VALUE = '__no_default_value__'
        NO_TYPE = '__no_type__'

        # TODO: Refactor this below to make it easier to be read
        for param in inspect.signature(method).parameters.values():
            if param.name in params_to_ignore:
                continue

            print(param.name)
            print(params_to_ignore)

            types = param.annotation if param.annotation is not inspect.Parameter.empty else NO_TYPE
            default_value = param.default if param.default is not inspect.Parameter.empty else NO_DEFAULT_VALUE

            # 'types' can be nothing, a single type or an Union
            if types:
                match_class = re.match(SINGLE_TYPE_REGEX, str(types))
                match_union = re.match(UNION_TYPE_REGEX, str(types))

                # Turn type to array of string types
                if match_class:
                    types = [match_class.group(1).split('.')[-1]]
                elif match_union:
                    classes = match_union.group(1).split(',')
                    types = [class_i.strip().split('.')[-1] for class_i in classes]

            # Now check with the param provided
            user_param = params.get(param.name, None)

            if types is NO_TYPE and user_param is None:
                # If no type we cannot validate anything, but I 
                # think if no type nor value it will not be
                # executed and this Exception below will never
                # happen
                raise Exception(f'The param "{str(param.name)}" has no type declaration but also None value, so it is not accepted.')
            elif user_param == None and (PythonValidator.is_list(types) and 'None' in types or default_value == None):
                # TODO: If we are strict with typing, a value that
                # can be None should be Union[None, ...] and also
                # param = None (as default value) to indicate it is
                # optional, but we accept both of them separately

                # Param value is None and None is accepted or is
                # default value
                pass
            elif user_param == None:
                raise Exception(f'The param "{str(param.name)}" has None value provided and we expected one of these types: {", ".join(types)}.')
            else:
                if not PythonValidator.is_instance(user_param, types) and types is not NO_TYPE:
                    print(types)
                    types_str = ', '.join(types)
                    raise Exception(f'The param value "{str(param.name)}" provided "{str(user_param)}" is not one of the expected types: {types_str}.')

        return True

class NumberValidator:
    """
    Class to simplify and encapsulate the functionality related
    to validate numeric values.
    """
    @staticmethod
    def is_number(element: Union[int, float, str], do_accept_string_number: bool = False):
        """
        Check if the provided 'element' is a numeric value. If
        'do_accept_string_number' is True, it will try to parse
        the 'element' as a float if a string is provided.
        """
        if not PythonValidator.is_instance(element, [int, float, str, np.number]):
            return False
        
        if PythonValidator.is_instance(element, str):
            if do_accept_string_number:
                try:
                    float(element)
                except:
                    return False
            else:
                return False
            
        return True
    
    @staticmethod
    def is_positive_number(element: Union[int, float, str], do_include_zero: bool = True):
        """
        This method checks if the provided 'element' is a numeric type,
        or tries to cast it as a float number if string provided, and
        returns True in the only case that the 'element' is actual a
        number by itself or as a string and it is 0 or above it. If 
        'do_include_zero' is set to False it won't be included.
        """        
        if not NumberValidator.is_number(element, False):
            return False
        
        element = float(element)

        if do_include_zero:
            return element >= 0
        
        return element > 0
    
    @staticmethod
    def is_number_between(element: Union[int, float, str], lower_limit: Union[int, float, str], upper_limit: Union[int, float, str], do_include_lower_limit: bool = True, do_include_upper_limit: bool = True):
        """
        This methods returns True if the provided 'variable' is a valid number
        that is between the also provided 'lower_limit' and 'upper_limit'. It
        will return False in any other case.
        """
        if not NumberValidator.is_number(element, True):
            return False
        
        if not NumberValidator.is_number(lower_limit) or not NumberValidator.is_number(upper_limit):
            return False
        
        element = float(element)
        lower_limit = float(lower_limit)
        upper_limit = float(upper_limit)
        
        # TODO: Should we switch limits if unordered (?)
        # if upper_limit < lower_limit:
        #     raise Exception(f'The provided "upper_limit" parameter {str(upper_limit)} is lower than the "lower_limit" parameter {str(lower_limit)} provided.')

        if do_include_lower_limit and do_include_upper_limit:
            return lower_limit <= element <= upper_limit
        elif do_include_lower_limit:
            return lower_limit <= element < upper_limit
        elif do_include_upper_limit:
            return lower_limit < element <= upper_limit
        else:
            return lower_limit < element < upper_limit
        
    @staticmethod
    def is_int(element: int):
        """
        Return True if the provided 'element' is an int
        number.
        """
        return PythonValidator.is_instance(element, int)
    
    @staticmethod
    def is_float(element: float):
        """
        Return True if the provided 'element' is a float
        number.
        """
        return PythonValidator.is_instance(element, float)
    
class ParameterValidator:
    @staticmethod
    def validate_mandatory_parameter(name: str, value):
        """
        Validates if the provided 'value' parameter with the also
        provided 'name' has a value, raising an Exception if not.

        This method returns the provided 'value' if everything is
        ok.
        """
        if not value:
            raise Exception(ErrorMessage.parameter_not_provided(name))

        return value

    @staticmethod
    def validate_string_parameter(name: str, value):
        """
        Validates if the provided 'value' parameter with the also
        provided 'name' is a string value, raising an Exception if
        not.

        This method returns the provided 'value' if everything is
        ok.
        """
        if not PythonValidator.is_string(value):
            raise Exception(ErrorMessage.parameter_is_not_string(name))

        return value
    
    @staticmethod
    def validate_bool_parameter(name: str, value: bool):
        """
        Validates if the provided 'value' parameter with the also
        provided 'name' is a boolean value, raising and Exception 
        if not.

        This method returns the provided 'value' if everything is
        ok.
        """
        if not PythonValidator.is_boolean(value):
            raise Exception(ErrorMessage.parameter_is_not_boolean(name))

        return value
    
# class ParameterValidator:
#     @classmethod
#     def validate_mandatory_parameter(cls, name: str, value):
#         """
#         Validates if the provided 'value' parameter with the also
#         provided 'name' has a value, raising an Exception if not.

#         This method returns the provided 'value' if everything is
#         ok.
#         """
#         if not value:
#             raise Exception(ErrorMessage.parameter_not_provided(name))

#         return value
        
#     @classmethod
#     def validate_string_parameter(cls, name: str, value: str):
#         """
#         Validates if the provided 'value' parameter with the also
#         provided 'name' is a string value, raising an Exception if
#         not.

#         This method returns the provided 'value' if everything is
#         ok.
#         """
#         if not isinstance(value, str):
#             raise Exception(ErrorMessage.parameter_is_not_string(name))

#         return value

#     @classmethod
#     def validate_bool_parameter(cls, name: str, value: bool):
#         """
#         Validates if the provided 'value' parameter with the also
#         provided 'name' is a boolean value, raising and Exception 
#         if not.

#         This method returns the provided 'value' if everything is
#         ok.
#         """
#         if not isinstance(value, bool):
#             raise Exception(ErrorMessage.parameter_is_not_boolean(name))

#         return value
        
#     @classmethod
#     def validate_file_exists(cls, name: str, value: str):
#         """
#         Validates if the provided 'value' parameter with the also
#         provided 'name' is a file that actually exists, raising
#         an Exception if not.

#         This method returns the provided 'value' if everything is
#         ok.
#         """
#         if not file_exists(value):
#             raise Exception(ErrorMessage.parameter_is_file_that_doesnt_exist(name))

#         return value
        
#     @classmethod
#     def validate_filename_is_type(cls, name: str, value: str, file_type: 'FileType'):
#         """
#         Validates if the provided 'value' parameter with the also
#         provided 'name' is a filename of the given 'file_type',
#         raising an Exception if not.

#         This method returns the provided 'value' if everything is
#         ok.
#         """
#         if not filename_is_type(value, file_type):
#             raise Exception(ErrorMessage.parameter_is_not_file_of_file_type(name, file_type))

#         return value
        
#     @classmethod
#     def validate_url_is_ok(cls, name: str, value: str):
#         """
#         Validates if the provided 'value' parameter with the also
#         provided 'name' is a valid url (the url is accessible),
#         raising an Exception if not.

#         This method returns the provided 'value' if everything is
#         ok.
#         """
#         if not url_is_ok(value):
#             raise Exception(ErrorMessage.parameter_is_not_valid_url(name))

#         return value
        
#     @classmethod
#     def validate_positive_number(cls, name: str, value: Union[int, float]):
#         """
#         Validates if the provided 'value' parameter with the also
#         provided 'name' is a positive number (0 or greater),
#         raising an Exception if not.

#         This method returns the provided 'value' as it is if 
#         everything is ok.
#         """
#         if not variable_is_positive_number(value):
#             raise Exception(ErrorMessage.parameter_is_not_positive_number(name))

#         return value

#     @classmethod
#     def validate_is_class(cls, name: str, value, class_names: Union[list[str], str]):
#         """
#         Validates if the provided 'value' is one of the provided 'class_names'
#         by using the 'type(value).__name__' checking.

#         This method returns the 'value' as it is if everything is ok.
#         """
#         if isinstance(class_names, str):
#             class_names = [class_names]

#         if not type(value).__name__ in class_names:
#             raise Exception(ErrorMessage.parameter_is_not_class(name, class_names))
        
#         return value
        
#     # Complex ones below
#     @classmethod
#     def validate_string_mandatory_parameter(cls, name: str, value: str):
#         """
#         Validates if the provided 'value' is a valid and non
#         empty string.
#         """
#         cls.validate_mandatory_parameter(name, value)
#         cls.validate_string_parameter(name, value)

#         return value

#     @classmethod
#     def validate_numeric_positive_mandatory_parameter(cls, name: str, value: str):
#         """
#         Validates if the provided 'value' is a positive numeric
#         value.
#         """
#         cls.validate_mandatory_parameter(name, value)
#         cls.validate_positive_number(name, value)

#         return value
    
#     @classmethod
#     def validate_is_enum_class(cls, enum: Union['YTAEnum', Enum]):
#         """
#         Validates if the provided 'value' is a valid Enum
#         class or subclass.

#         This method will raise an Exception if the provided
#         'value' is not a valid Enum class or subclass, or
#         will return it as it is if yes.
#         """
#         if not isinstance(enum, Enum) and not issubclass(enum, Enum):
#             raise Exception(f'The parameter "{enum}" provided is not an Enum class or subclass.')
        
#         return enum

#     @classmethod
#     def validate_enum(cls, value: Union['YTAEnum', str], enum: 'YTAEnum'):
#         """
#         Validates if the provided 'value' value is a valid
#         Enum or Enum value of the also provided 'enum' class.

#         This method will raise an Exception if something is
#         wrong or will return the 'value' as an 'enum' Enum.
#         instance if everything is ok.
#         """
#         cls.validate_mandatory_parameter('value', value)
#         cls.validate_is_enum_class(enum)
#         cls.validate_is_class('value', value, [enum.__class__.__name__, 'str'])

#         return enum.to_enum(value)