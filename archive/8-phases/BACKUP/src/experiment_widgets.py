import ipywidgets as widgets
from IPython.display import display
from ipywidgets import VBox, HBox
import json

# Create input fields for Participant and Experimenter
participant_input = widgets.Text(
    value='',
    placeholder='Enter participant ID',
    description='Participant:',
    layout=widgets.Layout(width='250px')
)

experimenter_input = widgets.Text(
    value='',
    placeholder="Enter scientist's name",
    description='Scientist:',
    layout=widgets.Layout(width='250px')
)


# Number of phases input
phases_input = widgets.IntText(
    value=1,
    description='Phases:',
    layout=widgets.Layout(width='140px')
)

# Layout adjustments
label_layout = widgets.Layout(width='155px')
input_box_layout = widgets.Layout(width='90px')

# Function to create a horizontal separator
def horizontal_separator():
    return widgets.HTML(value='<hr style="border: 1px solid gray; margin: 10px 0;">')

# Function to dynamically create widgets for each phase
def create_phase_widgets(*, phase_num):
    # Duration widget
    duration_widget = HBox([
        widgets.Label(value=f'Duration (Phase {phase_num}):', layout=widgets.Layout(width='155px')),
        widgets.IntText(value=30, layout=input_box_layout)
    ])

    skip_phase_if_widget = HBox([
        widgets.Label(value=f'Skip Phase If:', layout=widgets.Layout(width='155px')),
        widgets.Textarea(value='', placeholder='Optional: Code to be evaluated to see if we skip the phase.  Must input "False"(with the capital F, but no quotes) if you do not want to implement this feature.  Otherwise, you will see an error code.', layout=widgets.Layout(width='700px', height='100px'))
    ])

    # Background color widget (NEW: moved to top after duration)
    background_color_widget = HBox([
        widgets.Label(value=f'Background Color:', layout=widgets.Layout(width='155px')),
        widgets.ColorPicker(value="#000000", layout=input_box_layout)
    ])
    # Before-phase instructions (displayed centered before the phase starts)
    before_instructions_widget = HBox([
        widgets.Label(value=f'Before Phase Instructions:', layout=widgets.Layout(width='155px')),
        widgets.Textarea(value='', placeholder='Instructions shown before this phase (auto-wrapped)', layout=widgets.Layout(width='400px', height='80px'))
    ])

    # During-phase instructions (displayed at the top during the phase)
    during_instructions_widget = HBox([
        widgets.Label(value=f'During Phase Instructions:', layout=widgets.Layout(width='155px')),
        widgets.Textarea(value='', placeholder='Instructions shown during this phase (auto-wrapped)', layout=widgets.Layout(width='400px', height='80px'))
    ])

    free_contingency_widget = HBox([
        widgets.Label(value=f'Optional Free Contingency:', layout=widgets.Layout(width='155px')),
        widgets.Textarea(value='', placeholder='Optional Free Contingency Code to be executed each loop.  Must write code in other editor and paste in here if using the /tab button, as tab in here will advance to next widget.', layout=widgets.Layout(width='700px', height='280px'))
    ])

    # Number of balls widget
    number_balls_widget = HBox([
        widgets.Label(value=f'Number of Balls:', layout=widgets.Layout(width='155px')),
        widgets.IntText(value=3, layout=input_box_layout)
    ])

    # Dynamically adjust the number of ball settings
    def update_ball_settings(*, change=None):
        num_balls = number_balls_widget.children[1].value
        
        # Update all ball-specific widgets
        speed_widgets.children = [
            HBox([
                widgets.Label(value=f'Speed (Ball {i + 1}):', layout=label_layout),
                widgets.FloatText(value=1.0, layout=input_box_layout)
            ]) for i in range(num_balls)
        ]
        radii_widgets.children = [
            HBox([
                widgets.Label(value=f'Radius (Ball {i + 1}):', layout=label_layout),
                widgets.FloatText(value=60, layout=input_box_layout)
            ]) for i in range(num_balls)
        ]
        base_colors_widgets.children = [
            HBox([
                widgets.Label(value=f'Base Color (Ball {i + 1}):', layout=label_layout),
                widgets.ColorPicker(value="#ff0000", layout=input_box_layout)
            ]) for i in range(num_balls)
        ]
        points_per_reinforcement.children = [
            HBox([
                widgets.Label(value=f'Points (Ball {i + 1}):', layout=label_layout),
                widgets.IntText(value=1, layout=input_box_layout)
            ]) for i in range(num_balls)
        ]
        change_to_clicks_widgets.children = [
            HBox([
                widgets.Label(value=f'Change To Clicks (Ball {i + 1}):', layout=label_layout),
                widgets.IntText(value=1, layout=input_box_layout)
            ]) for i in range(num_balls)
        ]
        change_over_delay_widgets.children = [
            HBox([
                widgets.Label(value=f'Change Over Delay (Ball {i + 1}):', layout=label_layout),
                widgets.FloatText(value=5, layout=input_box_layout)
            ]) for i in range(num_balls)
        ]

    # Observe changes to number of balls (wrap to pass keyword arg)
    number_balls_widget.children[1].observe(lambda ch: update_ball_settings(change=ch), names='value')

    # Containers for the ball-specific widgets
    speed_widgets = HBox([])
    radii_widgets = HBox([])
    base_colors_widgets = HBox([])
    points_per_reinforcement = HBox([])
    change_to_clicks_widgets = HBox([])
    change_over_delay_widgets = HBox([])

    # Initial update for ball-specific widgets
    update_ball_settings(change=None)

    # # Yoked dropdown
    # yoked_widget = HBox([
    #     widgets.Label(value=f'Yoked (Phase {phase_num}):', layout=widgets.Layout(width='155px')),
    #     widgets.Dropdown(options=[('False', False), ('True', True)], value=False, layout=input_box_layout)
    # ])

    # # Debug dropdown
    debug_widget = HBox([
        widgets.Label(value=f'Debug (Phase {phase_num}):', layout=widgets.Layout(width='155px')),
        widgets.Dropdown(options=[('False', False), ('True', True)], value=False, layout=input_box_layout)
    ])


    # Assemble phase-specific widgets (NEW: background color is now 2nd child)
    phase_box = VBox([
        duration_widget,
        skip_phase_if_widget,
        background_color_widget,
        before_instructions_widget,
        during_instructions_widget,
        free_contingency_widget,
        number_balls_widget,
        speed_widgets,
        radii_widgets,
        base_colors_widgets,
        points_per_reinforcement,
        change_to_clicks_widgets,
        change_over_delay_widgets,
        # yoked_widget,
        debug_widget,
        horizontal_separator()
    ])

    return phase_box

# Function to update phase widgets dynamically
def update_phases(*, change=None):
    num_phases = phases_input.value
    phase_boxes.children = [create_phase_widgets(phase_num=(i + 1)) for i in range(num_phases)]

# Save settings to a JSON file
def save_settings(*, button):
    settings = {
        'participant': participant_input.value,
        'experimenter': experimenter_input.value,
        'phases': phases_input.value,
        'phase_data': []
    }

    for phase_num in range(phases_input.value):
        phase_widget = phase_boxes.children[phase_num]
        phase_info = {
            'duration': phase_widget.children[0].children[1].value,
            'skip_if': phase_widget.children[1].children[1].value,
            'background_color': phase_widget.children[2].children[1].value,  # NEW: added background color
            'before_instructions': phase_widget.children[3].children[1].value,
            'during_instructions': phase_widget.children[4].children[1].value,
            'free_contingency':phase_widget.children[5].children[1].value,
            'number_of_balls': phase_widget.children[6].children[1].value,
            # 'yoked': phase_widget.children[-3].children[1].value,
            'debug': phase_widget.children[-2].children[1].value,
            'balls': []
        }
        
        for ball_num in range(phase_info['number_of_balls']):
            ball_info = {
                'speed': phase_widget.children[7].children[ball_num].children[1].value,
                'radius': phase_widget.children[8].children[ball_num].children[1].value,
                'base_color': phase_widget.children[9].children[ball_num].children[1].value,
                'points_per_reinforcement': phase_widget.children[10].children[ball_num].children[1].value,
                'change_to_clicks': phase_widget.children[11].children[ball_num].children[1].value,
                'change_over_delay': phase_widget.children[12].children[ball_num].children[1].value
            }
            phase_info['balls'].append(ball_info)
        
        settings['phase_data'].append(phase_info)

    with open('settings.json', 'w') as f:
        json.dump(settings, f)
    print("Settings saved to settings.json")

# Load settings from a JSON file
def load_settings(*, button):
    try:
        with open('settings.json', 'r') as f:
            settings = json.load(f)
        
        participant_input.value = settings.get('participant', '')
        experimenter_input.value = settings.get('experimenter', '')
        phases_input.value = settings['phases']
        
        # Update phase boxes based on loaded data
        phase_boxes.children = []
        for phase in settings['phase_data']:
            phase_widget = create_phase_widgets(phase_num=(len(phase_boxes.children) + 1))
            
            # Set phase-level values
            phase_widget.children[0].children[1].value = phase['duration']
            phase_widget.children[1].children[1].value = phase['skip_if']
            phase_widget.children[2].children[1].value = phase.get('background_color', '#000000')  # NEW: load background color
            phase_widget.children[3].children[1].value = phase.get('before_instructions', '')
            phase_widget.children[4].children[1].value = phase.get('during_instructions', '')
            phase_widget.children[5].children[1].value = phase['free_contingency']
            phase_widget.children[6].children[1].value = phase['number_of_balls']
            # phase_widget.children[-3].children[1].value = phase['yoked']
            phase_widget.children[-2].children[1].value = phase['debug']
            
            # Set ball-specific values
            for ball_num in range(phase['number_of_balls']):
                phase_widget.children[7].children[ball_num].children[1].value = phase['balls'][ball_num]['speed']
                phase_widget.children[8].children[ball_num].children[1].value = phase['balls'][ball_num]['radius']
                phase_widget.children[9].children[ball_num].children[1].value = phase['balls'][ball_num]['base_color']
                phase_widget.children[10].children[ball_num].children[1].value = phase['balls'][ball_num]['points_per_reinforcement']
                phase_widget.children[11].children[ball_num].children[1].value = phase['balls'][ball_num]['change_to_clicks']
                phase_widget.children[12].children[ball_num].children[1].value = phase['balls'][ball_num]['change_over_delay']
            
            phase_boxes.children += (phase_widget,)
        
        print("Settings loaded from settings.json")

    except FileNotFoundError:
        print("No settings file found. Please save settings first.")
    except Exception as e:
        print(f"Error loading settings: {e}")

# Main interface
phase_boxes = VBox([create_phase_widgets(phase_num=1)])
# Observe with wrapper so keyword-only `update_phases` receives a named arg
phases_input.observe(lambda ch: update_phases(change=ch), names='value')

# Save and Load Buttons
save_button = widgets.Button(description="Save Settings")
# Wrap on_click so `save_settings` receives keyword-only arg
save_button.on_click(lambda btn: save_settings(button=btn))

load_button = widgets.Button(description="Open Settings")
# Wrap on_click so `load_settings` receives keyword-only arg
load_button.on_click(lambda btn: load_settings(button=btn))

# Attempt to auto-load settings on import (safe: ignore errors)
try:
    load_settings(button=None)
except Exception:
    # No settings to load or load failed; continue with defaults
    pass

# Display everything
display(VBox([
    participant_input,
    experimenter_input,
    phases_input,
    horizontal_separator(),
    phase_boxes,
    HBox([save_button, load_button])
]))