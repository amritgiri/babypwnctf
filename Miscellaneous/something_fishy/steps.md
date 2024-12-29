# Creating challenge

create a text file with a flag

pandoc plaintext.txt -o challenge.txt

qpdf --encrypt supersecreta_17 supersecreta_17 256 -- challenge.pdf private.pdf

# SOLUTION
sudo apt install john 

pdf2john private.pdf > pdf.hash

john --wordlist=/usr/share/wordlists/rockyou.txt pdf.hash

pdftotext -upw supersecreta_17 private.pdf output.txt

cat output.txt

i-CES{S01v3_7H3_9Uz2l3}

