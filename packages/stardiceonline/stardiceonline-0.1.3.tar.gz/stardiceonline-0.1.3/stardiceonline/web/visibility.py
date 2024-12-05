import visibility_widget
import bokeh.io
import datetime
"""
To run
bokeh serve app_visibility.py --port 5008 --dev

"""


date = datetime.datetime.now().strftime('%Y-%m-%d')
obsnight = visibility_widget.ObsNight(date)
layout = obsnight.get_widget()

doc = bokeh.io.curdoc()
doc.add_root(layout)
doc.add_periodic_callback(obsnight.callback_utcnow, 60000)


