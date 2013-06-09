Dataleach
=========

This project focuses on pulling in data from various web resources and parsing them 
for specific identifiers, such as IP addresses.

Configurations
==============

There are two types of configutaitons the data leach processes.  First, there
is a system configuration, which is devoted to locating site specific
congiguration files and the basic output information such as basic output file
names.  The second, is site specific files, which dictate how a site is treated.


System Configuration
--------------------

System configuration files dictate how the dataleach operates in general.  The
following looks for 

~~~
[INPUT]
DIR=data
EXTENSION=.conf

[OUTPUT]
DIR=data
FORMAT=%Y%M%D.%h
~~~

The configuration is divided into two sections.

1. **INPUT** - Defines where to look for sources.
   1. _DIR_ - The directory to use
   2. _EXTENSION_ - The extension to look for
2. **OUTPUT** - Output directory information
   1. _DIR_ - The path to which site specific outputs will be written
   2. _FORMAT_ - Specificaition for the output file names' format.

Site Configuration
------------------

Site Configuation files dictate how the dataleach processes a site.  Below is a
sample configuration file that extracts the google.com web page and places its
content in`output/source1`.

~~~
[DETAILS]
name=source1
type=WEB_SOURCE
address=http://www.google.com

[PROCESS]
search=([0-9]{1,3}\.{3})[0-9]{1,3}
filter=<?.*>
[IO]
output_dir=output/source1
~~~

The configuration is divided into three sections

1. **DETAILS** - The metadata about the source including
   1. _name_ - The name of source.
   2. _type_ - The type of sourc being referenced.
   3. _address_ - The root URL to be accessed.
2. **PROCESS** - How data returned should be accessed
   1. _search_ - A regular expression representing the data that should be extracted from the site.
   2. _filter_ - A regular expression represneing data that should be immediately filtered out before searching
3. **IO** - The file IO that should be used for this source 
