# %%
from cadbuildr.foundation import Part, Sketch, Point, Circle, Extrusion, show


class Shaft(Part):
    def __init__(self, diameter=10, length=100):
        self.DIAMETER = diameter
        self.LENGTH = length
        self.create_shaft()

    def create_shaft(self):
        s = Sketch(self.xy())
        center = Point(s, 0, 0)
        circle = Circle(center, self.DIAMETER / 2)
        extrusion = Extrusion(circle, self.LENGTH)
        self.add_operation(extrusion)


if __name__ == "__main__":
    show(Shaft())
# %%
