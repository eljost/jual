import datetime
import os
import webbrowser

from jinja2 import Environment, PackageLoader

class Output:
    def __init__(self, path):
        self.path = path
        self.env = Environment(loader=PackageLoader("jual", "templates"))
        if not self.path.endswith(os.sep):
            self.path += os.sep
        self.summary_name = "summary.html"
        self.measurements_name = "measurements"
        self.arrhenius_name = "arrhenius"
        self.contact_resist_name = "contact_resist"
        self.summary_path = self.path + self.summary_name

    def summary(self, manager):
        measurements = manager.get_all()
        contact_resists = manager.contact_resist_dict
        arrhenius = manager.arrhenius_dict
        geometry = manager.geometry
        date = datetime.datetime.now()

        template = self.env.get_template(self.summary_name)
        with open(self.summary_path, "w") as handle:
            handle.write(template.render(measurements=measurements,
                                        manager=manager,
                                        #contact_resists=contact_resists,
                                        #arrhenius=arrhenius,
                                        #geometry=geometry,
                                        date=date).encode("utf-8"))

    def measurements_raw(self, manager):
        self.write_raw(manager, self.measurements_name)
    
    def arrhenius_raw(self, manager):
        self.write_raw(manager, self.arrhenius_name)

    def contact_resist_raw(self, manager):
        self.write_raw(manager, self.contact_resist_name)

    def write_raw(self, manager, template_name):
        template = self.env.get_template(template_name)
        with open(self.path + template_name, "w") as handle:
            handle.write(template.render(manager=manager))
    
    def show_summary(self):
        try:
            firefox = webbrowser.get("firefox")
            firefox.open(self.summary_path)
        except webbrowser.Error:
            webbrowser.open(self.summary_path)
