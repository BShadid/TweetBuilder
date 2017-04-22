# twitterRNN / TweetBuilder

Data Structures Final Project, Spring 2017

tl;dr: This program generates tweets based on word correlations,
can be run with or without human interaction. Outputs:
[twitter](https://twitter.com/2Nip_DataMiner)

## Contributors

Jacob Beiter [@jcbbeiter](https://github.com/jcbbeiter)

Samuel Berning [@baronbird](https://github.com/baronbird)

Benjamin Shadid [@BShadid](https://github.com/bshadid)

## Abstract

This script fetches tweets about a user-specified topic, constructs a network of related words, and allows the user to build their own tweet using a recursive correlation tree. Once the character limit is reached or no words are closely related, the user has the option to tweet their creation.

Running aiDriver.py will run the interface script every 10 minutes and generate/send tweets automatically. Both human and automatic modes tweet as [@2Nip\_DataMiner](https://twitter.com/2Nip_DataMiner)

## Disclaimer

This project will be using the tweepy python package to interact with the
twitter's API. It will also use the pygame graphics library. Both are
available for free use under the MIT License and the LGPL 
Software License, respectively.
