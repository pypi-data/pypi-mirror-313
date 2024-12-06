from silica import Component


class ComponentInSubfolder(Component):
    def inline_template(self):
        return """
            <div>
                I'm component in subfolder!
            </div>
        """
