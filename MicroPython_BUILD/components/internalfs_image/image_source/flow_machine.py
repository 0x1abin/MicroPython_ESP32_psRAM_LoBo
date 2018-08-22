from m5stack import *
from mstate import MState, MStateManager
import utime as time

# Exit prev thread
if _ctx.get("loop_state"):
    _ctx["loop_state"] = False
    while _ctx["loop_state"] != "exit":
        pass

# ================ APP1 ================
def app1_enter(ctx):
    print('app1_enter')
    pass

def app1_loop(ctx):
    if buttonC.wasPressed():
        ctx['mstate'].change("APP2_STATE")

def app1_end(ctx):
    pass


# ================ APP2 ================
def app2_enter(ctx):
    print('app2_enter')
    pass

def app2_loop(ctx):
    if buttonC.wasPressed():
        ctx['mstate'].change("APP1_STATE")

def app2_end(ctx):
    pass


# ======== Flow machine Manager ========
flow_machine = MStateManager()
flow_machine.register("APP1_STATE", MState(start=app1_enter, loop=app1_loop, end=app1_end))
flow_machine.register("APP2_STATE", MState(start=app2_enter, loop=app2_loop, end=app2_end))
flow_machine.start("APP1_STATE")


_ctx["loop_state"] = True
while _ctx["loop_state"]:
    flow_machine.run()
_ctx["loop_state"] = "exit"


# test api: http://api.m5stack.com/v1/51ab5c8c84275190a642b3030e775bb4/thread
