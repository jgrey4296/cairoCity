
from enum import Enum
from random import choice
import logging as root_logger
logging = root_logger.getLogger(__name__)

verify_results = Enum("Verify Results", "PASS FAIL SANCTION")

class City:
    """
    A City Class to Relate the DCEL
    to city requirements 
    """

    def __init__(self, standard_rules=None, specific_rules=None):
        #Verification rules can be looked up,
        #passed in, or always applied
        assert(standard_rules is None or isinstance(rules, list))
        assert(specific_rules is None or isinstance(specific_rules, dict))
        self.standard_rules = []
        self.specific_rules = {}

        self.actors = {}
        self.current_actor = None
        
        if standard_rules is not None:
            self.standard_rules = standard_rules
        if specific_rules is not None:
            self.specific_rules.update(specific_rules)

    def choose_operator(self, operators):
        op = choice(operators)
        return op

    def verify(self, dc, delta, verify_type=None):
        logging.info("Verifying Latest Operator Tick")
        #Verify the dcel
        #where delta is the changes made this timestep
        result = verify_results.PASS
        for r in self.standard_rules:
            #apply the rule
            #result = r(dc, delta)
            continue
        if verify_type is not None and verify_type in self.specific_rules:
            for r in self.specific_rules[verify_type]:
                #apply the rule
                #result = r(dc, delta)
                continue

        if result is verify_results.SANCTION:
            #update the city state with a sanction
            self.sanction
            
        return result

    def sanction():
        logging.info("Sanctioning Actor: {}".format(self.current_actor))
