"""Run inside browser-use; native collection UI only, no Admin API replay."""
import time

def ax_find(role, name, timeout=8):
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        nodes = cdp('Accessibility.getFullAXTree')['nodes']
        found = [n for n in nodes if n.get('role', {}).get('value') == role
                 and n.get('name', {}).get('value') == name]
        if found:
            return found[0]
        time.sleep(.4)
    raise RuntimeError(f'UI element not found: {role} {name}')

def ui_click(node, native=False):
    if native:
        obj = cdp('DOM.resolveNode', backendNodeId=node['backendDOMNodeId'])['object']['objectId']
        cdp('Runtime.callFunctionOn', objectId=obj,
            functionDeclaration='function(){this.click()}', returnByValue=True)
    else:
        q = cdp('DOM.getBoxModel', backendNodeId=node['backendDOMNodeId'])['model']['content']
        x, y = sum(q[0::2])/4, sum(q[1::2])/4
        assert 0 <= x < page_info()['w'] and 0 <= y < page_info()['h'], 'Scroll before click'
        cdp('Input.dispatchMouseEvent', type='mouseMoved', x=x, y=y)
        click_at_xy(x, y)

def enter():
    for phase in ('keyDown', 'keyUp'):
        cdp('Input.dispatchKeyEvent', type=phase, key='Enter', code='Enter', windowsVirtualKeyCode=13)

def ui_fill(node, text):
    obj = cdp('DOM.resolveNode', backendNodeId=node['backendDOMNodeId'])['object']['objectId']
    cdp('Runtime.callFunctionOn', objectId=obj,
        functionDeclaration='function(){this.focus();this.select()}', returnByValue=True)
    press_key('Backspace')
    for char in text:
        press_key(char)
    value = cdp('Runtime.callFunctionOn', objectId=obj,
                functionDeclaration='function(){return this.value}', returnByValue=True)['result']['value']
    if value != text:
        # When hidden-page keyboard input is ignored, update this exact native
        # form control and fire ordinary composed input/change UI events.
        value = cdp('Runtime.callFunctionOn', objectId=obj,
            functionDeclaration='function(value){Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,"value").set.call(this,value);this.dispatchEvent(new Event("input",{bubbles:true,composed:true}));this.dispatchEvent(new Event("change",{bubbles:true,composed:true}));return this.value}',
            arguments=[{'value': text}], returnByValue=True)['result']['value']
    assert value == text, f'Input value did not match: {value}'

def create_current_collection(title, tag, expected_count):
    assert page_info()['url'].endswith('/collections/new'), 'Not a fresh collection form'
    try:
        title_field = ax_find('textbox', 'Collection title', timeout=1)
    except RuntimeError:
        button = ax_find('button', 'Add title')
        ui_click(button)
        try:
            title_field = ax_find('textbox', 'Collection title', timeout=2)
        except RuntimeError:
            ui_click(button, native=True)
            title_field = ax_find('textbox', 'Collection title')
    ui_fill(title_field, title)
    button = ax_find('button', 'Add condition')
    ui_click(button)
    try:
        tag_row = ax_find('row', 'Tag', timeout=2)
    except RuntimeError:
        ui_click(button, native=True)
        tag_row = ax_find('row', 'Tag')
    # The shadow-widget row previously ignored compositor clicks while hidden.
    ui_click(tag_row, native=True)
    field = ax_find('combobox', 'Tag values')
    time.sleep(.5)  # Native editor hydrates its condition field asynchronously.
    ui_fill(field, tag)
    ui_click(ax_find('option', tag), native=True)
    ax_find('button', 'Remove ' + tag)
    return save_current_collection(title, tag, expected_count)

def save_current_collection(title, tag, expected_count):
    for phase in ('keyDown', 'keyUp'):
        cdp('Input.dispatchKeyEvent', type=phase, key='Escape', code='Escape', windowsVirtualKeyCode=27)
    time.sleep(.3)
    end = time.monotonic() + 10
    while time.monotonic() < end:
        body = js('document.body.innerText')
        if f'Collection items{expected_count}' in body:
            break
        time.sleep(.4)
    else:
        raise RuntimeError('Collection membership count not confirmed; not saved')
    channel_button = ax_find('button', 'Manage sales channels: published to 2 channels')
    ui_click(channel_button)
    try:
        pos = ax_find('checkbox', 'Point of Sale', timeout=2)
    except RuntimeError:
        ui_click(channel_button, native=True)
        pos = ax_find('checkbox', 'Point of Sale')
    checked = next(p['value']['value'] for p in pos['properties'] if p['name'] == 'checked')
    if checked == 'true':
        ui_click(pos)
    ax_find('button', 'Manage sales channels: published to 1 channel')
    # Clicking outside the native channel popover closes it before saving.
    ui_click(ax_find('button', 'Add description'))
    ui_click(ax_find('button', 'Save'))
    end = time.monotonic() + 12
    while time.monotonic() < end:
        url = page_info()['url']
        if not url.endswith('/new') and '/collections/' in url:
            print({'title': title, 'tag': tag, 'count': expected_count, 'saved_url': url})
            return url
        time.sleep(.4)
    raise RuntimeError('Save outcome unknown; inspect before retry')
