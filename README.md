CS 3240: Turing Machine Simulator
=================================
My Python implementation of a Turing machine, in particular with a configuration which decides the language consisting of twice as many 0s as 1s.

Execution
---------
Input the string you want to run through the machine in `inputs.txt`, then invoke `python machine.py` to compute. The sequence of machine configurations will be outputted to `outputs.txt`.

In the output file, a caret below a cell on the tape indicates the head position. Following the tape contents, `=> state` indicates which state the machine is currently in. States prefixed with a `+` are accept states, and those prefixed with a `-` are reject states.
