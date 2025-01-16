# TODOs

## Why is this page published on this site?

Because this site is mostly about a collection of personal thoughts and ideas, including TODO items for itself. I don't typically maintain this site very often, but when I do I sometimes knock off items from this list.

## Will I ever knock off all of the items from this list?

Probably not.

## Does it make much difference to me, and should it matter to you, whether or not I decide to complete all of these items?

No. The features of this site are not my highest priority in life.

## The TODOs

- [] Fix issue where language code highlighting isn't colorizing (also, code blocks have way too much padding).
- [] Don't use drop-caps on leading paragraphs with custom styling (such as all italic, etc.)
- [] Fix formatting of https://blog.zenosmosis.com/z_Miscellaneous/Pyrhon%20via%20WASM.html#python-via-wasm so that it matches VSCode's preview
- [] Use dashes instead of "%20" for spaces in links (also use lower-case)
- [] [is it always an issue?] Don't auto-change URL hash on initial landing (issue caused by "deep linking" to URL hash but navigating to that hashed URL doesn't automatically scroll the page)
- [] Finish implementing multi-column layout, with the ability to toggle it on/off (can more than 2 columns be achieved?)
- [] Don't auto-split into two-column format if content is really short (and allow this to be configurable with a variable)
- [] 404 page JS auto-redirect (even better if it could somehow "smartly" determine which page to navigate to)
- [] Fix issue where subdirectories without direct files, but contain their own child directories do not appear in TOC
- [] Auto-replace relative links with %ROOT% prefix.
- [X] Implement custom sort ordering for files/directories (priority listing, per file; OR use a separate file to specify absolute list positioning?)
- [X] Add breadcrumb navigation links above main content
- [] Deep linking w/ aliases. The idea is to use an alias as metadata, and other articles can reference that same link alias where it is interpolated back to the actual link when building. If two or more pages share the same alias, an intermediary index page could be used to link them [harder] or, the build process could just throw an error [easier].
- [] Metadata for sharing w/ social media; SEO
- [] [maybe] [Related article: "Using Git for File Metadata"...sorry no link] Integrate per-file changelog generation into the build process, to track changes made to each content file more effectively. This could involve scripting around Git CLI commands to extract change history for individual files. (Example: `git log --pretty=format:"%h - %an, %ar : %s" -- <file_path>` for a basic changelog or `git log -p -- <file_path>` to include diffs).

    This could also be useful for tracking article creation and update dates across multiple systems, as well as in sitemap generation ("lastmod").

- [] Add simple Docker example that spits out a static website from a directory of Markdown files
- [] Auto-generated metadata keywords and content summarization for "SEO" (or just for kicks and giggles)
- [] [maybe] Add Docker example which auto-pushes to GitHub pages when directory content is updated (be careful with this)
- [] [isn't this working?] If no document title in Markdown, use the filename as the title
- [] Embed LaTeX as images instead of scripts? (is it possible as SVG and still respect font color?)
- [] Maintain aside scroll position when clicking on links, with the exception the active link is out of the viewport, then scroll to it by default (this should make the site feel more like a SPA)
- [] Replace bleach (https://github.com/mozilla/bleach/issues/698) Google and Slack linking issues in "Engineering Blogs" (appears to be an issue w/ bleach.linkify: https://bleach.readthedocs.io/en/latest/linkify.html; added debug.bleach-linkify.py script to debug)
- [] [maybe] Add "Edit on GitHub" link
- [] Add button to make full-screen
- [X] Ability to make an article not be included in TOC; i.e. for 404 pages (indexable: no/0/false; etc.)
- [X] Make it easy to add images (this would involve moving template.html and most existing static content into a template directory and enabling static, user-created content to be also included from the md-content directory w/ checks to ensure there are no overlaps)
- [X] Fix issue where long links can cause horizontal overflow on mobile
- [X] Need persistent "home" link
- [] History tracking would be nice (but wouldn't sync w/o having some sort of backend, which is not a goal I have in mind; could a QR code suffice, somehow??)
- [] Create a mindmap? (https://github.com/markmap/markmap)
- [X] Fix "Chapter 7" mobile horizontal overflow issue (see "personal reading list")
- [] Add sub-headings into table of contents (TOC) (navigation similar to: https://finalfusion.github.io/)
- [X] Fix TOC issue on mobile where it cannot be scrolled vertically
- [] Parse & include site name in title / header
- [] [partially-implemented] Sanitize strings / prevent XSS
- [X] Default "index.md" to top of navigation, per directory
- [X] <- -> article navigation
- [X] Fix invalid UL tag nesting
- [] W3C validation: https://validator.w3.org/nu/?doc=https%3A%2F%2Fzenosmosis.com%2F (see "void" elements: https://html.spec.whatwg.org/multipage/syntax.html#void-elements)
- [] Includes via env variables (i.e. for tracking, etc.)
- [] The ability to hotlink to a particular paragraph would be nice
- [X] Use font "very similar" to that used in Google Play Books
- [] Fix issue where "?" in MD names causes broken links
- [X] Add links to headings
- [X] Highlight active link
- [] Add [more] unit tests
- [PROBABLY-WON'T-DO] [] Live content update as Markdown content is changed
- [] Adding semantic search would be nice: 

    Related Hacker News discussion: https://news.ycombinator.com/item?id=38845061
    
    Key takeaways:
      - https://github.com/tantaraio/voy
      - https://dawchihliou.github.io/articles/share-rust-types-with-typescript-for-webassembly-in-30-seconds
      

- [X] Sitemap generation
- [] [maybe?] Auto-generated page which shows all external links (including link[s] to the page[s] the link was mentioned in)
- [] RSS generation
- [] Include download links to original Markdown files? (if so, slightly modified to include main document title, hierarchy, or link)
- [X] Add word count and estimated reading time to metadata
- [X] Show word count after compilation step
- [] Link graph similar to Obsidian
- [] Include configurable option to open external links as a new tab or not
- [] Tiny icon on aside to indicate if it can be scrolled (if overflown)
- [] optional titles in <- -> article navigation
- [] Implement PWA support (read offline); use discretion here; it might not be a great idea
- [] [maybe?] Add pydantic for string replacements?
- [] Use blockquote format for all "Think and Grow Rich" quotes
