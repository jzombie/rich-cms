# TODO

- [X] Implement custom sort ordering for files/directories (priority listing, per file; OR use a separate file to specify absolute list positioning?)
- [X] Add breadcrumb navigation links above main content
- [] Deep linking w/ aliases. The idea is to use an alias as metadata, and other articles can reference that same link alias where it is interpolated back to the actual link when building. If two or more pages share the same alias, an intermediary index page could be used to link them [harder] or, the build process could just throw an error [easier].
- [] [maybe] [Related article: "Using Git for File Metadata"...sorry no link] Integrate per-file changelog generation into the build process, to track changes made to each content file more effectively. This could involve scripting around Git CLI commands to extract change history for individual files. (Example: `git log --pretty=format:"%h - %an, %ar : %s" -- <file_path>` for a basic changelog or `git log -p -- <file_path>` to include diffs).

    This could also be useful for tracking article creation and update dates across multiple systems, as well as in sitemap generation ("lastmod").

- [] Add simple Docker example that spits out a static website from a directory of Markdown files
- [] Auto-generated metadata keywords for "SEO" (or just for kicks and giggles)
- [] [maybe] Add Docker example which auto-pushes to GitHub pages when directory content is updated (be careful with this)
- [] If no document title in Markdown, use the filename as the title
- [] Embed LaTeX as images instead of scripts? (is it possible as SVG and still respect font color?)
- [] Fix issue where language code highlighting isn't colorizing
- [] Maintain aside scroll position when clicking on links, with the exception the active link is out of the viewport, then scroll to it by default (this should make the site feel more like a SPA)
- [] Replace bleach (https://github.com/mozilla/bleach/issues/698) Google and Slack linking issues in "Engineering Blogs" (appears to be an issue w/ bleach.linkify: https://bleach.readthedocs.io/en/latest/linkify.html; added debug.bleach-linkify.py script to debug)
- [] Add "Edit on GitHub" link
- [] Add button to make full-screen
- [X] Ability to make an article not be included in TOC; i.e. for 404 pages (indexable: no/0/false; etc.)
- [X] Make it easy to add images (this would involve moving template.html and most existing static content into a template directory and enabling static, user-created content to be also included from the md-content directory w/ checks to ensure there are no overlaps)
- [X] Fix issue where long links can cause horizontal overflow on mobile
- [] Finish implementing multi-column layout, with the ability to toggle it on/off (can more than 2 columns be achieved?)
- [] Need persistent "home" link
- [] History tracking would be nice (but wouldn't sync w/o having some sort of backend, which is not a goal I have in mind; could a QR code suffice, somehow??)
- [X] Fix "Chapter 7" mobile horizontal overflow issue (see "personal reading list")
- [] Add sub-headings into table of contents (TOC) (navigation similar to: https://finalfusion.github.io/)
- [X] Fix TOC issue on mobile where it cannot be scrolled vertically
- [] Parse & include site name in title / header
- [] [partially-implemented] Sanitize strings / prevent XSS
- [X] Default "index.md" to top of navigation, per directory
- [X] <- -> article navigation
- [X] Fix invalid UL tag nesting
- [] W3C validation: https://validator.w3.org/nu/?doc=https%3A%2F%2Frichcms.zenosmosis.com%2F (see "void" elements: https://html.spec.whatwg.org/multipage/syntax.html#void-elements)
- [] Includes via env variables (i.e. for tracking, etc.)
- [] The ability to hotlink to a particular paragraph would be nice
- [X] Use font "very similar" to that used in Google Play Books
- [] Fix issue where "?" in MD names causes broken links
- [X] Add links to headings
- [X] Highlight active link
- [] Add [more] unit tests
- [PROBABLY-WON'T-DO] [] Live content update as Markdown content is changed
- [] Adding semantic search would be nice: 

    Related HN discussion: https://news.ycombinator.com/item?id=38845061
    
    Key takeaways:
      - https://github.com/tantaraio/voy
      - https://dawchihliou.github.io/articles/share-rust-types-with-typescript-for-webassembly-in-30-seconds
      

- [X] Sitemap generation
- [] [maybe?] Auto-generated page which shows all external links (including link[s] to the page[s] the link was mentioned in)
- [] RSS generation
- [] Include download links to original Markdown files? (if so, slightly modified to include main document title, hierarchy, or link)
- [X] Add word count and estimated reading time to meta data
- [X] Show word count after compilation step
- [] Link graph similar to Obsidian
- [] Metadata for sharing w/ social media; SEO
- [] Include configurable option to open external links as a new tab or not
- [] Tiny icon on aside to indicate if it can be scrolled (if overflown)
- [] optional titles in <- -> article navigation
- [] Implement PWA support (read offline); use discretion here; it might not be a great idea
- [] [maybe?] Add pydantic for string replacements?
- [] Use blockquote format for all "Think and Grow Rich" quotes
