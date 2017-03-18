Outline 
=========

Each part of the program's functionality should be broken up into its own file.
For instance, one script could be in charge of curling the API and extracting
the tweet fields, another could be a word-count MapReduce script for word
count, etc. There would then be a driver file for this that would put this all
together.

We would therefore need the following files (this list is subject to change),
written in the anticipated order of use by the driver file:

## Functional Files

|      Filename       |   Author   | Done |
|---------------------|------------|------|
| twitter_curl.py\*    |            |      |
| wordcount_MR.py     |            |      |
| word_mapper.py      |            |      |
| tree_mapper.py      |            |      |

*This file might not be written if we continue to use the tweepy package.

## Driving files and libraries

|       Filename        |    Author    | Done |
|-----------------------|--------------|------|
| twitterRNN.py         |              |      |
| graphics.py           | N/A          | [x]  |
| tweepy                | N/A          | [x]  |
| recursive_methods.pyc |              |      |
| math_methods.pyc\*     |              |      |


*This file will be written if calculating word correlations and sizes of words
requires unsightly or complicated functions. If written, its methods will be 
imported into the other method files, not necessarily the main driver file.

The functions/classes in Functional Files are imported into a main driver file
called twitterRNN.py, which will then utilize them to run the program.
twitter_curl.py may be replaced with twurl or another previously-written script
if twitter application application is too complicated of a process. Each of the
files maps to one or multiple of the objectives outlines in milestones.txt.


NOTE: The graphics library, graphics.py, is already written, so there shouldn't need
to be any changes made to it.
