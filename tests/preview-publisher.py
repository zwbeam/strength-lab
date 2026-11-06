"""Verify publication stops before altering an unexpected repository or Pages setup."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('publisher',ROOT/'scripts/publish-preview.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class PublisherGuards(unittest.TestCase):
 def api(self,path,method='GET',body=None,missing_ok=False):
  if path.endswith('/git/ref/heads/main'):return {'object':{'sha':'original-main'}}
  if path=='repos/zwbeam/strength-lab/pages':return {'source':{'branch':'main','path':'/'}}
  if path=='user':return {'login':'zwbeam'}
  if path=='repos/zwbeam/strength-lab-preview':return None
  if path=='user/repos':raise RuntimeError('Resource not accessible by integration (HTTP 403)')
  raise AssertionError((path,method))
 def test_creation_permission_failure_gives_required_action_without_source_writes(self):
  with patch.object(module,'api',side_effect=self.api) as api:
   with self.assertRaisesRegex(RuntimeError,'owner must create an empty public'):module.publish('HEAD',True)
   writes=[c for c in api.call_args_list if len(c.args)>1 and c.args[1]!='GET']
   self.assertEqual([c.args[0] for c in writes],['user/repos'])
 def test_wrong_owner_stops_before_creation(self):
  def api(path,*args,**kwargs):return {'login':'someone-else'} if path=='user' else self.api(path,*args,**kwargs)
  with patch.object(module,'api',side_effect=api) as mocked:
   with self.assertRaisesRegex(ValueError,'authorized repository owner'):module.publish('HEAD',True)
   self.assertFalse(any(len(c.args)>1 and c.args[1]!='GET' for c in mocked.call_args_list))
 def test_unknown_private_target_is_not_overwritten(self):
  def api(path,*args,**kwargs):return {'full_name':module.TARGET,'private':True} if path=='repos/'+module.TARGET else self.api(path,*args,**kwargs)
  with patch.object(module,'api',side_effect=api):
   with self.assertRaisesRegex(ValueError,'identity/visibility'):module.publish('HEAD',True)
 def test_existing_target_with_unexpected_branch_is_preserved(self):
  def api(path,*args,**kwargs):
   if path=='repos/'+module.TARGET:return {'full_name':module.TARGET,'private':False}
   if path.endswith('/branches?per_page=100'):return [{'name':'unrelated'}]
   return self.api(path,*args,**kwargs)
  with patch.object(module,'api',side_effect=api):
   with self.assertRaisesRegex(ValueError,'nothing was overwritten'):module.publish('HEAD',True)
if __name__=='__main__':unittest.main()
