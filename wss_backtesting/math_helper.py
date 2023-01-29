class MathHelper():
    def __init__(self) -> None:
        pass

    def variation(self, n_inicial,n_final) -> float:                
        return (n_final - n_inicial) / n_inicial * 100
    
    def percent(self,x, y):
        if not x and not y:
            print("x = 0%\ny = 0%")
        elif x < 0 or y < 0:
            print("The inputs can't be negative!")
        else:
            final = 100 / (x + y)
            x *= final
            y *= final
            return [x,y]