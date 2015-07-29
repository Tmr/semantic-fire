Semantic Fire is a tool for generating RDF from websites. This can be used to make it possible to query the data.

# What can it be used for? #
Say you have a website about fishing and you know that your local government publishes a list of all fishing sites in your area on their website, but this data is not available via an API or in downloadable format. In this case you could use Semantic Fire to extract the data as RDF and store it in a triplestore such as OpenLink Virtuoso, and use this as a backend to your website. This data can be linked to other data via for example DBPedia, so the fishing website could get information on various fishes.

# How to use #
To use Semantic Fire you create a simple yaml file that maps a website's content to Semantic Web ontologies.

The yaml file for a website contains to main types of elements
,dataitems and databags. A dataitem is a single thing such as title or a date, while a databag is a repeating structure, where each item is separated by a tag such as div, li or tr. Examples of databags would be a comment list or an event list.

Here is an example of how to create RDF from comments and other data from digg
```
url: http://digg.com/
require_id: Yes
dataitems:
  - predicate: dc:title
    xpath: id('title')/a
  - predicate: dc:creator
    xpath: //a[@rel='dc:creator']
  - predicate: foaf:primaryTopic
    xpath: id('title')/a[@href]/@href
databags:
  - predicate: sioc:has_container
    xpath: //*[@id="p-main"]
    databag_class: sioc:Thread
    subpredicate: sioc:container_of
    datarow_class: sioc:Post
    p-list: ['dc:creator', 'dc:created', 'sioc:content', 'rev:rating']
    skip_end_rows: 2
    row_separator: li
```
require\_id means it has to be used with a specific path on the site.
Example usage:

> python semanticfire.py digg.yaml comedy/My\_neighbor\_creeps\_me\_out\_Pic

More example can be found in the examples folder and includes comments, similar videos and metadata from youtube; comments, tags and metadata from flickr; what's showing today of syfy channel

To find the XPaths the firefox extensions XPath Checker and Firebug are useful. The initial found XPaths might not be good enough as there tends to be small differences between the different pages on site. This means you have to tweak the XPath a bit to make it general, some examples of this can be found in the YouTube and flickr examples.

Semantic Fire can download websites via urllib2, Gecko or WebKit. WebKit is not currently well supported. When using Gecko or WebKit it can process Javascript and clean up the HTML. This requires X, for headless usage install Xvfb and run:

> startx -- `which Xvfb` :5 -screen 0 1024x768x24&

Afterwards Semantic Fire can be run by using:

> DISPLAY:5 python semanticfire.py

# Requirements #
  * python-lxml
  * python-yaml
  * python-hulahop (required if using GeckoDownloader)
  * python-xpcom (required if using GeckoDownloader)
  * python-gobject (required if using GeckoDownloader)
  * python-gtk2 (required if using GeckoDownloader)

# Next steps #
For now, any work on this project is postponed indefinitely.

## Todo list ##

  * Support following links and creating entities from multiple pages, often there is a details page that contain more information on the item that is described on a page.
  * Make it possible to use semantic fire as a declarative way of writing spiders for [scrapy](http://scrapy.org/)