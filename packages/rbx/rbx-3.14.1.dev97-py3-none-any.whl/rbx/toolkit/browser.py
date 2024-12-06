import base64
import tempfile

from playwright.sync_api import sync_playwright
from tqdm import tqdm

from .upload import upload


def record(
    url: str, width: int, height: int, duration: int, fps: int, path: str
) -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            args=[
                "--enable-begin-frame-control",
                "--run-all-compositor-stages-before-draw",
                "--disable-gpu",
            ]
        )
        page = browser.new_page()

        client = page.context.new_cdp_session(page)
        client.send("Network.enable")
        client.send("Page.enable")
        client.send("DOM.enable")
        client.send("HeadlessExperimental.enable")
        client.send("Runtime.enable")
        client.send(
            "Storage.clearDataForOrigin",
            {"origin": url, "storageTypes": "local_storage"},
        )

        page.set_viewport_size({"width": width, "height": height})
        page.goto(url, wait_until="networkidle")

        interval = 1000 / fps
        total = duration * fps
        frames = []
        counter = 1

        res = client.send("Emulation.setVirtualTimePolicy", {"policy": "pause"})
        client.send("HeadlessExperimental.beginFrame")
        initial = res["virtualTimeTicksBase"]

        with tqdm(desc="Recording session", total=total) as pbar:
            while True:
                res = client.send(
                    "HeadlessExperimental.beginFrame",
                    {
                        "frameTimeTicks": initial + counter * interval,
                        "screenshot": {"format": "png"},
                    },
                )
                if "screenshotData" in res:
                    frames.append(res["screenshotData"])

                client.send(
                    "Emulation.setVirtualTimePolicy",
                    {"policy": "advance", "budget": interval},
                )

                pbar.update(1)
                if counter >= total:
                    break

                counter += 1

        browser.close()

    for i, frame in enumerate(tqdm(frames, desc="Saving frames")):
        with open(f"{path}/frame_{i + 1}.png", "wb") as fd:
            fd.write(base64.b64decode(frame))


def screenshot(url: str, width: int, height: int, output: str) -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_viewport_size({"width": width, "height": height})
        page.goto(url, wait_until="networkidle")

        if output.startswith("s3://"):
            with tempfile.NamedTemporaryFile() as fp:
                page.screenshot(path=fp.name)
                upload(fp.name, output)
        else:
            page.screenshot(path=output)

        browser.close()
