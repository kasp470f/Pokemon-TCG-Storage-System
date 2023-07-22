from models.grading_scale import getGradingScaleName

class GradingValue:
    Value = 0
    Description = None

class Corners:
    topLeft: type[GradingValue] = GradingValue()
    topRight: type[GradingValue] = GradingValue()
    bottomLeft: type[GradingValue] = GradingValue()
    bottomRight: type[GradingValue] = GradingValue()

    def score(self):
        avg = (self.topLeft.Value + self.topRight.Value + self.bottomLeft.Value + self.bottomRight.Value) / 4
        return round(avg, 1)
    

class Edges:
    top: type[GradingValue] = GradingValue()
    right: type[GradingValue] = GradingValue()
    bottom: type[GradingValue] = GradingValue()
    left: type[GradingValue] = GradingValue()

    def score(self):
        avg = (self.top.Value + self.right.Value + self.bottom.Value + self.left.Value) / 4
        return round(avg, 1)
    
class Centering:
    front: type[GradingValue] = GradingValue()
    back: type[GradingValue] = GradingValue()

    def score(self):
        avg = (self.front.Value + self.back.Value) / 2
        return round(avg, 1)

class Surface:
    front: type[GradingValue] = GradingValue()
    back: type[GradingValue] = GradingValue()

    def score(self):
        avg = (self.front.Value + self.back.Value) / 2
        return round(avg, 1)
    

class PersonalGrading:
    Corners: type[Corners] = Corners()
    Edges: type[Edges] = Edges()
    Centering: type[Centering] = Centering()
    Surface: type[Surface] = Surface()

    def totalScore(self):
        avg = (self.Corners.score() + self.Edges.score() + self.Centering.score() + self.Surface.score()) / 4
        return round(avg, 1)
    
    def totalScoreName(self):
        return getGradingScaleName(self.totalScore())