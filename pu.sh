#!/bin/bash

# Function to print bold text
print_bold() {
  BOLD=$(tput bold)
  NORMAL=$(tput sgr0)
  echo -e "${BOLD}$1${NORMAL}"
}


git add .;
git commit -m 'update';
git push origin main;

echo "" # padding
print_bold "Remote Repository pushed to GitHub"
echo "" # padding