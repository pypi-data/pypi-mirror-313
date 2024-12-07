from cadbuildr.foundation import *
import math


class HexNut(Part):
    def __init__(self, size, with_thread=True):
        self.size = size
        self.with_thread = with_thread

        dimensions = self.dimension_table[size]
        self.width_across_flats = dimensions["width_across_flats"]  # WAF
        self.thickness = dimensions["thickness"]
        self.nominal_diameter = dimensions["nominal_diameter"]
        self.thread_pitch = dimensions["thread_pitch"]

        self.get_body_sketch()
        if self.with_thread:
            self.add_thread()
        self.paint("grey")

    dimension_table = {
        "M3": {
            "width_across_flats": 5.5,
            "thickness": 2.4,
            "nominal_diameter": 3,
            "thread_pitch": 0.5,
        },
        "M4": {
            "width_across_flats": 7.0,
            "thickness": 3.2,
            "nominal_diameter": 4,
            "thread_pitch": 0.7,
        },
        "M5": {
            "width_across_flats": 8.0,
            "thickness": 4.0,
            "nominal_diameter": 5,
            "thread_pitch": 0.8,
        },
        "M6": {
            "width_across_flats": 10.0,
            "thickness": 5.0,
            "nominal_diameter": 6,
            "thread_pitch": 1.0,
        },
        "M8": {
            "width_across_flats": 13.0,
            "thickness": 6.5,
            "nominal_diameter": 8,
            "thread_pitch": 1.25,
        },
        "M10": {
            "width_across_flats": 16.0,
            "thickness": 8.0,
            "nominal_diameter": 10,
            "thread_pitch": 1.5,
        },
        "M12": {
            "width_across_flats": 18.0,
            "thickness": 10.0,
            "nominal_diameter": 12,
            "thread_pitch": 1.75,
        },
        "M14": {
            "width_across_flats": 21.0,
            "thickness": 11.0,
            "nominal_diameter": 14,
            "thread_pitch": 2.0,
        },
        "M16": {
            "width_across_flats": 24.0,
            "thickness": 13.0,
            "nominal_diameter": 16,
            "thread_pitch": 2.0,
        },
        "M20": {
            "width_across_flats": 30.0,
            "thickness": 16.0,
            "nominal_diameter": 20,
            "thread_pitch": 2.5,
        },
        "M24": {
            "width_across_flats": 36.0,
            "thickness": 19.0,
            "nominal_diameter": 24,
            "thread_pitch": 3.0,
        },
    }

    def get_body_sketch(self):
        sketch = Sketch(self.xy())

        side_length = self.width_across_flats / math.sqrt(3)

        for i in range(6):
            angle = math.radians(60 * i)
            x = side_length * math.cos(angle)
            y = side_length * math.sin(angle)
            if i == 0:
                sketch.pencil.move_to(x, y)
            else:
                sketch.pencil.line_to(x, y)

        hexagon_shape = sketch.pencil.close()
        e = Extrusion(hexagon_shape, self.thickness)
        self.add_operation(e)

        # Cut the inner cylindrical hole
        hole_center = Point(sketch, 0, 0)
        hole = Circle(hole_center, self.nominal_diameter / 2)
        cut_op = Extrusion(hole, self.thickness, cut=True)
        self.add_operation(cut_op)

    def add_thread(self):
        thread_height = self.thickness
        H = self.thread_pitch * math.sqrt(3) / 2
        thread_radius = self.nominal_diameter / 2 + H / 4

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
        H = pitch * math.sqrt(3) / 2
        s = Sketch(self.xz())
        s.pencil.move_to(0, -pitch / 2 + pitch / 16)
        s.pencil.line_to(-5 / 8 * H, -pitch / 8)
        s.pencil.line(0, pitch / 4)
        s.pencil.line_to(0, pitch / 2 - pitch / 16)
        profile = s.pencil.close()
        return profile


if __name__ == "__main__":
    show(HexNut(size="M6", with_thread=True))
