set export

year := "2025"

r:
  just run $(date "+%-d")
run DAY:
  [ -f day{{DAY}}/solve.py ] || just create {{DAY}}
  uv run day{{DAY}}/solve.py

create DAY:
  just load {{DAY}}
  cat template.py | sed 's/|DAY|/{{DAY}}/g' >day{{DAY}}/solve.py
  git add day{{DAY}}

code DAY:
  just create {{DAY}}
  nvim day{{DAY}}/solve.py

load DAY:
  mkdir -p day$DAY
  curl -sf "https://adventofcode.com/$year/day/$DAY/input" -H "Cookie: $(cat session)" -o day$DAY/input.txt
