# TweetBuilder

Data Structures Final Project, Spring 2017

tl;dr: This program generates word correlations by processing tweets, then a
user builds tweets based on these word correlations and Tweets the result. Outputs:
[twitter](https://twitter.com/2Nip_DataMiner)

## Contributors

Jacob Beiter [@jcbbeiter](https://github.com/jcbbeiter)

Samuel Berning [@baronbird](https://github.com/baronbird)

Benjamin Shadid [@BShadid](https://github.com/bshadid)

## Abstract

This script fetches tweets about a user-specified topic, constructs a network of related words, and allows the user to build their own tweet using a recursive correlation tree. Once the character limit is reached or no words are closely related, the user has the option to tweet their creation. During the creation process, the viewer has access to their current tweet, their current character count, and methods for editing / undoing certain actions.

The markov algorithm improves with increasingly large sample sizes, so information about word
frequencies and correlations is read in at the start of the program and dumped
to text files after the program is finished with new tweet content added to it.

This program requires the keys.py file to interact with Twitter's API. This is not in the repository. For access to this file, contact one of the contributors.

## Important Notes and Updates

MAY 1, 2017: aiDriver.py and interface2.py have both been removed from the repository temporarily. They may be added back later.These were originally intended to allow the program to be run without human interaction and were used to construct the .corrM.txt and .freqs.txt reference files.

## Disclaimer

This project will be using the tweepy python package to interact with
twitter's API. It will also use the pygame graphics library. Both are
available for free use under the MIT License and the LGPL 
Software License, respectively.
