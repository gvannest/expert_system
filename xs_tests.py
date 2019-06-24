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
						standard_algo(f"{path}/{file}")
				else:
					standard_algo(f"{path}/{file}")
				results = capsys.readouterr()
				with capsys.disabled():
					print(file)
				assert  results.out == out_target

