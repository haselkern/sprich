#!/usr/bin/env python3
import argparse
import glob
import json
import os
import sys

import lark

class SprichTransformer(lark.Transformer):
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


def main():
    with open(os.path.dirname(os.path.abspath(__file__)) + "/grammar.lark") as f:
        grammar = f.read()

    arg_parser = argparse.ArgumentParser(description="""
    Transform .sprich files into .json files.
    """)
    arg_parser.add_argument("input", help="Transform all files in this directory.")
    arg_parser.add_argument("-o", "--output", help="Write transformed files into this directory.")
    args = arg_parser.parse_args()

    if not args.output:
        args.output = args.input

    if not os.path.isdir(args.input):
        print(args.input + " is not a directory")
        return
    if not os.path.isdir(args.output):
        print(args.output + " is not a directory")
        return

    input_files = glob.glob(args.input + "/*.sprich")
    for input_file in input_files:
        with open(input_file) as f:
            parser = lark.Lark(grammar)
            try:
                tree = parser.parse(f.read())
                states = SprichTransformer().transform(tree)
                output = {
                    "generator": "sprich",
                    "version": "1",
                    "states": states
                }
                out_filename = args.output + "/" + os.path.basename(input_file)[:-6] + "json"
                with open(out_filename, "w") as out_f:
                    json.dump(output, out_f)
            except Exception as e:
                print(e)

if __name__ == "__main__":
    main()
