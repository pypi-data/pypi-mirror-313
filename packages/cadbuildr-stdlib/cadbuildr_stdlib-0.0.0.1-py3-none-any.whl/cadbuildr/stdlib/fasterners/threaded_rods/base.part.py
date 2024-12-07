# %%
from cadbuildr.foundation import (
    Part,
    Sketch,
    Point,
    Circle,
    Extrusion,
    show,
    Axis,
    Line,
    Lathe,
    Sweep,
    Helix3D,
    Point3D,
)
import math


class ThreadedRod(Part):
    def __init__(self, diameter, length, thread_pitch=1.25, with_thread=True):
        self.diameter = diameter
        self.length = length
        self.thread_pitch = thread_pitch
        self.with_thread = with_thread

        self.create_body()

        if with_thread:
            self.add_thread()

    def create_body(self):
        s = Sketch(self.xz())
        radius = self.diameter / 2

        s.pencil.line(radius, 0)
        s.pencil.line(0, self.length)
        s.pencil.line_to(0, self.length)
        s.pencil.line_to(0, 0)
        s.pencil.close()

        shape = s.pencil.get_closed_shape()
        axis = Axis(Line(s.origin, Point(s, 0, self.length)))
        self.add_operation(Lathe(shape, axis))

    def add_thread(self):
        # TODO simplify once threads are available in the foundation lib.
        thread_height = self.length
        H = self.thread_pitch * math.sqrt(3) / 2

        thread_radius = self.diameter / 2 - H / 4

        s = Sketch(self.xz())
        s.pencil.line_to(0, -self.thread_pitch / 2 + self.thread_pitch / 16)
        s.pencil.line_to(5 / 8 * H, -self.thread_pitch / 8)
        s.pencil.line(0, self.thread_pitch / 4)
        s.pencil.line_to(0, self.thread_pitch / 2 - self.thread_pitch / 16)

        profile = s.pencil.close()

        path = Helix3D(
            self.thread_pitch,
            thread_height - self.thread_pitch,
            thread_radius,
            center=Point3D(0, 0, self.thread_pitch / 2),
            dir=Point3D(0, 0, 1),
        )

        sweep = Sweep(profile, path)
        self.add_operation(sweep)


if __name__ == "__main__":
    show(ThreadedRod(diameter=5, length=30, thread_pitch=1.5, with_thread=True))
# %%
