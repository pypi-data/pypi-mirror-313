import plot_widgets
import image_selection_widget
import telescope_widget
import webcam_widget
import bokeh.plotting
import program_widget
from bokeh.layouts import row, column
from stardiceonline.archive import archive
import logging
import logger_widget

#bokeh_logger = logging.getLogger('bokeh')
#root_logger = logging.getLogger()
#root_logger.setLevel(bokeh_logger.getEffectiveLevel())
#print(root_logger.getEffectiveLevel())

doc = bokeh.plotting.curdoc()
error_monitor = logger_widget.ConsoleWidget(doc)

try:
    # Meteo monitoring widget
    caxes = ['Air_temperature_C', 'Relative_humidity_%', 'Wind_speed_average_mpers', 'Rain_intensity_mmperh']
    labels = ['T [°C]', 'Humidity [%]', 'Wind [m/s]', 'Rain [mm/h]']
    heights = [100, 100, 100, 100]
    plots = plot_widgets.MeteoPlotWidgets(caxes, labels, heights)

    # Webcams
    #tube = webcam_widget.Webcam(webcam.tube)
    tube = webcam_widget.Webcam()
    #sky = webcam_widget.Webcam(webcam.allsky)

    # Program
    program = program_widget.ObservationProgram()
    
    # Telescope
    telescope = telescope_widget.TelescopeWidget(program)
    plots.update_meteo()
    telescope.update_objects()

    # Setup callbacks for live updates
    doc.add_periodic_callback(tube.update_webcam, 1000)
    doc.add_periodic_callback(plots.update_meteo, 1000*60)
    doc.add_periodic_callback(telescope.update_objects, 1000)
    

    
    #doc.add_root(tube.figure)
    doc.add_root(row(
        column(#selector.get_widget(),
            plots.get_widget(),
            error_monitor.get_widget(),
            program.layout,
        ),
        column(tube.figure,
               telescope.get_widget(),
               #sky.figure
               ),
        
    ))
    
except Exception as e:
    doc.add_root(error_monitor.get_widget())
    logging.error(e)

#plots.update_meteo(archive.local_archive.meteo_today())
doc.title = 'StarDICE Monitoring'
