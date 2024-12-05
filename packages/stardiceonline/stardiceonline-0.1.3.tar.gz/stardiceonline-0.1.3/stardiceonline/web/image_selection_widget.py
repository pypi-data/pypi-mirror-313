from directories import image_dirs
import bokeh.models
import bokeh.plotting
import logging

class ImageSelectionWidget():
    def __init__(self, cd_callbacks=[], ci_callbacks=[]):
        self.cd_callbacks = cd_callbacks
        self.ci_callbacks = ci_callbacks
        self.directory_data = image_dirs.get_source()
        self.columns = [
            bokeh.models.TableColumn(
                field='nights', title='Night', width=80, sortable=True),
            bokeh.models.TableColumn(
                field='images', title='#images', width=20, sortable=False),
            bokeh.models.TableColumn(
                field='catalogs', title='#catalogs', width=20, sortable=False),
            bokeh.models.TableColumn(
                field='astrom_catalogs', title='#astrom', width=20, sortable=False),
        ]
        self.directory_table = bokeh.models.DataTable(source=self.directory_data, columns=self.columns, width=800, height=120)
        self._navigation()
        self.directory_data.selected.on_change('indices', self.change_directory)
        #image_dirs.set_children_callback(self.callback)
            
    def _navigation(self):
        self.numeric_input = bokeh.models.NumericInput(value=0, title="Expnum")
        self.bnext = bokeh.models.Button(label="Next")
        self.bnext.on_event('button_click', self.next_image)
        self.bprev = bokeh.models.Button(label="Prev")
        self.bprev.on_event('button_click', self.prev_image)
        self.blast = bokeh.models.Toggle(label="Last")
        self.blast.on_event('button_click', self.last_image)
        self.numeric_input.on_change('value', self.change_image)
        
    def next_image(self):
        self.numeric_input.value = image_dirs[self.directory_data.selected.indices[0]].next(self.numeric_input.value)
        
    def prev_image(self):
        self.numeric_input.value = image_dirs[self.directory_data.selected.indices[0]].prev(self.numeric_input.value)
        
    def last_image(self):
        if self.blast.active:
            self.numeric_input.value = image_dirs[self.directory_data.selected.indices[0]].last()
        
    def change_image(self, attr, old, new):
        for c in self.ci_callbacks:
            c(image_dirs[self.directory_data.selected.indices[0]], self.numeric_input.value)
        self.blast.active = self.numeric_input.value == image_dirs[self.directory_data.selected.indices[0]].last()

    def set_image(self, expnum):
        self.numeric_input.value = expnum
        
    def change_directory(self, attr, old_indices, new_indices):
        print(f'calling back {new_indices[0]}')
        self.numeric_input.value = image_dirs[new_indices[0]].last()
        print('calling back2')
        for c in self.cd_callbacks:
            c(image_dirs[new_indices[0]])
        #display_state['Last'] = True
        
    def get_widget(self):
        return bokeh.layouts.column(self.directory_table, bokeh.layouts.row(self.numeric_input, self.bnext, self.bprev, self.blast))

    def callback(self, attr, filename):
        logging.debug('Directory content as evolved, programing update')
        bokeh.plotting.curdoc().add_next_tick_callback(self.update)
         
    def update(self):
        new_source = image_dirs.update_source()
        old_source = self.directory_data.data
        logging.debug(f'new_source={new_source}, old_source={old_source}')
        if new_source != old_source:
            logging.debug('Directory content as evolved, updating')
            self.directory_data.data = new_source
            sel = self.directory_data.selected.indices[0]
            if old_source['astrom_catalogs'][sel] != new_source['astrom_catalogs'][sel]:
                logging.debug('Current directory content as evolved, updating')
                for c in self.cd_callbacks:
                    c(image_dirs[sel])
                
            #sel = self.directory_data.selected.indices[0]
            #if old_source['images'][sel] != new_source['images'][sel]:
            #    logging.debug('New image available')
            self.last_image()
            #    plot_widgets.update_summary(summary_source, image_dirs[directory_data.selected.indices[0]].directory)

            
#def directory_table_update():
#    if new_source != old_source:
#        print('
#        directory_data.data = new_source
#        sel = directory_data.selected.indices[0]
#        #print(sel, old_source['catalogs'][sel], new_source['catalogs'][sel])
#        if old_source['astrom_catalogs'][sel] != new_source['astrom_catalogs'][sel]:
#            
#            if display_state['Last'] and (numeric_input.value != image_dirs[directory_data.selected.indices[0]].last()):
#                update_image()
#
#        old_source = new_source
#    else:
#        print('No change at all, no update')
#
#def change_directory_callback(attr, old_indices, new_indices):
#    global display_state
#    print(attr)
#    print(old_indices)
#    print(new_indices)
#    numeric_input.value = image_dirs[new_indices[0]].last()
#    display_state['Last'] = True
#    update_image()
#    plot_widegts.update_summary(summary_source, image_dirs[directory_data.selected.indices[0]].directory)
#    
#directory_data.selected.on_change('indices', change_directory_callback)
#
#        

