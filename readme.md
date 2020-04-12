# Installing Flask
*On Python 3.8:*
```
alias python='python3.8'
python -m venv venv
. venv/bin/activate
python -m pip install Flask
```

# Status

## Conductor

Unique service, keeps track of all members. Also keep track of the depot to let other members know.

It registers (join) members and unregisters them (leave).

## Member

Finds Conductor and registers presence. Unregisters when closing.

Fetchers are Members that are meant to fetch data from the outside and then send them to the store. The stored document format is:
```
{
    'timestamp': 1234567890.7654321, 
    'member': {
        'name': '...', 
        'section': '...'
    }, 
    'document': {...}
}
```

## Depot

Special member that acts as data store. It listens to json documents from other members.

## FSM

There's a Finite State Machine now. It'll be the main event loop, handling inputs and keeping track of the board's state.

To see it in action run `python fsm.py` and see the state change.

# To see them in action

- Start three separate terminals
- Set up the environment: `. venv/bin/activate`
- *Terminal 1:* Start the Conductor: `python conductor.py`
  - Go to the Conductor info page: `http://127.0.0.1:1201/info/`
- *Terminal 2:* Start the Depot: `python depot.py`
  - Go to the Conductor info page and note the new member: `http://127.0.0.1:1201/info/`
  - Go to the Conductor depot page and note the depot: `http://127.0.0.1:1201/members/depot/`
- *Terminal 3:* Start the Fetcher: `python openweather-fetch.py`
  - Go to the Conductor info page and note the third member: `http://127.0.0.1:1201/info/`
  - Look at the Fetcher and Depot terminals and see them interact
