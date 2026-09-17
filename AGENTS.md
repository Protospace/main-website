# AGENTS.md

## Project overview

This is the static website for Protospace, a non-profit makerspace in Calgary, Alberta. It is served directly as static files; there is no static-site generator, build step, package manager, or templating system.

## Source of truth

- Edit the HTML, CSS, and metadata files directly.
- Do not create or reintroduce a static-site generator.
- Do not add a build script that overwrites manually maintained pages.
- There is intentionally no `build.js` or equivalent generator.
- Preserve manual improvements when making later changes.

## Page structure

- Every page must be an `index.html` inside its own route directory:
  - `/index.html`
  - `/the-space/index.html`
  - `/join-us/index.html`
  - `/contact/index.html`
  - `/wood-shop/index.html`
  - `/metal-shop/index.html`
  - `/laser-cutters/index.html`
  - `/sewing-room/index.html`
  - `/electronics-lab/index.html`
  - `/3d-printers/index.html`
- Use trailing-slash internal links, such as `/contact/` and `/wood-shop/`.
- Keep the shared header, navigation, sidebar, and footer consistent across pages.
- The sidebar should appear on the right on desktop and below the main content on mobile.
- The contact page is allowed to use its full-width layout when appropriate.

## Readable HTML

Keep source code pleasant for humans to read and edit.

- Use tabs for indentation.
- Keep one logical element per line where practical.
- Keep navigation links one per line.
- Keep adjacent image tags one per line when they are readable on one line.
- Keep iframe attributes split over separate lines, with the closing `></iframe>` on its own line:

  ```html
  <iframe
  	class="map"
  	src="https://example.com/embed"
  	title="Map to Protospace"
  ></iframe>
  ```

- Do not split inline links, `<strong>`, `<em>`, or their closing tags awkwardly across lines.
- Do not allow formatters to turn inline markup into structures such as:

  ```html
  <a
  	href="..."
  	>Some link</a
  >
  ```

- Avoid large runs of blank lines. Use a single blank line between meaningful sections; do not add blank lines between list items.
- Make targeted manual edits. Do not run an automated formatter over the whole site without checking every page afterward.
- Preserve whitespace carefully when editing inline text, since whitespace can affect rendered content.

## Shared layout

When adding or editing a page, match the existing structure:

- Header with Protospace logo and links to About, Membership, Wiki, Portal, and Contact
- Main page content with one meaningful `<h1>`
- Sidebar containing the current open-house information, address, parking details, map iframe, and search control where applicable
- Footer containing YouTube, FAQ, and Facebook links

Keep the current open-house information consistent:

- Every Tuesday from 7:00 pm to 9:00 pm
- Including holidays
- Visitors can drop in for a tour
- Address: 1530 27th Avenue NE, Bay 108, Calgary, Alberta, Canada, T2E 7S6

If this information changes, update the sidebar, relevant page copy, JSON-LD, and `llms.txt` together.

## Assets

- Store local images in `/assets/`.
- Use descriptive filenames rather than WordPress upload names such as `photo_6_2023-06-06_16-39-08.jpg`.
- Remove unused downloaded image variants when it is safe to do so.
- Update every reference when renaming or removing an asset.
- Do not link page content to the old WordPress upload paths.
- Give every image a useful `alt` attribute. Use `alt=""` only for genuinely decorative images.
- Keep image dimensions or CSS aspect ratios where possible to reduce layout shift.
- For every JPEG photo used in page content, generate a matching WebP version and serve it with the original JPEG as the fallback in a `<picture>` element:

  ```html
  <picture>
  	<source
  		type="image/webp"
  		srcset="/assets/example.webp 640w"
  		sizes="(max-width: 760px) 100vw, 750px"
  	/>
  	<img
  		width="640"
  		height="480"
  		src="/assets/example.jpg"
  		alt="Descriptive photo description"
  	/>
  </picture>
  ```
- Keep the WebP and fallback `srcset` candidates equivalent, preserve the fallback image's `alt`, dimensions, loading behavior, and decoding attributes, and verify that every referenced variant exists.

## Accessibility

- Use one meaningful `<h1>` per page.
- Keep heading levels logically ordered.
- Do not use empty headings for decorative icons.
- Give iframes descriptive `title` attributes.
- Give search inputs an explicit `type="search"` and accessible label.
- Use descriptive link text instead of vague labels such as “click here” where practical.
- Add `rel="noopener noreferrer"` to external links using `target="_blank"`.
- Prefer semantic HTML over generic classes and WordPress-derived class names.
- Do not add `wp-`, `wordpress`, or plugin-specific classes to new markup.

## SEO and metadata

- Give every page a unique, descriptive `<title>`.
- Add a useful page-specific meta description when adding new pages.
- Keep the canonical URL, sitemap, and structured data consistent with the route.
- Preserve the JSON-LD structured data in every page head. Keep the organization details, address, contact information, social links, and Tuesday open-house information accurate.
- Keep `robots.txt`, `sitemap.xml`, and `llms.txt` synchronized with the page set.

## Adding or removing pages

When creating a page:

1. Create a new route directory.
2. Add the page as `route/index.html`.
3. Add it to the navigation or relevant page links if appropriate.
4. Add its canonical URL to `sitemap.xml`.
5. Add a useful entry to `llms.txt`.
6. Check whether the page should be included in `robots.txt` rules.
7. Keep the page header, sidebar, footer, metadata, and JSON-LD consistent.

When removing or renaming a page:

1. Remove or redirect internal links pointing to it.
2. Remove its URL from `sitemap.xml`.
3. Remove or update its entry in `llms.txt`.
4. Update navigation and related facility links.
5. Check for orphaned assets.

## External links and subdomains

The following subdomains are intentional and should remain external links:

- `http://wiki.protospace.ca`
- `http://my.protospace.ca`

Do not convert those links into local routes. Preserve external links to the Protospace YouTube channel, Facebook page, forum, Google Maps, and other current resources unless the user specifically asks to change them.

## Validation checklist

Before finishing an HTML change:

- Check that all opened elements are closed and nesting is valid.
- Confirm all referenced local assets exist.
- Check internal links and route paths.
- Check image `alt` text and iframe titles.
- Confirm header, sidebar, and footer consistency.
- Confirm mobile behavior remains responsive.
- Run structural validation when available, for example:

  ```bash
  npx html-validate \
  	--rule doctype-style:off \
  	--rule void-style:off \
  	--rule wcag/h37:off \
  	--rule no-implicit-input-type:off \
  	--rule empty-heading:off \
  	--rule no-inline-style:off \
  	'**/*.html'
  ```

- Start a local static server and smoke-test every route:

  ```bash
  python3 -m http.server 8765
  ```

Do not finish with known broken HTML, missing assets, stale sitemap entries, or inconsistent shared navigation.
