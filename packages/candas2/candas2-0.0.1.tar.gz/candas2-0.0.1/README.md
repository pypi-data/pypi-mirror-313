# Candas2
This is a project inspired on the original Candas library by https://gist.github.com/JulianWgs, a blf file can be handle in a faster way using python data science classical libraries.

# Installation
```
pip install candas2
```

# Import module
```python
import candas2
```

#BLF file loading
The CAN file in BLF format is automatically converted into a DataFrame for subsequent processing.
The blf filepath should be provided.

```python
blf = Candas(r'C:\Users\Folder\file.blf')
```

# ID Filtering
IDs are filtered to allow for targeted analysis, ensuring only relevant data is processed.
id_filter --> str

```python
blf.id_filtering(id_filter)
```

# Time revision between each ID
The time interval between each ID is reviewed to ensure accurate temporal analysis and synchronization.

period_time(int) --> The time period between each ID, measured in milliseconds, is analyzed to ensure precise timing and synchronization in the data.

tolerance(int) --> As with all electronic instruments, a certain level of lag or tolerance is accounted for to ensure accurate data interpretation and analysis. It should be provided in a range from 0 to 100


```python
blf.time_rev(period_time, tolerance)
```
