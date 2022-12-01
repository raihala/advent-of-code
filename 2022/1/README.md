```bash
awk 'NF==1 {x=x+$1; next} {print x; x=0}' input | sort | tail -1
awk 'NF==1 {x=x+$1; next} {print x; x=0}' input | sort | tail -3 | paste -sd+ | bc
```
