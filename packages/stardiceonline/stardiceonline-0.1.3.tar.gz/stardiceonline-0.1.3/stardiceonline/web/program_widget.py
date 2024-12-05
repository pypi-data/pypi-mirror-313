from bokeh.io import curdoc
from bokeh.layouts import column, row
import bokeh.models
from bokeh.models.widgets import Paragraph
from stardiceonline.tools.metadatamanager import MetaDataManager
from stardiceonline.tools import orgfiles
from stardiceonline.tools.datesandtimes import utctime
import logging
import io
import pickle
import base64

class ObservationProgram:
    """A class to manage and display an observational program using Bokeh."""

    def __init__(self):
        """Initialize the ObservationProgram with necessary data and UI components."""
        self.manager = MetaDataManager()
        self.set_target_list()
        self.setup_source_and_table()
        self.setup_widgets()
        self.setup_layout()

    def set_target_list(self, target_list=[]):
        """Load and prepare the target data."""
        #targets, _ = orgfiles.fromorg(self.manager.get_data('targets.org', 'http://supernovae.in2p3.fr/stardice/stardiceot1/targets.org'))
        #self.target_list = list(targets['TARGET'])
        self.target_list = target_list
        if hasattr(self, 'new_target'):
            self.new_target.options=self.target_list
            
    def setup_source_and_table(self):
        """Set up the data source and table for the Bokeh application."""
        self.source = bokeh.models.ColumnDataSource(data=dict(targets=[], times=[]))
        self.columns = [
            bokeh.models.TableColumn(field="targets", title="Target"),
            bokeh.models.TableColumn(field="times", title="Time (UTC)", formatter=bokeh.models.DateFormatter(format='%FT%H:%M'))
        ]
        self.data_table = bokeh.models.DataTable(source=self.source, columns=self.columns, 
                                                 editable=False, width=650, index_position=None, selectable=True)
        self.source.on_change('data', self.update)
        self.source.selected.on_change('indices', self.change_selection)




    def setup_widgets(self):
        """Initialize widgets for user interaction."""
        self.new_target = bokeh.models.Select(title="Target:", value="G191B2B", options=self.target_list)
        self.new_time = bokeh.models.TimePicker(title="Time (UTC):", value=utctime().time())
        self.add_button = bokeh.models.Button(label="Add Row")
        self.modify_button = bokeh.models.Button(label="Modify Row")
        self.delete_button = bokeh.models.Button(label="Delete Row")
        self.feedback = Paragraph(text="")
        self.file_input = bokeh.models.FileInput(accept=".pkl")
        # Attach button events
        self.add_button.on_click(self.add_row)
        self.modify_button.on_click(self.modify_row)
        self.delete_button.on_click(self.delete_row)
        # Attach callback to file_input value attribute change
        self.file_input.on_change('value', self.load_file_callback)

        
    def setup_layout(self):
        """Create the layout for the Bokeh document."""
        label = bokeh.models.Div(text="Observation program", 
            styles={'text-align': 'right', 'font-size': '13px', 'font-weight': 'bold', 'color': '#444444'})
        control_row = row(self.new_target, self.new_time,  
                          self.add_button, self.modify_button, self.delete_button, self.file_input)
        self.layout = column(label, control_row, self.data_table, self.feedback, name="my_table")
        
    def add_row(self):
        """Add a new row to the data table."""
        new_data = {
            'targets': [self.new_target.value], 
            'times': [utctime(self.new_time.value.hour, self.new_time.value.minute)]
        }
        self.source.stream(new_data)

    def set_table(self, targets, times):
        new_data = {
            'targets': targets, 
            'times': times,
        }
        self.source.data= new_data

    def load_file_callback(self, attr, old, new):
        # This function will run on the server
        raw_contents = self.file_input.value
        #logging.info(raw_contents)
        if raw_contents:
            # Decode the file content (base64 encoded)
            file_contents = io.BytesIO(base64.b64decode(raw_contents))
            targets = pickle.load(file_contents)
            times = pickle.load(file_contents)
            self.set_table(targets, times)



    def modify_row(self):
        """Modify the selected row in the table."""
        selected_row = self.source.selected.indices
        if selected_row:
            index = selected_row[0]
            self.source.patch({
                'targets': [(index, self.new_target.value)],
                'times': [(index, utctime(self.new_time.value.hour, self.new_time.value.minute))]
            })

    def delete_row(self):
        """Delete the selected row from the table."""
        selected_row = self.source.selected.indices
        if selected_row:
            index = selected_row[0]
            data = dict(self.source.data)
            for key in data:
                data[key].pop(index)
            self.source.data = data

    def update(self, attr, old, new):
        """Callback for when data in the source changes."""
        print("Table Updated:", self.source.data)

    def change_selection(self, attr, old_indices, new_indices):
        """Update widgets when a new row is selected in the table."""
        if new_indices:
            selected_time = self.source.data['times'][new_indices[0]]
            selected_target = self.source.data['targets'][new_indices[0]]
            self.new_target.value = selected_target
            self.new_time.value = selected_time.time()

    def add_to_document(self):
        """Add the layout to the current Bokeh document."""
        curdoc().add_root(self.layout)
        curdoc().title = "Observation program"

if __name__== '__main__':
    # Instantiate and run the ObservationProgram
    program = ObservationProgram()
    program.add_to_document()
