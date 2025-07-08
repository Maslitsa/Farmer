#!/usr/bin/env python3
# send_whatsapp.py
#
# Dependencies:
#   pip install selenium chromedriver-autoinstaller

import os
import sys
import re
import time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# — Your message —
PREDEFINED_MESSAGE = (
    "Здравствуйте! У меня есть одна идея, которой я хотел бы с Вами поделиться. Это возможно?"
)

def choose_file_or_arg() -> str:
    """
    If a valid filename was passed on the command line, use it.
    Otherwise list .txt files in cwd and ask the user to pick one.
    """
    # 1) Check argv
    if len(sys.argv) > 1:
        fn = sys.argv[1]
        if os.path.isfile(fn):
            return fn
        else:
            print(f"File not found: '{fn}'\n")

    # 2) Scan for .txt files
    txts = [f for f in os.listdir('.') if f.lower().endswith('.txt')]
    if not txts:
        print("No .txt files found in this folder. Exiting.")
        sys.exit(1)

    print("Please choose a .txt file from the list below:")
    for i, f in enumerate(txts, start=1):
        print(f"  {i}. {f}")
    print("  0. Cancel / Exit")

    while True:
        choice = input("Enter number: ").strip()
        if choice == '0':
            print("Exiting.")
            sys.exit(0)
        if choice.isdigit() and 1 <= int(choice) <= len(txts):
            return txts[int(choice)-1]
        print("Invalid choice, try again.")

def load_whatsapp_numbers(filename: str) -> list[str]:
    """
    Reads the file, finds lines like 'WhatsApp : 77012345678' (case-insensitive),
    extracts the digits (drops '+'), skips empty/'None', and returns a list.
    """
    pattern = re.compile(r'WhatsApp\s*:\s*([0-9+,\s]+)', re.IGNORECASE)
    numbers: list[str] = []

    with open(filename, encoding='utf-8') as f:
        for line in f:
            m = pattern.search(line)
            if not m:
                continue
            chunk = m.group(1).strip()
            if not chunk or chunk.lower() == 'none':
                continue
            # if there are multiple numbers separated by commas, split them
            for part in chunk.split(','):
                num = part.strip().lstrip('+')
                if num.isdigit():
                    numbers.append(num)
    # dedupe while preserving order
    seen = set()
    unique = []
    for x in numbers:
        if x not in seen:
            seen.add(x)
            unique.append(x)
    return unique

def send_whatsapp_messages(numbers: list[str], profile_path: str = "./whatsapp_profile"):
    """
    Opens WhatsApp Web once (QR-scan if needed), then for each phone:
    - navigates to the chat
    - waits for the conversation panel (#main)
    - finds the message input box in the footer
    - clears any draft (Ctrl+A, Del)
    - types PREDEFINED_MESSAGE and presses Enter
    """
    # auto-install the matching ChromeDriver
    chromedriver_autoinstaller.install()

    opts = Options()
    opts.add_argument(f"--user-data-dir={os.path.abspath(profile_path)}")
    opts.add_argument("--profile-directory=Default")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=opts)
    wait   = WebDriverWait(driver, 60)

    # 1) Open WhatsApp Web and wait for sidebar
    driver.get("https://web.whatsapp.com/")
    print("Open WhatsApp Web and scan the QR code if this is your first run…")
    wait.until(EC.presence_of_element_located((By.ID, "pane-side")))
    print("✅ Logged in. Starting message loop…\n")

    # 2) Iterate numbers
    for idx, phone in enumerate(numbers, start=1):
        print(f"[{idx}/{len(numbers)}] → {phone}")
        driver.get(f"https://web.whatsapp.com/send?phone={phone}&app_absent=0")
        try:
            # wait until the chat container loads
            wait.until(EC.presence_of_element_located((By.ID, "main")))
            # now find the footer input
            msg_box = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "#main footer div[contenteditable='true']"
            )))
            time.sleep(0.3)
            # clear any existing draft, type & send
            msg_box.send_keys(Keys.CONTROL, "a", Keys.DELETE)
            msg_box.send_keys(PREDEFINED_MESSAGE)
            time.sleep(0.2)
            msg_box.send_keys(Keys.ENTER)
            print("   ✔ Sent")
        except Exception as e:
            print("   ✘ Failed:", e)
        time.sleep(2)  # brief pause

    driver.quit()
    print("\nAll done. Browser closed.")

if __name__ == "__main__":
    # on Windows ensure UTF-8 output
    if os.name == "nt":
        os.system("chcp 65001 > nul")

    fn = choose_file_or_arg()
    print(f"\nLoading WhatsApp numbers from: {fn}\n")
    nums = load_whatsapp_numbers(fn)
    if not nums:
        print("No valid WhatsApp numbers found in that file. Exiting.")
        sys.exit(0)

    print(f"→ {len(nums)} unique numbers extracted. Launching WhatsApp Web…\n")
    send_whatsapp_messages(nums)