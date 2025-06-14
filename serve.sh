#!/bin/bash

# Run Jekyll serve and filter out Sass @import deprecation warnings
bundle exec jekyll serve 2>&1 | grep -v "Deprecation Warning \[import\]" | grep -v "More info and automated migrator" | grep -v "│" | grep -v "╷" | grep -v "╵" 