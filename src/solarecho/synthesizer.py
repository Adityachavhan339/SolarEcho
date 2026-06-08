import numpy as np
import sounddevice as sd
import threading

class SolarEchoSynthesizer:
    def __init__(self, samplerate: int = 44100, blocksize: int = 512):
        self.samplerate = samplerate
        self.blocksize = blocksize
        self.lock = threading.Lock()

        self.params = {
            "speed": 500.0,
            "halfAngle": 30.0,
            "latitude": 0.0,
            "longitude": 0.0,
        }

        self._phase = 0.0
        self._phase_harmonic = 0.0
        self._phase_mod = 0.0
        self._stream = None

        self._prints_left = 2
        self._last_signature = None

    def update_params(self, new_params: dict):
        with self.lock:
            old_signature = (
                self.params["speed"],
                self.params["halfAngle"],
                self.params["latitude"],
                self.params["longitude"],
            )

            self.params.update(new_params)

            new_signature = (
                self.params["speed"],
                self.params["halfAngle"],
                self.params["latitude"],
                self.params["longitude"],
            )

            if new_signature != old_signature:
                self._prints_left = 2
                self._last_signature = new_signature

    def start(self):
        self._stream = sd.OutputStream(
            samplerate=self.samplerate,
            channels=2,
            dtype="float32",
            blocksize=self.blocksize,
            callback=self._callback,
        )
        self._stream.start()
        print("[AUDIO] Output stream started successfully")

    def stop(self):
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None

    def _speed_to_freq(self, speed: float) -> float:
        s = np.clip(speed, 200.0, 3000.0)
        t = (np.log10(s) - np.log10(200.0)) / (np.log10(3000.0) - np.log10(200.0))
        return 80.0 + t * (880.0 - 80.0)

    def _half_angle_to_amp(self, angle: float) -> float:
        return 0.1 + 0.9 * np.clip((angle - 10.0) / 80.0, 0.0, 1.0)

    def _latitude_to_pan(self, lat: float) -> float:
        return np.clip(lat / 90.0, -1.0, 1.0)

    def _longitude_to_mod(self, lon: float) -> float:
        return 0.5 + 7.5 * ((lon + 180.0) / 360.0)

    def _callback(self, outdata, frames, time_info, status):
        with self.lock:
            p = self.params.copy()

        if self._prints_left > 0:
            print(
                f"[AUDIO CALLBACK] speed={p['speed']} "
                f"halfAngle={p['halfAngle']} "
                f"lat={p['latitude']} "
                f"lon={p['longitude']}"
            )
            self._prints_left -= 1

        if status:
            print("[AUDIO STATUS]", status)

        freq = self._speed_to_freq(p["speed"])
        amp = self._half_angle_to_amp(p["halfAngle"])
        pan = self._latitude_to_pan(p["latitude"])
        mod_freq = self._longitude_to_mod(p["longitude"])

        t = np.arange(frames) / self.samplerate

        phase = self._phase + freq * t
        phase_h = self._phase_harmonic + (freq * 1.5) * t
        phase_m = self._phase_mod + mod_freq * t

        mod = 0.5 + 0.5 * np.sin(2.0 * np.pi * phase_m)

        gain = 4.0
        wave = gain * amp * mod * (
            0.6 * np.sin(2.0 * np.pi * phase) +
            0.4 * np.sin(2.0 * np.pi * phase_h)
        )
        wave = np.clip(wave, -1.0, 1.0)

        angle = 0.25 * np.pi * (pan + 1.0)
        left_gain = np.cos(angle)
        right_gain = np.sin(angle)

        outdata[:, 0] = wave * left_gain
        outdata[:, 1] = wave * right_gain

        self._phase = (phase[-1] + freq / self.samplerate) % 1.0
        self._phase_harmonic = (phase_h[-1] + (freq * 1.5) / self.samplerate) % 1.0
        self._phase_mod = (phase_m[-1] + mod_freq / self.samplerate) % 1.0