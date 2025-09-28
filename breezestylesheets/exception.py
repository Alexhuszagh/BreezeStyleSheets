'''
exception
=========

Custom exception types.
'''

import typing

if typing.TYPE_CHECKING:
    import os


class BreezeStyleSheetError(Exception):
    '''The base exception type for all errors.'''

    message: 'str'
    '''The descriptive error message of the exception.'''

    def __init__(self, message: 'str') -> None:
        '''
        Args:
            message (`str`): The descriptive error message of the exception.
        '''
        super().__init__(message)
        self.message = message


class ConfigError(BreezeStyleSheetError):
    '''The base exception for all config errors.'''


class ConfigParseError(ConfigError):
    '''Exceptions that occur when parsing configuration data.'''

    data: 'str | bytes | bytearray'
    '''The input data provided to the parser.'''

    path: 'os.PathLike | None'
    '''The path to the input file that caused the error, if parsing from file.'''

    inner: 'Exception | None'
    '''The exception that caused the parse error, if applicable.'''

    def __init__(
        self,
        message: 'str',
        data: 'str | bytes | bytearray',
        path: 'os.PathLike | None' = None,
        inner: 'Exception | None' = None,
    ) -> None:
        '''
        Args:
            message (`str`): The descriptive error message of the exception.
            data: (`str`, `bytes`, `bytearray`): The input data provided to the parser.
            path: (`str`, `Path`, `None`): The path to the input file that caused the error,
                if parsing from file.
            inner: (`Exception`, `None`): The exception that caused the parse error, if applicable.
        '''
        super().__init__(message)
        self.message = message
        self.data = data
        self.path = path
        self.inner = inner
