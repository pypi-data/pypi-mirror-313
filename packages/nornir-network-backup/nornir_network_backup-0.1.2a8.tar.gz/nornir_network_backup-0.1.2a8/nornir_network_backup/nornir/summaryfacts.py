class SummaryFact:
    """Ojbect for storing a single summary fact

    Summary facts are the fact elements that are optionally provided at the top
    of a config backup file
    """

    def __init__(self, **fact: dict) -> None:
        """initializes the SummaryFact object"""
        self.key = fact["key"]
        self.enabled = fact.get("enabled", True)
        self.textfsm = fact.get("textfsm", True)

    def __str__(self) -> str:
        return f"<SummaryFact: {self.key}>"


class SummaryFacts:
    """Object for storing a list of summary facts"""

    def __init__(self, facts: list[dict]) -> None:
        """initializes the SummaryFacts object

        The input is supposed to have a list of dicts, each
        dict contains
        """
        self._facts = []
        for fact in facts:
            self._facts.append(SummaryFact(**fact))

    @property
    def facts(self) -> list:
        """generator to return all stored facts"""
        for fact in self._facts:
            yield fact

    def fact_keys(self) -> list[str]:
        """Returns a list of fact keys"""
        fact_keys = [fact.key for fact in self.facts]
        return fact_keys

    def __str__(self) -> str:
        return f"<SummaryFacts: {','.join(self.fact_keys())}>"
