# SolarEcho 🌞🔊

An open-source Python DSP application that transforms real-time NASA space weather data into ambient electronic audio landscapes. Built for the **Stardance Challenge** (NASA × Hack Club).

## 🚀 Run Instantly via pipx (No Cloning Required)

You can run this project with a single command without downloading any files or setting up virtual environments manualy! Ensure you have `pipx` installed (`sudo apt install pipx`), then execute:

```bash
pipx run --spec git+https://github.com/Adityachavhan339/SolarEcho solarecho
```

*Note: Make sure to set your `NASA_API_KEY` environment variable first, or it will default to a public `DEMO_KEY` with restricted request limits.*

## What it does

SolarEcho polls NASA's DONKI database for Coronal Mass Ejection (CME) data, extracts plasma speed and angular width, and turns those numbers into a living drone:

- **Plasma speed (km/s)** → pitch/frequency
- **CME angular width (°)** → volume/amplitude 
- **Latitude / Longitude** → stereo panning & tremolo rate

The result is an immersive, data-driven audio experience representing live solar activity.

## Prerequisites

If you plan to run the project locally or via `pipx`, ensure your machine has the system-level audio dependencies installed:

- **Ubuntu/Debian**: `sudo apt-get install libportaudio2`
- **macOS**: `brew install portaudio`
- **Windows**: Built-in, but if errors occur install [ASIO4ALL](https://asio4all.org).

## Local Development Installation

If you prefer to clone and tweak the code layout locally:

```bash
# Clone the repository
git clone https://github.com/Adityachavhan339/SolarEcho/
cd SolarEcho

# Install project dependencies
pip install -r requirements.txt
```

## Running Manually

Set your NASA key as an environment variable so you never accidentally commit your private credentials:

### Linux / macOS:
```bash
export NASA_API_KEY="your-key-here"
python3 -m src.solarecho.main
```

### Windows PowerShell:
```powershell
$env:NASA_API_KEY="your-key-here"
python -m src.solarecho.main
```

Press **Ctrl+C** to stop the audio engine gracefully.

## Project Structure

```text
SolarEcho/
├── pyproject.toml      # Modern packaging metadata & entrypoint definition
├── requirements.txt    # Project dependencies listing
├── README.md           
└── src/
    └── solarecho/
        ├── __init__.py # Package initialization
        ├── main.py     # Event-loop coordinator & entrypoint
        ├── nasa_client.py   # Async NASA DONKI telemetry poller (aiohttp)
        └── synthesizer.py   # Audio synthesis DSP engine (numpy + sounddevice)
```

## How the mapping works


| NASA Data Field | Audio Parameter | Mapping Range |
|-----------------|-----------------|---------------|
| `speed` (km/s)  | Base frequency  | 200–3000 km/s → 80–880 Hz (logarithmic) |
| `halfAngle` (°) | Amplitude       | 10–90° → 0.1–1.0 gain |
| `latitude` (°)  | Stereo pan      | −90° to +90° → left/right |
| `longitude` (°) | Tremolo speed   | −180° to +180° → 0.5–8 Hz |
| 10–90° → 0.1–1.0 gain |
| `latitude` (°)  | Stereo pan      | −90° to +90° → left/right |
| `longitude` (°) | Tremolo speed   | −180° to +180° → 0.5–8 Hz |
