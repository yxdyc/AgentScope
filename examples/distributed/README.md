# Distributed multi-agent example

## Distributed dialogue (`distributed_dialog.py`)

This example run a assistant agent and a user agent as seperate processes and use rpc to communicate between them.

First, use the following command to start the assistant agent.

```
cd examples/distributed
python distributed_dialog.py --role assistant --assistant-host localhost --assistant-port 12010
# please make sure the port is available
# if the assistant agent and the user agent are started on different machines
# please fill in the ip address of the assistant agent in the host field
```

Then, run the user agent.

```
python distributed_dialog.py --role user --assistant-host localhost --assistant-port 12010
# if the assistant agent is started on another machine
# please fill in the ip address of the assistant agent in the host field
```

Now, you can chat with the assistant agent using the command line.

## Distributed debate competition (`distributed_debate.py`)

This example simulate a debate competition with three participant agents, including the affirmative side (**Pro**), the negative side (**Con**), and the adjudicator (**Judge**).

Pro believes that AGI can be achieved using the GPT model framework, while Con contests it. Judge listens to both sides' arguments and provides an analytical judgment on which side presented a more compelling and reasonable case.

Each agent is an independent process and can run on different machines.
Messages generated by any agents can be observed by other agents in the debate.

```
# step 1: setup Pro, Con, Judge agent server separately

# please make sure the ports are available and the ip addresses are accessible, here we use localhost as an example.
# if you run all agent servers on the same machine, you can ignore the host field, it will use localhost by default.

# setup Pro
cd examples/distributed
python distributed_debate.py --role pro --pro-host localhost --pro-port 12011

# setup Con
cd examples/distributed
python distributed_debate.py --role con --con-host localhost --con-port 12012

# setup Judge
cd examples/distributed
python distributed_debate.py --role judge --judge-host localhost --judge-port 12013


# step 2: run the main process

cd example/distributed
python distributed_debate.py --role main \
    --pro-host localhost --pro-port 12011 \
    --con-host localhost --con-port 12012 \
    --judge-host localhost --judge-port 12013


# step 3: watch the debate process in the terminal of the main process.
```
