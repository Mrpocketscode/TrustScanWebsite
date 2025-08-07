# Copilot Instructions for TrustScanWebsite

## Project Overview
This is a static website project consisting of HTML, CSS, and JavaScript files. The site is designed to present information visually, using a variety of custom images stored in the `assets/` directory. There is no build system, backend, or package management—changes are reflected immediately in the browser.

## Key Files and Structure
- `index.html`: Main entry point. Defines the page structure and references styles/scripts.
- `styles.css`: Contains all custom styles for layout, colors, and responsive design.
- `script.js`: Handles all client-side interactivity. No frameworks are used; vanilla JS only.
- `assets/`: Contains all images and visual assets referenced in the site.
- `CNAME`: Used for custom domain configuration (likely for GitHub Pages).

## Developer Workflow
- **Edit and Refresh**: Make changes directly to HTML, CSS, or JS files. Refresh the browser to see updates.
- **No Build Step**: There is no build, test, or deployment automation. All changes are manual.
- **Custom Domain**: The presence of `CNAME` suggests deployment via GitHub Pages with a custom domain.

## Project-Specific Patterns
- **Image Usage**: Images are referenced directly from the `assets/` folder. Use relative paths (e.g., `assets/filename.png`).
- **Styling**: All styles are centralized in `styles.css`. Follow existing class naming and layout conventions.
- **JavaScript**: All scripts are in `script.js`. Use vanilla JS and avoid introducing frameworks or modules.
- **Accessibility**: Follow semantic HTML practices as seen in `index.html` (e.g., use of headings, alt attributes for images).

## Integration Points
- **No External Dependencies**: The project does not use npm, package managers, or external JS/CSS libraries.
- **Deployment**: For publishing, push changes to the main branch. GitHub Pages will serve the site automatically.

## Example Patterns
- To add a new image: Place it in `assets/`, then reference it in `index.html` or `styles.css` using a relative path.
- To update site content: Edit `index.html` for structure/text, `styles.css` for appearance, and `script.js` for behavior.

## Conventions
- Keep all code in a single file per type (one HTML, one CSS, one JS).
- Use descriptive class and ID names for styling and scripting.
- Do not add build tools, package files, or external dependencies unless explicitly requested.

---
For questions about unclear patterns or missing documentation, ask the user for clarification before making structural changes.
