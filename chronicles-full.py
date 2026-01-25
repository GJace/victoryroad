import time
import random
import os
from datetime import datetime
from PIL import Image
import pyautogui

# Global stop flag
stop_flag = False


def humanize(seconds):
    """
    Add human-like variation to timing.
    Varies between -10% and +20% of the given time.
    """
    variation = random.uniform(-0.10, 0.20)
    return seconds * (1 + variation)


def listen_for_stop():
    """Listen for 'Q' key press to stop the script"""
    global stop_flag

    def on_press(key):
        global stop_flag
        try:
            if key.char == "q":
                stop_flag = True
                print("\n[STOP] Q pressed - stopping script...")
        except AttributeError:
            pass

    listener = keyboard.Listener(on_press=on_press)
    listener.daemon = True
    listener.start()


def press_key(key, duration=2):
    """Press and release a keyboard key"""
    wait_time = humanize(duration)
    print(f"[KEY] Pressing '{key}' (waiting {wait_time:.2f}s after)")
    pyautogui.press(key)
    time.sleep(wait_time)


def take_screenshot(filename=None):
    """Take a screenshot and optionally save it"""
    screenshot = pyautogui.screenshot()
    if filename:
        # Create rewards folder if it doesn't exist
        os.makedirs("rewards", exist_ok=True)
        filepath = os.path.join("rewards", filename)
        screenshot.save(filepath)
        print(f"[SCREENSHOT] Saved: {filepath}")
    return screenshot


def compare_screenshots(img1, img2, threshold=0.95):
    """
    Compare two screenshots to detect if screen has changed.
    Returns True if images are similar (above threshold).
    Returns False if significantly different (screen changed).
    threshold: 0-1, where 1 is identical and 0 is completely different
    """
    if img1.size != img2.size:
        return False

    # Simple pixel-by-pixel comparison
    pixels1 = list(img1.getdata())
    pixels2 = list(img2.getdata())

    matching = sum(1 for p1, p2 in zip(pixels1, pixels2) if p1 == p2)
    similarity = matching / len(pixels1)

    return similarity >= threshold


def wait_for_screen_change(timeout=60, check_interval=0.5):
    """
    Wait for the screen to change by comparing screenshots.
    Returns True if screen changed, False if timeout.
    """
    print(f"[WAIT] Waiting for screen change (timeout: {timeout}s)...")

    baseline = take_screenshot()
    start_time = time.time()

    while time.time() - start_time < timeout:
        if stop_flag:
            return False

        time.sleep(check_interval)
        current = take_screenshot()

        # If screen has changed significantly
        if not compare_screenshots(baseline, current, threshold=0.90):
            print("[WAIT] Screen change detected!")
            return True

    print(f"[WAIT] Timeout reached ({timeout}s)")
    return False


def start_game():
    """Start the game with the initial sequence"""
    print("[START] Starting game sequence...")

    # Enter
    press_key("return")

    # 4 times arrow down
    for i in range(4):
        press_key("down")

    # Enter
    press_key("return")

    # Enter
    press_key("return")

    # Enter
    press_key("return")

    # Wait 10 seconds
    print("[START] Waiting 10 seconds...")
    time.sleep(humanize(10))

    # Enter
    press_key("return")

    # Wait 5 seconds
    print("[START] Waiting 5 seconds...")
    time.sleep(humanize(5))

    # Enter
    press_key("return")

    # Wait 10 seconds (team walking in)
    print("[START] Waiting 10 seconds (team walking in)...")
    time.sleep(humanize(10))

    # Enter
    press_key("return")

    # Enter
    press_key("return")

    # Click (kickoff)
    print("[START] Waiting 5 seconds before kickoff...")
    time.sleep(humanize(5))

    print("[CLICK] Clicking for kickoff")
    pyautogui.click()
    time.sleep(humanize(1))

    # U (auto mode)
    press_key("u")

    # C (camera)
    press_key("c")

    print("[START] ✓ Game started successfully!")


def farm_cycle(cycle_num=1):
    """Execute one complete farm cycle"""
    print(f"\n{'='*50}")
    print(f"[CYCLE {cycle_num}] Starting farm cycle")
    print(f"{'='*50}")

    try:
        # Start the game
        start_game()

        # Wait 4 minutes (first half)
        print("[CYCLE] Waiting 4 minutes for first half...")
        time.sleep(humanize(240))

        # Left click
        print("[CYCLE] Pressing alt to proceed")
        press_key("alt")

        # Enter
        press_key("return")

        # Wait 4 minutes (second half)
        print("[CYCLE] Waiting 4 minutes for second half...")
        time.sleep(humanize(240))

        # Enter
        press_key("return")

        # Wait 5 seconds before screenshot
        print("[CYCLE] Waiting 5 seconds...")
        time.sleep(humanize(5))

        # Save screenshot
        print("[CYCLE] Saving loot screenshot...")
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        take_screenshot(f"{timestamp}_reward_n_{cycle_num}.png")

        # Enter
        press_key("return")

        # Wait 10 seconds
        print("[CYCLE] Waiting 10 seconds...")
        time.sleep(humanize(10))

        print(f"[CYCLE {cycle_num}] ✓ Cycle completed successfully!")
        return True

    except Exception as e:
        print(f"[ERROR] Exception in cycle: {e}")
        return False


def main():
    """Main farming loop"""
    print("=" * 50)
    print("Inazuma Eleven Victory Road Auto Farm")
    print("=" * 50)
    print("Press Ctrl+C to stop the script")
    print("Starting in 11 seconds...")
    time.sleep(11)

    try:
        cycle_count = 0

        while True:
            cycle_count += 1

            success = farm_cycle(cycle_count)

            if not success:
                print("[MAIN] Cycle failed - pausing 10 seconds before retry...")
                time.sleep(10)
                continue

            # Small delay between cycles
            print("[MAIN] Waiting 5 seconds before next cycle...")
            time.sleep(5)

    except KeyboardInterrupt:
        print("\n[MAIN] ✓ Script stopped cleanly (Ctrl+C)")
    except Exception as e:
        print(f"\n[MAIN] Fatal error: {e}")
    finally:
        print("[MAIN] Cleaning up...")


if __name__ == "__main__":
    main()
