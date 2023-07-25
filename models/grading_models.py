from models.grading_scale import getGradingScaleName
from enum import Enum

class AreaEnum(Enum):
    Corners = 1
    Edges = 2
    Centering = 3
    Surface = 4

class GradingValue:
    Value = 0
    Description = None

class Corners:
    topLeft: GradingValue = GradingValue()
    topRight: GradingValue = GradingValue()
    bottomLeft: GradingValue = GradingValue()
    bottomRight: GradingValue = GradingValue()

    def score(self):
        avg = (self.topLeft.Value + self.topRight.Value + self.bottomLeft.Value + self.bottomRight.Value) / 4
        return round(avg, 1)
    

class Edges:
    top: GradingValue = GradingValue()
    right: GradingValue = GradingValue()
    bottom: GradingValue = GradingValue()
    left: GradingValue = GradingValue()

    def score(self):
        avg = (self.top.Value + self.right.Value + self.bottom.Value + self.left.Value) / 4
        return round(avg, 1)
    
class Centering:
    front: GradingValue = GradingValue()
    back: GradingValue = GradingValue()

    def score(self):
        avg = (self.front.Value + self.back.Value) / 2
        return round(avg, 1)

class Surface:
    front: GradingValue = GradingValue()
    back: GradingValue = GradingValue()

    def score(self):
        avg = (self.front.Value + self.back.Value) / 2
        return round(avg, 1)
    

class RawGrading:
    Corners: Corners = Corners()
    Edges: Edges = Edges()
    Centering: Centering = Centering()
    Surface: Surface = Surface()

    def totalScore(self):
        avg = (self.Corners.score() + self.Edges.score() + self.Centering.score() + self.Surface.score()) / 4
        if avg.is_integer():
            return int(avg)
        else:
            return round(avg, 1)
    
    def totalScoreName(self):
        return getGradingScaleName(self.totalScore())