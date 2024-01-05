# TODO

- [X] Implement custom sort ordering for files/directories (priority listing, per file; OR use a separate file to specify absolute list positioning?)
- [X] Add breadcrumb navigation links above main content
- [] Maintain aside scroll position when clicking on links, with the exception the active link is out of the viewport, then scroll to it by default (this should make the site feel more like a SPA)
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
- [X] Sanitize strings / prevent XSS
- [X] Default "index.md" to top of navigation, per directory
- [X] <- -> article navigation
- [] Includes via env variables (i.e. for tracking, etc.)
- [] Show word count after compilation step
- [] The ability to hotlink to a particular paragraph would be nice
- [X] Use font "very similar" to that used in Google Play Books
- [] Fix issue where "?" in MD names causes broken links
- [] Add links to headings (including hover links)
- [X] Highlight active link
- [] Add [more] unit tests
- [] Add simple Docker example that spits out a static website from a directory of markdown files
- [PROBABLY-WON'T-DO] [] Live content update as markdown content is changed
- [] Adding semantic search would be nice: 

    Related HN discussion: https://news.ycombinator.com/item?id=38845061
    
    Key takeaways:
      - https://github.com/tantaraio/voy
      - https://dawchihliou.github.io/articles/share-rust-types-with-typescript-for-webassembly-in-30-seconds
      

- [] Sitemap and RSS (this may require using a separate metadata file to keep track of file creations/modifications, unless somehow able to source through git [or just using hardcoded metadata keys -> easy])
- [] Include download links to original Markdown files? (if so, slightly modified to include main document title, hierarchy, or link)
- [] Add word count and estimated reading time to meta data
- [] Metadata for sharing w/ social media; SEO
- [] Include configurable option to open external links as a new tab or not
- [] Tiny icon on aside to indicate if it can be scrolled (if overflown)
- [] optional titles in <- -> article navigation
- [] Implement PWA support (read offline); use discretion here; it might not be a great idea
- [] [maybe?] Add pydantic for string replacements?
