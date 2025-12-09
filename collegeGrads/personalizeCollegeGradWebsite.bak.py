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
                    "You will be generating HTML and CSS code for a professional "
                    "resume/portfolio website for a recent college graduate who majored in "
                    "{{Major}}.\n\nThe graduate's name is:\n<name>\n{{NAME}}\n</name>\n\nThe "
                    "website color scheme will be {{COLOR1}}, {{COLOR2}}, and {{COLOR3}} on a "
                    "{{LightOrDark}} background.  It should include the following "
                    "sections:\n\n1. **Header/Hero Section**: Include the person's name "
                    "prominently next to or below a stock headshot photo, along with a brief "
                    'tagline like "{{Major}} Graduate" or "Recent {{Major}} Major"\n\n2. '
                    "**About Section**: Write a brief professional summary (2-3 sentences) "
                    "about a {{Major}} graduate's interests and career goals. Keep it general "
                    "but professional.\n\n3. **Education Section**: Include a bachelor's "
                    'degree in {{Major}} from a university (you can use a placeholder like '
                    '"University Name" and "Graduation Year: {{YEAR}}" or similar recent '
                    "year). Mention relevant coursework or academic achievements typical for "
                    "{{Major}} majors.\n\n4. **Skills Section**: List skills relevant to a "
                    "{{Major}} major, such as:\n   - Research and analysis\n   - Writing and "
                    "communication\n   - Critical thinking\n   - Archival research\n   - "
                    "Historical analysis\n   - Any relevant technical skills (databases, "
                    "digital humanities tools, etc.)\n\n5. **Experience Section**: Create 1-2 "
                    "placeholder work/internship experiences relevant to {{Major}} majors "
                    "(such as museum internships, research assistant positions, teaching "
                    "assistant roles, or archival work). Include placeholder organization "
                    "names, dates, and 2-3 bullet points describing "
                    "responsibilities.\n\n6. **Projects Section** (optional but recommended): "
                    "Include 1-2 academic projects or research papers typical for {{Major}} "
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
# Replace placeholders like {{Major}} with real values,
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
                    "text": (
                        "You will be generating HTML and CSS code for a professional "
                        "resume/portfolio website for a recent college graduate who majored in "
                        "{{Major}}.\n\nThe graduate's name is:\n<name>\n{{NAME}}\n</name>\n\nThe "
                        "website color scheme will be {{COLOR1}}, {{COLOR2}}, and {{COLOR3}} on a "
                        "{{LightOrDark}} background.  It should include the following "
                        "sections:\n\n1. **Header/Hero Section**: Include the person's name "
                        "prominently next to or below a stock headshot photo, along with a brief "
                        'tagline like "{{Major}} Graduate" or "Recent {{Major}} Major"\n\n2. '
                        "**About Section**: Write a brief professional summary (2-3 sentences) "
                        "about a {{Major}} graduate's interests and career goals. Keep it general "
                        "but professional.\n\n3. **Education Section**: Include a bachelor's "
                        'degree in {{Major}} from a university (you can use a placeholder like '
                        '"University Name" and "Graduation Year: {{YEAR}}" or similar recent '
                        "year). Mention relevant coursework or academic achievements typical for "
                        "{{Major}} majors.\n\n4. **Skills Section**: List skills relevant to a "
                        "{{Major}} major, such as:\n   - Research and analysis\n   - Writing and "
                        "communication\n   - Critical thinking\n   - Archival research\n   - "
                        "Historical analysis\n   - Any relevant technical skills (databases, "
                        "digital humanities tools, etc.)\n\n5. **Experience Section**: Create 1-2 "
                        "placeholder work/internship experiences relevant to {{Major}} majors "
                        "(such as museum internships, research assistant positions, teaching "
                        "assistant roles, or archival work). Include placeholder organization "
                        "names, dates, and 2-3 bullet points describing "
                        "responsibilities.\n\n6. **Projects Section** (optional but recommended): "
                        "Include 1-2 academic projects or research papers typical for {{Major}} "
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
                }
            ]
        }
    ]
)
print(message.content)
