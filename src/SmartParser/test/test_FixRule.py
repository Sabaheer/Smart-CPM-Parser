import unittest

import GrammarDesc
from FixRule import FixRule


from Rule import Rule

class FixRuleCustom1(FixRule):
    def __init__(self):
        FixRule.__init__(self)
        self.rules = [{"name": "rule1",
                        "conditions": [{"field": "ULDBayDesignation",
                            "value": "12L"}
                        ],
                        "action": {"field": "ULDBayDesignation", "action_type": "replace", "value": "ABC"}}]

class FixRuleCustom_meta(FixRule):
    def __init__(self):
        FixRule.__init__(self)
        self.rules = [{"name": "rule1",
                        "conditions": [{"field": "ULDBayDesignation",
                            "value": "12L"},
                        {"field": "FILENAME",
                            "value": "FILE1"}
                        ],
                        "action": {"field": "ULDBayDesignation", "action_type": "replace", "value": "ABC"}}]

class MyTestCase(unittest.TestCase):
    def test_fix_simple(self):
        rule = Rule(GrammarDesc.ULD, FixRuleCustom1())
        toParse = "-12L/AKE/MAN/551/BJ1-12R/N"

        print(toParse)
        result = rule.match_line(toParse)
        print(result)
        self.assertEqual([{'ULDBayDesignation': 'ABC', 'ULDTypeCode': 'AKE', 'UnloadingStation': 'MAN', 'Weight': '551', 'LoadCategory': ['BJ'], 'VolumeCode': '1'}, {'ULDBayDesignation': '12R', 'LoadCategory': ['N']}], result)


    def test_fix_simple_metadata(self):
        rule = Rule(GrammarDesc.ULD, FixRuleCustom_meta(), metadata={"FILENAME":"FILE1"})
        toParse = "-12L/AKE/MAN/551/BJ1-12R/N"

        print(toParse)
        result = rule.match_line(toParse)
        print(result)
        self.assertEqual([{'ULDBayDesignation': 'ABC', 'ULDTypeCode': 'AKE', 'UnloadingStation': 'MAN', 'Weight': '551', 'LoadCategory': ['BJ'], 'VolumeCode': '1'}, {'ULDBayDesignation': '12R', 'LoadCategory': ['N']}], result)

if __name__ == '__main__':
    unittest.main()
