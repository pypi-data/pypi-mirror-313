#!/usr/bin/env python

"""
Contains all possible exceptions thrown during the validation
of a Steuer-ID.
"""

class SteuerIDValidationException(Exception):
    pass

class EmptyInputException(SteuerIDValidationException):
    pass

class OnlyDigitsAllowedException(SteuerIDValidationException):
    pass

class InvalidLengthException(SteuerIDValidationException):
    pass

class SteuerTestIdNotAllowedException(SteuerIDValidationException):
    pass

class OnlyOneRepeatedDigitException(SteuerIDValidationException):
    pass

class InvalidDigitRepetitionException(SteuerIDValidationException):
    pass

class InvalidRepeatedDigitChainException(SteuerIDValidationException):
    pass

class InvalidChecksumDigitException(SteuerIDValidationException):
    pass
