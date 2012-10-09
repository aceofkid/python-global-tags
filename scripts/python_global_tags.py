#! /usr/bin/env python

import argparse
import ast
import linecache
import os
import subprocess
import sys

class DefinitionVisitor(ast.NodeVisitor):
    def __init__(self, filename):
        ast.NodeVisitor.__init__(self)
        self.filename = os.path.relpath(filename, os.getcwd())

    def visit_FunctionDef(self, node):
        print('{name}\t{lineno} {filename}\t{code}'.format(
            name=node.name,
            lineno=node.lineno,
            filename=self.filename,
            code=linecache.getline(self.filename, node.lineno).rstrip()))
        return self.generic_visit(node)

    def visit_ClassDef(self, node):
        print('{name}\t{lineno} {filename}\t{code}'.format(
            name=node.name,
            lineno=node.lineno,
            filename=self.filename,
            code=linecache.getline(self.filename, node.lineno).rstrip()))
        return self.generic_visit(node)

class ReferenceVisitor(ast.NodeVisitor):
    def __init__(self, filename):
        ast.NodeVisitor.__init__(self)
        self.filename = os.path.relpath(filename, os.getcwd())

    def visit_Call(self, node):
        print('{name}\t{lineno} {filename}\t{code}'.format(
            name=node.func.id,
            lineno=node.lineno,
            filename=self.filename,
            code=linecache.getline(self.filename, node.lineno).rstrip()))
        return self.generic_visit(node)

def process_python_file(filename, visitor_type):
    with open(filename, 'r') as f:
        code = f.read()

    try:
        root_node = ast.parse(code, filename)
    except Exception:
        return

    v = visitor_type(filename).visit(root_node)

    return 0

python_extensions = ['.py', '.pyw']

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filenames', metavar='F', type=str, nargs='*',
        help='a file to process')
    parser.add_argument(
        '-s', '--symbol', dest='symbol', action='store_true',
        help='Collect symbols other than object definitions and references. By default, locate object definitions.')
    args = parser.parse_args()

    rval = 0

    for filename in args.filenames:
        ext = os.path.splitext(filename)[1].lower()

        if ext not in python_extensions:
            if args.symbol:
                rval = subprocess.call(['gtags-parser', '-dts', filename])
            else:
                rval = subprocess.call(['gtags-parser', '-dt', filename])
        else:
            vtype = ReferenceVisitor if args.symbol else DefinitionVisitor
            rval = process_python_file(filename, vtype)

    sys.exit(rval)

if __name__ == '__main__':
    main()
