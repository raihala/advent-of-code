Part 1:
```
gamma_b2=$(for x in $(sed 's/./& /g' input | numsum -c); do (( x >= 500 )) && echo -n 1 || echo -n 0; done); gamma=$(echo "ibase=2;obase=A;$gamma_b2" | bc); epsilon=$(( 4095 - gamma )); echo $(( gamma * epsilon ))
```

Part 2:
```
foo () { p=''; for i in $(seq 1 12); do ps=$(grep "^$p" input | cut -c "1-$i" | sort | uniq -c); if [ "$1" == "c" ]; then sps=$(echo "$ps" | sort -nr -k 1); else sps=$(echo "$ps" | sort -n -k 1); fi; p=$(echo "$sps" | awk 'END {print $2}'); done; echo "ibase=2;obase=A;$p" | bc; }; echo $(( $(foo) * $(foo c) ))
```

Also have some Python for part 2.