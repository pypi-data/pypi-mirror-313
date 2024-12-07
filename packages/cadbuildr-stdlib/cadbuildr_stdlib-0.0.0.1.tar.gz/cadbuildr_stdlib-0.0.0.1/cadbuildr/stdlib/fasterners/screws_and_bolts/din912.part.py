from cadbuildr.foundation import (
    Helix3D,
    Sweep,
    Part,
    Sketch,
    Axis,
    Line,
    Extrusion,
    Point,
    Lathe,
    show,
    Point3D,
)
import math


class Screw(Part):
    def __init__(
        self,
        head_radius=10,
        head_height=5,
        body_radius=5,
        body_height=30,
        hexagon_width=7.5,
        hexagon_depth=3,
        thread_pitch=1.25,
        with_thread=True,
    ):
        self.head_radius = head_radius
        self.head_height = head_height
        self.body_radius = body_radius
        self.body_height = body_height
        self.hexagon_width = hexagon_width
        self.hexagon_depth = hexagon_depth
        self.thread_pitch = thread_pitch
        self.with_thread = with_thread

        self.get_body_sketch()
        self.get_hexagonal_cut()

        if with_thread:
            self.add_thread()
        self.paint("grey")

    def get_body_sketch(self):
        s = Sketch(self.xz())
        H = self.thread_pitch * math.sqrt(3) / 2

        effective_body_radius = self.body_radius
        if self.with_thread:
            DELTA = 0.01
            effective_body_radius -= H / 4 + DELTA

        s.pencil.line(effective_body_radius, 0)
        s.pencil.line(0, self.body_height)
        s.pencil.line_to(self.head_radius, self.body_height)
        s.pencil.line(0, self.head_height)
        s.pencil.line_to(0, self.body_height + self.head_height)
        s.pencil.close()

        shape = s.pencil.get_closed_shape()
        axis = Axis(Line(s.origin, Point(s, 0, self.body_height + self.head_height)))
        self.add_operation(Lathe(shape, axis))

    def get_hexagonal_cut(self):
        sketch = Sketch(self.xy())

        # Calculate the side length of the hexagon
        side_length = self.hexagon_width / math.sqrt(3)

        for i in range(6):
            angle = math.radians(60 * i)
            x = side_length * math.cos(angle)
            y = side_length * math.sin(angle)
            if i == 0:
                sketch.pencil.move_to(x, y)
            else:
                sketch.pencil.line_to(x, y)

        hexagon_shape = sketch.pencil.close()

        cut_e = Extrusion(
            hexagon_shape,
            self.body_height + self.head_height - self.hexagon_depth,
            self.body_height + self.head_height,
            cut=True,
        )
        self.add_operation(cut_e)

    def add_thread(self):
        thread_height = self.body_height
        H = self.thread_pitch * math.sqrt(3) / 2

        thread_radius = self.body_radius - H / 4

        path = Helix3D(
            self.thread_pitch,
            thread_height - self.thread_pitch,
            thread_radius,
            center=Point3D(0, 0, self.thread_pitch / 2),
            dir=Point3D(0, 0, 1),
        )

        profile = self.get_thread_profile(self.thread_pitch)
        sweep = Sweep(profile, path)
        self.add_operation(sweep)

    def get_thread_profile(self, pitch):
        """https://en.wikipedia.org/wiki/Screw_thread#/media/File:ISO_and_UTS_Thread_Dimensions.svg"""
        H = pitch * math.sqrt(3) / 2
        s = Sketch(self.xz())
        s.pencil.line_to(0, -pitch / 2 + pitch / 16)
        s.pencil.line_to(5 / 8 * H, -pitch / 8)
        s.pencil.line(0, pitch / 4)
        s.pencil.line_to(0, pitch / 2 - pitch / 16)
        profile = s.pencil.close()

        # profile = s.pencil.close_with_mirror()
        return profile


# Define the DIN912Screw class
class DIN912Screw(Screw):
    # Class constant: dimension table
    dimension_table = {
        "M3": {
            "head_diameter": 5.5,
            "head_height": 3,
            "hexagon_width": 2.5,  # H2.5
            "hexagon_depth": 1.3,
            "thread_pitch": 0.5,
        },
        "M4": {
            "head_diameter": 7.0,
            "head_height": 4,
            "hexagon_width": 3,
            "hexagon_depth": 2,
            "thread_pitch": 0.7,
        },
        "M5": {
            "head_diameter": 8.5,
            "head_height": 5,
            "hexagon_width": 4,
            "hexagon_depth": 2.5,
            "thread_pitch": 0.8,
        },
        "M6": {
            "head_diameter": 10.0,
            "head_height": 6,
            "hexagon_width": 5,
            "hexagon_depth": 3,
            "thread_pitch": 1.0,
        },
        "M8": {
            "head_diameter": 13.0,
            "head_height": 8,
            "hexagon_width": 6,
            "hexagon_depth": 4,
            "thread_pitch": 1.25,
        },
        "M10": {
            "head_diameter": 16.0,
            "head_height": 10,
            "hexagon_width": 8,
            "hexagon_depth": 5,
            "thread_pitch": 1.5,
        },
        "M12": {
            "head_diameter": 18.0,
            "head_height": 12,
            "hexagon_width": 10,
            "hexagon_depth": 6,
            "thread_pitch": 1.75,
        },
        "M14": {
            "head_diameter": 21.0,
            "head_height": 14,
            "hexagon_width": 12,
            "hexagon_depth": 7,
            "thread_pitch": 2.0,
        },
        "M16": {
            "head_diameter": 24.0,
            "head_height": 16,
            "hexagon_width": 14,
            "hexagon_depth": 8,
            "thread_pitch": 2.0,
        },
        "M20": {
            "head_diameter": 30.0,
            "head_height": 20,
            "hexagon_width": 17,
            "hexagon_depth": 10,
            "thread_pitch": 2.5,
        },
        "M24": {
            "head_diameter": 36.0,
            "head_height": 24,
            "hexagon_width": 19,
            "hexagon_depth": 12,
            "thread_pitch": 3.0,
        },
    }

    def __init__(self, size, length, with_thread=True):
        if size not in self.dimension_table:
            raise ValueError(f"Size '{size}' not found in dimension table.")

        # Retrieve dimensions from the table
        dimensions = self.dimension_table[size]

        # Calculate body diameter from size
        body_diameter = float(
            size[1:]
        )  # Extract diameter from size string, e.g., 'M6' -> 6.0

        # Call the superclass constructor with the retrieved dimensions
        super().__init__(
            head_radius=dimensions["head_diameter"] / 2,
            head_height=dimensions["head_height"],
            body_radius=body_diameter / 2,
            body_height=length - dimensions["head_height"],
            hexagon_width=dimensions["hexagon_width"],
            hexagon_depth=dimensions["hexagon_depth"],
            thread_pitch=dimensions["thread_pitch"],
            with_thread=with_thread,
        )

        # Store additional attributes specific to DIN912Screw
        self.size = size
        self.length = length


if __name__ == "__main__":
    show(DIN912Screw(size="M6", length=20, with_thread=True))
