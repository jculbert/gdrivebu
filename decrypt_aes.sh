in="$1"

if [[ "$in" == *.aes ]]; then
    # Out filename is same as input but with suffix removed
    out="${in%.aes}"
    echo $out
else
    echo "Error: Input filename '$in' does not end with 'aes'" >&2
    exit 2
fi

openssl enc -d -aes-256-cbc -salt -pbkdf2 -iter 100000 -pass "pass:$(< /tmp/encp.txt)" -in $in -out $out
