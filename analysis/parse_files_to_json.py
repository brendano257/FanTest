import os
import json
from pathlib import Path
from datetime import datetime

DATA_PATH = Path(os.getcwd()) / 'data'
JSON_PATH = Path(os.getcwd()) / 'json'


def parse_log_file(path: Path):
	"""
	Reads a log file and returns a list containing all measurements as dictionaries of date and temperature/fan params.

	:param Path path: pathlib path to the file to be parsed
	:return list: list containing all measurement dictionaries
	"""

	FMT = '%Y-%m-%dT%H:%M:%S%z'  # date format for GNU ISO-8601 (except colon in tz/offset)

	with path.open('r') as f:
		contents = [line.rstrip() for line in f]

	all_measurements = []
	measurement = {}

	for index, line in enumerate(contents):
		if line.startswith("DATE::"):

			if measurement:
				all_measurements.append(measurement)  # move previous measurement to list

			measurement = {}  # create new active measurement

			datestring = line.replace('DATE::', '')
			date = datetime.strptime(datestring[:-3] + datestring[-2:], FMT)  # drop the colon in the tz, then parse

			measurement['date'] = date.isoformat(' ')  # write date as Python iso-8601

		elif line.startswith('coretemp-isa-0000'):
			temp_lines = range(index + 3, index + 9)  # core temperatures are the 3rd:9th elements after this line

			for num, temp_line in enumerate(temp_lines):
				parsed_line = [el for el in contents[temp_line].split(' ') if el]  # split on spaces and strip empty strings

				measurement[f'CPU-{num}'] = float(parsed_line[2][:-2])  # grab third element and drop "*C" at end

		elif line.startswith('amdgpu-pci-0100'):
			voltage_line = contents[index + 2]
			fan_line = contents[index + 3]
			temp_line = contents[index + 4]
			wattage_line = contents[index + 5]

			measurement['GPU Voltage'] = float([el for el in voltage_line.split(' ') if el][1])
			# voltage is the second non-empty element in it's line
			measurement['GPU Fan'] = int([el for el in fan_line.split(' ') if el][1])
			# same as voltage
			measurement['GPU Watts'] = float([el for el in wattage_line.split(' ') if el][1])
			# same as voltage and fan

			measurement['GPU'] = float([el for el in temp_line.split(' ') if el][1][:-2])
			# GPU temp is the second non-empty element, with "*C" stripped from the end


	return all_measurements


def write_to_json(path: Path):
	"""
	Writes the created measurements list to a JSON file with the same name as the input file (but with .json)

	:param Path path: pathlib Path to the file that was read for the data.
	:return: None
	"""
	measurements_dict = parse_log_file(path)

	json_file_path = JSON_PATH / path.name.replace('.txt', '.json')

	with json_file_path.open('w') as f:
		f.write(json.dumps(measurements_dict).replace('},', '},\n'))
		print(f'Wrote {json_file_path.name}')


def load_from_json(path: Path):
	"""
	Reads the specified JSON file and returns the list of measurement dictionaries with a datetime date

	:param Path path: pathlib path to the file to be read back in
	:return list: list containing all measurement dictionaries
	"""
	with path.open('r') as f:
		measurements = json.loads(f.read())

		for m in measurements:
			if m.get('date'):
				m['date'] = datetime.strptime(m['date'], '%Y-%m-%d %H:%M:%S%z')

		return measurements


if __name__ == "__main__":
	for file in [f for f in DATA_PATH.iterdir() if f.is_file() and f.suffix == '.txt']:
		write_to_json(file)