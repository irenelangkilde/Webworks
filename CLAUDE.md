# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a web development portfolio repository containing multiple website projects:

1. **collegeGrads/** - AI-generated college graduate portfolio/resume websites
2. **photography/prana-photoart/** - Photography studio website template
3. **my-awesome-site/** - Jekyll-based blog site

## Architecture

### CollegeGrads Project (Primary Focus)

The collegeGrads directory contains template-based portfolio websites for recent college graduates in various majors (Accounting, Art, Biology, Civil Engineering, etc.).

#### Key Components:

- **Static HTML Files**: Individual major-specific portfolio pages (e.g., `accountingGrad.html`, `psychologyGrad.html`)
- **Python Personalization Script**: `personalizeCollegeGradWebsite.py` - Uses Claude API to generate personalized HTML/CSS based on user inputs (name, major, colors)
- **Netlify Functions**: `.netlify/functions/` contains serverless functions for API integration
  - `payhipProductCodeBlock.js` - Calls Claude API with prompts to generate HTML code

#### Python Personalization Workflow:

The personalization script uses:
- **Pyodide** (in-browser Python runtime) to run Python in the client browser
- **Claude API** (Anthropic) to generate customized portfolio HTML based on major, name, and color scheme
- Template variables in double curly braces: `{{MAJOR}}`, `{{NAME}}`, `{{COLOR1}}`, etc.
- The script includes both UI form inputs and API integration logic

#### Netlify Integration:

- Serverless functions deployed to Netlify for API calls
- Functions require `ANTHROPIC_API_KEY` environment variable
- Current model: `claude-sonnet-4-20250514` (may need updating to current models)

### Photography Project

Located in `photography/prana-photoart/`:
- Complete photography studio website template
- Includes pages: Home, About, Services, Pricing, Portfolio, Reviews, Contact
- Custom CSS with modern design system
- No build process - static HTML/CSS

### Jekyll Site

Located in `my-awesome-site/`:
- Standard Jekyll blog setup using Minima theme
- Configuration: `_config.yml`
- Static site generation via Jekyll

## Development Workflow

### Working with CollegeGrads Templates:

1. **Editing Existing Templates**: Modify HTML files directly in `collegeGrads/`
2. **Testing Personalization**: Run `personalizeCollegeGradWebsite.py` locally (requires Python environment with Pyodide setup)
3. **Deploying Functions**: Netlify functions auto-deploy from `.netlify/functions/`

### Working with Jekyll Site:

```bash
cd my-awesome-site
bundle install          # Install dependencies
bundle exec jekyll serve # Run local development server
bundle exec jekyll build # Build static site to _site/
```

### CloudCannon CMS:

The repository is configured for CloudCannon CMS editing:
- Configuration: `cloudcannon.config.yml`
- Collections defined for `collegeGrads` and `photography` directories
- Visual editor enabled for HTML content

### Pinegrow:

CollegeGrads templates can be edited with Pinegrow Web Editor:
- Project file: `collegeGrads/projectdb.pgml`
- Configuration: `collegeGrads/pinegrow.json`
- Design panel generates CSS to `css/theme.css`

## API Integration

### Claude API Usage:

The Python personalization script calls the Claude API to generate portfolio HTML:
- API Key: Set via `ANTHROPIC_API_KEY` environment variable
- Model: `claude-sonnet-4-5-20250929` (in Python script)
- Model: `claude-sonnet-4-20250514` (in Netlify function - may be outdated)
- Max tokens: 4000-20000 depending on script
- Temperature: 1

**Important**: Never commit API keys to the repository. Always use environment variables.

## File Organization

```
collegeGrads/
├── *.html              # Major-specific portfolio templates
├── assets/images/      # Stock photos for templates
├── css/                # Stylesheets (some auto-generated)
├── personalizeCollegeGradWebsite.py  # Main personalization script
└── payhipProductCodeBlock.js         # Payhip integration code

photography/prana-photoart/
├── *.html              # Website pages
├── assets/css/         # Stylesheets
└── _layouts/           # Layout templates

my-awesome-site/
├── _config.yml         # Jekyll configuration
├── _site/              # Generated static files (git-ignored)
└── *.markdown          # Content pages

.netlify/functions/     # Serverless function handlers
```

## Key Technologies

- **Frontend**: Static HTML/CSS with embedded styles
- **Backend**: Netlify serverless functions (Node.js)
- **Python**: Pyodide (browser-based Python), Claude API SDK
- **CMS**: CloudCannon, Pinegrow
- **Static Site Generator**: Jekyll (for blog site only)
- **AI**: Claude API for generating personalized portfolio content

## Important Notes

- The personalizeCollegeGradWebsite.py script contains both UI code (HTML in docstring) and Python logic
- Template variables use `{{VARIABLE}}` syntax for Claude API prompt substitution
- The `.netlify/` directory contains deployment-specific files
- Git status shows modified `personalizeCollegeGradWebsite.py` and untracked Netlify/Payhip files
