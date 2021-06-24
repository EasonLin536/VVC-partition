# VVC_partition
A recursive implementation of VVC partition from [[1]](#1).

## Usage
### Install packages
``` bash
pip3 install -r requirements.txt
```
## Execute
``` bash
python3 src/main.py <input_image> <output_image>
```
Don't use `input_image` with resolution higher than **1080p**, or the runtime would be extremely long.

## Parameters
* `CTU_SIZE` and `MAX_DEPTH` in `src/main.py` specify the size of coding tree unit and the maximum partition depth. 
* `MIN_CU_SIZE` in `src/CodingUnit.py` specifies the minimum coding unit size.
* In `src/early_terminate.py`, if a coding unit's variance is lower than `TH_1`, further partition will be terminated.
* In `src/gradient_select.py`, `TH_2` and `TH_3` specify the threshold for selecting QT over MT.
> Note that different parameters leads to different time required for execution.

## Example
![example](asset/example_1.png)

## References
<a id="1">[1]</a> 
Y. Fan, J. Chen, H. Sun, J. Katto and M. Jing, "A Fast QTMT Partition Decision Strategy for VVC Intra Prediction," in IEEE Access, vol. 8, pp. 107900-107911, 2020