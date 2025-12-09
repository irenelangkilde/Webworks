"""<!-- UI: put this in a Text block -->
<div id="app">
  <h2>Personalize your template</h2>

  <label>
    Your Name
    <input id="userName" type="text" placeholder="e.g. Jane Doe" />
  </label>

  <label>
    Your Major
    <input id="major" type="text" placeholder="Psychology" />
  </label>

  <label>
    Your Email
    <input id="email" type="text" placeholder="e.g. janedoe@gmail.com" />
  </label>

  <label>
    Your Phone
    <input id="userName" type="text" placeholder="e.g. 123-456-7890" />
  </label>

  <label style="display:block;margin-top:8px;">
    Background Color 1 (hex)
    <input id="backgroundColor1" type="text" placeholder="#000000" />
  </label>
<label style="display:block;margin-top:8px;">
    Background Color 2 (hex)
    <input id="backgroundColor2" type="text" placeholder="#ffffff" />
  </label>
<label style="display:block;margin-top:8px;">
    Accent Color 1(hex)
    <input id="accentColor1" type="text" placeholder="#1e90ff" />
  </label>
<label style="display:block;margin-top:8px;">
    Accent Color 2(hex)
    <input id="accentColor2" type="text" placeholder="#aaaaaa" />
  </label>

  <button id="runBtn" style="margin-top:12px;">Generate</button>

  <pre id="output" style="background:#f6f8fa;padding:12px;white-space:pre-wrap;margin-top:12px;"></pre>
</div>
"""
# filename: personalize_combined.py
# Single-file approach: loads Pyodide runtime and runs your personalization logic.
# No external SCRIPT_URL needed. Keep secrets out of this code—runs in the buyer’s browser.

import js

PYODIDE_URL = "https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"

# --- Your personalization logic (merged from personalizeTemplate.py) ---
def main(name, major, email, phone, bg1, bg2, accent1, accent2):
    # Example output. Replace with your real logic:
    print("✅ Personalization summary\n")
    print(f"Name: {name}")
    print(f"Major: {major}")
    print(f"Email: {email}")
    print(f"Phone: {phone}")
    print(f"Background Colors: {bg1}, {bg2}")
    print(f"Accent Colors: {accent1}, {accent2}")

    # You can generate text/JSON here and let JS offer a download if needed.
    # For example:
    config = {
        "name": name,
        "major": major,
        "email": email,
        "phone": phone,
        "backgroundColor1": bg1,
        "backgroundColor2": bg2,
        "accentColor1": accent1,
        "accentColor2": accent2,
    }
    print("\nGenerated config JSON:")
    import json
    print(json.dumps(config, indent=2))


# --- Runtime + DOM glue ---
async def load_pyodide_runtime():
    # Insert Pyodide script tag
    script = js.document.createElement("script")
    script.src = PYODIDE_URL
    js.document.head.appendChild(script)

    # Wait until loaded
    fut = js.Promise.new(lambda resolve, reject: setattr(script, "onload", resolve))
    await fut

    return await js.loadPyodide()

def _read_value(id_, fallback=""):
    el = js.document.getElementById(id_)
    if not el:
        return fallback
    v = el.value
    return v if v else fallback

async def run():
    # Load Pyodide once; subsequent clicks reuse it
    if not getattr(js.window, "_pyodide_instance", None):
        js.window._pyodide_instance = await load_pyodide_runtime()
    pyodide = js.window._pyodide_instance

    # Redirect print() to the page
    import sys
    class PageWriter:
        def write(self, s):
            out = js.document.getElementById("output")
            out.textContent = (out.textContent or "") + str(s)
        def flush(self): pass
    sys.stdout = PageWriter()
    sys.stderr = PageWriter()

    # Read inputs from the Text block
    name     = _read_value("name", "Jane Doe")
    major    = _read_value("major", "Psychology")
    email    = _read_value("email", "janedoe@gmail.com")
    phone    = _read_value("phone", "123-456-7890")
    bg1      = _read_value("backgroundColor1", "#000000")
    bg2      = _read_value("backgroundColor2", "#ffffff")
    accent1  = _read_value("accentColor1", "#1e90ff")
    accent2  = _read_value("accentColor2", "#aaaaaa")

    # Clear previous output before printing new results
    js.document.getElementById("output").textContent = ""

    # Call your merged main() directly
    try:
        main(name, major, email, phone, bg1, bg2, accent1, accent2)
    except Exception as e:
        js.document.getElementById("output").textContent = f"Error: {e}"

# Wire the button click
btn = js.document.getElementById("runBtn")
btn.addEventListener("Click to personalize", js.eval("(e) => window._runPersonalize()"))
js.window._runPersonalize = js.python_async(run)

#############################################
import anthropic
import re

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    #api_key="my_api_key",
    api_key="ANTHROPIC_API_KEY"
)

def extract_variables(text):
    """Return sorted unique placeholders enclosed in double curly braces."""
    matches = re.findall(r"\{\{\s*([^{}]+?)\s*\}\}", text)
    return sorted(set(matches))


prompt_message = (
                    "You will be generating HTML and CSS code for a professional-looking "
                    "resume/portfolio website of a recent college graduate who majored in "
                    "{{MAJOR}}.\n\nThe graduate's name is:\n<name>\n{{NAME}}\n</name>\n\nThe "
                    "website background color scheme will alternate each section between "
                    "{{COLOR1}} and {{COLOR2}}. The accents are {{COLOR3}} and "
                    "{{COLOR2}} background.  It should include the following "
                    "sections:\n\n1. **Header/Hero Section**: Include the person's name "
                    "prominently next to or below a stock headshot photo, along with a brief "
                    'tagline like "{{MAJOR}} Graduate" or "Recent {{MAJOR}} Major"\n\n2. '
                    "**About Section**: Write a brief professional summary (2-3 sentences) "
                    "about a {{MAJOR}} graduate's interests and career goals. Keep it general "
                    "but professional.\n\n3. **Education Section**: Include a bachelor's "
                    'degree in {{MAJOR}} from a university (you can use a placeholder like '
                    '"University Name" and "Graduation Year: {{YEAR}}" or similar recent '
                    "year). Mention relevant coursework or academic achievements typical for "
                    "{{MAJOR}} majors.\n\n4. **Skills Section**: List skills relevant to a "
                    "{{MAJOR}} major, such as:\n   - Research and analysis\n   - Writing and "
                    "communication\n   - Critical thinking\n   - Archival research\n   - "
                    "Historical analysis\n   - Any relevant technical skills (databases, "
                    "digital humanities tools, etc.)\n\n5. **Experience Section**: Create 1-2 "
                    "placeholder work/internship experiences relevant to {{MAJOR}} majors "
                    "(such as museum internships, research assistant positions, teaching "
                    "assistant roles, or archival work). Include placeholder organization "
                    "names, dates, and 2-3 bullet points describing "
                    "responsibilities.\n\n6. **Projects Section** (optional but recommended): "
                    "Include 1-2 academic projects or research papers typical for {{MAJOR}} "
                    "majors, with brief descriptions.\n\n7. **Contact Section**: Include "
                    "placeholder contact information (email, LinkedIn, etc.)\n\nThe website "
                    "should be:\n- Clean, professional, and modern in design\n- Responsive "
                    "and well-structured\n- Use appropriate fonts for a professional "
                    "portfolio\n- Include both HTML and CSS code\n- Be complete and ready to "
                    "use (all code should be functional)\n\nWrite the complete HTML code with "
                    "embedded CSS (using a <style> tag in the <head> section). Make sure to "
                    "use the provided name throughout the website where "
                    "appropriate.\n\nProvide your complete website code inside "
                    "<website_code> tags."
                )
prompt_variables = extract_variables(prompt_message)
# Replace placeholders like {{MAJOR}} with real values,
# because the SDK does not support variables.
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=20000,
    temperature=1,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt_message
                }
            ]
        }
    ]
)
print(message.content)
#############################################