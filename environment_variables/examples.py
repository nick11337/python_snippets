from env import get_config, Vars, assign_stack, Stacks

assign_stack(stack=Stacks.DEV)
print(get_config(Vars.TEST1))
print(get_config(Vars.TEST2))

assign_stack(stack=Stacks.TEST)
print(get_config(Vars.TEST1))
print(get_config(Vars.TEST2))

assign_stack(stack=Stacks.PROD)
print(get_config(Vars.TEST1))
print(get_config(Vars.TEST2))