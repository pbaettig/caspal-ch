SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
set -e

cd $SCRIPT_DIR

zip -0 -o main.py.zip main.py >/dev/null 2>&1

os="$(uname -s)"
case "${os}" in
    Linux*)     chksum=`sha256sum main.py`;;
    Darwin*)    chksum=`shasum -a 256 main.py`;;
esac


echo "{\"sha256\": \"$(echo $chksum | cut -d' ' -f1)\"}"
