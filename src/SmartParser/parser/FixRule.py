import re


class FixRule:
    def __init__(self, rules = []):
        self.rules = rules


    def does_match(self, data, rule, metadata = {}):
        for condition in rule["conditions"]:
            print("Checking: ", condition, data)
            field = condition["field"]
            ruleRegex = condition["value"]
            if field in data:
                 if ruleRegex != data[field]:
                     print("Not matching", ruleRegex, data[field])
                     return False
            else:
                print("No ", field, "in", data)
                return False

        return True

    def do_action(self, data_result, rule):

        rule_type = rule["action"]["action_type"]
        rule_field = rule["action"]["field"]
        rule_value = rule["action"]["value"]

        if rule_type == "replace":
            data_result[rule_field] = rule_value



    def fixData(self, data_result, metadata= {}):
        for rule in self.rules:
            if self.does_match(data_result | metadata, rule):
                self.do_action(data_result, rule)

        return data_result