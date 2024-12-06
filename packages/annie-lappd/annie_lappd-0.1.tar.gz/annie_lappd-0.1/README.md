# annie_lappd

This is a Python package that reads and processes the ASCII files

## Installation

You can install the package using pip:

```bash
pip install annie_lappd
```

## Examples:

```bash
from annie_lappd import plotLAPPD

events = 2
data = 'datafile.txt'
pedestal1 = 'pedestal01.txt'
pedestal2 = 'pedestal02.txt'

pedestals = [pedestal1, pedestal2]

lappd = plotLAPPD(data, pedestals)
lappd.pedestalSubtraction
lappd.convertADCtoVoltage
lappd.correctingACDCmetadata
lappd.convertACDCtoStripIndex
lappd.baselineCorrection(50)
lappd.filterFFT

lappd.displayEvent(4, 1, 1)
```
