import re
from sphinx.directives.other import TocTree


def setup(app):
    app.add_config_value('toc_filter_include', [], 'html')
    app.add_directive('toctree-filt', TocTreeFilt)

class TocTreeFilt(TocTree):
    hasPat = re.compile('^\s*:(.+):(.+)$')

    def filter_entries(self, entries):
        excl = self.state.document.settings.env.config._raw_config['tags']
        filtered = []
        for e in entries:
            m = self.hasPat.match(e)
            if m != None:
                if m.groups()[0] in excl:
                    filtered.append(m.groups()[1].strip())
            else:
                filtered.append(e)
        return filtered

    def run(self):
        self.content = self.filter_entries(self.content)
        return super().run()
