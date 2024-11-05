## VICTRE Phantom Generator

This script generates a voxelized phantom using the [VICTRE Pipeline](https://github.com/DIDSR/VICTRE_PIPELINE).

The script must be located in the folder where the VICTRE Pipeline is installed and can be run typing in the terminal:

```python3
python3 phantom_generation.py
```

For now, preset parameters from [Victre/Constants.py](https://github.com/DIDSR/VICTRE_PIPELINE/blob/main/Victre/Constants.py) can be used.

It also enables set parameters manually modifying **define_arguments_manually** method and **arguments_generation** dictionary.