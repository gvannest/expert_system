import os
import sys

import pytest

from expert_system import standard_algo


class TestExpertSystem:


	def test_and(self, capsys):
		path = "/Users/gvannest/git_perso/expert_system/tests/input/and"
		list_files = os.listdir(path)
		for file in list_files:
			if file.endswith('.txt'):
				with open(f"/Users/gvannest/git_perso/expert_system/tests/output/out_{file}", 'r') as fd:
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
		path = "/Users/gvannest/git_perso/expert_system/tests/input/and_conclusion"
		list_files = os.listdir(path)
		for file in list_files:
			if file.endswith('.txt'):
				with open(f"/Users/gvannest/git_perso/expert_system/tests/output/out_{file}", 'r') as fd:
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
		path = "/Users/gvannest/git_perso/expert_system/tests/input/or"
		list_files = os.listdir(path)
		for file in list_files:
			if file.endswith('.txt'):
				with open(f"/Users/gvannest/git_perso/expert_system/tests/output/out_{file}", 'r') as fd:
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
		path = "/Users/gvannest/git_perso/expert_system/tests/input/xor"
		list_files = os.listdir(path)
		for file in list_files:
			if file.endswith('.txt'):
				with open(f"/Users/gvannest/git_perso/expert_system/tests/output/out_{file}", 'r') as fd:
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
		path = "/Users/gvannest/git_perso/expert_system/tests/input/not"
		list_files = os.listdir(path)
		for file in list_files:
			if file.endswith('.txt'):
				with open(f"/Users/gvannest/git_perso/expert_system/tests/output/out_{file}", 'r') as fd:
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
		path = "/Users/gvannest/git_perso/expert_system/tests/input/conclusion_same_fact"
		list_files = os.listdir(path)
		for file in list_files:
			if file.endswith('.txt'):
				with open(f"/Users/gvannest/git_perso/expert_system/tests/output/out_{file}", 'r') as fd:
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
		path = "/Users/gvannest/git_perso/expert_system/tests/input/priority"
		list_files = os.listdir(path)
		for file in list_files:
			if file.endswith('.txt'):
				with open(f"/Users/gvannest/git_perso/expert_system/tests/output/out_{file}", 'r') as fd:
					out_target = fd.read()
				standard_algo(f"{path}/{file}", False)
				results = capsys.readouterr()
				with capsys.disabled():
					print(file)
				assert  results.out == out_target


	def test_imply(self, capsys):
		path = "/Users/gvannest/git_perso/expert_system/tests/input/imply"
		list_files = os.listdir(path)
		for file in list_files:
			if file.endswith('.txt'):
				with open(f"/Users/gvannest/git_perso/expert_system/tests/output/out_{file}", 'r') as fd:
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