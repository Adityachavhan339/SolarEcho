# SolarEcho 🌞🔊

An open-source Python DSP application that transforms real-time NASA space weather data into ambient electronic audio landscapes. Built for the **Stardance Challenge** (NASA × Hack Club).

## What it does

SolarEcho polls NASA's DONKI database for Coronal Mass Ejection (CME) data, extracts plasma speed and angular width, and turns those numbers into a living drone:

- **Plasma speed (km/s)** → pitch/frequency
- **CME angular width (°)** → volume/amplitude 
- **Latitude / Longitude** → stereo panning & tremolo rate

The result is an immersive, data-driven audio experience representing live solar activity.

## Prerequisites

1. **Python 3.10+**
2. **NASA API Key** – get one free at [api.nasa.gov](https://api.nasa.gov)
3. **PortAudio** (required by `sounddevice`)
  - **macOS**: `brew install portaudio`
  - **Ubuntu/Debian**: `sudo apt-get install libportaudio2`
  - **Windows**: usually included in the wheel, but if you get errors install [ASIO4ALL](https://asio4all.org) or check sounddevice docs.

## Installation

```bash
pip install -r requirements.txt
```

## Running

Set your NASA key as an environment variable (so you never accidentally commit it):

```bash
export NASA_API_KEY="your-key-here"
python main.py
```

On Windows PowerShell:
```powershell
$env:NASA_API_KEY="your-key-here"
python main.py
```

Press **Ctrl+C** to stop.

## Project Structure

stardance-synthesizer/
├── nasa_client.py # Async NASA DONKI poller (aiohttp)
├── synthesizer.py # DSP audio engine (numpy + sounddevice)
├── main.py # Event-loop coordinator
├── requirements.txt # Dependencies
└── README.md # You are here!


## How the mapping works

| NASA Data Field | Audio Parameter | Mapping Range |
|-----------------|-----------------|---------------|
| `speed` (km/s)  | Base frequency  | 200–3000 km/s → 80–880 Hz (logarithmic) |
| `halfAngle` (°) | Amplitude       | 10–90° → 0.1–1.0 gain |
| `latitude` (°)  | Stereo pan      | −90° to +90° → left/right |
| `longitude` (°) | Tremolo speed   | −180° to +180° → 0.5–8 Hz |