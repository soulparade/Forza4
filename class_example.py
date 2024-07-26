
class Position:

    def __init__(self, x: int, y: int) -> None:
        self.__x = x
        self.y = y

    def get_x(self):
        return self.__x
    
    @staticmethod
    def constant():
        return "MY_CONSTANT"
    
    @property
    def x(self):
        return self.__x
    
    
    
p = Position(10, 11)
p.get_x()
p.x 