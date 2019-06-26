import os
import sys

import pytest

from expert_system import standard_algo


class TestExpertSystem:


	def test_and(self, capsys):
		path = "tests/input/and"
		list_files = os.listdir(path)
		for file in list_files:
			if file.endswith('.txt'):
				with open(f"tests/output/out_{file}", 'r') as fd:
					out_target = fd.read()
				if file == 'and_7.txt':
					with pytest.raises(SystemExit) as e:
						standard_algo(f"{path}/{file}", False)
				else:
					standard_algo(f"{path}/{file}", False)
				results = capsys.readouterr()
				with capsys.disabled():
					print(file)
				assert  results.out == out_target


	def test_and_conclusion(self, capsys):
		path = "tests/input/and_conclusion"
		list_files = os.listdir(path)
		for file in list_files:
			if file.endswith('.txt'):
				with open(f"tests/output/out_{file}", 'r') as fd:
					out_target = fd.read()
				if file == 'and_conclusion_2.txt':
					with pytest.raises(SystemExit) as e:
						standard_algo(f"{path}/{file}", False)
				else:
					standard_algo(f"{path}/{file}", False)
				results = capsys.readouterr()
				with capsys.disabled():
					print(file)
				assert  results.out == out_target


	def test_or(self, capsys):
		path = "tests/input/or"
		list_files = os.listdir(path)
		for file in list_files:
			if file.endswith('.txt'):
				with open(f"tests/output/out_{file}", 'r') as fd:
					out_target = fd.read()
				if file == 'or_5.txt':
					with pytest.raises(SystemExit) as e:
						standard_algo(f"{path}/{file}", False)
				else:
					standard_algo(f"{path}/{file}", False)
				results = capsys.readouterr()
				with capsys.disabled():
					print(file)
				assert  results.out == out_target


	def test_xor(self, capsys):
		path = "tests/input/xor"
		list_files = os.listdir(path)
		for file in list_files:
			if file.endswith('.txt'):
				with open(f"tests/output/out_{file}", 'r') as fd:
					out_target = fd.read()
				if file == 'xor_5.txt':
					with pytest.raises(SystemExit) as e:
						standard_algo(f"{path}/{file}", False)
				else:
					standard_algo(f"{path}/{file}", False)
				results = capsys.readouterr()
				with capsys.disabled():
					print(file)
				assert  results.out == out_target


	def test_not(self, capsys):
		path = "tests/input/not"
		list_files = os.listdir(path)
		for file in list_files:
			if file.endswith('.txt'):
				with open(f"tests/output/out_{file}", 'r') as fd:
					out_target = fd.read()
				if file == 'not_8.txt':
					with pytest.raises(SystemExit) as e:
						standard_algo(f"{path}/{file}", False)
				else:
					standard_algo(f"{path}/{file}", False)
				results = capsys.readouterr()
				with capsys.disabled():
					print(file)
				assert  results.out == out_target


	def test_conclusion_same_fact(self, capsys):
		path = "tests/input/conclusion_same_fact"
		list_files = os.listdir(path)
		for file in list_files:
			if file.endswith('.txt'):
				with open(f"tests/output/out_{file}", 'r') as fd:
					out_target = fd.read()
				if file == 'conclusion_same_fact_2.txt':
					with pytest.raises(SystemExit) as e:
						standard_algo(f"{path}/{file}", False)
				else:
					standard_algo(f"{path}/{file}", False)
				results = capsys.readouterr()
				with capsys.disabled():
					print(file)
				assert  results.out == out_target


	def test_priority(self, capsys):
		path = "tests/input/priority"
		list_files = os.listdir(path)
		for file in list_files:
			if file.endswith('.txt'):
				with open(f"tests/output/out_{file}", 'r') as fd:
					out_target = fd.read()
				standard_algo(f"{path}/{file}", False)
				results = capsys.readouterr()
				with capsys.disabled():
					print(file)
				assert  results.out == out_target


	def test_imply(self, capsys):
		path = "tests/input/imply"
		list_files = os.listdir(path)
		for file in list_files:
			if file.endswith('.txt'):
				with open(f"tests/output/out_{file}", 'r') as fd:
					out_target = fd.read()
				if file != 'imply_3.txt':
					with pytest.raises(SystemExit) as e:
						standard_algo(f"{path}/{file}", False)
				else:
					standard_algo(f"{path}/{file}", False)
				results = capsys.readouterr()
				with capsys.disabled():
					print(file)
				assert  results.out == out_target

	def test_eval(self, capsys):
		path = "tests/input/eval"
		list_files = os.listdir(path)
		for file in list_files:
			if file.endswith('.txt'):
				with open(f"tests/output/out_{file}", 'r') as fd:
					out_target = fd.read()
				standard_algo(f"{path}/{file}", False)
				results = capsys.readouterr()
				with capsys.disabled():
					print(file)
				assert  results.out == out_target


	def test_error(self, capsys):
		path = "tests/input/error"
		list_files = os.listdir(path)
		for file in list_files:
			if file.endswith('.txt'):
				with open(f"tests/output/out_{file}", 'r') as fd:
					out_target = fd.read()
				with capsys.disabled():
					print(f"{file} getting in")
				if file in ['error_14.txt', 'error_17.txt', 'error_10.txt', 'error_08.txt',
							'error_09.txt','error_18.txt']:
					with pytest.raises(SystemExit) as e:
						standard_algo(f"{path}/{file}", False)
				else:
					standard_algo(f"{path}/{file}", False)
				results = capsys.readouterr()
				with capsys.disabled():
					print(f"{file} getting out")
				assert  results.out == out_target

	def test_parsinsg_error(self, capsys):
		path = "tests/input/parsing_error"
		list_files = os.listdir(path)
		for file in list_files:
			with open(f"tests/output/out_{file}", 'r') as fd:
				out_target = fd.read()
			with capsys.disabled():
				print(f"{file} getting in")
			if file not in ['error_03.txt', 'error_07.txt', 'error_11.txt',
							'error_21.txt']:
				with pytest.raises(SystemExit) as e:
					standard_algo(f"{path}/{file}", False)
			else:
				standard_algo(f"{path}/{file}", False)
			results = capsys.readouterr()
			with capsys.disabled():
				print(f"{file} getting out")
			assert  results.out == out_target


	def test_failing(self, capsys):
		path = "tests/failing_tests"
		list_files = os.listdir(path)
		for file in list_files:
			with open(f"tests/output/out_{file}", 'r') as fd:
				out_target = fd.read()
			with capsys.disabled():
				print(f"{file} getting in")
			if file in ['ideas.txt', 'test3.txt']:
				with pytest.raises(SystemExit) as e:
					standard_algo(f"{path}/{file}", False)
			else:
				standard_algo(f"{path}/{file}", False)
			results = capsys.readouterr()
			with capsys.disabled():
				print(f"{file} getting out")
			assert  results.out == out_target