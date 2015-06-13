import unittest
from subprocess import check_output
from Node import *
from os import listdir
from os.path import isfile, join


class TestNF(unittest.TestCase):
    
    def normalize(self,  ans):
        lines = ans.split('\n')
        lines = sorted(lines,  key=lambda line: line.split(':')[0])
        lines = filter(None,  lines)
        ans = ""
        for line in lines:
            node = line.split(':')[0]
            rest = line.split(':')[1].split(',')
            rest = sorted(rest)
            ans += node + ":"
            for stuff in rest:
                ans += stuff + ","
            ans = ans[:-1]
        return ans
    
    def test_topos(self):
        onlyfiles = [ f for f in listdir(".") if isfile(join(".",f)) ]
        for file in onlyfiles:
            if file.endswith(".py") and file.startswith("topo"):
                print file[:-3]
                ans = check_output(["python", "run_topo.py", file[:-3], "/dev/null"])
                ans = ans.split('-----')[-2]
                ans = self.normalize(ans)
                correct = (__import__(file[:-3]).ans)
                #print "checking",  ans, '\n',  correct
                self.assertEqual(ans, correct)
	
if __name__ == '__main__':
	unittest.main()
