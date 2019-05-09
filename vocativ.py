#!/usr/bin/env python3
import json
import sys
import re

class State:
    def __init__(self, lines):
        self.id = lines[0][1:-1]

        self.actions = []
        for line in lines[1:]:
            self.actions.append(Action(line))

    def to_json(self):
        return {
            "id": self.id,
            "actions": [a.to_json() for a in self.actions if a.type != "option"],
            "options": [a.to_json() for a in self.actions if a.type == "option"]
        }

class Action:
    def __init__(self, line):
        if line.startswith("::"):
            self.type = "option"
            if line.rfind("[") > 0:
                self.body = line[2:line.rfind("[")].strip()
                next = line[line.rfind("["):][1:-1]
                if len(next) > 0:
                    if "?" in next:
                        next, condition = next.split("?")
                        if len(next.strip()) > 0:
                            self.next = next.strip()
                        if len(condition.strip()) > 0:
                            self.condition = condition.strip()
                    else:
                        self.next = next
            else:
                self.body = line[2:].strip()
        if line.startswith("~"):
            self.type = "function"
            line = re.split("\W+", line[1:])
            self.body = line[0]
            self.params = line[1:]
        else:
            self.type = "message"
            self.body = line.strip()

    def to_json(self):
        d = {
            "type": self.type,
            "body": self.body
        }
        if hasattr(self, "next"):
            d["next"] = self.next
        if hasattr(self, "params"):
            d["params"] = self.params
        if hasattr(self, "condition"):
            d["condition"] = self.condition
        return d


def get_states(file):
    with open(file) as f:
        lines = f.readlines()
        # Remove comments
        lines = [x[:x.index("#")] if "#" in x else x for x in lines]
        # Remove empty lines
        lines = [x.strip() for x in lines if len(x.strip()) > 0]

        buffer = []
        states = []
        for line in lines:
            if line.startswith("["):
                if len(buffer) > 0:
                    states.append(State(buffer))
                    buffer = []
            buffer.append(line)
        states.append(State(buffer))
    return states

input_files = sys.argv[1:]
for file in input_files:
    print(json.dumps([s.to_json() for s in get_states(file)]))
