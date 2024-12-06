#!/usr/bin/env python3
"""
Propose quelques fonctions et procédures outils pour le projet
"""

import os.path
import re
from datetime import date
import polars as pl

from polars.testing import assert_frame_equal


# ==================================================
# ============ Tools ===============================
# ==================================================

def delEntete(string, char):
    first_index = string.find(char)
    if first_index == -1:
        return ''  # Le caractère n'est pas dans la chaîne
    second_index = string.find(char, first_index + 1)
    return string[second_index+2:]

def existFile(f: str) -> bool:
    return os.path.isfile(f)


def existDir(d: str) -> bool:
    return os.path.exists(d)


# == changer date d'un fichier
# touch -t 2006010000 tmp/s88581.ics
# ==
def modifDate(f: str) -> date:
    return date.fromtimestamp(os.stat(f).st_mtime)


def daysOld(f: str) -> int:
    """
    Calculate the number of days since the last modification of a file.

    Parameters:
    - f (str): The path to the file.

    Returns:
    - int: The number of days since the last modification.

    This function uses the `modifDate` function to get the last modification date of the file.
    It then calculates the difference between the current date and the modification date using the `date.today()` and `datetime.timedelta` functions.
    Finally, it returns the number of days as an integer.
    """
    n = date.today()
    d = modifDate(f)
    delta = n - d
    return delta.days


def bold_substring(string: str, substring: str) -> str:
    """
    This function takes a string and a substring as input, and returns a new string with the substring
    enclosed in ANSI escape codes for bold formatting.

    Parameters:
    - string (str): The original string.
    - substring (str): The substring to be bolded.

    Returns:
    - str: The new string with the substring bolded.

    Example:
    >>> bold_substring("Hello, World!", "World")
    "Hello, #\033[1mWorld\033[0m!"
    """
    match = re.search(re.escape(substring), rf"{string}", re.IGNORECASE)
    coord = match.span()
    return string[:coord[0]] + " #\033[1m" + substring + "\033[0m# " + string[coord[1]:]


def df_similaire(df1: pl.DataFrame, df2: pl.DataFrame) -> int:
    """
    Fonction qui compare deux résultats de requêtes
    :param df1: table de la requête SQL à comparer
    :param df2: l'autre table de la requête SQL à comparer
    :return: {0,1,2,3,4}
        0 : diff,
        1 : pas le même ordre des lignes et/ou des colonnes,
        2 : même ordre colonnes, pas le même ordre des lignes,
        3 : même ordre lignes, pas le même ordre des colonnes,
        4 : même ordre des colonnes et des lignes
    """

    try:
        # Tester l'égalité stricte avec Panda -> 4
        assert_frame_equal(df1, df2)
        return 4
    except AssertionError:
        try:
            # Tester l'égalité (ordre compris) sans les colonnes -> 3
            assert_frame_equal(df1, df2, check_column_order=False)
            return 3
        except AssertionError:
            try:
                # Tester l'égalité (ordre compris) sans les lignes -> 2
                assert_frame_equal(df1, df2, check_row_order=False)
                return 2
            except AssertionError:
                try:
                    # Tester l'égalité à l'ordre près -> 1
                    assert_frame_equal(df1, df2, check_column_order=False, check_row_order=False)
                    return 1
                except AssertionError:
                    # pas du tout égal -> 0
                    return 0
