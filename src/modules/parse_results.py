# -*- coding: utf-8 -*-
"""
Summary:
		This Module will take json logs and convert them into tsv format
author:
grimm venom <grimmvenom@gmail.com>

"""

import platform, os, sys, re, time, json, csv
from src.base.base import Base
import xlsxwriter
import pandas
try:
	from pandas.io.json import json_normalize
except Exception as e:
	# print(f"Error importing module: {e}")
	pass


class Parse_Excel:
	def __init__(self, arguments):
		self.arguments = arguments
		self.date = time.strftime("%Y-%m-%d")  # Date Format ISO 8601
		self.start = time.strftime("%I_%M")  # Time
		self.exec_time = str(time.strftime("%I_%M_%p"))  # Time
		self.base = Base()
		self.log_dir = self.base.get_log_dir()
		self.main()
		
	def main(self):
		if not os.path.isdir(self.log_dir):
			os.makedirs(self.log_dir)

	def scraper_to_excel(self, json_results: dict, filename=''):
		headers = dict()
		total_records = dict()
		
		if filename:
			report_path = self.log_dir + filename + "-" + self.date + "-" + self.exec_time + ".xlsx"
		else:
			report_path = self.log_dir + self.date + "-" + self.exec_time + ".xlsx"
		
		# print(json_results.keys())
		print("\nWriting results to: " + str(report_path))
		
		# Get Unique Headers
		for url, url_data in json_results.items():
			for element_type, type_data in url_data.items():
				if element_type not in headers:
					headers[element_type] = list()
				for index, data in type_data.items():
					# json_results[url][element_type][index]['scraped_from'] = url
					for key, value in data.items():
						if key not in headers[element_type]:
							headers[element_type].append(key)
		
		# sort headers
		for element_type in headers.keys():
			if 'scraped_from' in headers[element_type]:
				headers[element_type].insert(0, headers[element_type].pop(headers[element_type].index('scraped_from')))
			if 'text' in headers[element_type]:
				headers[element_type].insert(1, headers[element_type].pop(headers[element_type].index('text')))
			if 'target_url' in headers[element_type]:
				headers[element_type].insert(2, headers[element_type].pop(headers[element_type].index('target_url')))
			
			if 'href' in headers[element_type]:
				headers[element_type].insert(3, headers[element_type].pop(headers[element_type].index('href')))
			elif 'src' in headers[element_type]:
				headers[element_type].insert(3, headers[element_type].pop(headers[element_type].index('src')))
			
			if 'htmlTag' in headers[element_type]:
				headers[element_type].insert(4, headers[element_type].pop(headers[element_type].index('htmlTag')))
			
			if 'status' in headers[element_type]:
				headers[element_type].insert(5, headers[element_type].pop(headers[element_type].index('status')))
				if 'message' in headers[element_type]:
					headers[element_type].insert(6, headers[element_type].pop(headers[element_type].index('message')))
				if 'pageTitle' in headers[element_type]:
					headers[element_type].insert(7, headers[element_type].pop(headers[element_type].index('pageTitle')))
			if 'valid_url' in headers[element_type]:
				headers[element_type].insert(-1, headers[element_type].pop(headers[element_type].index('valid_url')))
				
		# Combine dictionary results by element_type
		for url, url_data in json_results.items():
			for element_type, type_data in url_data.items():
				if element_type not in total_records.keys():
					total_records[element_type] = list()
				for index, data in type_data.items():
					total_records[element_type].append(data)
		
		workbook = xlsxwriter.Workbook(report_path, {'strings_to_urls': False})
		header_cells = workbook.add_format()
		header_cells.set_bold()
		header_cells.set_align('center')
		
		for element_type, type_data in total_records.items():
			row = 0
			column = 0
			worksheet = workbook.add_worksheet(str(element_type))
			for head in headers[element_type]:
				worksheet.write(row, column, head, header_cells)
				column += 1
			row += 1
			for item in type_data:
				for key, value in item.items():
					index = headers[element_type].index(key)
					column = index
					worksheet.write(row, column, str(value))
				row += 1
		workbook.close()
		return report_path
	
	def status_to_excel(self, json_results: dict, filename=''):
		print("Writing json to excel")
		report_path = self.log_dir + filename + "-" + self.date + "-" + self.exec_time + ".xlsx"
		# Append List of dictionary results to a single dictionary
		json_dictionary = {}
		for d in json_results:
			for url, data in d.items():
				json_dictionary[url] = data
		
		loop_data = list()
		for url, data in json_dictionary.items():
			loop_data.append(data)
			
		df = pandas.DataFrame(loop_data)
		columns = list(df.columns.values)
		if 'url' in columns:
			columns.insert(0, columns.pop(columns.index('url')))
		if 'status' in columns:
			columns.insert(1, columns.pop(columns.index('status')))
		if 'pageTitle' in columns:
			columns.insert(2, columns.pop(columns.index('pageTitle')))
	
		workbook = xlsxwriter.Workbook(str(report_path), {'strings_to_urls': False})
		header_cells = workbook.add_format()
		header_cells.set_bold()
		header_cells.set_align('center')
		workbook.add_worksheet('Status')  # Add Named Sheet to Workbook
		workbook.close()
		writer = pandas.ExcelWriter(str(report_path), engine='xlsxwriter', options={'strings_to_urls': False})  # Write DataFrame to excel
		df[columns].to_excel(writer, sheet_name='Status')  # Write sorted Dataframe
		writer.close()
		return report_path
