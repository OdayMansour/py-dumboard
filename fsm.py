# Finite state machine code

def say_hello():
    print("Hello!")


class State:
    name = ""
    description = ""

    def __init__(self, name):
        self.name = name


class Event:
    name = ""
    description = ""

    def __init__(self, name):
        self.name = name


class Action:
    name = ""
    description = ""
    callback = None

    def __init__(self, name, callback):
        self.name = name
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

    def __init__(self, name, in_state, in_event, out_action, out_state):
        self.name = name
        self.in_state = in_state
        self.in_event = in_event
        self.out_action = out_action
        self.out_state = out_state


class FSM:
    states = []
    events = []
    actions = []
    transitions = []
    current_state = None

    def __init__(self):
        self.states.append(State("summary"))
        self.states.append(State("helloing"))
        self.events.append(Event("click"))
        self.actions.append(Action("say_hello", say_hello))
        self.transitions.append(Transition("summary_to_hello", self.states[0], self.events[0], self.actions[0], self.states[1]))

        self.current_state = self.states[0]


    def transition(self, event_name):
        event = Event("")
        transition = Transition("", None, None, None, None)

        print("Looking for event " + event_name)
        event_list = list(filter(lambda event: event.name == event_name, self.events))
        if len(event_list) == 1:
            event = event_list[0]
            print("Found event " + event.name)
        else:
            print("Did not find one event " + event_name)
            return False
        
        print("Currently at state " + self.current_state.name)
        print("Looking for transaction with inputs " + self.current_state.name + " + " + event.name)
        transition_list = list(filter(lambda transition: transition.in_state == self.current_state and transition.in_event == event, self.transitions))

        if len(transition_list) == 1:
            transition = transition_list[0]
            print("Found transition " + transition.name)
        else:
            print("Did not find transition with inputs " + self.current_state + " + " + event.name)
            return False

        print("Running action and moving to new state:")
        transition.out_action.run()
        self.current_state = transition.out_state
        
        print("Now at state " + self.current_state.name)


fsm = FSM()
fsm.transition("click")
