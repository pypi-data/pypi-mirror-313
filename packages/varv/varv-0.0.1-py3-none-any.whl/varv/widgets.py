#
#      Copyright (C) 2024 Thijn Hoekstra
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import matplotlib
import pandas as pd
from matplotlib import pyplot as plt
import warnings

try:
    from ipywidgets import AppLayout, FloatSlider, Button, ToggleButton, HBox, VBox, Layout, BoundedIntText, Checkbox
except ImportError as e:
    raise warnings.warn("Cannot find ipywidgets.")

def set_lightness(color, l=0.5):
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    rgb =  colorsys.hls_to_rgb(c[0], max(0, min(1, l)), c[2])
    return '#%02x%02x%02x' % tuple(int(v * 255) for v in rgb)



class ColoredButton(Button):

    def __init__(self, color, init_state: bool = False, **kwargs, ):
        super().__init__(**kwargs)
        self.color = color
        self.light_color = set_lightness(color, 0.90)

        if init_state:
            self.set_on()
        else:
            self.set_off()


    def set_on(self):
        self.style.button_color = self.color
        self.style.text_color = '#FFFFFF'  # White

    def set_off(self):
        self.style.button_color = self.light_color
        self.style.text_color = '#000000'  # Black

class EventViewer:

    def __init__(self, eves, label_df: pd.DataFrame = None):
        self.events = eves
        self.label_df = label_df

        if label_df is not None:
            self.buttons = [ColoredButton(c, description=d) for d, c
                            in zip(label_df.description, label_df.color)]
            [button.on_click(self.button_clicked) for button in self.buttons]

        self.button_next = Button(description=">", icon='right')
        self.selector = BoundedIntText(
                value=0,
                min=0,
                max=len(eves) - 1,
                step=1,
            )
        self.auto_select = Checkbox(
            value=True,
            description='Auto Forward',
        )
        self.button_prev = Button(description="<", icon='left')

        plt.ioff()

        self.fig, self.ax = plt.subplots(1, 1, figsize=(12, 4))
        self.fig.canvas.header_visible = False
        self.fig.canvas.layout.min_height = '400px'
        self.ax.set_ylim(0, 300)
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Current (pA)")

        self.event = self.events[0]
        self.event_label: int = self.events.info.label
        self.i = 0

        self.lines = plt.plot(self.event.get_t(), self.event.get_i())
        if self.event.info.open_pore_current:
            self.open_line = self.ax.axhline(
                self.event.info.open_pore_current,
                linestyle='--', color='grey', alpha=0.5)
        else:
            self.open_line = None


        self.button_next.on_click(self.do_next)
        self.button_prev.on_click(self.do_prev)
        self.selector.observe(self.new_event, names='value')

    def __call__(self):

        if matplotlib.get_backend() != 'ipympl':
            raise RuntimeError('Error, please use the ipympl backend. In '
                               'Jupyter, use %matplotlib ipympl')

        box_layout = Layout(display='flex',
                            flex_flow='column',
                            align_items='center',
                            width='100%')
        navigation_array = HBox(children=[self.button_prev, self.selector,
                                          self.button_next, self.auto_select], )

        if self.label_df is not None:
            button_array = HBox(children=self.buttons)
            footer = VBox(children=[button_array, navigation_array], layout=box_layout)
        else:
            footer = navigation_array

        self.new_event({"new" : 0})

        return AppLayout(
            center=self.fig.canvas,
            footer=footer,
            pane_heights=[0, 6, 1]
        )

    def do_next(self, b):
        i = self.i + 1
        i = min(max(0, i), len(self.events) - 1)
        self.selector.value = i


    def do_prev(self, b):
        i = self.i - 1
        i = min(max(0, i), len(self.events) - 1)
        self.selector.value = i


    def new_event(self, change):
        self.i = change['new']
        self.event = self.events[self.i]

        if self.label_df is not None:
            label = self.event.info.label
            descr = self.get_descr_from_label(label)

            for button in self.buttons:
                if button.description == descr:
                    button.set_on()
                    self.update_color()
                else:
                    button.set_off() # Only one button on at a time

        self.ax.set_title(f"Event {self.i} from Channel {self.event.info.chan_num}")
        self.lines[0].set_data(self.event.get_t(), self.event.get_i())

        if self.open_line:
            self.open_line.set_ydata([self.event.info.open_pore_current] * 2)

        self.ax.relim()
        self.ax.autoscale(axis='x')
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def update_color(self):
        color = self.get_color_from_label(self.event.info.label)
        self.lines[0].set_color(color)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def set_button_color(self, b, color):
        b.style.button_color = color

    def get_label_num(self, description) -> int:
        return self.label_df.loc[self.label_df['description'] == description, 'id'].item()

    def get_color_from_label(self, label) -> str:
        return self.label_df.loc[self.label_df['id'] == label, 'color'].item()

    def get_descr_from_label(self, label) -> str:
        return self.label_df.loc[self.label_df['id'] == label, 'description'].item()

    def button_clicked(self, b):
        for button in self.buttons:
            if button == b:

                button.set_on()
                self.event.info.label = self.get_label_num(button.description)

                self.update_color()
                if self.auto_select.value:
                    self.do_next(None)
            else:
                button.set_off()  # Only one button on at a time