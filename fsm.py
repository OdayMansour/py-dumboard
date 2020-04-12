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

    def addEvent(self, event):
        self.events.append(event)

    def addAction(self, action):
        self.actions.append(action)

    def addTransition(self, transition):
        self.transitions.append(transition)

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

        print("Running action and moving to new state: " + transition.out_state.name)
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
s_summary = State("summary", "Summary page")
fsm.addState(s_summary, start_state=True)

s_hellowing = State("hellowing", "Page after saying hello")
fsm.addState(s_hellowing)

# Events ##################
e_click = Event("click", "Click event")
fsm.addEvent(e_click)

# Actions #################
a_sayhello = Action("say_hello", "Say hello", say_hello)
fsm.addAction(a_sayhello)

# Transitions #############
t_summary_click = Transition("summary_click", "Click while on Summary", s_summary, e_click, a_sayhello, s_hellowing)
fsm.addTransition(t_summary_click)


###############################################
# Section to play around ######################

fsm.transition("click")
