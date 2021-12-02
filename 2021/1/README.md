```
awk 'FNR==NR {a[NR]=$1; next} $1>a[FNR] {res=res+1} END {print res}' <(head -n 1999 input) <(tail -n 1999 input)
awk 'FNR==NR {a[NR]=$1; next} $1>a[FNR] {res=res+1} END {print res}' <(head -n 1997 input) <(tail -n 1997 input)
```
