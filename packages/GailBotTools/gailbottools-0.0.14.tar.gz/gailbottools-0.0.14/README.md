# GailBotPluginsTools

## Overview

GailBotPluginsTools is a package designed to facilitate the creation and management of plugins for the GailBot platform. It simplifies the interaction with transcriptions, providing data handlers that manipulate XML markers and utterances.

## Features

- **Marker Utterance Dictionary**: Efficiently manages utterances, their timings, and speaker information.
- **Structured Interaction**: Provides an outer layer that wraps around the marker utterance dictionary for enhanced functionality.
- **Data Objects**: Defines necessary data structures for handling utterances effectively.

## Usage

The package includes several key modules:

### `marker_utterance_dict.py`

- **Class**: `MarkerUtteranceDict`
- **Purpose**: Creates a dictionary to manage utterances, keeping track of speaker information, start and end times, and overlaps.
- **Key Methods**:
  - `__init__`: Initializes the dictionary with utterance data.
  - `turn_criteria_overlaps`: Checks if the difference between two utterances meets a defined threshold.

### `StructureInteract.py`

- **Class**: `StructureInteract`
- **Purpose**: Interacts with the marker utterance dictionary and manages the output path for plugin results.
- **Key Methods**:
  - `apply`: The main driver function that processes the input data and populates the data structure.
  - `parse_xml_to_gbpluginmethods`: Converts XML data into a format usable by the GailBot Plugin methods.

### `data_objects.py`

- **Class**: `UttObj`
- **Purpose**: Defines the structure for an utterance object, encapsulating its properties like start time, end time, speaker, and text.

## Installation

To install the package, use the following command:

```bash
pip install gailbottools
```

## Example

Here is a simple example of how to use the package:

```python
from gailbot_plugin_tools import StructureInteract

# Sample XML data
xml_data = """
<transcript>
    <u speaker="Speaker1">
        <w start="0.0" end="0.5">Hello</w>
        <w start="0.6" end="1.0">World</w>
    </u>
</transcript>
"""

# Create an instance of StructureInteract
interactor = StructureInteract()
# Apply the XML data
interactor.apply(xml_data)
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for suggestions and enhancements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

- Hannah Shader
- Jason Wu
- Jacob Boyar
- Vivian Li
- Eva Caro
- Manuel Pena
