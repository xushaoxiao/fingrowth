import copy, importlib.util, json, pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('analysis',ROOT/'scripts/analyze.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class AnalysisTest(unittest.TestCase):
 def setUp(self): self.rows=json.loads((ROOT/'examples/lending/cohorts.json').read_text())
 def test_economics(self):
  a,b=map(m.analyze,self.rows)
  self.assertEqual(a['contribution'],4000);self.assertEqual(b['contribution'],-1000)
  self.assertLess(b['funded_cac'],a['funded_cac'])
 def test_zero_denominator(self):
  r=self.rows[0];r['counts']={k:0 for k in m.STAGES}
  self.assertIsNone(m.analyze(r)['funded_cac'])
 def test_immature(self):
  self.rows[0]['mature']=False
  self.assertIsNone(m.analyze(self.rows[0])['contribution'])
 def test_invalid(self):
  for key,value in [('revenue',float('nan')),('credit_loss',-1),('synthetic',False)]:
   r=copy.deepcopy(self.rows[0]);r[key]=value
   with self.assertRaises(ValueError):m.analyze(r)
 def test_non_nested(self):
  self.rows[0]['counts']['approved']=99999
  with self.assertRaises(ValueError):m.analyze(self.rows[0])
