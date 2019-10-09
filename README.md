# A Linux Temperature Testing Experiment

When building a new system, it's easy to gloss over some seemingly insignificant details, like which directions to point 
your fans. Multiple logics exist, like your fans should direct air from the front to the back of the case, or it's 
better to create negative pressure drawing air out of the case. Of course, any logical hypothesis sounds good, 
but how to they actually work in practice?

Here, I set out to figure that out, testing a couple common configurations with my six 120mm fans and a rigorous testing 
method.

## Methodology

With any experiment, a sound methodology is needed to get reliable and repeatable results. To do this, I'll be implementing the same configuration for every test. Once a fan configuration is created, the tests will proceed as follows:

1) System is booted without networking, and left idle for 15 minutes. This should nearly eliminate differences in 
running state. No other applications will be run at the time of testing and the system will be left alone. 

2) Tests will be run from bash scripts to ensure similar timing and logging across multiple configurations. 

3) Multiple runs on the same fan configuration will be spaced by [TK] minutes to allow for a complete cool-down to idle 
temperatures before repeat tests.

4) A minimum of three trials will be conducted on each configuration, and first checked for consistency before other 
analyses.

### Fan Configurations
I'll only be testing a subset of all possible fan combinations on my system, which is housed in a CoolerMaster HAF 912 
Mid Tower case. With support for a variety of 120mm, 140mm and a single optional 200mm fan, theres nearly infinite 
combinations available. Even with the six, 120mm fans I have available, there's a staggering 216 options (6^3) if you 
consider fans can be pointing in, out, or be altogether disabled. Assuming fans are better off than on still creates 36 
(6^2) options, so I'll only be testing a small subset of these, relying on a couple hypotheses to test out. Of course, 
anyone is welcome to a more exhaustive testing on their own systems.

#### Configurations used

Tests will be denoted by a ASCII-art diagram of the case, with +/- denoting fans pushing air in or pulling air out respectively.

In the below diagram, 'F' represents the front of the case. The CPU, GPU, and PSU are labeled to denote how the 
internals of the system are organized. The PSU also has a [TK]mm fan that is always drawing air out -- it is not labeled but 
the direction will be the same in all configurations. In this configuration, two front fans and a side fan pull air in, and two top and a 
back fan pull air out. In theory, air flows from the front and side fans past the GPU, CPU, and up/out the top and 
back of the case. 

<pre>
    ________________F
    |   - -        |
    | -   CPU      |
    |              |
    | GUP  +      +|
    |----          |
    |PSU|         +|
    ----------------
</pre>

## Layout

### /testing
Testing contains the scripts responsible for running stress tests together.

### /logging
Logging contains the scripts responsible for logging temperatures.

### /analysis
Analysis contains mostly Python scripts for processing the created data into more usable forms, then plotting and 
further analyzing the subsequent data.