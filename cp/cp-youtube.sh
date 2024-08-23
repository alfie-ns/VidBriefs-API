#!/bin/bash
if find ../youtube -name "*.py" -type f -exec echo "File: {}" \; -exec cat {} \; -exec echo \; | pbcopy; then
  echo -e "\033[1mCopied all youtube/ Python files to clipboard\033[0m"
fi