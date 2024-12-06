# Import the libraries
import ipyvuetify as v
import ipywidgets as widgets
from IPython.display import display, HTML
from ipywidgets import Layout
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
from seeq import spy
import numpy as np
from datetime import datetime, timedelta
import pytz
import plotly.graph_objects as go
from configparser_crypt import ConfigParserCrypt
import os
import logging

spy.options.friendly_exceptions = False
colors = {
    'app_bar': '#007960',
    'controls_background': '#F6F6F6',
    'visualization_background': '#FFFFFF',
    'seeq_primary': '#007960',
    'slider_selected': '#007960',
    'slider_track_unselected': '#BDBDBD'
}


def on_change(change):
    selected_value = change['new']
    return selected_value


def convert_datetime(time):
    date_time = time
    if not isinstance(date_time, datetime):
        date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
    cet = pytz.timezone('Europe/Berlin')
    if date_time.tzinfo is None:
        date_time = date_time.replace(tzinfo=cet)
    return date_time


def Clean_Events_List(Events_List, start_time, end_time):
    List = list(map(list, zip(*[Events_List['Capsule Start'], Events_List['Capsule End']])))
    List = [[convert_datetime(row[0]), convert_datetime(row[1])] for row in List]
    # List=sorted(List, key=lambda row: row[0])

    if pd.isna(List[0][0]):
        List[0][0] = start_time
    if pd.isna(List[-1][1]):
        List[-1][1] = end_time
    return List


def CreateSlider():
    slider = v.Slider(color=colors['slider_selected'], track_color=colors['slider_track_unselected'],
                      thumb_color=colors['slider_selected'], thumb_label=True, model='range',
                      style_='max-width: 120px; align-self: center;', class_="mt-3", height='80px',
                      dense=True, step=1, min=0, max=100, v_model=[0, 1])
    return slider


def Progress_Layout(text, progress, indicator):
    layout = v.Container(style_='max-width: 120px; align-self: top;',
                         children=[v.Row(children=[v.Col(children=[text, v.Spacer(), progress, v.Spacer(), indicator],
                                                         class_='text-center')])])

    return layout


def create_progress_widget(type_):
    if type_ == 'Circular':
        progress_icon = v.ProgressCircular(size=100, width=10, color='primary', value=0, rotate=-90)
    elif type_ == 'Linear':
        progress_icon = v.ProgressLinear(size=100, width=800, height=100, color='primary', value=0,
                                         style_='transform: rotate(-90deg)')
    return progress_icon


# License Creation Function
def create_license(expire_date, trial_version):
    file = 'Addon_License.encrypted'
    conf_file = ConfigParserCrypt()

    # Create new AES key
    conf_file.aes_key = b'\xfd\xa2G7}s\xe3F\xf9b\xc3{\x82M\xbbg\xc14\xce\xf5\xca[\x0c\xe0\xe5\xd15BY\xc8:\xe1'
    aes_key = conf_file.aes_key

    # Use like normal configparser class
    conf_file.add_section('CONFIGURATION')
    conf_file['CONFIGURATION']['ExpirationDate'] = expire_date
    conf_file['CONFIGURATION']['TrialVersion'] = trial_version

    # Write encrypted config file
    with open(file, 'wb') as file_handle:
        conf_file.write_encrypted(file_handle)


def check_license(host):
    file = 'Addon_License.encrypted'
    if not os.path.isfile(file):
        # Use host parameter
        api_url = "https://sds-2-ematica.it/LicenseManager/License"
        payload = {
            'Addon': 'EA_PCA',
            'Host': host
        }
        username = 'LicenseWS'
        password = 'bw&q7QnvX`^r$<g-:(A6as'
        response = requests.post(api_url, json=payload, auth=HTTPBasicAuth(username, password))
        print(response)
        response = response.json()
        expire_date = response['expirationDate']
        trial_version = response['featureParameters']['Trial']

        create_license(expire_date, trial_version)
    else:
        conf_file = ConfigParserCrypt()
        # Set AES key
        conf_file.aes_key = b'\xfd\xa2G7}s\xe3F\xf9b\xc3{\x82M\xbbg\xc14\xce\xf5\xca[\x0c\xe0\xe5\xd15BY\xc8:\xe1'

        # Read encrypted config file
        conf_file.read_encrypted(file)
        expire_date = conf_file['CONFIGURATION']['ExpirationDate']
        Trial = conf_file['CONFIGURATION']['TrialVersion']
        expire_date = datetime.strptime(expire_date[:19], "%Y-%m-%dT%H:%M:%S")

    # Import current time
    today = datetime.now()
    return today > expire_date, Trial, expire_date


def define_context_info():
    display(HTML('''
    <style>
    .absolute-position {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        padding: 0;
        margin: 0;
    }
    .bold-text {
        font-weight: bold;
    }
    .no-header {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    </style>
    '''))

    additional_styles = """
        <style>
        #appmode-leave {display: none;}
        .background_box { background-color:#007960 !important; } 
        .js-plotly-plot .plotly .modebar-btn[data-title="Produced with Plotly"] {display: none;}
        .vuetify-styles .theme--light.v-list-item .v-list-item__action-text, 
        .vuetify-styles .theme--light.v-list-item .v-list-item__subtitle {color: #212529;}
        .vuetify-styles .theme--light.v-list-item:not(.v-list-item--active):not(.v-list-item--disabled) 
        {color: #007960 !important;}
        .vuetify-styles .v-label {font-size: 14px;}
        .vuetify-styles .v-application {font-family: "Source Sans Pro","Helvetica Neue",Helvetica,Arial,sans-serif;}
        .v-snack {position: absolute !important;top: -470px;right: 0 !important; left: unset !important;}
        </style>"""

    v.theme.themes.light.success = '#007960'
    v.theme.themes.light.primary = '#007960'


class PCA_Widget_Addon:

    def __init__(self, host, url, workbook_id, worksheet_id):
        # Prepare interface to display any error with snackbar
        self.snackbar = v.Snackbar(v_model=False, children=['The value entered is not a float between 0 and 1!'],
                                   color='error')
        self.snackbar.hide()

        # License variable
        [self.expired, self.trial_version, self.expiration_date] = check_license(host)
        self.expiration_date = self.expiration_date.strftime("%Y/%m/%d")

        define_context_info()
        # Retrieve workbook parameters
        self.url = url
        self.workbook_id = workbook_id
        self.worksheet_id = worksheet_id

        # Initiate initialization variables
        self.current_page = 'Batch'
        self.current_index = 1
        self.plots = []
        self.plot_trend = []
        self.anomalies = []
        self.total_observations = []

        # Create selection variables widgets
        self.Signals_training_dropdown = self.Create_DropDownBox("Train Condition")
        self.Signals_Master_testing_dropdown = self.Create_DropDownBox("Batch Condition")
        self.Signals_testing_dropdown = self.Create_DropDownBox("Phase Condition")

        # Define LAUNCH BOX
        self.Save_Output = v.Switch(v_model=False, label="", persistent_hint=False, color='#007960',
                                    flat=False, small=True, inset=True)  # , class_='mr-3 mb-5')

        self.Save_Output_Box = v.Html(tag='div', dense=True, class_='d-flex flex-row', children=
        [v.Html(tag='h12', children=['Save Output'], class_='mt-6 bold-text'),
         v.Spacer(), self.Save_Output])

        self.Launch_PCA = v.Btn(dark=True, color=colors['seeq_primary'], children=['Launch PCA'],  # v_on='x.on',
                                class_='align-self-center', style_='text-transform: capitalize;')
        self.Launch_PCA.on_event('click', lambda widget, event,
                                                 data: self.submit_formula())
        self.Launch_PCA.disabled = True
        self.Launch_Box = v.Html(tag='div', dense=True, filled=True, color=colors['controls_background'],
                                 class_='d-flex flex-column justify-left align-top',
                                 style_=f"max-width: 350px; max-height: 900px; vertical-align: middle; background-color: {colors['controls_background']}; opacity: 1",
                                 children=[self.Save_Output_Box,
                                           self.Launch_PCA,
                                           v.Spacer()])  # No Spacer, close spacing with ml-2 on second field
        start_time, end_time = self.find_worksheet_items()

        # Create base widgets

        # Create Time Variables with their basic dependencies
        self.train_end_time = self.create_time_widget('End Time', end_time)
        self.train_start_time = self.create_time_widget('Start Time', start_time)
        self.test_end_time = self.create_time_widget('End Time', end_time)
        self.test_start_time = self.create_time_widget('Start Time', start_time)
        # Organize base time variables on widget layout
        self.train_time = self.create_time_box(self.train_start_time, self.train_end_time)
        self.test_time = self.create_time_box(self.test_start_time, self.test_end_time)
        # Create control buttons
        self.Batch = self.CreateUpdatePageButton('Batch', 'seeq_primary')
        self.Phases = self.CreateUpdatePageButton('Phases', 'seeq_primary')

        self.toggle_single = v.BtnToggle(v_model=2, class_='mr-3 mb-5', children=[self.Batch, self.Phases])
        self.MasterSignal_Box_Header = v.Html(
            tag='div', dense=True, class_='d-flex flex-row', children=[v.Html(tag='h12',
                                                                              children=['Test Condition'],
                                                                              class_='bold-text'), v.Spacer(),
                                                                       self.toggle_single])

        # Define Master Signal Box
        self.MasterSignal_Box = v.Html(tag='div', dense=True, class_='d-flex flex-column',
                                       style_=f"max-width: 350px; max-height: 900; vertical-align: middle; background-color: {colors['controls_background']}; opacity: 1",
                                       children=[v.Spacer(),
                                                 v.Html(tag='h12', children=['Train Condition'], class_='bold-text'),
                                                 self.train_time, v.Spacer(), self.Signals_training_dropdown,
                                                 v.Spacer(), self.MasterSignal_Box_Header,
                                                 self.test_time, v.Spacer(), self.Signals_Master_testing_dropdown,
                                                 self.Signals_testing_dropdown])

        # Create fundamental variables for PARAMETER SELECTION and their dependencies
        self.time_min = self.create_text_field('Minutes', '1', 'mr-3', self.validate_text_field)
        self.time_sec = self.create_text_field('Seconds', '0', 'ml-3', self.validate_text_field)
        self.time_shifts_container = v.Html(tag='div', class_='d-flex flex-row',
                                            children=[self.time_min, self.time_sec])

        self.pca_reduction = CreateSlider()
        self.value_box = v.TextField(color=colors['seeq_primary'], dense=False,
                                     style_='max-width: 60px;max-: 40px; font-size: small; align-self: center;',
                                     shaped=False,
                                     hide_details="auto", filled=True, solo=True, classes='mb-3 mt-4', v_model='0')

        self.pca_red_container = v.Html(tag='div', dense=True, class_='d-flex flex-row align-center',
                                        children=[v.Html(tag='h12', children=['Data Reduction'], class_="bold-text",
                                                         style_='align-self: center;'), v.Spacer(), self.pca_reduction,
                                                  self.value_box])

        self.pca_reduction.observe(self.update_box, 'v_model')
        self.value_box.observe(self.update_slider, 'v_model')

        self.PCA_Parameters_box = v.Html(tag='div', dense=True, filled=True, outlined=True,
                                         color=colors['controls_background'],
                                         class_='d-flex flex-column justify-top align-left',
                                         style_=f"max-width: 350px; vertical-align: middle; background-color: {colors['controls_background']}; opacity: 1",
                                         children=[v.Spacer(),
                                                   v.Html(tag='h12', children=['Time Interpolation'],
                                                          class_='bold-text'),
                                                   self.time_shifts_container,
                                                   self.pca_red_container]
                                         # No Spacer, close spacing with ml-2 on second field
                                         )

        self.appBar = v.AppBar(color=colors['app_bar'], dark=True, dense=True,
                               children=[v.ToolbarTitle(children=['PCA Analysis'])])
        # Create plot widgets
        trace = go.Scatter(
            x=[],
            y=[],
            mode='lines+markers',
        )

        # Layout for the plot
        layout = go.Layout(
            title="PCA Error",
            xaxis=dict(title='X Axis'),
            yaxis=dict(title='Y Axis')
        )

        # Create figure and display it
        self.error_plot = go.FigureWidget(data=[trace], layout=layout)
        self.error_plot.layout.paper_bgcolor = 'rgba(0,0,0,0)'
        self.error_plot.layout.plot_bgcolor = 'rgba(0,0,0,0)'
        self.error_plot.layout.dragmode = False
        self.error_plot.update_layout(
            modebar_remove=["autoScale2d", "autoscale", "pan", "pan2d", "pan3d", "reset", "toImage", "toimage",
                            "select", "select2d", "lasso", "lasso2d", "reset",
                            "select", "select2d", "zoom", "zoom2d", "zoomIn2d", "zoomin", "zoomout"])

        self.anomaly_title = v.Html(tag='div', children=["Anomalies detected"], class_='text-h4')
        self.anomaly_bar = create_progress_widget('Linear')
        self.anomaly_indicator = v.Html(tag='div', children=["0/0"], class_='text-h4')

        self.anomaly_box = Progress_Layout(self.anomaly_title, self.anomaly_bar, self.anomaly_indicator)

        # Create Loading Widgets
        self.progress_train = create_progress_widget('Circular')
        self.progress_master = create_progress_widget('Circular')

        self.train_title = v.Html(tag='div', children=["Train Progress"], class_='text-h4')
        self.master_title = v.Html(tag='div', children=["Test Progress"], class_='text-h4')

        self.train_indicator = v.Html(tag='div', children=["0/0 events processed"], class_='text-h4')
        self.master_indicator = v.Html(tag='div', children=["0/0 events processed"], class_='text-h4')

        self.Ptrain_Box = Progress_Layout(self.train_title, self.progress_train, self.train_indicator)

        self.Pmaster_Box = Progress_Layout(self.master_title, self.progress_master, self.master_indicator)

        # Create a layout to combine the text, progress icon, and number
        self.Progress_Indicator = v.Html(tag='div', dense=True, filled=True, color=colors['controls_background'],
                                         class_='d-flex flex-row justify-left align-top',
                                         children=[self.Ptrain_Box, self.Pmaster_Box],
                                         layout=Layout(display='flex', align_items='center', justify_content='center'))

        self.plot_error = widgets.Output(style={'height': '800px'}, layout=Layout(
            width='800px'))  # widgets.Output(layout=Layout(width='800px', height='800px'))

        # Define bar chart trace without any scatter-specific parameters
        trace = go.Bar(
            x=[],  # Categories
            y=[],  # Values
            marker=dict(color='blue')  # Optional: Set bar color
        )

        # Define layout for the plot
        layout = go.Layout(
            title="PCA Contributions",
            xaxis=dict(title='Categories'),
            yaxis=dict(title='Values'),
            bargap=0.2  # Gap between bars
        )

        self.barchart = go.FigureWidget(data=[trace], layout=layout)
        self.barchart.layout.paper_bgcolor = 'rgba(0,0,0,0)'
        self.barchart.layout.plot_bgcolor = 'rgba(0,0,0,0)'
        self.barchart.layout.dragmode = False
        self.barchart.update_layout(
            modebar_remove=["autoScale2d", "autoscale", "pan", "pan2d", "pan3d", "reset", "toImage", "toimage",
                            "select", "select2d", "lasso", "lasso2d", "reset",
                            "select", "select2d", "zoom", "zoom2d", "zoomIn2d", "zoomin", "zoomout"])

        self.plot_bar = widgets.Output(style={'height': '800px'},
                                       layout=Layout(width='800px'))  # widgets.Output(layout=Layout(width='800px'))

        self.Contrib = self.CreateUpdatePageButton('Root Cause Analysis', 'seeq_primary')
        self.Err = self.CreateUpdatePageButton('Anomaly Detection', 'seeq_primary')

        self.event_slider = v.Slider(color=colors['slider_selected'], track_color=colors['slider_track_unselected'],
                                     thumb_color=colors['slider_selected'], outlined=True, filled=True,
                                     thumb_label=True, label="Pick Event: ",
                                     model='range', height='80px', dense=True, step=1, min=0, max=10, v_model=1)
        self.event_slider.v_model = 0
        self.event_slider.observe(lambda change: self.Switch_Page(self.current_page, change['new']), names='v_model')

        self.bottom_row = v.Html(tag='div', dense=True, class_='inline-flex d-flex flex-row',
                                 children=[v.Html(tag='div', style_="min-width: 250px", filled=True, outlined=True,
                                                  children=[self.event_slider]),
                                           v.Spacer(),
                                           v.BtnToggle(v_model=2, class_='mr-3', children=[self.Contrib, self.Err])])

        self.anomaly_detection_plots = v.Html(tag='div', dense=True, class_='d-flex flex-row',
                                              children=[self.plot_error, self.anomaly_box])

        self.Fig_Plot = v.Html(
            tag='div',
            dense=True,
            class_='d-flex flex-column align-self: top',
            style_='padding=10px',
            children=[self.plot_bar, self.anomaly_detection_plots, self.bottom_row])

        self.trial_box = v.Card(
            children=[
                v.CardText(children=[f"Trial valid up to {self.expiration_date}"],
                           style_='font-weight: bold; font-size: 16px;')
            ],
            style_='background-color: white; border: 4px solid #CC7722; border-radius: 10px; padding: 10px; height: 50px; display: flex; align-items: center; justify-content: flex-end;'
        )

        self.Left_Box = v.Html(tag='div', dense=True, filled=True, outlined=True, color=colors['controls_background'],
                               class_='d-flex flex-column', style_="max-width: 350px;",
                               children=[self.MasterSignal_Box,
                                         self.PCA_Parameters_box,
                                         self.Launch_Box, self.trial_box])
        if not self.trial_version:
            self.trial_box.hide()

        self.SettingsBar = v.Html(tag='div', dense=True, filled=True, outlined=True,
                                  color=colors['controls_background'],
                                  class_='d-flex flex-column no-header',
                                  children=[self.appBar, v.Html(tag='div', dense=True, filled=True,
                                                                outlined=True, color=colors['controls_background'],
                                                                class_='d-flex flex-row justify-left align-left',
                                                                children=[self.Left_Box, self.Progress_Indicator,
                                                                          self.Fig_Plot, self.snackbar])])

        if not self.expired:
            self.Switch_Page(self.current_page, self.current_index)
        else:
            self.diasble_notification = v.Card(
                children=[
                    v.CardText(children=["License Expired please contact us at software@e-matica"],
                               style_='font-weight: bold; font-size: 20px;')],
                style_='background-color: white; border: 4px solid #8B0000; border-radius: 10px; padding: 10px; height: 50px; display: flex; align-items: center; justify-content: flex-end;'
            )

            self.SettingsBar = v.Html(tag='div', dense=True, filled=True, outlined=True,
                                      color=colors['controls_background'],
                                      class_='d-flex flex-column no-header',
                                      children=[self.appBar, self.diasble_notification, self.snackbar])

            display(self.SettingsBar)
            self.ThrowError("License Expired contact as at am_addon@e-matica.com")

    # Widget Creation Function
    def create_text_field(self, label, initial_value, class_name, validate_func):
        text_field = v.TextField(class_=class_name, color=colors['seeq_primary'], v_model=initial_value, disabled=False,
                                 label=label, style_="max-width=120px;")
        text_field.observe(lambda *args: validate_func(text_field, *args), 'v_model')

        return text_field

    def CreateUpdatePageButton(self, page_name, color):
        button = v.Btn(dark=True, color=colors[color], small=True, style_='text-transform: capitalize;',
                       v_model=True, children=[page_name])
        button.on_event('click', lambda *args: self.Switch_Page(page_name, self.current_index))
        return button

    def Create_DropDownBox(self, label):
        widget = v.Select(
            dense=True,
            outlined=True,
            label=label,
            color=colors['seeq_primary'],
            v_model=None,
            return_object=True
        )
        widget.observe(self.check_if_button_should_be_enabled, 'v_model')
        return widget

    def create_time_box(self, start, end):
        widget = v.Html(
            tag='div',
            dense=True,
            class_='d-flex flex-row',
            style_="max-width: 350px;",
            children=[start, end])
        return widget

    def create_time_widget(self, label, time):
        widget = v.TextField(
            class_='ml-3',
            color='#00695C',
            v_model=time,
            disabled=False,
            label=label,
            hint='YYYY-MM-DD hh:mm:ss',
            style_="max-width=120px;"
        )
        widget.observe(lambda *args: self.validate_time(widget, *args), 'v_model')
        widget.observe(self.check_if_button_should_be_enabled, 'v_model')
        return widget

    # Define control conditions
    def update_box(self, *args):
        self.value_box.v_model = self.pca_reduction.v_model
        return

    def update_slider(self, *args):
        self.pca_reduction.v_model = self.value_box.v_model
        return

    def validate_text_field(self, widget, *args):
        try:
            # Try converting the value to float
            float(widget.v_model)
            widget.error = False
            widget.error_messages = []
            self.snackbar.v_model = False
        except ValueError:
            # If conversion fails, show an error message
            widget.error = True
            widget.error_messages = ['This value is not a float!']
            self.snackbar.children = ['This value is not a float!']
            self.snackbar.v_model = True

    def validate_time(self, widget, *args):
        try:
            # Try converting the value to datetime
            datetime.strptime(str(widget.v_model), '%Y-%m-%d %H:%M:%S')
            widget.error = False
            widget.error_messages = []
        except ValueError:
            # If conversion fails, show an error message
            widget.error = True
            widget.error_messages = ['Incorrect time format!']

    def check_if_button_should_be_enabled(self, *args):
        try:
            # Validate date formats
            datetime.strptime(str(self.test_start_time.v_model), '%Y-%m-%d %H:%M:%S')
            datetime.strptime(str(self.test_end_time.v_model), '%Y-%m-%d %H:%M:%S')
            datetime.strptime(str(self.train_start_time.v_model), '%Y-%m-%d %H:%M:%S')
            datetime.strptime(str(self.train_end_time.v_model), '%Y-%m-%d %H:%M:%S')
            # Enable or disable the button based on dropdown values
            self.Launch_PCA.disabled = (
                    self.Signals_training_dropdown.v_model is None or
                    self.Signals_Master_testing_dropdown.v_model is None or
                    (self.current_page == 'Phases' and self.Signals_testing_dropdown.v_model is None))
        except ValueError:
            self.Launch_PCA.disabled = True

    def find_worksheet_items(self):
        start_time, end_time = [], []
        self.Signals_training_dropdown.items = ''
        self.Signals_testing_dropdown.items = ''
        self.Signals_Master_testing_dropdown.items = ''

        try:
            workbooks_df = spy.workbooks.search({'ID': self.workbook_id}, quiet=True)

            # Pull the workbook details
            workbooks = spy.workbooks.pull(workbooks_df, quiet=True)

            # Find the specific worksheet
            worksheet = None
            for wb in workbooks:
                for ws in wb.worksheets:
                    if ws.id == self.worksheet_id:
                        worksheet = ws
                        break
                if worksheet:
                    break

            if worksheet:
                # Extract start and end times
                start_time = str(worksheet.display_range['Start']).replace('T', ' ')[0:19]
                end_time = str(worksheet.display_range['End']).replace('T', ' ')[0:19]
                meta_items = spy.search(self.url, quiet=True)

                signals = meta_items.loc[meta_items.Type.str.contains('Condition')]
                self.Signals_training_dropdown.items = signals['Name'].tolist()
                self.Signals_testing_dropdown.items = signals['Name'].tolist()
                self.Signals_Master_testing_dropdown.items = signals['Name'].tolist()

        except:

            self.ThrowError("Database not found")
        return start_time, end_time

    # FUNCTION for the navigation inside of the app
    def Switch_Page(self, Page, index=0):
        self.current_page = Page
        self.current_index = index

        if Page == 'Batch':
            self.Signals_testing_dropdown.hide()
            self.event_slider.hide()
            self.Contrib.hide()
            self.Err.hide()

            self.Ptrain_Box.hide()
            self.Pmaster_Box.hide()
            self.anomaly_box.hide()

            self.plot_bar.layout.display = 'none'
            self.plot_error.layout.display = 'none'


        elif Page == 'Phases':
            self.Signals_testing_dropdown.show()
            self.event_slider.hide()
            self.Contrib.hide()
            self.Err.hide()

            self.Ptrain_Box.hide()
            self.Pmaster_Box.hide()
            self.anomaly_box.hide()

            self.plot_bar.layout.display = 'none'
            self.plot_error.layout.display = 'none'

        elif Page == 'Root Cause Analysis':
            self.Ptrain_Box.hide()
            self.Pmaster_Box.hide()
            self.anomaly_box.hide()

            self.plot_bar.clear_output()
            self.plot_error.clear_output()
            self.barchart = self.plots[self.current_index]

            with self.plot_bar:
                self.barchart.show()

            self.plot_bar.layout.display = 'block'
            self.plot_error.layout.display = 'none'

            self.event_slider.show()
            self.Contrib.show()
            self.Err.show()
        elif Page == 'Anomaly Detection':
            self.Ptrain_Box.hide()
            self.Pmaster_Box.hide()

            anomalies = self.anomalies[self.current_index]
            observations = self.total_observations[self.current_index]
            self.anomaly_title.children = [f'Anomalies detected']
            self.anomaly_bar.v_model = 100 * anomalies / observations
            self.anomaly_indicator.children = [f'{anomalies}/{observations}']

            self.plot_bar.clear_output()
            self.plot_error.clear_output()
            self.error_plot = self.plot_trend[self.current_index]

            with self.plot_error:
                self.error_plot.show()

            self.plot_bar.layout.display = 'none'
            self.plot_error.layout.display = 'block'
            self.anomaly_box.show()

            self.event_slider.show()
            self.Contrib.show()
            self.Err.show()
        elif Page == 'Training':
            self.Contrib.hide()
            self.Err.hide()

            self.plot_bar.layout.display = 'none'
            self.plot_error.layout.display = 'none'
            self.event_slider.hide()

            self.Ptrain_Box.show()
            self.Pmaster_Box.show()
        return display(self.SettingsBar)

    def clear_plot_section(self):
        self.Progress_Indicator.hide()
        self.Ptrain_Box.hide()
        self.Pmaster_Box.hide()
        self.progress_train.hide()
        self.progress_master.hide()
        self.train_title.hide()
        self.master_title.hide()
        self.train_indicator.hide()
        self.master_indicator.hide()

        self.Contrib.hide()
        self.Err.hide()
        self.event_slider.hide()
        self.plot_error.layout.display = 'none'
        self.plot_bar.layout.display = 'none'

    def ThrowError(self, full_error_message):
        self.Launch_PCA.loading = False
        self.snackbar.children = [full_error_message]
        self.snackbar.v_model = True
        self.snackbar.show()

    # ANALYSIS FORMULAS
    def CleanTable(self, X):

        try:
            nan_positions = np.argwhere(np.isnan(X))
        except Exception as e:
            full_error_message = "All signals must be int, bool or float. Please avoid using strings signals for analysis"
            self.ThrowError(full_error_message)
            return -1, -1

        NaNs_0 = [tuple(pos) for pos in nan_positions]
        NaNs_0 = sorted(NaNs_0, key=lambda x: x[0], reverse=True)
        seen = set()
        unique_rows = []
        for row in NaNs_0:
            if row[0] not in seen:
                unique_rows.append(row)
                seen.add(row[0])
        try:
            for NaN in unique_rows:
                X.pop(NaN[0])
        except Exception as e:
            full_error_message = "Training period contains too many NaN vals. Calculation cannot be performed. Please widen the training period"
            self.ThrowError(full_error_message)
            return -1, -1

        return X, unique_rows

    def submit_formula(self):
        self.Launch_PCA.loading = True
        train_start = self.train_start_time.v_model
        train_end = self.train_end_time.v_model
        test_start = self.test_start_time.v_model
        test_end = self.test_end_time.v_model
        train_signal = self.Signals_training_dropdown.v_model
        m_test_signal = self.Signals_Master_testing_dropdown.v_model
        test_signal = self.Signals_testing_dropdown.v_model

        self.current_page = 'Training'
        self.current_index = 1
        self.Switch_Page(self.current_page, self.current_index)
        max_plots = []
        try:
            max_plots = 1
            Results = []
            PCA_Error_Index = []

            meta_items = spy.search(self.url, all_properties=True, quiet=True, include_archived=True)

            Items = meta_items.loc[meta_items.Type.str.contains('Signal', regex=False)]

            original_names = Items['Name'].tolist()
            names = [name + '_PCA_Contrib' for name in Items['Name'].tolist()]

            train_start_date = convert_datetime(train_start)
            train_end_date = convert_datetime(train_end)
            test_start_date = convert_datetime(test_start)
            test_end_date = convert_datetime(test_end)

            same_name = True
            GridTime = str(60 * float(self.time_min.v_model) + float(self.time_sec.v_model)) + "s"

            #########################################TRAINING SECTION#################################################
            # return
            Event_Name = meta_items.loc[meta_items.Name.str.contains(str(train_signal), regex=False)]
            Events = spy.pull(Event_Name, start=train_start_date, end=train_end_date, header='Name')
            total_train = len(Events)
            if len(Events) == 0:
                self.ThrowError("No events detected on the training period. Please widen the Training Period Time")
                self.Launch_PCA.loading = False

            self.train_indicator.children = [f"0/{total_train} events processed"]

            Periods = Clean_Events_List(Events, train_start_date, train_end_date)

            X_table = []

            F = 0
            for current_train, period in enumerate(Periods):
                start0 = train_start_date if isinstance(period[0], pd._libs.tslibs.nattype.NaTType) else period[
                    0].strftime('%Y-%m-%d %H:%M:%S')
                end0 = train_end_date if isinstance(period[1], pd._libs.tslibs.nattype.NaTType) else period[1].strftime(
                    '%Y-%m-%d %H:%M:%S')

                Events = spy.pull(Items, grid=GridTime, start=start0, end=end0, header='Name', quiet=True)
                X_table = X_table + Events.values.tolist()
                self.progress_train.value = 100 * (current_train + 1) / total_train
                self.train_indicator.children = [f"{(current_train + 1)}/{total_train} events processed"]

            X_Table_Train, NaNs = self.CleanTable(X_table)
            if X_Table_Train == -1:
                return True
            from sklearn.decomposition import PCA
            from sklearn.preprocessing import StandardScaler

            perccontribution = True
            reduction_perc = self.pca_reduction.v_model / 100
            csvtable_train = np.array(X_Table_Train, dtype=float)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(csvtable_train)

            fidelity = [0, 0]

            if float(self.pca_reduction.v_model) == 0:

                for i in range(0, 100):

                    red = 0.15 + 0.7 * i / 100

                    n_comp = max(2, int(float(red) * len(csvtable_train[0])) - 1)
                    # Create PCA object
                    pca = PCA(n_components=n_comp)

                    # Fit PCA to the scaled data
                    pca.fit(X_scaled)

                    X_pca = pca.transform(X_scaled)

                    fidelity.append(round(100 * sum(pca.explained_variance_ratio_), 6))
                    fid_diff = float(fidelity[-2]) - float(fidelity[-1])

                    if fid_diff > -1 and fid_diff != 0:
                        reduction_perc = red
                        break
                self.pca_reduction.v_model = red * 100
            else:
                n_comp = max(2, int(float(reduction_perc) * len(csvtable_train[0])) - 1)
                # Create PCA object
                pca = PCA(n_components=n_comp)
                # Fit PCA to the scaled data
                pca.fit(X_scaled)

                X_pca = pca.transform(X_scaled)

            covariance_matrix = np.cov(X_pca, rowvar=False)
            inverse_covariance_matrix = np.linalg.inv(covariance_matrix)
            hotelling_t2 = np.zeros(X_pca.shape[0])
            for i in range(X_pca.shape[0]):
                hotelling_t2[i] = np.dot(X_pca[i], np.dot(inverse_covariance_matrix, X_pca[i]))

            # Hotelling's T^2 contribution can be interpreted as a chi-squared distribution
            alpha = 0.05
            threshold = np.percentile(hotelling_t2, 100 * (1 - alpha))  # formula custom implementabile pt.1

            ####################################################################TESTING####################################################################################
            Event_Master_Name = meta_items.loc[meta_items.Name.str.contains
            (str(m_test_signal), regex=False)]

            Events_Master = spy.pull(Event_Master_Name,
                                     start=test_start_date,
                                     end=test_end_date, header='Name', quiet=True)

            if len(Events_Master) == 0:
                self.ThrowError("No events detected on the testing period. Please widen the Testing Period Time")
                self.Launch_PCA.loading = False

            Master_Periods = Clean_Events_List(Events_Master, test_start_date, test_end_date)

            total_test = 1
            if self.current_page == 'Phases':
                Event_Name = meta_items.loc[meta_items.Name.str.contains
                (str(test_signal), regex=False)]
                Events = spy.pull(Event_Name, grid=GridTime, start=test_start_date,
                                  end=test_end_date, header='Name', quiet=True)
                total_test = len(Periods)
                if len(Events) == 0:
                    self.ThrowError(
                        "No phase events detected on the testing period. Please widen the Testing Period Time")
                    self.Launch_PCA.loading = False

                Periods = Clean_Events_List(Events, test_start_date, test_end_date)

            X_table_test = []
            X_Time = []
            total_master = len(Master_Periods)

            self.master_indicator.children = [f"0/0 events processed"]
            for current_master, Master in enumerate(Master_Periods):
                X_Master, X_Master_Time = [], []

                start_master = test_start_date if isinstance(Master[0],
                                                             pd._libs.tslibs.nattype.NaTType) else convert_datetime(
                    Master[0])
                end_master = test_end_date if isinstance(Master[1],
                                                         pd._libs.tslibs.nattype.NaTType) else convert_datetime(
                    Master[1])

                if self.current_page == 'Phases':
                    write = 0
                    for current_test, period in enumerate(Periods):
                        start_period = test_start_date if isinstance(period[0],
                                                                     pd._libs.tslibs.nattype.NaTType) else convert_datetime(
                            period[0])
                        end_period = test_end_date if isinstance(period[1],
                                                                 pd._libs.tslibs.nattype.NaTType) else convert_datetime(
                            period[1])
                        if end_period >= start_master and start_period <= end_master:
                            write = 1
                            if start_period < start_master:
                                check, start0, end0 = 1, start_master, end_period
                            elif end_period > end_master:
                                check, start0, end0 = 2, start_period, end_master
                            else:
                                check, start0, end0 = 0, start_period, end_period

                            Events = spy.pull(Items, grid=GridTime, start=start0, end=end0, header='Name', quiet=True)
                            X_Master += Events.values.tolist()
                            X_Master_Time.extend(Events.index.tolist())

                    self.progress_master.value = 100 * (current_master + 1) / total_master
                    self.master_indicator.children = [f"{(current_master + 1)}/{total_master} events processed"]


                else:
                    write = 1
                    start0, end0 = start_master, end_master
                    Events = spy.pull(Items, grid=GridTime, start=start0, end=end0, header='Name', quiet=True)
                    X_Master += Events.values.tolist()
                    X_Master_Time.extend(Events.index.tolist())
                    self.progress_master.value = 100 * (current_master + 1) / total_master
                    self.master_indicator.children = [f"{(current_master + 1)}/{total_master} events processed"]

                if write:
                    X_table_test.append(X_Master)
                    X_Time.append([x.timestamp() for x in X_Master_Time])

            Timestamps = []
            tot_len = 0
            max_plots = len(X_table_test)
            Time_Clean = []
            for iteration, X in enumerate(X_table_test):
                try:
                    start_batch_time = datetime.utcfromtimestamp(X_Time[iteration][0]).strftime('%Y-%m-%d %H:%M:%S')
                    X_Table_Test, NaNs = self.CleanTable(X)
                    if X_Table_Test == -1:
                        return True

                    X_Table_Time = X_Time[iteration]
                    for NaN in NaNs:
                        X_Table_Time.pop(NaN[0])

                    X_float = np.array(X_Table_Test, dtype=float)
                    X_Scaled = scaler.fit_transform(X_float)
                    # print(X_Table_Test)

                    X_pca = pca.transform(X_Scaled)

                    # hotelling's
                    covariance_matrix = np.cov(X_pca, rowvar=False)

                    # Calculate the inverse of the covariance matrix
                    inverse_covariance_matrix = np.linalg.inv(covariance_matrix)
                    # Calculate Hotelling's T^2 for each data point
                    hotelling_t2 = np.zeros(X_pca.shape[0])
                    for i in range(X_pca.shape[0]):
                        hotelling_t2[i] = np.dot(X_pca[i], np.dot(inverse_covariance_matrix, X_pca[i]))

                    hotelling_t2_total = np.mean(hotelling_t2) / threshold

                    ####################################################################REPORTING####################################################################################

                    # Calculate the contribution of each data point
                    contribution = hotelling_t2 / threshold
                    event_anomalies = len([value for value in contribution if value > 1])

                    self.anomalies.append(event_anomalies)
                    self.total_observations.append(len(contribution))
                    plot_time = [i for i in range(len(contribution))]

                    # print("Plotting Hotelling")
                    # Plot the temporal contributions
                    LocalTimes = []
                    A0 = (Master_Periods[iteration][0])
                    B0 = (datetime.fromtimestamp(X_Table_Time[0]))
                    hours = float(str(A0)[11:13]) - float(str(B0)[11:13])
                    LocalTimes = [datetime.fromtimestamp(B) + timedelta(hours=hours) for B in
                                  X_Table_Time]  # Timestamp aggiornato al tempo locale

                    PCA_Error_Index.extend(contribution)
                    Time_Clean.extend(LocalTimes)

                    trace = go.Scatter(
                        x=LocalTimes,
                        y=contribution,
                        mode='lines+markers',
                    )

                    # Layout for the plot
                    layout = go.Layout(
                        title=f"PCA Error at {start_batch_time}, with mean hotelling for period: {round(hotelling_t2_total, 3)}",
                        xaxis=dict(title='Observation Index'),
                        yaxis=dict(title="Hotelling's T^2 Contribution")
                    )

                    # Create figure and display it
                    hotel = go.FigureWidget(data=[trace], layout=layout)
                    hotel.layout.height = 550
                    hotel.layout.paper_bgcolor = 'rgba(0,0,0,0)'
                    hotel.layout.plot_bgcolor = 'rgba(0,0,0,0)'
                    hotel.layout.dragmode = "select"
                    hotel.update_layout(
                        modebar_remove=["autoScale2d", "autoscale", "pan", "pan2d", "pan3d", "reset", "toImage",
                                        "toimage",
                                        "select", "select2d", "lasso", "lasso2d", "reset",
                                        "select", "select2d", "zoom", "zoom2d", "zoomIn2d", "zoomout"])

                    self.plot_trend.append(hotel)

                    bar_var = np.dot((pca.components_.T) ** 2, np.diag(inverse_covariance_matrix))
                    bar_var = bar_var / np.sum(bar_var)

                    trace = go.Bar(
                        x=original_names,  # Categories
                        y=bar_var,  # Values
                        marker=dict(color='blue')  # Optional: Set bar color
                    )

                    # Define layout for the plot
                    layout = go.Layout(
                        title=f"PCA Contributions at {start_batch_time}",
                        xaxis=dict(title='Categories'),
                        yaxis=dict(title='Values'),
                        bargap=0.2  # Gap between bars
                    )

                    barchart = go.FigureWidget(data=[trace], layout=layout)
                    barchart.layout.height = 550
                    barchart.layout.paper_bgcolor = 'rgba(0,0,0,0)'
                    barchart.layout.plot_bgcolor = 'rgba(0,0,0,0)'
                    barchart.layout.dragmode = "select"
                    barchart.update_layout(
                        modebar_remove=["autoScale2d", "autoscale", "pan", "pan2d", "pan3d", "reset", "toImage",
                                        "toimage",
                                        "select", "select2d", "lasso", "lasso2d", "reset",
                                        "select", "select2d", "zoom", "zoom2d", "zoomIn2d", "zoomin", "zoomout"])

                    self.plots.append(barchart)
                    # print("calculation completed 5")
                    fidelity = round(100 * sum(pca.explained_variance_ratio_), 2)
                    # print("finished PCA")

                    time = pd.Timestamp(datetime.strptime(str(Master_Periods[iteration][1])[0:19], '%Y-%m-%d %H:%M:%S'))
                    Timestamps.append(time.tz_localize('UTC'))
                    Results.append(bar_var)
                    tot_len = tot_len + len(X_table_test)
                except Exception as e:
                    full_error_message = f"{e}"  # \nError occurred at: {line_number}"
                    self.ThrowError(full_error_message)

            if len(self.plots) == 0 and self.current_page == 'Phases':
                self.ThrowError("No Phases found in Batch capsules")
                return
            elif len(self.plots) == 0:
                self.ThrowError("No Batch capsules  found in time range")
                return
            self.event_slider.max = max_plots - 1
            if self.Save_Output.v_model:
                headers = names

                ws = []
                wb = []

                # Define your data
                title = "PCA_CONTRIBUTION_ANALYSIS"
                OUTPUT = pd.DataFrame(data=Results, columns=headers, index=Timestamps)
                OUTPUT.index = pd.to_datetime(OUTPUT.index)

                # Push the new data to Seeq
                push_output = spy.push(data=OUTPUT, workbook=self.workbook_id, worksheet=title, quiet=True)

                # Search for the workbook
                workbooks_df = spy.workbooks.search({'ID': self.workbook_id}, quiet=True)

                # Pull the workbook that contains the worksheet you want to update
                wb = spy.workbooks.pull(workbooks_df, quiet=True)[0]

                # Find the worksheet by title
                wsheet = next((ws for ws in wb.worksheets if ws.name == title), None)

                if wsheet:
                    # Update the worksheet with the new data
                    wsheet.display_items = push_output
                else:
                    # Create a new worksheet if it doesn't exist
                    new_worksheet = spy.workbooks.Worksheet(name=title, display_items=push_output)
                    wb.worksheets.append(new_worksheet)

                # Push the updated workbook back to Seeq
                spy.workbooks.push(wb, quiet=True)
                title = "PCA_Error_ANALYSIS"
                OUTPUT_Error = pd.DataFrame(data=PCA_Error_Index, columns=['PCA_Deviation_Index'], index=Time_Clean)
                OUTPUT_Error.index = pd.to_datetime(OUTPUT_Error.index)

                spy.push(data=OUTPUT_Error, workbook=self.workbook_id, worksheet=title, quiet=True)

                title = "PCA_Error_ANALYSIS"
                OUTPUT_Error = pd.DataFrame(data=PCA_Error_Index, columns=['PCA_Deviation_Index'], index=Time_Clean)
                OUTPUT_Error.index = pd.to_datetime(OUTPUT_Error.index)

                spy.push(data=OUTPUT_Error, workbook=self.workbook_id, worksheet=title, quiet=True)

            self.current_page = 'Root Cause Analysis'
            self.current_index = 1

            self.Switch_Page(self.current_page, self.current_index)

        except Exception as e:
            full_error_message = f"{e}"  # \nError occurred at: {line_number}"
            self.ThrowError(full_error_message)
            # Error.show()
        self.Launch_PCA.loading = False
        return True


# Import the libraries
import ipyvuetify as v
import ipywidgets as widgets
from IPython.display import display, HTML
from ipywidgets import Layout
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
from seeq import spy
import numpy as np
from datetime import datetime, timedelta
import pytz
import plotly.graph_objects as go
from configparser_crypt import ConfigParserCrypt
import os
import logging

spy.options.friendly_exceptions = False
colors = {
    'app_bar': '#007960',
    'controls_background': '#F6F6F6',
    'visualization_background': '#FFFFFF',
    'seeq_primary': '#007960',
    'slider_selected': '#007960',
    'slider_track_unselected': '#BDBDBD'
}


def on_change(change):
    selected_value = change['new']
    return selected_value


def convert_datetime(time):
    date_time = time
    if not isinstance(date_time, datetime):
        date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
    cet = pytz.timezone('Europe/Berlin')
    if date_time.tzinfo is None:
        date_time = date_time.replace(tzinfo=cet)
    return date_time


def Clean_Events_List(Events_List, start_time, end_time):
    List = list(map(list, zip(*[Events_List['Capsule Start'], Events_List['Capsule End']])))
    List = [[convert_datetime(row[0]), convert_datetime(row[1])] for row in List]
    # List=sorted(List, key=lambda row: row[0])

    if pd.isna(List[0][0]):
        List[0][0] = start_time
    if pd.isna(List[-1][1]):
        List[-1][1] = end_time
    return List


def CreateSlider():
    slider = v.Slider(color=colors['slider_selected'], track_color=colors['slider_track_unselected'],
                      thumb_color=colors['slider_selected'], thumb_label=True, model='range',
                      style_='max-width: 120px; align-self: center;', class_="mt-3", height='80px',
                      dense=True, step=1, min=0, max=100, v_model=[0, 1])
    return slider


def Progress_Layout(text, progress, indicator):
    layout = v.Container(style_='max-width: 120px; align-self: top;',
                         children=[v.Row(children=[v.Col(children=[text, v.Spacer(), progress, v.Spacer(), indicator],
                                                         class_='text-center')])])

    return layout


def create_progress_widget(type_):
    if type_ == 'Circular':
        progress_icon = v.ProgressCircular(size=100, width=10, color='primary', value=0, rotate=-90)
    elif type_ == 'Linear':
        progress_icon = v.ProgressLinear(size=100, width=800, height=100, color='primary', value=0,
                                         style_='transform: rotate(-90deg)')
    return progress_icon


# License Creation Function
def create_license(expire_date, trial_version):
    file = 'Addon_License.encrypted'
    conf_file = ConfigParserCrypt()

    # Create new AES key
    conf_file.aes_key = b'\xfd\xa2G7}s\xe3F\xf9b\xc3{\x82M\xbbg\xc14\xce\xf5\xca[\x0c\xe0\xe5\xd15BY\xc8:\xe1'
    aes_key = conf_file.aes_key

    # Use like normal configparser class
    conf_file.add_section('CONFIGURATION')
    conf_file['CONFIGURATION']['ExpirationDate'] = expire_date
    conf_file['CONFIGURATION']['TrialVersion'] = trial_version

    # Write encrypted config file
    with open(file, 'wb') as file_handle:
        conf_file.write_encrypted(file_handle)


def check_license(host):
    file = 'Addon_License.encrypted'
    if not os.path.isfile(file):
        # Use host parameter
        api_url = "https://sds-2-ematica.it/LicenseManager/License"
        payload = {
            'Addon': 'EA_PCA',
            'Host': host
        }
        username = 'LicenseWS'
        password = 'bw&q7QnvX`^r$<g-:(A6as'
        response = requests.post(api_url, json=payload, auth=HTTPBasicAuth(username, password))
        print(response)
        response = response.json()
        expire_date = response['expirationDate']
        trial_version = response['featureParameters']['Trial']

        create_license(expire_date, trial_version)
    else:
        conf_file = ConfigParserCrypt()
        # Set AES key
        conf_file.aes_key = b'\xfd\xa2G7}s\xe3F\xf9b\xc3{\x82M\xbbg\xc14\xce\xf5\xca[\x0c\xe0\xe5\xd15BY\xc8:\xe1'

        # Read encrypted config file
        conf_file.read_encrypted(file)
        expire_date = conf_file['CONFIGURATION']['ExpirationDate']
        Trial = conf_file['CONFIGURATION']['TrialVersion']
        expire_date = datetime.strptime(expire_date[:19], "%Y-%m-%dT%H:%M:%S")

    # Import current time
    today = datetime.now()
    return today > expire_date, Trial, expire_date


def define_context_info():
    display(HTML('''
    <style>
    .absolute-position {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        padding: 0;
        margin: 0;
    }
    .bold-text {
        font-weight: bold;
    }
    .no-header {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    </style>
    '''))

    additional_styles = """
        <style>
        #appmode-leave {display: none;}
        .background_box { background-color:#007960 !important; } 
        .js-plotly-plot .plotly .modebar-btn[data-title="Produced with Plotly"] {display: none;}
        .vuetify-styles .theme--light.v-list-item .v-list-item__action-text, 
        .vuetify-styles .theme--light.v-list-item .v-list-item__subtitle {color: #212529;}
        .vuetify-styles .theme--light.v-list-item:not(.v-list-item--active):not(.v-list-item--disabled) 
        {color: #007960 !important;}
        .vuetify-styles .v-label {font-size: 14px;}
        .vuetify-styles .v-application {font-family: "Source Sans Pro","Helvetica Neue",Helvetica,Arial,sans-serif;}
        .v-snack {position: absolute !important;top: -470px;right: 0 !important; left: unset !important;}
        </style>"""

    v.theme.themes.light.success = '#007960'
    v.theme.themes.light.primary = '#007960'


class PCA_Widget_Addon:

    def __init__(self, host, url, workbook_id, worksheet_id):
        # Prepare interface to display any error with snackbar
        self.snackbar = v.Snackbar(v_model=False, children=['The value entered is not a float between 0 and 1!'],
                                   color='error')
        self.snackbar.hide()

        # License variable
        [self.expired, self.trial_version, self.expiration_date] = check_license(host)
        self.expiration_date = self.expiration_date.strftime("%Y/%m/%d")

        define_context_info()
        # Retrieve workbook parameters
        self.url = url
        self.workbook_id = workbook_id
        self.worksheet_id = worksheet_id

        # Initiate initialization variables
        self.current_page = 'Batch'
        self.current_index = 1
        self.plots = []
        self.plot_trend = []
        self.anomalies = []
        self.total_observations = []

        # Create selection variables widgets
        self.Signals_training_dropdown = self.Create_DropDownBox("Train Condition")
        self.Signals_Master_testing_dropdown = self.Create_DropDownBox("Batch Condition")
        self.Signals_testing_dropdown = self.Create_DropDownBox("Phase Condition")

        # Define LAUNCH BOX
        self.Save_Output = v.Switch(v_model=False, label="", persistent_hint=False, color='#007960',
                                    flat=False, small=True, inset=True)  # , class_='mr-3 mb-5')

        self.Save_Output_Box = v.Html(tag='div', dense=True, class_='d-flex flex-row', children=
        [v.Html(tag='h12', children=['Save Output'], class_='mt-6 bold-text'),
         v.Spacer(), self.Save_Output])

        self.Launch_PCA = v.Btn(dark=True, color=colors['seeq_primary'], children=['Launch PCA'],  # v_on='x.on',
                                class_='align-self-center', style_='text-transform: capitalize;')
        self.Launch_PCA.on_event('click', lambda widget, event,
                                                 data: self.submit_formula())
        self.Launch_PCA.disabled = True
        self.Launch_Box = v.Html(tag='div', dense=True, filled=True, color=colors['controls_background'],
                                 class_='d-flex flex-column justify-left align-top',
                                 style_=f"max-width: 350px; max-height: 900px; vertical-align: middle; background-color: {colors['controls_background']}; opacity: 1",
                                 children=[self.Save_Output_Box,
                                           self.Launch_PCA,
                                           v.Spacer()])  # No Spacer, close spacing with ml-2 on second field
        start_time, end_time = self.find_worksheet_items()

        # Create base widgets

        # Create Time Variables with their basic dependencies
        self.train_end_time = self.create_time_widget('End Time', end_time)
        self.train_start_time = self.create_time_widget('Start Time', start_time)
        self.test_end_time = self.create_time_widget('End Time', end_time)
        self.test_start_time = self.create_time_widget('Start Time', start_time)
        # Organize base time variables on widget layout
        self.train_time = self.create_time_box(self.train_start_time, self.train_end_time)
        self.test_time = self.create_time_box(self.test_start_time, self.test_end_time)
        # Create control buttons
        self.Batch = self.CreateUpdatePageButton('Batch', 'seeq_primary')
        self.Phases = self.CreateUpdatePageButton('Phases', 'seeq_primary')

        self.toggle_single = v.BtnToggle(v_model=2, class_='mr-3 mb-5', children=[self.Batch, self.Phases])
        self.MasterSignal_Box_Header = v.Html(
            tag='div', dense=True, class_='d-flex flex-row', children=[v.Html(tag='h12',
                                                                              children=['Test Condition'],
                                                                              class_='bold-text'), v.Spacer(),
                                                                       self.toggle_single])

        # Define Master Signal Box
        self.MasterSignal_Box = v.Html(tag='div', dense=True, class_='d-flex flex-column',
                                       style_=f"max-width: 350px; max-height: 900; vertical-align: middle; background-color: {colors['controls_background']}; opacity: 1",
                                       children=[v.Spacer(),
                                                 v.Html(tag='h12', children=['Train Condition'], class_='bold-text'),
                                                 self.train_time, v.Spacer(), self.Signals_training_dropdown,
                                                 v.Spacer(), self.MasterSignal_Box_Header,
                                                 self.test_time, v.Spacer(), self.Signals_Master_testing_dropdown,
                                                 self.Signals_testing_dropdown])

        # Create fundamental variables for PARAMETER SELECTION and their dependencies
        self.time_min = self.create_text_field('Minutes', '1', 'mr-3', self.validate_text_field)
        self.time_sec = self.create_text_field('Seconds', '0', 'ml-3', self.validate_text_field)
        self.time_shifts_container = v.Html(tag='div', class_='d-flex flex-row',
                                            children=[self.time_min, self.time_sec])

        self.pca_reduction = CreateSlider()
        self.value_box = v.TextField(color=colors['seeq_primary'], dense=False,
                                     style_='max-width: 60px;max-: 40px; font-size: small; align-self: center;',
                                     shaped=False,
                                     hide_details="auto", filled=True, solo=True, classes='mb-3 mt-4', v_model='0')

        self.pca_red_container = v.Html(tag='div', dense=True, class_='d-flex flex-row align-center',
                                        children=[v.Html(tag='h12', children=['Data Reduction'], class_="bold-text",
                                                         style_='align-self: center;'), v.Spacer(), self.pca_reduction,
                                                  self.value_box])

        self.pca_reduction.observe(self.update_box, 'v_model')
        self.value_box.observe(self.update_slider, 'v_model')

        self.PCA_Parameters_box = v.Html(tag='div', dense=True, filled=True, outlined=True,
                                         color=colors['controls_background'],
                                         class_='d-flex flex-column justify-top align-left',
                                         style_=f"max-width: 350px; vertical-align: middle; background-color: {colors['controls_background']}; opacity: 1",
                                         children=[v.Spacer(),
                                                   v.Html(tag='h12', children=['Time Interpolation'],
                                                          class_='bold-text'),
                                                   self.time_shifts_container,
                                                   self.pca_red_container]
                                         # No Spacer, close spacing with ml-2 on second field
                                         )

        self.appBar = v.AppBar(color=colors['app_bar'], dark=True, dense=True,
                               children=[v.ToolbarTitle(children=['PCA Analysis'])])
        # Create plot widgets
        trace = go.Scatter(
            x=[],
            y=[],
            mode='lines+markers',
        )

        # Layout for the plot
        layout = go.Layout(
            title="PCA Error",
            xaxis=dict(title='X Axis'),
            yaxis=dict(title='Y Axis')
        )

        # Create figure and display it
        self.error_plot = go.FigureWidget(data=[trace], layout=layout)
        self.error_plot.layout.paper_bgcolor = 'rgba(0,0,0,0)'
        self.error_plot.layout.plot_bgcolor = 'rgba(0,0,0,0)'
        self.error_plot.layout.dragmode = False
        self.error_plot.update_layout(
            modebar_remove=["autoScale2d", "autoscale", "pan", "pan2d", "pan3d", "reset", "toImage", "toimage",
                            "select", "select2d", "lasso", "lasso2d", "reset",
                            "select", "select2d", "zoom", "zoom2d", "zoomIn2d", "zoomin", "zoomout"])

        self.anomaly_title = v.Html(tag='div', children=["Anomalies detected"], class_='text-h4')
        self.anomaly_bar = create_progress_widget('Linear')
        self.anomaly_indicator = v.Html(tag='div', children=["0/0"], class_='text-h4')

        self.anomaly_box = Progress_Layout(self.anomaly_title, self.anomaly_bar, self.anomaly_indicator)

        # Create Loading Widgets
        self.progress_train = create_progress_widget('Circular')
        self.progress_master = create_progress_widget('Circular')

        self.train_title = v.Html(tag='div', children=["Train Progress"], class_='text-h4')
        self.master_title = v.Html(tag='div', children=["Test Progress"], class_='text-h4')

        self.train_indicator = v.Html(tag='div', children=["0/0 events processed"], class_='text-h4')
        self.master_indicator = v.Html(tag='div', children=["0/0 events processed"], class_='text-h4')

        self.Ptrain_Box = Progress_Layout(self.train_title, self.progress_train, self.train_indicator)

        self.Pmaster_Box = Progress_Layout(self.master_title, self.progress_master, self.master_indicator)

        # Create a layout to combine the text, progress icon, and number
        self.Progress_Indicator = v.Html(tag='div', dense=True, filled=True, color=colors['controls_background'],
                                         class_='d-flex flex-row justify-left align-top',
                                         children=[self.Ptrain_Box, self.Pmaster_Box],
                                         layout=Layout(display='flex', align_items='center', justify_content='center'))

        self.plot_error = widgets.Output(style={'height': '800px'}, layout=Layout(
            width='800px'))  # widgets.Output(layout=Layout(width='800px', height='800px'))

        # Define bar chart trace without any scatter-specific parameters
        trace = go.Bar(
            x=[],  # Categories
            y=[],  # Values
            marker=dict(color='blue')  # Optional: Set bar color
        )

        # Define layout for the plot
        layout = go.Layout(
            title="PCA Contributions",
            xaxis=dict(title='Categories'),
            yaxis=dict(title='Values'),
            bargap=0.2  # Gap between bars
        )

        self.barchart = go.FigureWidget(data=[trace], layout=layout)
        self.barchart.layout.paper_bgcolor = 'rgba(0,0,0,0)'
        self.barchart.layout.plot_bgcolor = 'rgba(0,0,0,0)'
        self.barchart.layout.dragmode = False
        self.barchart.update_layout(
            modebar_remove=["autoScale2d", "autoscale", "pan", "pan2d", "pan3d", "reset", "toImage", "toimage",
                            "select", "select2d", "lasso", "lasso2d", "reset",
                            "select", "select2d", "zoom", "zoom2d", "zoomIn2d", "zoomin", "zoomout"])

        self.plot_bar = widgets.Output(style={'height': '800px'},
                                       layout=Layout(width='800px'))  # widgets.Output(layout=Layout(width='800px'))

        self.Contrib = self.CreateUpdatePageButton('Root Cause Analysis', 'seeq_primary')
        self.Err = self.CreateUpdatePageButton('Anomaly Detection', 'seeq_primary')

        self.event_slider = v.Slider(color=colors['slider_selected'], track_color=colors['slider_track_unselected'],
                                     thumb_color=colors['slider_selected'], outlined=True, filled=True,
                                     thumb_label=True, label="Pick Event: ",
                                     model='range', height='80px', dense=True, step=1, min=0, max=10, v_model=1)
        self.event_slider.v_model = 0
        self.event_slider.observe(lambda change: self.Switch_Page(self.current_page, change['new']), names='v_model')

        self.bottom_row = v.Html(tag='div', dense=True, class_='inline-flex d-flex flex-row',
                                 children=[v.Html(tag='div', style_="min-width: 250px", filled=True, outlined=True,
                                                  children=[self.event_slider]),
                                           v.Spacer(),
                                           v.BtnToggle(v_model=2, class_='mr-3', children=[self.Contrib, self.Err])])

        self.anomaly_detection_plots = v.Html(tag='div', dense=True, class_='d-flex flex-row',
                                              children=[self.plot_error, self.anomaly_box])

        self.Fig_Plot = v.Html(
            tag='div',
            dense=True,
            class_='d-flex flex-column align-self: top',
            style_='padding=10px',
            children=[self.plot_bar, self.anomaly_detection_plots, self.bottom_row])

        self.trial_box = v.Card(
            children=[
                v.CardText(children=[f"Trial valid up to {self.expiration_date}"],
                           style_='font-weight: bold; font-size: 16px;')
            ],
            style_='background-color: white; border: 4px solid #CC7722; border-radius: 10px; padding: 10px; height: 50px; display: flex; align-items: center; justify-content: flex-end;'
        )

        self.Left_Box = v.Html(tag='div', dense=True, filled=True, outlined=True, color=colors['controls_background'],
                               class_='d-flex flex-column', style_="max-width: 350px;",
                               children=[self.MasterSignal_Box,
                                         self.PCA_Parameters_box,
                                         self.Launch_Box, self.trial_box])
        if not self.trial_version:
            self.trial_box.hide()

        self.SettingsBar = v.Html(tag='div', dense=True, filled=True, outlined=True,
                                  color=colors['controls_background'],
                                  class_='d-flex flex-column no-header',
                                  children=[self.appBar, v.Html(tag='div', dense=True, filled=True,
                                                                outlined=True, color=colors['controls_background'],
                                                                class_='d-flex flex-row justify-left align-left',
                                                                children=[self.Left_Box, self.Progress_Indicator,
                                                                          self.Fig_Plot, self.snackbar])])

        if not self.expired:
            self.Switch_Page(self.current_page, self.current_index)
        else:
            self.diasble_notification = v.Card(
                children=[
                    v.CardText(children=["License Expired please contact us at software@e-matica"],
                               style_='font-weight: bold; font-size: 20px;')],
                style_='background-color: white; border: 4px solid #8B0000; border-radius: 10px; padding: 10px; height: 50px; display: flex; align-items: center; justify-content: flex-end;'
            )

            self.SettingsBar = v.Html(tag='div', dense=True, filled=True, outlined=True,
                                      color=colors['controls_background'],
                                      class_='d-flex flex-column no-header',
                                      children=[self.appBar, self.diasble_notification, self.snackbar])

            display(self.SettingsBar)
            self.ThrowError("License Expired contact as at am_addon@e-matica.com")

    # Widget Creation Function
    def create_text_field(self, label, initial_value, class_name, validate_func):
        text_field = v.TextField(class_=class_name, color=colors['seeq_primary'], v_model=initial_value, disabled=False,
                                 label=label, style_="max-width=120px;")
        text_field.observe(lambda *args: validate_func(text_field, *args), 'v_model')

        return text_field

    def CreateUpdatePageButton(self, page_name, color):
        button = v.Btn(dark=True, color=colors[color], small=True, style_='text-transform: capitalize;',
                       v_model=True, children=[page_name])
        button.on_event('click', lambda *args: self.Switch_Page(page_name, self.current_index))
        return button

    def Create_DropDownBox(self, label):
        widget = v.Select(
            dense=True,
            outlined=True,
            label=label,
            color=colors['seeq_primary'],
            v_model=None,
            return_object=True
        )
        widget.observe(self.check_if_button_should_be_enabled, 'v_model')
        return widget

    def create_time_box(self, start, end):
        widget = v.Html(
            tag='div',
            dense=True,
            class_='d-flex flex-row',
            style_="max-width: 350px;",
            children=[start, end])
        return widget

    def create_time_widget(self, label, time):
        widget = v.TextField(
            class_='ml-3',
            color='#00695C',
            v_model=time,
            disabled=False,
            label=label,
            hint='YYYY-MM-DD hh:mm:ss',
            style_="max-width=120px;"
        )
        widget.observe(lambda *args: self.validate_time(widget, *args), 'v_model')
        widget.observe(self.check_if_button_should_be_enabled, 'v_model')
        return widget

    # Define control conditions
    def update_box(self, *args):
        self.value_box.v_model = self.pca_reduction.v_model
        return

    def update_slider(self, *args):
        self.pca_reduction.v_model = self.value_box.v_model
        return

    def validate_text_field(self, widget, *args):
        try:
            # Try converting the value to float
            float(widget.v_model)
            widget.error = False
            widget.error_messages = []
            self.snackbar.v_model = False
        except ValueError:
            # If conversion fails, show an error message
            widget.error = True
            widget.error_messages = ['This value is not a float!']
            self.snackbar.children = ['This value is not a float!']
            self.snackbar.v_model = True

    def validate_time(self, widget, *args):
        try:
            # Try converting the value to datetime
            datetime.strptime(str(widget.v_model), '%Y-%m-%d %H:%M:%S')
            widget.error = False
            widget.error_messages = []
        except ValueError:
            # If conversion fails, show an error message
            widget.error = True
            widget.error_messages = ['Incorrect time format!']

    def check_if_button_should_be_enabled(self, *args):
        try:
            # Validate date formats
            datetime.strptime(str(self.test_start_time.v_model), '%Y-%m-%d %H:%M:%S')
            datetime.strptime(str(self.test_end_time.v_model), '%Y-%m-%d %H:%M:%S')
            datetime.strptime(str(self.train_start_time.v_model), '%Y-%m-%d %H:%M:%S')
            datetime.strptime(str(self.train_end_time.v_model), '%Y-%m-%d %H:%M:%S')
            # Enable or disable the button based on dropdown values
            self.Launch_PCA.disabled = (
                    self.Signals_training_dropdown.v_model is None or
                    self.Signals_Master_testing_dropdown.v_model is None or
                    (self.current_page == 'Phases' and self.Signals_testing_dropdown.v_model is None))
        except ValueError:
            self.Launch_PCA.disabled = True

    def find_worksheet_items(self):
        start_time, end_time = [], []
        self.Signals_training_dropdown.items = ''
        self.Signals_testing_dropdown.items = ''
        self.Signals_Master_testing_dropdown.items = ''

        try:
            workbooks_df = spy.workbooks.search({'ID': self.workbook_id}, quiet=True)

            # Pull the workbook details
            workbooks = spy.workbooks.pull(workbooks_df, quiet=True)

            # Find the specific worksheet
            worksheet = None
            for wb in workbooks:
                for ws in wb.worksheets:
                    if ws.id == self.worksheet_id:
                        worksheet = ws
                        break
                if worksheet:
                    break

            if worksheet:
                # Extract start and end times
                start_time = str(worksheet.display_range['Start']).replace('T', ' ')[0:19]
                end_time = str(worksheet.display_range['End']).replace('T', ' ')[0:19]
                meta_items = spy.search(self.url, quiet=True)

                signals = meta_items.loc[meta_items.Type.str.contains('Condition')]
                self.Signals_training_dropdown.items = signals['Name'].tolist()
                self.Signals_testing_dropdown.items = signals['Name'].tolist()
                self.Signals_Master_testing_dropdown.items = signals['Name'].tolist()

        except:

            self.ThrowError("Database not found")
        return start_time, end_time

    # FUNCTION for the navigation inside of the app
    def Switch_Page(self, Page, index=0):
        self.current_page = Page
        self.current_index = index

        if Page == 'Batch':
            self.Signals_testing_dropdown.hide()
            self.event_slider.hide()
            self.Contrib.hide()
            self.Err.hide()

            self.Ptrain_Box.hide()
            self.Pmaster_Box.hide()
            self.anomaly_box.hide()

            self.plot_bar.layout.display = 'none'
            self.plot_error.layout.display = 'none'


        elif Page == 'Phases':
            self.Signals_testing_dropdown.show()
            self.event_slider.hide()
            self.Contrib.hide()
            self.Err.hide()

            self.Ptrain_Box.hide()
            self.Pmaster_Box.hide()
            self.anomaly_box.hide()

            self.plot_bar.layout.display = 'none'
            self.plot_error.layout.display = 'none'

        elif Page == 'Root Cause Analysis':
            self.Ptrain_Box.hide()
            self.Pmaster_Box.hide()
            self.anomaly_box.hide()

            self.plot_bar.clear_output()
            self.plot_error.clear_output()
            self.barchart = self.plots[self.current_index]

            with self.plot_bar:
                self.barchart.show()

            self.plot_bar.layout.display = 'block'
            self.plot_error.layout.display = 'none'

            self.event_slider.show()
            self.Contrib.show()
            self.Err.show()
        elif Page == 'Anomaly Detection':
            self.Ptrain_Box.hide()
            self.Pmaster_Box.hide()

            anomalies = self.anomalies[self.current_index]
            observations = self.total_observations[self.current_index]
            self.anomaly_title.children = [f'Anomalies detected']
            self.anomaly_bar.v_model = 100 * anomalies / observations
            self.anomaly_indicator.children = [f'{anomalies}/{observations}']

            self.plot_bar.clear_output()
            self.plot_error.clear_output()
            self.error_plot = self.plot_trend[self.current_index]

            with self.plot_error:
                self.error_plot.show()

            self.plot_bar.layout.display = 'none'
            self.plot_error.layout.display = 'block'
            self.anomaly_box.show()

            self.event_slider.show()
            self.Contrib.show()
            self.Err.show()
        elif Page == 'Training':
            self.Contrib.hide()
            self.Err.hide()

            self.plot_bar.layout.display = 'none'
            self.plot_error.layout.display = 'none'
            self.event_slider.hide()

            self.Ptrain_Box.show()
            self.Pmaster_Box.show()
        return display(self.SettingsBar)

    def clear_plot_section(self):
        self.Progress_Indicator.hide()
        self.Ptrain_Box.hide()
        self.Pmaster_Box.hide()
        self.progress_train.hide()
        self.progress_master.hide()
        self.train_title.hide()
        self.master_title.hide()
        self.train_indicator.hide()
        self.master_indicator.hide()

        self.Contrib.hide()
        self.Err.hide()
        self.event_slider.hide()
        self.plot_error.layout.display = 'none'
        self.plot_bar.layout.display = 'none'

    def ThrowError(self, full_error_message):
        self.Launch_PCA.loading = False
        self.snackbar.children = [full_error_message]
        self.snackbar.v_model = True
        self.snackbar.show()

    # ANALYSIS FORMULAS
    def CleanTable(self, X):

        try:
            nan_positions = np.argwhere(np.isnan(X))
        except Exception as e:
            full_error_message = "All signals must be int, bool or float. Please avoid using strings signals for analysis"
            self.ThrowError(full_error_message)
            return -1, -1

        NaNs_0 = [tuple(pos) for pos in nan_positions]
        NaNs_0 = sorted(NaNs_0, key=lambda x: x[0], reverse=True)
        seen = set()
        unique_rows = []
        for row in NaNs_0:
            if row[0] not in seen:
                unique_rows.append(row)
                seen.add(row[0])
        try:
            for NaN in unique_rows:
                X.pop(NaN[0])
        except Exception as e:
            full_error_message = "Training period contains too many NaN vals. Calculation cannot be performed. Please widen the training period"
            self.ThrowError(full_error_message)
            return -1, -1

        return X, unique_rows

    def submit_formula(self):
        self.Launch_PCA.loading = True
        train_start = self.train_start_time.v_model
        train_end = self.train_end_time.v_model
        test_start = self.test_start_time.v_model
        test_end = self.test_end_time.v_model
        train_signal = self.Signals_training_dropdown.v_model
        m_test_signal = self.Signals_Master_testing_dropdown.v_model
        test_signal = self.Signals_testing_dropdown.v_model

        self.current_page = 'Training'
        self.current_index = 1
        self.Switch_Page(self.current_page, self.current_index)
        max_plots = []
        try:
            max_plots = 1
            Results = []
            PCA_Error_Index = []

            meta_items = spy.search(self.url, all_properties=True, quiet=True, include_archived=True)

            Items = meta_items.loc[meta_items.Type.str.contains('Signal', regex=False)]

            original_names = Items['Name'].tolist()
            names = [name + '_PCA_Contrib' for name in Items['Name'].tolist()]

            train_start_date = convert_datetime(train_start)
            train_end_date = convert_datetime(train_end)
            test_start_date = convert_datetime(test_start)
            test_end_date = convert_datetime(test_end)

            same_name = True
            GridTime = str(60 * float(self.time_min.v_model) + float(self.time_sec.v_model)) + "s"

            #########################################TRAINING SECTION#################################################
            # return
            Event_Name = meta_items.loc[meta_items.Name.str.contains(str(train_signal), regex=False)]
            Events = spy.pull(Event_Name, start=train_start_date, end=train_end_date, header='Name')
            total_train = len(Events)
            if len(Events) == 0:
                self.ThrowError("No events detected on the training period. Please widen the Training Period Time")
                self.Launch_PCA.loading = False

            self.train_indicator.children = [f"0/{total_train} events processed"]

            Periods = Clean_Events_List(Events, train_start_date, train_end_date)

            X_table = []

            F = 0
            for current_train, period in enumerate(Periods):
                start0 = train_start_date if isinstance(period[0], pd._libs.tslibs.nattype.NaTType) else period[
                    0].strftime('%Y-%m-%d %H:%M:%S')
                end0 = train_end_date if isinstance(period[1], pd._libs.tslibs.nattype.NaTType) else period[1].strftime(
                    '%Y-%m-%d %H:%M:%S')

                Events = spy.pull(Items, grid=GridTime, start=start0, end=end0, header='Name', quiet=True)
                X_table = X_table + Events.values.tolist()
                self.progress_train.value = 100 * (current_train + 1) / total_train
                self.train_indicator.children = [f"{(current_train + 1)}/{total_train} events processed"]

            X_Table_Train, NaNs = self.CleanTable(X_table)
            if X_Table_Train == -1:
                return True
            from sklearn.decomposition import PCA
            from sklearn.preprocessing import StandardScaler

            perccontribution = True
            reduction_perc = self.pca_reduction.v_model / 100
            csvtable_train = np.array(X_Table_Train, dtype=float)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(csvtable_train)

            fidelity = [0, 0]

            if float(self.pca_reduction.v_model) == 0:

                for i in range(0, 100):

                    red = 0.15 + 0.7 * i / 100

                    n_comp = max(2, int(float(red) * len(csvtable_train[0])) - 1)
                    # Create PCA object
                    pca = PCA(n_components=n_comp)

                    # Fit PCA to the scaled data
                    pca.fit(X_scaled)

                    X_pca = pca.transform(X_scaled)

                    fidelity.append(round(100 * sum(pca.explained_variance_ratio_), 6))
                    fid_diff = float(fidelity[-2]) - float(fidelity[-1])

                    if fid_diff > -1 and fid_diff != 0:
                        reduction_perc = red
                        break
                self.pca_reduction.v_model = red * 100
            else:
                n_comp = max(2, int(float(reduction_perc) * len(csvtable_train[0])) - 1)
                # Create PCA object
                pca = PCA(n_components=n_comp)
                # Fit PCA to the scaled data
                pca.fit(X_scaled)

                X_pca = pca.transform(X_scaled)

            covariance_matrix = np.cov(X_pca, rowvar=False)
            inverse_covariance_matrix = np.linalg.inv(covariance_matrix)
            hotelling_t2 = np.zeros(X_pca.shape[0])
            for i in range(X_pca.shape[0]):
                hotelling_t2[i] = np.dot(X_pca[i], np.dot(inverse_covariance_matrix, X_pca[i]))

            # Hotelling's T^2 contribution can be interpreted as a chi-squared distribution
            alpha = 0.05
            threshold = np.percentile(hotelling_t2, 100 * (1 - alpha))  # formula custom implementabile pt.1

            ####################################################################TESTING####################################################################################
            Event_Master_Name = meta_items.loc[meta_items.Name.str.contains
            (str(m_test_signal), regex=False)]

            Events_Master = spy.pull(Event_Master_Name,
                                     start=test_start_date,
                                     end=test_end_date, header='Name', quiet=True)

            if len(Events_Master) == 0:
                self.ThrowError("No events detected on the testing period. Please widen the Testing Period Time")
                self.Launch_PCA.loading = False

            Master_Periods = Clean_Events_List(Events_Master, test_start_date, test_end_date)

            total_test = 1
            if self.current_page == 'Phases':
                Event_Name = meta_items.loc[meta_items.Name.str.contains
                (str(test_signal), regex=False)]
                Events = spy.pull(Event_Name, grid=GridTime, start=test_start_date,
                                  end=test_end_date, header='Name', quiet=True)
                total_test = len(Periods)
                if len(Events) == 0:
                    self.ThrowError(
                        "No phase events detected on the testing period. Please widen the Testing Period Time")
                    self.Launch_PCA.loading = False

                Periods = Clean_Events_List(Events, test_start_date, test_end_date)

            X_table_test = []
            X_Time = []
            total_master = len(Master_Periods)

            self.master_indicator.children = [f"0/0 events processed"]
            for current_master, Master in enumerate(Master_Periods):
                X_Master, X_Master_Time = [], []

                start_master = test_start_date if isinstance(Master[0],
                                                             pd._libs.tslibs.nattype.NaTType) else convert_datetime(
                    Master[0])
                end_master = test_end_date if isinstance(Master[1],
                                                         pd._libs.tslibs.nattype.NaTType) else convert_datetime(
                    Master[1])

                if self.current_page == 'Phases':
                    write = 0
                    for current_test, period in enumerate(Periods):
                        start_period = test_start_date if isinstance(period[0],
                                                                     pd._libs.tslibs.nattype.NaTType) else convert_datetime(
                            period[0])
                        end_period = test_end_date if isinstance(period[1],
                                                                 pd._libs.tslibs.nattype.NaTType) else convert_datetime(
                            period[1])
                        if end_period >= start_master and start_period <= end_master:
                            write = 1
                            if start_period < start_master:
                                check, start0, end0 = 1, start_master, end_period
                            elif end_period > end_master:
                                check, start0, end0 = 2, start_period, end_master
                            else:
                                check, start0, end0 = 0, start_period, end_period

                            Events = spy.pull(Items, grid=GridTime, start=start0, end=end0, header='Name', quiet=True)
                            X_Master += Events.values.tolist()
                            X_Master_Time.extend(Events.index.tolist())

                    self.progress_master.value = 100 * (current_master + 1) / total_master
                    self.master_indicator.children = [f"{(current_master + 1)}/{total_master} events processed"]


                else:
                    write = 1
                    start0, end0 = start_master, end_master
                    Events = spy.pull(Items, grid=GridTime, start=start0, end=end0, header='Name', quiet=True)
                    X_Master += Events.values.tolist()
                    X_Master_Time.extend(Events.index.tolist())
                    self.progress_master.value = 100 * (current_master + 1) / total_master
                    self.master_indicator.children = [f"{(current_master + 1)}/{total_master} events processed"]

                if write:
                    X_table_test.append(X_Master)
                    X_Time.append([x.timestamp() for x in X_Master_Time])

            Timestamps = []
            tot_len = 0
            max_plots = len(X_table_test)
            Time_Clean = []
            for iteration, X in enumerate(X_table_test):
                try:
                    start_batch_time = datetime.utcfromtimestamp(X_Time[iteration][0]).strftime('%Y-%m-%d %H:%M:%S')
                    X_Table_Test, NaNs = self.CleanTable(X)
                    if X_Table_Test == -1:
                        return True

                    X_Table_Time = X_Time[iteration]
                    for NaN in NaNs:
                        X_Table_Time.pop(NaN[0])

                    X_float = np.array(X_Table_Test, dtype=float)
                    X_Scaled = scaler.fit_transform(X_float)
                    # print(X_Table_Test)

                    X_pca = pca.transform(X_Scaled)

                    # hotelling's
                    covariance_matrix = np.cov(X_pca, rowvar=False)

                    # Calculate the inverse of the covariance matrix
                    inverse_covariance_matrix = np.linalg.inv(covariance_matrix)
                    # Calculate Hotelling's T^2 for each data point
                    hotelling_t2 = np.zeros(X_pca.shape[0])
                    for i in range(X_pca.shape[0]):
                        hotelling_t2[i] = np.dot(X_pca[i], np.dot(inverse_covariance_matrix, X_pca[i]))

                    hotelling_t2_total = np.mean(hotelling_t2) / threshold

                    ####################################################################REPORTING####################################################################################

                    # Calculate the contribution of each data point
                    contribution = hotelling_t2 / threshold
                    event_anomalies = len([value for value in contribution if value > 1])

                    self.anomalies.append(event_anomalies)
                    self.total_observations.append(len(contribution))
                    plot_time = [i for i in range(len(contribution))]

                    # print("Plotting Hotelling")
                    # Plot the temporal contributions
                    LocalTimes = []
                    A0 = (Master_Periods[iteration][0])
                    B0 = (datetime.fromtimestamp(X_Table_Time[0]))
                    hours = float(str(A0)[11:13]) - float(str(B0)[11:13])
                    LocalTimes = [datetime.fromtimestamp(B) + timedelta(hours=hours) for B in
                                  X_Table_Time]  # Timestamp aggiornato al tempo locale

                    PCA_Error_Index.extend(contribution)
                    Time_Clean.extend(LocalTimes)

                    trace = go.Scatter(
                        x=LocalTimes,
                        y=contribution,
                        mode='lines+markers',
                    )

                    # Layout for the plot
                    layout = go.Layout(
                        title=f"PCA Error at {start_batch_time}, with mean hotelling for period: {round(hotelling_t2_total, 3)}",
                        xaxis=dict(title='Observation Index'),
                        yaxis=dict(title="Hotelling's T^2 Contribution")
                    )

                    # Create figure and display it
                    hotel = go.FigureWidget(data=[trace], layout=layout)
                    hotel.layout.height = 550
                    hotel.layout.paper_bgcolor = 'rgba(0,0,0,0)'
                    hotel.layout.plot_bgcolor = 'rgba(0,0,0,0)'
                    hotel.layout.dragmode = "select"
                    hotel.update_layout(
                        modebar_remove=["autoScale2d", "autoscale", "pan", "pan2d", "pan3d", "reset", "toImage",
                                        "toimage",
                                        "select", "select2d", "lasso", "lasso2d", "reset",
                                        "select", "select2d", "zoom", "zoom2d", "zoomIn2d", "zoomout"])

                    self.plot_trend.append(hotel)

                    bar_var = np.dot((pca.components_.T) ** 2, np.diag(inverse_covariance_matrix))
                    bar_var = bar_var / np.sum(bar_var)

                    trace = go.Bar(
                        x=original_names,  # Categories
                        y=bar_var,  # Values
                        marker=dict(color='blue')  # Optional: Set bar color
                    )

                    # Define layout for the plot
                    layout = go.Layout(
                        title=f"PCA Contributions at {start_batch_time}",
                        xaxis=dict(title='Categories'),
                        yaxis=dict(title='Values'),
                        bargap=0.2  # Gap between bars
                    )

                    barchart = go.FigureWidget(data=[trace], layout=layout)
                    barchart.layout.height = 550
                    barchart.layout.paper_bgcolor = 'rgba(0,0,0,0)'
                    barchart.layout.plot_bgcolor = 'rgba(0,0,0,0)'
                    barchart.layout.dragmode = "select"
                    barchart.update_layout(
                        modebar_remove=["autoScale2d", "autoscale", "pan", "pan2d", "pan3d", "reset", "toImage",
                                        "toimage",
                                        "select", "select2d", "lasso", "lasso2d", "reset",
                                        "select", "select2d", "zoom", "zoom2d", "zoomIn2d", "zoomin", "zoomout"])

                    self.plots.append(barchart)
                    # print("calculation completed 5")
                    fidelity = round(100 * sum(pca.explained_variance_ratio_), 2)
                    # print("finished PCA")

                    time = pd.Timestamp(datetime.strptime(str(Master_Periods[iteration][1])[0:19], '%Y-%m-%d %H:%M:%S'))
                    Timestamps.append(time.tz_localize('UTC'))
                    Results.append(bar_var)
                    tot_len = tot_len + len(X_table_test)
                except Exception as e:
                    full_error_message = f"{e}"  # \nError occurred at: {line_number}"
                    self.ThrowError(full_error_message)

            if len(self.plots) == 0 and self.current_page == 'Phases':
                self.ThrowError("No Phases found in Batch capsules")
                return
            elif len(self.plots) == 0:
                self.ThrowError("No Batch capsules  found in time range")
                return
            self.event_slider.max = max_plots - 1
            if self.Save_Output.v_model:
                headers = names

                ws = []
                wb = []

                # Define your data
                title = "PCA_CONTRIBUTION_ANALYSIS"
                OUTPUT = pd.DataFrame(data=Results, columns=headers, index=Timestamps)
                OUTPUT.index = pd.to_datetime(OUTPUT.index)

                # Push the new data to Seeq
                push_output = spy.push(data=OUTPUT, workbook=self.workbook_id, worksheet=title, quiet=True)

                # Search for the workbook
                workbooks_df = spy.workbooks.search({'ID': self.workbook_id}, quiet=True)

                # Pull the workbook that contains the worksheet you want to update
                wb = spy.workbooks.pull(workbooks_df, quiet=True)[0]

                # Find the worksheet by title
                wsheet = next((ws for ws in wb.worksheets if ws.name == title), None)

                if wsheet:
                    # Update the worksheet with the new data
                    wsheet.display_items = push_output
                else:
                    # Create a new worksheet if it doesn't exist
                    new_worksheet = spy.workbooks.Worksheet(name=title, display_items=push_output)
                    wb.worksheets.append(new_worksheet)

                # Push the updated workbook back to Seeq
                spy.workbooks.push(wb, quiet=True)
                title = "PCA_Error_ANALYSIS"
                OUTPUT_Error = pd.DataFrame(data=PCA_Error_Index, columns=['PCA_Deviation_Index'], index=Time_Clean)
                OUTPUT_Error.index = pd.to_datetime(OUTPUT_Error.index)

                spy.push(data=OUTPUT_Error, workbook=self.workbook_id, worksheet=title, quiet=True)

                title = "PCA_Error_ANALYSIS"
                OUTPUT_Error = pd.DataFrame(data=PCA_Error_Index, columns=['PCA_Deviation_Index'], index=Time_Clean)
                OUTPUT_Error.index = pd.to_datetime(OUTPUT_Error.index)

                spy.push(data=OUTPUT_Error, workbook=self.workbook_id, worksheet=title, quiet=True)

            self.current_page = 'Root Cause Analysis'
            self.current_index = 1

            self.Switch_Page(self.current_page, self.current_index)

        except Exception as e:
            full_error_message = f"{e}"  # \nError occurred at: {line_number}"
            self.ThrowError(full_error_message)
            # Error.show()
        self.Launch_PCA.loading = False
        return True
