# Where is it?

Dear course team,

Please check out a small **compiled** website I made back in November of 2025:

[d-language.website](https://d-language.website)

And, specifically, the Dockerfile for the server:

[Dockerfile](https://github.com/Error10556/dsite/blob/main/site/Dockerfile)

This is a showcase for an interpreted language we made for the Compiler Construction course. However,
this interpreted language is called from C++ through an interpreter library that gets compiled from source in a
2-stage build! Dmitry Creed said during the lecture that this is the main point of the bonus task.

## How it works

Through NginX, the client connects to the server written in C++ using Oat++ framework. The server handles connections.
When a page is requested, the C++ server uses the D language library (compiled!) to call an interpreted function that
would return the HTML page text or an image.

Sure, the site was originally meant to showcase the interpreter, but I feel like the compiled part also deserves
appreciation.
