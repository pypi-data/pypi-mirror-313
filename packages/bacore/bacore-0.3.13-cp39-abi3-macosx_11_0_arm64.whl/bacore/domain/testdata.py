"""Test data generation."""
from dataclasses import dataclass
from faker import Faker
from hypothesis import strategies as st
from typing import Optional


@dataclass(frozen=True)
class CountryCodes:
    """Country code for countries and regions.

    Examples:
        >>> CountryCodes.denmark
        'da_DK'

        >>> CountryCodes.nordics()
        ['da_DK', 'fi_FI', 'no_NO', 'sv_SE']
    """

    china = 'zh_CN'
    denmark = 'da_DK'
    estonia = 'et_EE'
    finland = 'fi_FI'
    france = 'fr_FR'
    germany = 'de_DE'
    italy = 'it_IT'
    latvia = 'lv_LV'
    lithuania = 'lt_LT'
    netherlands = 'nl_NL'
    norway = 'no_NO'
    poland = 'pl_PL'
    portugal = 'pt_PT'
    russia = 'ru_RU'
    spain = 'es_ES'
    sweden = 'sv_SE'
    ukraine = 'uk_UA'
    united_kingdom = 'en_GB'
    united_states_of_america = 'en_US'

    @classmethod
    def nordics(cls) -> list[str]:
        return [cls.denmark, cls.finland, cls.norway, cls.sweden]

    @classmethod
    def europe(cls) -> list[str]:
        countries = cls.nordics() + [
            cls.estonia, cls.latvia, cls.lithuania,
            cls.france, cls.germany, cls.italy,
            cls.netherlands, cls.poland, cls.portugal,
            cls.spain, cls.ukraine, cls.united_kingdom
        ]
        return sorted(countries)

    @classmethod
    def world(cls) -> list[str]:
        countries = cls.europe() + [
            cls.china, cls.russia, cls.united_states_of_america
        ]
        return sorted(countries)

    @classmethod
    def for_locale(cls, name: str) -> list[str]:
        """Takes a locale specifier (country or region) and returns country codes.
        If the "attribute" is a function, then is it called.

        Examples:
            >>> CountryCodes.for_locale("sweden")
            'sv_SE'
        """
        if not hasattr(cls, name):
            raise AttributeError(f"Country code with attribute '{name}' does not exist")
        if callable(getattr(cls, name)):
            return getattr(cls, name)()
        else:
            return getattr(cls, name)


@dataclass
class PytestRunData:
    """Test result."""
    pytest_exit_codes = {
        0: "All tests were collected and passed successfully.",
        1: "Tests were collected and run but some of the tests failed.",
        2: "Test execution was interrupted by the user.",
        3: "Internal error happened while executing tests.",
        4: "pytest command line usage error.",
        5: "No tests were collected."
    }
    status: int
    testrun_parameters: Optional[str] = None

    @property
    def message(self) -> str:
        """Return status message."""
        return self.pytest_exit_codes[self.status]


@dataclass
class FakerData(Faker):
    """Test data for locale (country or region).

    Parameters:
        `country_or_region`: A country or region for which test data is generated.
        `match_real_world_occurrences`: Makes `Faker` try to match the real world occurrences of the data. If `True`
            will data generation be slower.

    Methods:
        `seed()`: Seed the random number generator for reproducibility.
    """

    def __init__(self, country_or_region: str, match_real_world_occurrences: bool = False):
        country_codes = CountryCodes.for_locale(country_or_region)
        self.match_real_world_occurrences = match_real_world_occurrences
        super().__init__(country_codes, use_weighting=self.match_real_world_occurrences)


class TestData:
    """Test data strategies for hypothesis.

    Parameters:
        `country_or_region`: A country or region for which test data is generated.
        `match_real_world_occurrences`: Makes `Faker` try to match the real world occurrences of the data. Default is
            `False` and if `True` will data generation be slower.

    Examples:
        >>> company = TestData(country_or_region="sweden").company()
        >>> isinstance(company, st.SearchStrategy)
        True
    """

    def __init__(self, country_or_region: str, match_real_world_occurrences: bool = False):
        self.country_or_region = country_or_region
        self.faker_data = FakerData(self.country_or_region, match_real_world_occurrences=match_real_world_occurrences)

    def company(self) -> st.SearchStrategy:
        return st.builds(self.faker_data.company)

    def currency_code(self) -> st.SearchStrategy:
        return st.builds(self.faker_data.currency_code)

    def first_name(self) -> st.SearchStrategy:
        return st.builds(self.faker_data.first_name)

    def isin(self) -> st.SearchStrategy:
        regex_map = {
            "sweden": r"\ASE[0-9]{10}\Z",
            "finland": r"\AFI[0-9]{10}\Z"
        }
        return st.from_regex(regex_map.get(self.country_or_region, r"\A[X]{2}[A-Z0-9]{9}[0-9]\Z"))

    def last_name(self) -> st.SearchStrategy:
        return st.builds(self.faker_data.last_name)

    def ssn(self) -> st.SearchStrategy:
        return st.builds(self.faker_data.ssn)
