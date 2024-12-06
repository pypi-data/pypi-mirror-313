# gocadgo

## To Do

- [x] Add depedencies <br>
- [x] Add example code and readme. <br>
- [x] k_p, k_t calcs <br>
- [ ] Add link to documentation <br>
- [ ] ensure network is connected correctly and propagates - check error <br>
- [x] get the fields to actually print (somehow) <br>

## Installation

```bash
pip install gocadgo
```

This code creates a Network of Cell elements, with heat transfer properties approximated to heat transfer in the pipe of
a heat exchanger. The cells in the network are connected using a pre-defined flow defintion, and the solution is updated
iteratively.

## Basic Usage

```python
from gocadgo.network import Network
from gocadgo.plotter import show_fields

# scaling size 400 for mesh. Create mesh and run network:
from_task = Network('from_task.json')

# re-run with new mesh size finding k_t and k_p.
actual_size = Network('actual_size.json', from_task.k_t, from_task.k_p)

# display fields of interest on network hot or cold network:
show_fields(from_task.hot_network, 'T')
```
##### Input
Input is undertaken using a json file, in the following format:  <br>

**sim**: simulation conditions <br>
**cold**: cold side of heat exchanger <br>
**hot**: hot side of heat exchanger network  <br>
**i**: initial cell conditions, in order of key_list <br>
**s**: second cell conditions, in order of key list <br>
```json
{
  "sim": {
    "dimensions": [8, 8, 20],
    "key_list": ["T", "P", "m"]
  },
  "cold": {
    "i": [20, 100000, 0.034],
    "gas_type": "air",
    "s": [ 30, 99985]
  },
  "hot": {
    "i": [ 350, 4400000, 0.01],
    "gas_type": "N2",
    "s": [ 318, 4399995]
  }
}
```

### Documentation
TO DO 
## How Conjugate Heat Transfer is Calculated

Heat exchange transfer rate can be approximated by the equation below. In a parallel flow heat exchanger, there is a
balance in the Q values of the two cells.

Q = m_c * C_p * (T_out - T_in)

Overall for heat exchangers with a heat exchange coefficient of U: 
Q = U A (T_out - T_in)

Assume no losses, and assume negligable conductivity, therefore: 
Q_hot = Q_cold

For the network, we rearrange and reformulate the above equations to get a pressure_based constant and a temperature_based constant:  
k_p = (P_1(C) - P_0(C)) / rho_1(C) * m_dot(C) <br>
k_t = (T_1(H) - T_0(H)) * m_dot(H) * c_p(H) /((T_0(H) - T_0(C))

These are assumed constant and can be used for stepping through the rest of the network


