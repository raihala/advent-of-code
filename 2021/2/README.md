awk '$1=="forward" {h=h+$2} $1=="up" {d=d-$2} $1=="down" {d=d+$2} END {print h*d}' input
awk '$1=="forward" {h=h+$2; d=d+($2*aim)} $1=="up" {aim=aim-$2} $1=="down" {aim=aim+$2} END {print h*d}' input
