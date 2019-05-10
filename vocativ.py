#!/usr/bin/env python3
import json
import sys
import lark

class Transformer(lark.Transformer):
    def start(self, states):
        return states
    def state(self, p):
        id_token, *statements = p
        return {
            "id": id_token,
            "actions": [s for s in statements if s["type"] != "option"],
            "options": [s for s in statements if s["type"] == "option"]
        }
    def message(self, p):
        return {
            "type": "message",
            "text": p[0].value[1:-1]
        }
    def function(self, p):
        return {
            "type": "function",
            "name": p[0],
            "params": p[1]
        }
    def parameters(self, p):
        return p
    def parameter(self, p):
        value = p[0].value
        try:
            return int(value)
        except:
            try:
                return float(value)
            except:
                return str(value)[1:-1]
    def option(self, p):
        result = {
            "type": "option",
        }
        if len(p) > 0:
            result["text"] = p[0][1:-1]
        if len(p) > 1:
            result["next"] = p[1]
        if len(p) > 2:
            result["condition"] = p[2]
        return result
    def instant(self, p):
        result = {
            "type": "instant",
            "next": p[0]
        }
        if len(p) > 1:
            result["condition"] = p[1]
        return result
    def condition(self, p):
        return p[0].value[1:-1]
    def identifier(self, p):
        return p[0].value

with open("grammar.lark") as f:
    grammar = f.read()

input_file = sys.argv[1]

with open(input_file) as f:
    parser = lark.Lark(grammar, start="start")
    try:
        tree = parser.parse(f.read())
        print(tree)
        print(tree.pretty())
        print(json.dumps(Transformer().transform(tree)))
    except Exception as e:
        print(e)
