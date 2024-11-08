#!/bin/bash
cd ..
# Get the current directory name
current_dir=$(basename "$PWD")

# if succesfully pushed, back out of the directory and delete it off local
if ./pu.sh; then
  # Change to the parent directory if push.sh succeeds
  cd ..
  # Remove the original directory
  rm -rf "$current_dir"
else
  echo "Error: pu.sh failed. Exiting."
fi

# 1. Push
# 2. Back out of dir
# 3. Delete repo

# 'alfie-ns' ascii
cat <<'EOF'
╔════════════════════════════════════════════════════════════════════════════════════════════╗
║ ╬⚙️ Process complete ⚙️╬                                        ⠀⢀⣀⣤⣤⣴⣶⣾⣿⣿⣶⣦⣤⣤⣀⠀           ║
╚════════════════════════════════════════════════════════════════════════════════════════════╝
║        _  __ _                                              ⠀⠈⠉⠙⠛⠿⣿⣿⣿⣿⣿⣿⠿⠛⠋⠉⠁⠀           ║
║  __ _ | |/ _(_) ___       _ __  ___                         ⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀          ║
║ / _` || | |_| |/ _ \_____| '_ \/ __|                       ⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣄⠀⠀⠀⠀⠀⠀⠀           ║
║| (_| || |  _| |  __/_____| | | \__ \                       ⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀           ║
║ \__,_||_|_| |_|\___|     |_| |_|___/                        ⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀           ║
║                                                             ⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀           ║
║                                                             ⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀           ║
╚════════════════════════════════════════════════════════════════════════════════════════════╝
EOF
