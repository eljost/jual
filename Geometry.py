class Geometry:
    def __init__(self, film_thickness):
        # All lengths in cm
        self.film_thickness = film_thickness
        self.contact_length = 6e-1
        self.contact_dists = {  "5-1" : 8.5e-2,
                                "5-2" : 2.5e-2,
                                "5-3" : 5.3e-2}
