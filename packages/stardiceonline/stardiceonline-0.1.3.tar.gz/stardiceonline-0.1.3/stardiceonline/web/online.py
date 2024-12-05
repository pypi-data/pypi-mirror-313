import plot_widgets
import image_selection_widget
import science_image_widget 
import bokeh.plotting
from bokeh.layouts import row, column
import logging
import logger_widget

doc = bokeh.plotting.curdoc()

error_monitor = logger_widget.ConsoleWidget(doc)

try:
    # Monitoring plots
    axes = ['seeing',  'skylev']
    labels = ['Seeing [pixels]', 'Sky level [ADU]']
    heights = [200, 200]
    print('Preping plots')
    plots = plot_widgets.NightPlotWidgets(axes, labels, heights)

    print('science image')
    # Data preview
    preview = science_image_widget.ScienceImageWidget()

    # Directory and image selection
    print('preping selector')
    selector = image_selection_widget.ImageSelectionWidget(cd_callbacks=[plots.update_summary],
                                                           ci_callbacks=[preview.load_image])

    print('setting callbacks')
    plots.selection_callback = [selector.set_image]

    print('selecting last image')
    selector.directory_data.selected.indices = [-1]
    print('selecting last image')
    selector.last_image()
    print('forming doc')
    doc.add_periodic_callback(selector.update, 1000)
    doc.add_root(row(preview.get_widget(),
                     column(selector.get_widget(),
                            plots.get_widget(),
                            error_monitor.get_widget()
                            )
                     ))

except Exception as e:
    doc.add_root(error_monitor.get_widget())
    logging.error(e)


doc.title = 'StarDICE Online'

