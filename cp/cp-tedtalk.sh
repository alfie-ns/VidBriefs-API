#!/bin/bash
if find ../ted_talks -name "*.py" -type f -exec echo "File: {}" \; -exec cat {} \; -exec echo \; | pbcopy; then
  echo -e "\033[1mCopied all TedTalk-Related Python files to clipboard\033[0m"
fi