# LLM Usage

## Overview

This document describes how LLM was utilized in the development of this assignment. Overall, LLM was used to assist in creating RegEx for cookie parsing, debuging issues with HTTP request formatting, and resolving issues with HTTP 2 checker.

## LLM utilization

- I noticed the cookie was separated by colons, but there is also a colon in the expiry time, so I asked LLM to help me create a RegEx that would parse the cookie correctly. The result is `,\s*(?=[a-zA-Z][a-zA-Z0-9_]*\s*=)`.
- I had issues with the HTTP2 checker where every requests would return `http2_handshake_failed`. I asked LLM to help me debug the issue, and it suggested that I print out the raw HTTP request being sent.
