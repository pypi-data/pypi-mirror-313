 # pymlogic

 a package for executing mindustry logic (mlog) code within python

 here's a basic example:
 ```py
 from pymlogic import Env, blocks

 #a simple mlog example program
 code = r"""
 Loop:
    op add i i 1
    print i
    print "\n"
 jump Loop lessThan i 50
 printflush message1
 stop
 """

 #create a new mlog environment
 env = Env()

 #create a message block, and add it to the environment
 message = blocks.Message()
 env.add(message, (1, 0))

 #create a processor with the code from before, and a link to the message block from before
 proc = blocks.Processor(code, links=[message])
 env.add(proc, (0, 0))

 while not env.halted:
    env.tick() #Env.tick() will execute a single tick for all processors in the environment
    env.wait() #Env.wait() waits some time so that the loop runs at 60 tps

#and finally print the contents of the message block
print(message.message)
```

## State of development

Implemented instructions:
 - `read`
 - `write`
 - `draw`
   - excluding `draw image`
 - `print`
 - `format`
 - `printflush`
 - `drawflush`
 - `getlink`
 - `control`
   - only `control enabled`
 - `sensor`
   - only `@x`, `@y`, `@enabled`
 - `set`
 - `op`
   - excluding `op noise`
 - `packcolor`
 - `wait`
 - `stop`
 - `end`
 - `jump`
 - `setrate`
