
class ZoneOperator:
    """ Operator to create a zone/face with particular characteristics """
    
    def __init__(self):
        self.deta = []
        return

    
    def operate(self, draw=True, override=False):
        """ Performs the operator, returns all changes as a list """
        self.delta = []
        #if necessary to exit early:
        #return delta

        if not draw:
            return self.delta
        
        return self.delta

    def __enter__(self):
        """ Enters the context for op parameterization """
        return

    def __exit__(self, type, value, traceback):
        """ Exits, and can unwind the operator """
        if type(value) is not None:
            logging.warning("Operator Failed, rewinding")
            self.unwind()
            
        self.delta = []
            

    def is_oneshot(self):
        return False

    def unwind(self):
        raise Exception("Unwind: Unimplemented")
