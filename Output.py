import os

from jinja2 import Environment, PackageLoader

class Output:
    def __init__(self, path):
        self.path = path
        self.env = Environment(loader=PackageLoader("jual", "templates"))
        if not self.path.endswith(os.sep):
            self.path += os.sep

    def summary(self, manager):
        measurements = manager.get_all()
        contact_resists = manager.contact_resist_dict
        arrhenius = manager.arrhenius_dict
        geometry = manager.geometry

        template = self.env.get_template("summary.html")
        with open(self.path + "summary.html", "w") as handle:
            handle.write(template.render(measurements=measurements,
                                        contact_resists=contact_resists,
                                        arrhenius=arrhenius,
                                        geometry=geometry))
