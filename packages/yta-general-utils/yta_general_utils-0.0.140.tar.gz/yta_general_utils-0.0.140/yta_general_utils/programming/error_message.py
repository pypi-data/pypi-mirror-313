from typing import Union


class ErrorMessage:
    @staticmethod
    def parameter_is_not_a_class(parameter_name: str):
        return f'The provided "{parameter_name}" parameter is not a class.'
    
    # TODO: All this methods below must be 'staticmethod', we do not
    # use instances with this class and will not use them.
    @classmethod
    def parameter_not_provided(cls, parameter_name: str):
        return f'The parameter "{parameter_name}" was not provided.'
    
    @classmethod
    def parameter_is_not_string(cls, parameter_name: str):
        return f'The parameter "{parameter_name}" provided is not a string.'
    
    @classmethod
    def parameter_is_not_boolean(cls, parameter_name: str):
        return f'The "{parameter_name}" parameter is not boolean.'
    
    @classmethod
    def parameter_is_not_positive_number(cls, parameter_name: str):
        return f'The parameter "{parameter_name}" provided is not a valid and positive number.'
    
    @classmethod
    def parameter_is_file_that_doesnt_exist(cls, parameter_name: str):
        return f'The "{parameter_name}" parameter provided is not a file that exists.'
    
    @classmethod
    def parameter_is_not_file_of_file_type(cls, parameter_name: str, file_type: 'FileType'):
        return f'The "{parameter_name}" provided is not a {file_type.value} filename.'
    
    @classmethod
    def parameter_is_not_valid_url(cls, parameter_name: str):
        return f'The provided "{parameter_name}" parameter is not a valid url.'
    
    @classmethod
    def parameter_is_not_class(cls, parameter_name: str, class_names: Union[list[str], str]):
        # TODO: Check if 'class_names' is not array of str nor str
        if isinstance(class_names, str):
            class_names = [class_names]

        class_names = ', '.join(class_names)
        return f'The provided "{parameter_name}" parameter is not one of the next classes: {class_names}'

    @classmethod
    def parameter_is_not_name_of_ytaenum_class(cls, name: str, enum):
        return f'The provided YTAEnum name "{name}" is not a valid {enum.__class__.__name__} YTAEnum name.'
    
    @classmethod
    def parameter_is_not_value_of_ytaenum_class(cls, value: any, enum):
        return f'The provided YTAEnum value "{value}" is not a valid {enum.__class__.__name__} YTAEnum value.'
    
    @classmethod
    def parameter_is_not_name_nor_value_of_ytaenum_class(cls, name_or_value: any, enum):
        return f'The provided YTAEnum name or value "{name_or_value}" is not a valid {enum.__class__.__name__} YTAEnum name or value.'
    
    @classmethod
    def parameter_is_not_name_nor_value_nor_enum_of_ytaenum_class(cls, name_or_value_or_enum: any, enum):
        return f'The provided YTAEnum name, value or instance "{name_or_value_or_enum}" is not a valid {enum.__class__.__name__} YTAEnum name, value or instance.'