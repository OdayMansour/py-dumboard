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

To test, run the app:
```
python conductor.py
```

Go to the info page: `http://127.0.0.1:1201/info/`

Register a few Members:
```
curl --data "name=secondone&type=fetcher" http://localhost:1201/join/
curl --data "name=firstone&type=fetcher" http://localhost:1201/join/
```

Refresh the info page and see the difference.

Unregister a Member:
```
curl --data "name=secondone&type=fetcher" http://localhost:1201/leave/
```

Refresh the info page and see the difference.

Try registering the same name/type more than once, or deregistering it twice.
