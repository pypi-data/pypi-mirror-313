from invoke import Collection, Program
from petljapub import tasks
program = Program(namespace=Collection.from_module(tasks), version='2.1.4')
