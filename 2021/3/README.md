```
gamma_b2=$(for x in $(sed 's/./& /g' input | numsum -c); do (( x >= 500 )) && echo -n 1 || echo -n 0; done); gamma=$(echo "ibase=2;obase=A;$gamma_b2" | bc); epsilon=$(( 4095 - gamma )); echo $(( gamma * epsilon ))
```