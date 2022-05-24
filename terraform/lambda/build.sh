SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
set -e

cd $SCRIPT_DIR

fname='main.py.zip'
full_path="$(pwd)/$fname"

zip -0 -o "$fname" main.py >/dev/null 2>&1

echo "{\"path\": \"$full_path\"}"
