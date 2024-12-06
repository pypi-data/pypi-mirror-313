# PSOut Reader

A reader for the PSCAD *.psout file

## Example

```python
import mhi.psout
import matplotlib.pyplot as plt

with mhi.psout.File('Cigre.psout') as file:

    ac_voltage = file.call("Root/Main/AC Voltage/0")
    run = file.run(0)

    for call in ac_voltage.calls():
        trace = run.trace(call)
        time = trace.domain
        plt.plot(time.data, trace.data, label=trace['Description'])

    plt.xlabel(time['Unit'])
    plt.ylabel(trace['Unit'])
    plt.legend()
    plt.show()
```

## Documentation

See: ``py -m mhi.psout help``
