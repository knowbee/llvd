
#!/usr/bin/env bash
#Author:Igwaneza Bruce
#Email:knowbeeinc@gmail.com


echo "installing packages..."

pip3 install -r requirements.txt
filename="run.py"
path=$PWD/$filename
echo "configuring llvd"
echo "alias llvd='python3 $path'" >> ~/.bashrc 
exec bash
echo "llvd installed successfully"
