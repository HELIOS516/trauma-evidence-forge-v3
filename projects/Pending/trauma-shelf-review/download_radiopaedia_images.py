#!/usr/bin/env python3
"""Download full-resolution images from Radiopaedia cases.

Captures both:
1. Gallery images (_big_gallery) — annotated teaching images
2. CT viewer slices — individual frames for MP4 conversion

Separates them into gallery/ and ct_slices/ subdirectories.
"""

import asyncio
import os
import re
from pathlib import Path
from playwright.async_api import async_playwright

IMAGES_DIR = Path(__file__).parent / "images"
GALLERY_DIR = IMAGES_DIR / "gallery"
CT_DIR = IMAGES_DIR / "ct_slices"
IMAGES_DIR.mkdir(exist_ok=True)
GALLERY_DIR.mkdir(exist_ok=True)
CT_DIR.mkdir(exist_ok=True)

# Gallery image cases (annotated stills for slides)
GALLERY_CASES = [
    ("03_herniation",
     "https://radiopaedia.org/cases/subdural-hematoma-with-midline-shift-2?lang=gb",
     "CT brain with midline shift and uncal herniation"),
    ("04_tension_ptx",
     "https://radiopaedia.org/cases/tension-pneumothorax-annotated-signs",
     "CXR tension pneumothorax with annotations"),
    ("05_hemothorax",
     "https://radiopaedia.org/cases/haemothorax-2",
     "CXR hemothorax - traumatic"),
    ("06_widened_mediastinum",
     "https://radiopaedia.org/cases/traumatic-aortic-injury-chest-x-ray",
     "CXR widened mediastinum - aortic injury"),
    ("07_fast_morrisons",
     "https://radiopaedia.org/cases/haemoperitoneum?lang=us",
     "FAST ultrasound - free fluid Morison's pouch"),
    ("08_fast_tamponade",
     "https://radiopaedia.org/cases/pericardial-effusion-with-tamponade-2",
     "FAST subxiphoid - pericardial effusion"),
    ("09_pelvic_fracture",
     "https://radiopaedia.org/cases/open-book-pelvic-injury-2?lang=us",
     "AP pelvis XR - open book fracture"),
]

# CT slice cases (for MP4 scroll-through conversion)
CT_CASES = [
    ("ct_herniation",
     "https://radiopaedia.org/cases/subdural-hematoma-with-midline-shift-2?lang=gb",
     "CT brain herniation - full scroll"),
    ("ct_hemothorax",
     "https://radiopaedia.org/cases/haemothorax-2",
     "CT chest hemothorax - full scroll"),
]


async def download_gallery_images(page, prefix, url, description):
    """Capture _big_gallery annotated images from a case."""
    print(f"\n  GALLERY: {prefix} — {description}")

    captured = []

    async def on_response(response):
        u = response.url
        if "prod-images-static" in u and "_big_gallery" in u:
            ct = response.headers.get("content-type", "")
            if "image" in ct:
                try:
                    body = await response.body()
                    captured.append({"url": u, "size": len(body), "body": body})
                    print(f"      Gallery: {len(body)/1024:.1f} KB")
                except Exception:
                    pass

    page.on("response", on_response)
    try:
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(3000)

        # Click through gallery thumbnails to trigger all gallery image loads
        thumbs = await page.query_selector_all(
            ".case-study-image, .gallery-item, .study-image img, "
            ".image-wrapper img, [data-study-image], .case-section img"
        )
        print(f"      Found {len(thumbs)} clickable elements")

        for i, t in enumerate(thumbs[:8]):
            try:
                await t.click()
                await page.wait_for_timeout(1500)
            except Exception:
                pass

        # Scroll page to trigger lazy loads
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(2000)

    finally:
        page.remove_listener("response", on_response)

    if captured:
        # Save all unique gallery images
        seen_sizes = set()
        saved = 0
        for i, img in enumerate(sorted(captured, key=lambda x: -x["size"])):
            # Skip duplicates (same size = likely same image)
            if img["size"] in seen_sizes:
                continue
            seen_sizes.add(img["size"])

            suffix = "" if i == 0 else f"_view{i+1}"
            outpath = GALLERY_DIR / f"{prefix}{suffix}.jpeg"
            outpath.write_bytes(img["body"])
            saved += 1
            print(f"      Saved: {outpath.name} ({img['size']/1024:.1f} KB)")

        print(f"      Total: {saved} unique gallery images")
    else:
        print(f"      WARNING: No gallery images captured")


async def download_ct_slices(page, prefix, url, description):
    """Capture ALL image slices from the CT viewer for MP4 conversion."""
    print(f"\n  CT SLICES: {prefix} — {description}")

    slice_dir = CT_DIR / prefix
    slice_dir.mkdir(exist_ok=True)

    captured = []
    slice_count = 0

    async def on_response(response):
        nonlocal slice_count
        u = response.url
        # CT slices come from prod-images-static but are NOT _big_gallery
        # They're individual JPEG frames loaded by the Cornerstone viewer
        if "prod-images-static" in u and "_big_gallery" not in u:
            ct = response.headers.get("content-type", "")
            if "image" in ct:
                try:
                    body = await response.body()
                    if len(body) > 5000:  # Skip tiny thumbnails
                        slice_count += 1
                        outpath = slice_dir / f"slice_{slice_count:04d}.jpeg"
                        outpath.write_bytes(body)
                        if slice_count % 20 == 0:
                            print(f"      Slice {slice_count}: {len(body)/1024:.1f} KB")
                except Exception:
                    pass

    page.on("response", on_response)
    try:
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(3000)

        # Click on the first study to open the viewer
        study = await page.query_selector(
            ".case-study-image, .study-image img, .image-wrapper img"
        )
        if study:
            await study.click()
            await page.wait_for_timeout(2000)

        # Scroll through the CT viewer to load all slices
        # The viewer loads slices on scroll/mouse wheel
        viewer = await page.query_selector("canvas, .viewer-container, .study-container")
        if viewer:
            box = await viewer.bounding_box()
            if box:
                cx = box["x"] + box["width"] / 2
                cy = box["y"] + box["height"] / 2

                # Scroll through ~200 slices
                print(f"      Scrolling through CT slices...")
                for i in range(250):
                    await page.mouse.wheel(0, 3)  # Small scroll increments
                    if i % 50 == 0:
                        await page.wait_for_timeout(500)
                    else:
                        await page.wait_for_timeout(100)

        # Wait for remaining loads
        await page.wait_for_timeout(3000)

    finally:
        page.remove_listener("response", on_response)

    print(f"      Total CT slices captured: {slice_count}")
    return slice_count


async def main():
    async with async_playwright() as p:
        user_data_dir = os.path.expanduser("~/.playwright-radiopaedia")

        browser = await p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=2,
        )

        page = browser.pages[0] if browser.pages else await browser.new_page()

        # Login check
        await page.goto("https://radiopaedia.org", wait_until="networkidle", timeout=15000)
        await page.wait_for_timeout(2000)
        html = await page.content()
        if "EVAN DECAN" not in html.upper() and "sign out" not in html.lower():
            print("\nPlease log in to Radiopaedia in the browser window.")
            print("Press Enter when done...")
            input()
        else:
            print("Logged in to Radiopaedia\n")

        # Phase 1: Download all gallery (annotated) images
        print("=" * 60)
        print("PHASE 1: GALLERY IMAGES (annotated stills for slides)")
        print("=" * 60)

        for prefix, url, desc in GALLERY_CASES:
            existing = list(GALLERY_DIR.glob(f"{prefix}*"))
            if existing:
                print(f"\n  Skipping {prefix} ({len(existing)} files exist)")
                continue
            try:
                await download_gallery_images(page, prefix, url, desc)
            except Exception as e:
                print(f"  ERROR: {e}")

        # Phase 2: Download CT slices for scroll-through
        print("\n" + "=" * 60)
        print("PHASE 2: CT SLICES (for MP4 scroll-through)")
        print("=" * 60)

        for prefix, url, desc in CT_CASES:
            slice_dir = CT_DIR / prefix
            existing = list(slice_dir.glob("slice_*"))
            if len(existing) > 10:
                print(f"\n  Skipping {prefix} ({len(existing)} slices exist)")
                continue
            try:
                count = await download_ct_slices(page, prefix, url, desc)
            except Exception as e:
                print(f"  ERROR: {e}")

        # Summary
        print("\n" + "=" * 60)
        print("RESULTS")
        print("=" * 60)

        print("\nGallery images:")
        for f in sorted(GALLERY_DIR.glob("*.jpeg")):
            print(f"  {f.name:45s} {f.stat().st_size/1024:8.1f} KB")

        print("\nCT slice sequences:")
        for d in sorted(CT_DIR.iterdir()):
            if d.is_dir():
                slices = list(d.glob("slice_*"))
                total_mb = sum(s.stat().st_size for s in slices) / 1024 / 1024
                print(f"  {d.name:45s} {len(slices):4d} slices ({total_mb:.1f} MB)")

        print("\nStatic images (already downloaded):")
        for f in sorted(IMAGES_DIR.glob("*")):
            if f.is_file() and f.suffix in ('.jpeg', '.jpg', '.svg'):
                print(f"  {f.name:45s} {f.stat().st_size/1024:8.1f} KB")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
