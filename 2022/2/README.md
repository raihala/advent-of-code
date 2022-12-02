```bash
awk '{switch($0){ case "B Z": x++; case "A Y": x++; case "C X": x++; case "C Z": x++; case "B Y": x++; case "A X": x++; case "A Z": x++; case "C Y": x++; case "B X": x++ }} END {print x}' input 
awk '{switch($0){ case "B Z": x++; case "A Z": x++; case "C Z": x++; case "C Y": x++; case "B Y": x++; case "A Y": x++; case "A X": x++; case "C X": x++; case "B X": x++ }} END {print x}' input 
```
