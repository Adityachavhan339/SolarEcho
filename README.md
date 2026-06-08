# SolarEcho 🌞🔊

SolarEcho is an open-source Python DSP application that transforms live NASA space weather data into ambient electronic audio landscapes.

Built for the Stardance Challenge, it pulls NASA DONKI Coronal Mass Ejection (CME) data and maps live solar values into sound parameters like pitch, loudness, tremolo, and stereo movement.

## Quick Start with pipx

The easiest way to try SolarEcho is with `pipx`, which runs Python applications in isolated environments.

First, make sure `pipx` is installed.

### Ubuntu / Debian
```bash
sudo apt install pipx
pipx ensurepath
```

### macOS
```bash
brew install pipx
pipx ensurepath
```

### Windows
```powershell
py -m pip install --user pipx
pipx ensurepath
```

Then set your NASA API key:

### Linux / macOS
```bash
export NASA_API_KEY="your-key-here"
```

### Windows PowerShell
```powershell
$env:NASA_API_KEY="your-key-here"
```

Now run SolarEcho directly from GitHub:

```bash
pipx run --spec git+https://github.com/Adityachavhan339/SolarEcho solarecho
```

If you do not set `NASA_API_KEY`, SolarEcho falls back to NASA's public `DEMO_KEY`, which has much lower request limits than a personal key [web:1][web:168].

## What SolarEcho does

SolarEcho polls NASA's DONKI database for recent CME events and converts space weather values into audio in real time.

### Sonification mapping

- **Plasma speed (km/s)** → pitch / frequency
- **CME half-angle (°)** → loudness / amplitude
- **Latitude** → stereo panning
- **Longitude** → tremolo speed

This creates a continuously shifting ambient drone based on real solar activity.

## System dependencies

`pipx` installs the Python package cleanly, but SolarEcho still depends on your operating system's audio stack.

### Ubuntu / Debian / Linux Mint
```bash
sudo apt update
sudo apt install libportaudio2 portaudio19-dev ffmpeg
```

### macOS
```bash
brew install portaudio ffmpeg
```

### Windows
Usually `sounddevice` works directly, but if audio errors occur you may need PortAudio-compatible drivers or additional setup.

## Local development

If you want to clone and modify the project:

```bash
git clone https://github.com/Adityachavhan339/SolarEcho.git
cd SolarEcho
pip install -r requirements.txt
```

Then run:

```bash
python3 -m src.solarecho.main
```

## Project structure

```text
SolarEcho/
├── pyproject.toml
├── requirements.txt
├── README.md
└── src/
    └── solarecho/
        ├── __init__.py
        ├── main.py
        ├── nasa_client.py
        └── synthesizer.py
```

## How to test it

1. Install the system audio dependencies.
2. Set your NASA API key.
3. Run the app with `pipx run --spec git+https://github.com/Adityachavhan339/SolarEcho solarecho`
4. Wait for a CME event line to appear in the terminal.
5. Listen for the ambient audio output.

## Known limitations

- NASA DONKI is polled periodically rather than streamed live.
- Some CME records may omit fields, so fallback defaults are used.
- Audio behavior depends on local speaker/output configuration.
- NASA API usage is rate-limited across `api.nasa.gov` requests [web:1][web:168].

## Why I built this

I wanted to turn scientific telemetry into something people could hear, not just read. SolarEcho explores space weather as a creative medium by combining NASA open data, async Python networking, and real-time digital signal processing.

## License

MIT
