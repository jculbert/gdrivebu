#/bin/sh
echo file: $2 key: $1
openssl enc -des3 -md md5 -k $1 -in $2 -out $2.des
