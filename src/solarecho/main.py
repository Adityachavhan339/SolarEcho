import asyncio
import os
import signal

from .import synthesizer
from .nasa_client import cme_poller
from .synthesizer import SolarEchoSynthesizer


API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")
POLL_INTERVAL = 60   

#-----------------------------------------------------------------
# Shutdown handler
#-----------------------------------------------------------------

shutdown_event = asyncio.Event()

def _on_sigint():
    print("\n[MAIN] Shutdown signal received.")
    shutdown_event.set()

async def bridge(queue: asyncio.Queue, synth: SolarEchoSynthesizer):
    while not shutdown_event.is_set():
        try:
            params = await asyncio.wait_for(queue.get(), timeout=1.0)
            #print("[BRIDGE] Sending params to synth:", params)
            synth.update_params(params)
            queue.task_done()
        except asyncio.TimeoutError:
            continue

async def main():
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, _on_sigint)

    queue = asyncio.Queue(maxsize=4)
    synth = SolarEchoSynthesizer()
    synth.start()

    print("=" * 50)
    print("  SolarEcho is live 🌞")
    print("  Listening to the Sun via NASA DONKI...")
    print("  Press Ctrl+C to stop.")
    print("=" * 50)

    poller_task = asyncio.create_task(cme_poller(queue, API_KEY, POLL_INTERVAL))
    bridge_task = asyncio.create_task(bridge(queue, synth))

    await shutdown_event.wait()
    print("[MAIN] Shutting down...")
    synth.stop()
    poller_task.cancel()
    bridge_task.cancel()
    try:
        await poller_task
    except asyncio.CancelledError:
        pass
    try:
        await bridge_task
    except asyncio.CancelledError:
        pass
    print("[MAIN] See You Later!")


def run_app():
    asyncio.run(main())

if __name__ == "__main__":
    run_app()
