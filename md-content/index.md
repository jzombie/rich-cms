# Welcome to zenOSmosis

## What is this website?

<img src="%ROOT%/images/zen-like-water-ripple.jpeg" style="width: 120px; margin-left: 20px; float: right;" title="zen-like water ripple" />

This is a collection of thoughts... (not very organized yet, mind you...)

This site a [static site generator that I hand-rolled](https://github.com/jzombie/rich-cms): A basic Python script that "compiles" a recursive directory structure mostly consisting of markdown files (don't diss the source-code too hard; my Python skills aren't as well-versed as say, my JavaScript skills, but I didn't want to create a Node.js project for this site).

I did not choose to use a conventional static website generator because I just wanted to create one for myself and be in control of what features it consists of and how often they are updated.

The goal here was to just keep things simple... not use a framework of any sort, at least for the "presentation layer" (the generated static HTML files).

Over the years I've become very well acquainted with React, and this is probably the first "vanilla" JavaScript project that I've done since 2018 (yes there is a little bit of JavaScript in here, though this website by no means requires the usage of it to function).

In regards to this static site, I was initially inspired by [Insomnia](https://insomnia.rest/) (because it works off of markdown files as well, and organizes thoughts), but mostly just wanted a blog to publish thoughts and ideas.

## What is zenOSmosis?

Short version: My alias.

Long version: An experimental "company" (or so it was originally conceived to be as one), always experimenting with new ideas, helping me to learn and grow (whatever that means).  At the peak of the experience, I guess I may have fooled a few people into thinking that this was an actual company, but I've since then taken a number of its projects offline, as I was far too attached in them, and the only thing they were gaining were sentimental value.

Enter the world of "jzombie," another alias of mine.  Jzombie helps me to realize to take myself way less seriously, plus, the name is a hell of a lot shorter.

## Who am I?

Just a fellow with some ideas and a mix of ADD and OCD, depending on the day and the task.

I started messing with computers at the ripe age of around 5 or 6, sometime in the early 80's, playing around on a [Tandy TRS-80](https://en.wikipedia.org/wiki/TRS-80), copying [BASIC](https://en.wikipedia.org/wiki/BASIC) programs from a book into my computer, though I had no clue how to read at the time.

I believe that when I started first grade, I told my teacher that my goal was to learn how to read, probably so that I could understand what that book actually said.

Fast forward a few years, towards the end of high-school, I tried to convince myself and any of my friends that computers were not what I was really into, and mostly drove a forklift in a lumberyard.

Most of my early 20's were spent traveling to other states, getting random jobs that mostly did no involve offices whatsoever, and doing a bit of physical work (such as landscaping, transplanting trees, stepping on nails [once, ouch]...)

It wasn't until I turned 25 or 26 (early 2000's) that I started helping my dad run an e-commerce business selling motorcycle accessories online. He initially started off with a handful of products that he was drop-shipping, and I was impressed with whomever had built the site in its latest incarnation at the time (I believe that I developed an early static HTML prototype in a document editor), as this latest incarnation was database driven and a bit more complex than the rudimentary HTML that I knew at the time.

I learned that it was programmed in Perl, and our "webmaster" gave me the "keys" to the source code and I don't think either one of us knew what a staging server was, so I just learned how to hack on it live, in production... and we still stayed in business.

One of the first things that I did was add a "SKU" field to the database, then made a way for customers to track orders (by copying UPS links to another field), then started digging through manuals we had of our suppliers and adding parts directly to the site.

We went from selling less than 100 products to over 10,000 products over the course of a few months, and the business grew quite substantially (for a 2 person team with no prior experience in online sales or web programming). My dad was the one handling customer service, and I was doing my "in production hacking" somehow without crashing the site (those were simple times, indeed).

I was also working at a local RadioShack at the time, though it wasn't your typical RadioShack. We sold bedding and appliances as well.

One of our customers got to talking with me about PHP, and gave me a book on it, and I eventually rewrote that store, from scratch in PHP, but my dad wasn't originally convinced after just seeing "Hello World" in a single line of black text on a white screen, and told me, "this is going to be a very complicated task."

Fast-forward one year, we launched the new site, with over 10,000 products, and I believe that our first customer spent over $1,000 immediately. We got a pretty good bit of traffic, for just two people who ran the store (I think it was something like 1,000 visitors per day, consistently... nothing huge, but it felt like a decent number to me at the time). Our daily averages were about $1,000 in sales, so you could say that we averaged about $1 per visitor, and we had a fairly consistent traffic stream.

I wired the incoming traffic from search engines into Twitter, so that other people could see what others were searching for and what pages they were landing on.  Over a few years, that produced a feed several hundreds of thousands of results long, and actually gained a few followers on that Twitter account that nobody managed personally.  Where it is today?  No clue.  Long gone.

Some things outside of programming that I learned from this were: PCI compliance, merchant accounts, SSL certs, DNS, and Linux.

So, my experience programming websites, up to that point, was the way that I self-taught myself... that was my education; I just learned as I went.

----

Rich CMS is an experimental Markdown-driven content management system, written in Python.

It outputs static HTML files that can be used locally without a web server, served via [GitHub Pages](https://pages.github.com/), etc.

<img src="%ROOT%/images/thinker.png" style="width: 180px" title="This is me thinking" />

https://github.com/jzombie/rich-cms

---

I envision this project to eventually become sort of a "database of personal thoughts" that I don't mind sharing with the world.
