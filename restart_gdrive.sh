#! /bin/bash
# google-drive input/output error and ll=> d??????? ?? ?? google-drive

# start over
rm -rf $HOME/.gdfuse
sudo umount $HOME/google-drive

google-drive-ocamlfuse << security from gmail search google-drive-ocamlfuse>>

echo "After authorizing in browser should see 'Access token retrieved' in term"
echo "Ready to continue?"
read ans
google-drive-ocamlfuse ~/google-drive/ 

