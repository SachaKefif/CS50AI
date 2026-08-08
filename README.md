# CS50's Introduction to Artificial Intelligence with Python

My coursework for [CS50's Introduction to Artificial Intelligence with
Python](https://cs50.harvard.edu/ai/), organized by course unit.

## Projects

| Unit | Topic | Project | Status |
| --- | --- | --- | --- |
| 0 | Search | [Degrees](0/degrees) | In progress |

More projects will be added as I progress through the course.

## Repository structure

```text
CS50AI/
├── 0/
│   └── degrees/
│       ├── small/       # Small dataset for development
│       ├── degrees.py   # Project entry point
│       └── util.py      # Search frontier utilities
└── README.md
```

The large Degrees dataset is intentionally excluded from Git because it is
generated course data and is not needed for quick local testing. If it already
exists in `0/degrees/large`, it remains available locally.

## Running Degrees

This project requires Python 3 and uses only the standard library.

```bash
cd 0/degrees
python degrees.py small
```

Enter two actor names when prompted. The completed program finds the shortest
chain of films connecting them.

## Course checks

From the `0/degrees` directory, the official CS50 tools can be run with:

```bash
check50 ai50/projects/2024/x/degrees
style50 degrees.py
```

## Academic honesty

This repository documents my personal coursework. If you are currently taking
CS50 AI, follow the course's [academic honesty
policy](https://cs50.harvard.edu/ai/honesty/) and complete the projects
yourself.
