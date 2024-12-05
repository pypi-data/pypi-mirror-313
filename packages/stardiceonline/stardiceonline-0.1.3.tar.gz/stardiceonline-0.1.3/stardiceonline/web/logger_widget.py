import logging
from io import StringIO
import bokeh.models
from bokeh.layouts import column
# Configure logging to match the bokeh reporting level
bokeh_logger = logging.getLogger('bokeh')
root_logger = logging.getLogger()
root_logger.setLevel(bokeh_logger.getEffectiveLevel())
print(root_logger.getEffectiveLevel())

class ConsoleWidget():
    def __init__(self, doc):
        self.doc = doc
        self.error_monitor = bokeh.models.PreText(text="",width=800, height=200, height_policy='fixed', sizing_mode='fixed', max_height=200)
        string ='Monitor'
        class ParagraphIO(StringIO):
            def flush(self2):
                StringIO.flush(self2)
                doc.add_next_tick_callback(self.displaylog)
        self.errorstream = ParagraphIO(string)
        self.handler = logging.StreamHandler(self.errorstream)
        root_logger.addHandler(self.handler)
        bokeh_logger.addHandler(self.handler)
        self.labels = ['DEBUG', 'INFO', 'ERROR', 'CRITICAL']
        self.radio = bokeh.models.RadioButtonGroup(labels=self.labels)
        self.radio.on_event('button_click', self.set_level)
        self.radio.active = 1

    def set_level(self, new):
        root_logger.setLevel(self.labels[new.model.active])
        self.handler.setLevel(self.labels[new.model.active])
        
    def displaylog(self):
        self.error_monitor.text = '\n'.join(self.errorstream.getvalue().splitlines()[-10:])
        
    def get_widget(self):
        return column(self.radio, self.error_monitor)



# Add logging display to the application itself




    
        
