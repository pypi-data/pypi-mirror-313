#!/usr/bin/env python

"""
This module contains the logic to validate a given Steuer-ID.
It performs solely the structural validations and does not check
whether the provided Steuer-ID is actually assigned to a person.
"""

from os import environ
from collections import Counter

from .exceptions import *

STEUER_ID_LENGTH = 11
STEUERID_PRODUCTION_ENV = "STEUERID_PRODUCTION"

class SteuerIdValidator:
    @staticmethod
    def _validate_structure(steuer_id: str) -> None:
        """
        Performs following checks on steuer_id:
        1. steuer_id is not empty.
        2. Length of steuer_id is valid.
        3. steuer_id does not contain characters other than digits.

        Args:
            steuer_id (str): The Steuer-ID to check the structure for.

        Raises:
            EmptyInput: raised if the Steuer-ID is empty.
            InvalidLength: raised if the length of Steuer-ID is invalid.
            OnlyDigitsAllowed: raised if the Steuer-ID contains character(s)
                that are not digits.

        Returns:
            bool
        """
        if not steuer_id:
            raise EmptyInputException

        if not len(steuer_id) == STEUER_ID_LENGTH:
            raise InvalidLengthException

        if not steuer_id.isdigit():
            raise OnlyDigitsAllowedException

    @staticmethod
    def _validate_test_id(steuer_id: str) -> None:
        """In PRODUCTION mode, test steuer_ids are not allowed.

        Args:
            steuer_id (str)

        Raises:
            TestSteuerIdNotAllowed: raised if in PRODUCTION mode and
            test steuer_id (starting with '0') is provided.
        """
        production = bool(environ.get(STEUERID_PRODUCTION_ENV, False))
        if production and steuer_id[0] == '0':
            raise SteuerTestIdNotAllowedException

    @staticmethod
    def _validate_digit_repetitions(steuer_id: str) -> None:
        """
        Performs the following checks on steuer_id:
        1. One and only one digit is repeating in first 10 digits of steuer_id.
        2. The repeating digit occurs maximum of 3 times.
        3. If the repeating digit occurs 3 times then this repetition should not
        be consecutive.

        Args:
            steuer_id (str)

        Raises:
            OnlyOneRepeatedDigit
            InvalidDigitRepetition
            InvalidRepeatedDigitChain
        """
        first_ten_digits = steuer_id[:10]
        digit_counts = Counter(first_ten_digits)
        repeated_digit_counts = {
            k: v for k, v in digit_counts.items()
            if v > 1
        }

        if len(repeated_digit_counts) != 1:
            raise OnlyOneRepeatedDigitException

        repeated_digit = next(iter(repeated_digit_counts))
        digit_repetitions = repeated_digit_counts[repeated_digit]
        if digit_repetitions not in [2, 3]:
            raise InvalidDigitRepetitionException

        if digit_repetitions == 3 and repeated_digit * digit_repetitions in steuer_id:
            raise InvalidRepeatedDigitChainException

    @staticmethod
    def _get_checksum_digit(steuer_id: str) -> int:
        """Computes the checksum digit based on ELSTER algorithm.

        Args:
            steuer_id (str)

        Returns:
            int: the checksum digit.
        """
        product = STEUER_ID_LENGTH - 1
        modulo = STEUER_ID_LENGTH - 1

        for c in steuer_id[:10]:
            digit = int(c)
            summ = (digit + product) % modulo
            if summ == 0:
                summ = modulo
            product = (2 * summ) % STEUER_ID_LENGTH

        checksum_digit = STEUER_ID_LENGTH - product
        return 0 if checksum_digit == modulo else checksum_digit

    @staticmethod
    def _validate_checksum_digit(steuer_id: str) -> None:
        """
        Validates if the last digit in steuer_id is valid using
        the validation algorithm provided by ELSTER.

        Args:
            steuer_id (str)

        Raises:
            InvalidChecksumDigit
        """
        if steuer_id[-1] != str(SteuerIdValidator._get_checksum_digit(steuer_id)):
            raise InvalidChecksumDigitException

    @staticmethod
    def validate(steuer_id: str) -> tuple[bool, None] | tuple[bool, SteuerIDValidationException]:
        """
        Validates the steuer_id based on criterion provided by ELSTER
        handbook (Pruefung_der_Steuer_und_Steueridentifikatsnummer.pdf).

        Args:
            steuer_id (str)

        Returns:
            tuple[bool, None] | tuple[bool, SteuerIDValidationException]: A tuple where first element is a
            boolean indicating the status of validation. If the validation
            encountered errors, the second element in the tuple contains
            the Exception object.
        """
        try:
            SteuerIdValidator._validate_structure(steuer_id)
            SteuerIdValidator._validate_test_id(steuer_id)
            SteuerIdValidator._validate_digit_repetitions(steuer_id)
            SteuerIdValidator._validate_checksum_digit(steuer_id)

            # input is a valid steuer id
            return True, None
        except SteuerIDValidationException as ex:
            return False, ex
        except:
            raise
