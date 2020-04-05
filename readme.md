# Installing Flask
*On Python 3.8:*
```
alias python='python3.8'
python -m venv venv
. venv/bin/activate
python -m pip install Flask
```

# Status

Conductor works now, registers (join) name/type pairs and unregisters them (leave).

To test, run the app: `python conductor.py`

Go to the Conductor info page: `http://127.0.0.1:1201/info/`

Start a Member and it will register itself: `python member.py`

Refresh the Conductor info page and see the difference.

Ctrl+C on the Member, refresh the Conductor info page and see the difference.
