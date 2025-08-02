
class Demands:
    def __init__(self) -> None:
        self.main_demand:str = ''
        self.reverse_order: bool = False



    def demands_set(self) -> bool:
        if self.main_demand:
            return True
        return False

