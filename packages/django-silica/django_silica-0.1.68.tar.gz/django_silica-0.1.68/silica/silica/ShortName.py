from silica import Component


class ShortName(Component):
    def inline_template(self):
        return """
            <div>
                I'm component called with short name!
            </div>
        """
