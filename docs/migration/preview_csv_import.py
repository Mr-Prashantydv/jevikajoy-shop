"""Run inside browser-use; prepare the import preview, never confirm the import."""

import time
from pathlib import Path


def migration_nodes():
    return cdp("Accessibility.getFullAXTree")["nodes"]


def migration_click(name, role="button"):
    matches = [n for n in migration_nodes()
               if n.get("role", {}).get("value") == role
               and n.get("name", {}).get("value") == name]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one {role} named {name!r}, got {len(matches)}")
    q = cdp("DOM.getBoxModel", backendNodeId=matches[0]["backendDOMNodeId"])["model"]["content"]
    click_at_xy(sum(q[0::2]) / 4, sum(q[1::2]) / 4)


def migration_wait(predicate, label, timeout=20):
    started = time.monotonic()
    while time.monotonic() - started < timeout:
        if predicate():
            return
        time.sleep(0.5)
    raise RuntimeError(f"Timed out waiting for {label}; no import was confirmed")


assert js("location.origin + location.pathname") == "https://admin.shopify.com/store/1uz1hi-01/products"
assert not any(n.get("role", {}).get("value") == "dialog" for n in migration_nodes())
migration_click("Import")
migration_wait(lambda: js("!!document.querySelector('input[type=file]')"), "CSV file input")
root = cdp("DOM.getDocument")["root"]["nodeId"]
file_input = cdp("DOM.querySelector", nodeId=root, selector="input[type=file]")["nodeId"]
cdp("DOM.setFileInputFiles", nodeId=file_input, files=[str(Path(migration_csv_path).resolve())])
migration_wait(lambda: Path(migration_csv_path).name in js("document.body.innerText"), "selected CSV")
check = next(n for n in migration_nodes() if n.get("role", {}).get("value") == "checkbox"
             and "Publish new products" in n.get("name", {}).get("value", ""))
if any(p.get("name") == "checked" and p.get("value", {}).get("value") == "true"
       for p in check.get("properties", [])):
    migration_click(check["name"]["value"], "checkbox")
migration_click("Upload file")
migration_wait(lambda: "Preview your first product" in js("document.body.innerText"), "product preview", 30)
print(js("document.body.innerText").split("Preview your first product", 1)[1][:7000])
