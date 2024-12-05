class MockMatch:
    def __init__(self):
        self.dport = None


class MockRule:
    def __init__(self):
        self.protocol = None
        self.target = None
        self.matches = []
        self.comment = ""

    def create_match(self, protocol):
        match = MockMatch()
        self.matches.append(match)
        return match

    def __eq__(self, other):
        if not isinstance(other, MockRule):
            return False

        return (
            self.protocol == other.protocol
            and len(self.matches) == len(other.matches)
            and all(
                s_match.dport == o_match.dport
                for s_match, o_match in zip(self.matches, other.matches)
            )
            and self.comment == other.comment
        )

    def __str__(self):
        return f"Rule(protocol={self.protocol}, comment={self.comment})"


class MockChain:
    def __init__(self):
        self._rules = []

    def insert_rule(self, rule):
        self._rules.append(rule)

    def delete_rule(self, rule):
        matching_rules = [
            r
            for r in self._rules
            if (r.protocol == rule.protocol and r.comment == rule.comment)
        ]
        if matching_rules:
            self._rules.remove(matching_rules[0])

    @property
    def rules(self):
        return self._rules


class MockTable:
    NAT = "nat"

    def __init__(self, name):
        self.name = name
        self._chains = {}

    def refresh(self):
        pass


class MockState:
    def __init__(self):
        self.chains = {}

    def get_chain(self, table, chain_name):
        key = f"{table.name}_{chain_name}"
        if key not in self.chains:
            self.chains[key] = MockChain()
        return self.chains[key]
