import threading, time

class Orchestra:
    name = ""
    members = []

    def __init__(self, name):
        self.name = name

    def addMember(self, member):
        if member not in self.members:
            self.members.append(member)
            return True
        else:
            print(f"Member {member.name}-{member.section} already exists")
            return False

    def removeMember(self, member):
        if member in self.members:
            self.members.remove(member)
            return True
        else:
            print(f"Member {member.name}-{member.section} does not exist")
            return False


class Conductor:
    port = -1

    def __init__(self, port = -1):
        self.port = port


class Member:
    name = ""
    section = ""
    port = -1
    conductor = Conductor()

    def __init__(self, name, section, port, conductor):
        self.name = name
        self.section = section
        self.port = port
        self.conductor = conductor

    def __eq__(self, other): 
        if not isinstance(other, Member):
            return False
        return self.name == other.name and self.section == other.section

    def toDict(self):
        return {
            "name": self.name,
            "section": self.section,
            "port": self.port
        }


class BackgroundScheduler:
    def __init__(self, interval, callback):
        self.interval = interval
        self.callback = callback

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            self.callback()
            time.sleep(self.interval)


class FetchedDocument:
    document = ""
    timestamp = -1
    def __init__(self, document, member):
        self.document = document
        self.member = member
        self.timestamp = time.time()

