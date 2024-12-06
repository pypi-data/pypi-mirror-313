# RecordLoader Extension for pyPhases

This package extends pyPhases with the ability to load generic records from a dataset. This package properly requires another more specific plugin to load the data.

This Extension adds:
- a normalized interface for a Signal (wraps a raw signal like numpy array): `pyPhasesRecordloader/Signal.py`
- a normalized interface for RecordSignals: `pyPhasesRecordloader/RecordSignal.py` containing a list of Signals
- an inerface to load data from datasets: `pyPhasesRecordloader/RecordLoader.py`
  - `loadRecord(recordName: str) -> RecordSignal` - check if a record exists
  - `exist(recordName: str) -> bool` - check if a record exists
  - `delete(recordName)` - delete a record
- some default Recordloader to load data itself or inherit from:
  - `EDFRecordLoader`
  - `H5RecordLoader`
  - `MatRecordLoader`
  - `WFDBRecordLoader`
  - `XMLAnnotationLoader`
- some possible ways to download data:
  - `Folderdownloader`: From a Folder
  - `HtmlDownloader`: From a Web Folder
  - `S3Downloader`: From a S3 compatible bucket storage
