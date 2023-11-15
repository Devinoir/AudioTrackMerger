
# Audio Track Merger

Audio Track Merger is a Python application with a graphical user interface (GUI) designed to merge multiple audio tracks in a video file. It uses FFmpeg, a powerful multimedia framework, to process video files and merge their audio tracks. The GUI is built with CustomTkinter to provide a modern, flat, and user-friendly experience.

## Features

- Merge two audio tracks in a video file into one.
- Display progress of the merging process.
- Modern GUI with progress bar and status messages.
- Easy to use with Browse and Save As dialogs for file selection.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your system.
- FFmpeg installed and added to your system's PATH.
- CustomTkinter library installed (can be installed via pip).

## Installation

Clone the repository or download the source code to your local machine:

```
git clone https://github.com/Devinoir/AudioTrackMerger.git
```

Navigate to the project directory and install the required Python packages using the requirements.txt file:

```
pip install -r requirements.txt
```

## Usage

To run the application, execute the following command in the project's root directory:

```
python main.py
```

Once the application starts:

1. Click the "Browse" button to select the input video file.
2. Click the "Save As..." button to specify the location and name of the output video file.
3. Click the "Merge Audio Tracks" button to start the merging process.

The progress bar will indicate the progress of the merging process, and a success message will be displayed once the operation is complete.

## Contributing

Contributions to the Audio Track Merger project are welcome. To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

## License

Distributed under the MIT License. See `LICENSE` for more information.
