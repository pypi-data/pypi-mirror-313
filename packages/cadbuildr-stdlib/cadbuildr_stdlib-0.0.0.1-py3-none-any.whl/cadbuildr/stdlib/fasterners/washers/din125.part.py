from cadbuildr.foundation import Part, Sketch, Circle, Extrusion, show


class Washer(Part):
    def __init__(self, outer_radius=20, inner_radius=10, thickness=2):
        self.outer_radius = outer_radius
        self.inner_radius = inner_radius
        self.thickness = thickness

        self.create_washer()

    def create_washer(self):
        s = Sketch(self.xy())

        # Create outer circle
        outer_circle = Circle(s.origin, self.outer_radius)

        # Extrude the outer circle to create the washer base
        e_outer = Extrusion(outer_circle, self.thickness)
        self.add_operation(e_outer)

        # Create inner circle
        inner_circle = Circle(s.origin, self.inner_radius)

        # Extrude the inner circle with cut=True to create the hole
        e_inner = Extrusion(inner_circle, self.thickness, cut=True)
        self.add_operation(e_inner)


class DIN125Washer(Washer):
    DIN_SPECS = {
        "M1.6": {"outer_diameter": 4, "inner_radius": 1.7 / 2, "thickness": 0.3},
        "M2": {"outer_diameter": 5, "inner_radius": 2.2 / 2, "thickness": 0.3},
        "M2.5": {"outer_diameter": 6, "inner_radius": 2.7 / 2, "thickness": 0.5},
        "M3": {"outer_diameter": 7, "inner_radius": 3.2 / 2, "thickness": 0.5},
        "M4": {"outer_diameter": 9, "inner_radius": 4.3 / 2, "thickness": 0.8},
        "M5": {"outer_diameter": 10, "inner_radius": 5.3 / 2, "thickness": 1},
        "M6": {"outer_diameter": 12, "inner_radius": 6.4 / 2, "thickness": 1.6},
        "M7": {"outer_diameter": 14, "inner_radius": 7.4 / 2, "thickness": 1.6},
        "M8": {"outer_diameter": 16, "inner_radius": 8.4 / 2, "thickness": 1.6},
        "M10": {"outer_diameter": 20, "inner_radius": 10.5 / 2, "thickness": 2},
        "M12": {"outer_diameter": 24, "inner_radius": 13 / 2, "thickness": 2.5},
        "M14": {"outer_diameter": 28, "inner_radius": 15 / 2, "thickness": 2.5},
        "M16": {"outer_diameter": 30, "inner_radius": 17 / 2, "thickness": 3},
        "M18": {"outer_diameter": 34, "inner_radius": 19 / 2, "thickness": 3},
        "M20": {"outer_diameter": 37, "inner_radius": 21 / 2, "thickness": 3},
        "M22": {"outer_diameter": 39, "inner_radius": 23 / 2, "thickness": 3},
        "M24": {"outer_diameter": 44, "inner_radius": 25 / 2, "thickness": 4},
    }

    def __init__(self, size):
        if size not in self.DIN_SPECS:
            raise ValueError(f"Size '{size}' not found in DIN specifications.")

        # Retrieve dimensions from the DIN specifications
        specs = self.DIN_SPECS[size]

        # Call the superclass constructor with the retrieved dimensions
        super().__init__(
            outer_radius=specs["outer_diameter"] / 2,
            inner_radius=specs["inner_radius"],
            thickness=specs["thickness"],
        )

        # Store additional attributes specific to DIN125Washer
        self.size = size


if __name__ == "__main__":
    show(DIN125Washer(size="M6"))
