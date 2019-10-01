---
name: Single Qubit Hackathon
about: Handle contributions for the Single Qubit Hackathon
title: ''
labels: hackathon
assignees: quantumjim

---

Use this form to contribute the function you created for the [Single Qubit Hackathon](https://github.com/quantumjim/MicroQiskit/blob/master/Terrain-Hackathon.ipynb).

You were challened to create a new function to procedural generate terrain. Replace the code block below with the function you want to contribute.

```python
# define a function that determines a brightness for any given point
# uses a seed that is a list of four numbers
def get_brightness(x,y,qc,seed):
    qc.data.clear() # empty the circuit
    
    # perform rotations, whose angles depend on x and y
    qc.rx((1/8)*(seed[0]*x-seed[1]*y)*pi,0)
    qc.ry((1/8)*(seed[2]*x+seed[3]*y**2)*pi+pi,0)

    # calculate probability for outcome 1
    qc.measure(0,0)
    p = simulate(qc,shots=1000,get='counts')['1']/1000
    # return brightness depending on this probability
    # the chosen values here are fairly arbitrarily
    if p>0.7:
        if p<0.8:
            return 1
        elif p<0.9:
            return 2
        else:
            return 3
    else:
        return 0
```

**Describe the type of terrain your function creates**
Replace this line with a short description, such as 'It creates islands in a world with a strong easterly wind'.

**List the contributors**

- Replace this list...
- ...with GitHub handles and/or names...
- ...like James Wootton, IBM Research - Zurich (@quantumjim)

**License**

Please delete as appropriate to show whether you agree to your contribution being licensed under the [Apache 2.0 License](https://github.com/quantumjim/MicroQiskit/blob/master/LICENSE) and the Qiskit [Contribution License Agreement](https://qiskit.org/license/qiskit-cla.pdf).

**I agree**/**I do not agree**
