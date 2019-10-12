import os
from pathlib import Path
from datetime import datetime

file = Path(os.getcwd()) / 'test.txt'

def parse_log_file(path: Path):

	FMT = '%Y-%m-%dT%H:%M:%S%z'  # date format for GNU ISO-8601
	# !! *requires* Python 3.7 for %z to accept -04:00 as a TZ (GNU format) and not just -0400

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
			date = datetime.strptime(datestring, FMT)  # drop the colon in the tz, then parse

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

all = parse_log_file(file)

for el in all:
	print(el)
