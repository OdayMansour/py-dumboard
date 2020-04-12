# Finite state machine code

###############################################
# State machine code ##########################
class State:
    name = ""
    description = ""

    def __init__(self, name, description):
        self.name = name
        self.description = description


class Event:
    name = ""
    description = ""

    def __init__(self, name, description):
        self.name = name
        self.description = description


class Action:
    name = ""
    description = ""
    callback = None

    def __init__(self, name, description, callback):
        self.name = name
        self.description = description
        self.callback = callback

    def run(self):
        self.callback()


class Transition:
    name = ""
    description = ""
    in_state = None
    in_event = None
    out_action = None
    out_state = None

    def __init__(self, name, description, in_state, in_event, out_action, out_state):
        self.name = name
        self.description = description
        self.in_state = in_state
        self.in_event = in_event
        self.out_action = out_action
        self.out_state = out_state


class FSM:
    name = ""
    description = ""
    states = []
    events = []
    actions = []
    transitions = []
    current_state = None

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def addState(self, state, start_state=False):
        self.states.append(state)
        if start_state:
            self.current_state = state
        return state

    def addEvent(self, event):
        self.events.append(event)
        return event

    def addAction(self, action):
        self.actions.append(action)
        return action

    def addTransition(self, transition):
        self.transitions.append(transition)
        return transition

    def transition(self, event_name):
        print("Looking for event " + event_name + "... ", end = '')
        event_list = list(filter(lambda event: event.name == event_name, self.events))
        if len(event_list) == 1:
            event = event_list[0]
            print("found event " + event.name)
        else:
            print("did not find one event " + event_name)
            return False
        
        print("Looking for transaction with inputs " + self.current_state.name + " + " + event.name + "... ", end = '')
        transition_list = list(filter(lambda transition: transition.in_state == self.current_state and transition.in_event == event, self.transitions))
        if len(transition_list) == 1:
            transition = transition_list[0]
            print("found transition " + transition.name)
        else:
            print("fid not find transition with inputs " + self.current_state + " + " + event.name)
            return False

        print("Running action " + transition.out_action.name + " and moving to state " + transition.out_state.name)
        transition.out_action.run()
        self.current_state = transition.out_state
        

###############################################
# State machine configuration #################

# Initialise ##############
fsm = FSM("fsm", "Main interaction and display state machine")

# Callbacks ###############
def say_hello():
    print("Hello!")

# States ##################
s_sleep = fsm.addState(State("sleep", "Sleeping, lights off"), start_state=True)
s_summary = fsm.addState(State("summary", "Summary page"))
s_selection = fsm.addState(State("selection", "Selection"))
s_display = fsm.addState(State("display", "Displaying daily temperature info"))

# Events ##################
e_click = fsm.addEvent(Event("click", "Click event"))
e_rot_pos = fsm.addEvent(Event("rorate_pos", "Rotating knob, positive"))
e_rot_neg = fsm.addEvent(Event("rotate_neg", "Rotating knob, positive"))
e_timer = fsm.addEvent(Event("timer", "Sleep timer expiring"))

# Actions #################
a_show_summary = fsm.addAction(Action("show_summary", "Display summary page", say_hello))
a_show_selection = fsm.addAction(Action("show_selection", "Display selection page", say_hello))
a_show_display = fsm.addAction(Action("show_display", "Display temperature info page", say_hello))
a_pos_selection = fsm.addAction(Action("pos_selection", "Increase selection counter", say_hello))
a_neg_selection = fsm.addAction(Action("neg_selection", "Decrease selection counter", say_hello))
a_goto_sleep = fsm.addAction(Action("goto_sleep", "Go to sleep", say_hello))

# Transitions #############
t_sleep_click = fsm.addTransition(Transition("sleep_click", "Click while sleeping", s_sleep, e_click, a_show_summary, s_summary))
t_sleep_rot_pos = fsm.addTransition(Transition("sleep_rot_pos", "Rotate positive while sleeping", s_sleep, e_rot_pos, a_show_selection, s_selection))
t_sleep_rot_neg = fsm.addTransition(Transition("sleep_rot_neg", "Rotate negative while sleeping", s_sleep, e_rot_neg, a_show_selection, s_selection))
t_sleep_timer = fsm.addTransition(Transition("sleep_timer", "Timer runs out while sleeping", s_sleep, e_timer, a_show_selection, s_sleep))

t_summary_click = fsm.addTransition(Transition("summary_click", "Click while on summary", s_summary, e_click, a_goto_sleep, s_sleep))
t_summary_rot_pos = fsm.addTransition(Transition("summary_rot_pos", "Rotate positive while on summary", s_summary, e_rot_pos, a_show_selection, s_selection))
t_summary_rot_neg = fsm.addTransition(Transition("summary_rot_neg", "Rotate negative while on summary", s_summary, e_rot_neg, a_show_selection, s_selection))
t_summary_timer = fsm.addTransition(Transition("summary_timer", "Timer runs out while on summary", s_summary, e_timer, a_goto_sleep, s_sleep))

t_selection_click = fsm.addTransition(Transition("selection_click", "Click while on selection", s_selection, e_click, a_show_display, s_display))
t_selection_rot_pos = fsm.addTransition(Transition("selection_rot_pos", "Rotate positive while on selection", s_selection, e_rot_pos, a_pos_selection, s_selection))
t_selection_rot_neg = fsm.addTransition(Transition("selection_rot_neg", "Rotate negative while on selection", s_selection, e_rot_neg, a_neg_selection, s_selection))
t_selection_timer = fsm.addTransition(Transition("selection_timer", "Timer runs out while on selection", s_selection, e_timer, a_show_summary, s_summary))

t_display_click = fsm.addTransition(Transition("display_click", "", s_display, e_click, a_show_summary, s_summary))
t_display_rot_pos = fsm.addTransition(Transition("display_rot_pos", "", s_display, e_rot_pos, a_show_selection, s_selection))
t_display_rot_neg = fsm.addTransition(Transition("display_rot_neg", "", s_display, e_rot_neg, a_show_selection, s_selection))
t_display_timer = fsm.addTransition(Transition("display_timer", "", s_display, e_timer, a_show_summary, s_summary))

###############################################
# Section to play around ######################

fsm.transition("click")
