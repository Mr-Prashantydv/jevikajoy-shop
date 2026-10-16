"""Run in browser-use, scoped to the existing catalog tab; submit one batch at a time."""

import json
import time
from pathlib import Path

root = Path("D:/projects/JEVIKAJOY.SHOP")
export = root / "docs/migration/export-1uz1hi-01-20261004"
catalog = "44F30B427995F1F97C9CF432BFD31A7E"
media = json.loads((export / "media-manifest.json").read_text(encoding="utf-8"))
collector = (root / "docs/migration/collect_file_urls.py").read_text(encoding="utf-8")
sid = cdp("Target.attachToTarget", targetId=catalog, flatten=True)["sessionId"]
progress_path = export / "upload-progress.json"
next_index = json.loads(progress_path.read_text(encoding="utf-8"))["submitted"]
started = time.monotonic()
last_report = None
awaiting_since = None
last_refresh = None
read_failures = 0
while time.monotonic() - started < 3600:
    try:
        location = js("location.origin + location.pathname", target_id=catalog)
        body = js("document.body.innerText", target_id=catalog)
        read_failures = 0
    except RuntimeError:
        read_failures += 1
        if read_failures >= 5:
            raise
        print("Read timeout; retrying observation only, never the upload", flush=True)
        time.sleep(5)
        continue
    if location != "https://admin.shopify.com/store/1uz1hi-01/content/files":
        raise RuntimeError("Catalog tab changed; stop rather than upload to the wrong screen")
    if "Uploading" in body:
        status = body[body.rfind("Uploading"):]
        if status != last_report:
            print(status[:500], flush=True)
            last_report = status
        time.sleep(5)
        continue
    exec(collector, {"js": lambda expression: js(expression, target_id=catalog),
                     "print": lambda *args, **kwargs: None})
    urls = json.loads((export / "uploaded-image-urls.json").read_text(encoding="utf-8"))
    required = {Path(m["path"]).name for m in media[:next_index]}
    missing = required - set(urls)
    if missing:
        # The upload banner disappears before Shopify refreshes its Files table.
        # Wait for observed rows, rather than duplicate files or count submission as success.
        awaiting_since = awaiting_since or time.monotonic()
        if time.monotonic() - awaiting_since > 600:
            raise RuntimeError(f"Previous batch has missing files: {sorted(missing)}")
        # Files can finish uploading while the list keeps its cached rows. A page
        # refresh after the upload banner clears reads the existing server state;
        # it must never resubmit that batch.
        if time.monotonic() - (last_refresh or awaiting_since) > 30:
            cdp("Page.reload", session_id=sid, ignoreCache=False)
            last_refresh = time.monotonic()
            print("Refreshing completed Files list; no upload retried", flush=True)
        if last_report != "Waiting for Files table refresh":
            print("Waiting for Files table refresh", flush=True)
            last_report = "Waiting for Files table refresh"
        time.sleep(5)
        continue
    awaiting_since = None
    last_refresh = None
    print(f"Confirmed {len(urls)}/80 photo URLs", flush=True)
    (export / "upload-progress.json").write_text(json.dumps({
        "confirmed": len(urls), "submitted": next_index, "complete": next_index == len(media)
    }, indent=2), encoding="utf-8")
    if next_index == len(media):
        break
    batch = media[next_index:next_index + 4]
    doc = cdp("DOM.getDocument", session_id=sid)["root"]["nodeId"]
    file_input = cdp("DOM.querySelector", session_id=sid, nodeId=doc,
                     selector="input[type=file]")["nodeId"]
    if not file_input:
        raise RuntimeError("Content Files upload input is absent")
    cdp("DOM.setFileInputFiles", session_id=sid, nodeId=file_input,
        files=[str(root / m["path"]) for m in batch])
    next_index += len(batch)
    (export / "upload-progress.json").write_text(json.dumps({
        "confirmed": len(urls), "submitted": next_index, "complete": False
    }, indent=2), encoding="utf-8")
    print(f"Submitted through photo {next_index}/80", flush=True)
    time.sleep(5)
else:
    raise RuntimeError("Upload wait limit reached; inspect progress before retrying")
