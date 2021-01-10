# rsm
A tool for measuring remote web pages, with the name reversed for pseudo-anonymity

## Install

`python -m venv venv && source venv/bin/activate && ./test.sh`

## Future Work

- Add better XDG support (e.g. for the aggregation data files)
- Refactor `measurement_service.py` and maybe split it up
- Make the data model more generic, so that it can handle non-float data
- Implement a lower-level networking service to avoid HTTP overhead
- Add proper dependency injection
