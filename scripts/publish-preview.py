"""Publish only the isolated preview to a dedicated free GitHub Pages repository.

Never writes the source repository's main branch or its Pages settings.
Publication is not considered verified until tests/preview-url.py passes.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
SOURCE='zwbeam/strength-lab'
TARGET='zwbeam/strength-lab-preview'
BRANCH='preview'
EXPECTED_URL='https://zwbeam.github.io/strength-lab-preview/'

def run(*args,cwd=ROOT):
 return subprocess.check_output(args,cwd=cwd,text=True).strip()

def api(path,method='GET',body=None,missing_ok=False):
 command=['gh','api',path,'--method',method]
 if body is not None:command+=['--input','-']
 result=subprocess.run(command,input=json.dumps(body) if body is not None else None,text=True,capture_output=True)
 if result.returncode:
  if missing_ok and 'HTTP 404' in result.stderr:return None
  raise RuntimeError(result.stderr.strip() or result.stdout.strip())
 return json.loads(result.stdout) if result.stdout.strip() else None

def publish(ref,create=False):
 source_before=api(f'repos/{SOURCE}/git/ref/heads/main')['object']['sha']
 source_pages=api(f'repos/{SOURCE}/pages')
 if api('user')['login']!='zwbeam':raise ValueError('Expected the authorized repository owner zwbeam')
 target=api(f'repos/{TARGET}',missing_ok=True)
 if target is None:
  if not create:raise ValueError('Preview repository does not exist; use --create-repository for first publication')
  try:
   target=api('user/repos','POST',{'name':'strength-lab-preview','description':'Isolated Strength Lab development preview; not a production release','private':False,'auto_init':False,'has_issues':False,'has_projects':False,'has_wiki':False})
  except RuntimeError as error:
   if 'Resource not accessible by integration' in str(error):
    raise RuntimeError('The GitHub connection cannot create repositories. The owner must create an empty public zwbeam/strength-lab-preview repository and grant this connection access; then rerun without --create-repository. The existing application was not changed.') from error
   raise
 if target['full_name']!=TARGET or target['private']:raise ValueError('Unexpected preview repository identity/visibility')
 branches=api(f'repos/{TARGET}/branches?per_page=100')
 if branches and BRANCH not in [b['name'] for b in branches]:raise ValueError('Existing repository is not the expected preview deployment; nothing was overwritten')
 pages=api(f'repos/{TARGET}/pages',missing_ok=True)
 if pages and (pages.get('build_type')!='legacy' or pages.get('source')!={'branch':BRANCH,'path':'/'} or pages.get('cname')):
  raise ValueError('Preview Pages settings differ from the expected isolated deployment')
 if ref=='origin/development/reconciliation':
  subprocess.run(['git','fetch','origin','refs/heads/development/reconciliation:refs/remotes/origin/development/reconciliation'],cwd=ROOT,check=True)
 spec=importlib.util.spec_from_file_location('preview_builder',ROOT/'scripts/build-preview.py')
 builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
 with tempfile.TemporaryDirectory(prefix='strength-lab-publish-') as tmp:
  payload=Path(tmp)/'payload';metadata=builder.build(payload,ref)
  (payload/'.nojekyll').touch()
  checkout=Path(tmp)/'site'
  if branches:
   subprocess.run(['git','clone','--single-branch','--branch',BRANCH,f'https://github.com/{TARGET}.git',str(checkout)],check=True)
   old=json.loads((checkout/'preview-build.json').read_text())
   if old.get('channel')!='development-preview' or old.get('storage_namespace')!='sl-dev-preview':raise ValueError('Existing files are not a managed Strength Lab preview')
   worker=(checkout/'sw.js').read_text();match=re.search(r'const FILES=(\[.*?\]);',worker,re.S)
   if not match:raise ValueError('Cannot verify previous managed asset inventory')
   owned={urlsplit(x).path.removeprefix('./') or 'index.html' for x in json.loads(match[1])}|{'.nojekyll'}
   tracked=run('git','ls-files',cwd=checkout).splitlines()
   if set(tracked)-owned:raise ValueError('Unrecognized deployment files; preserving them instead of overwriting')
   for name in tracked:(checkout/name).unlink()
  else:
   checkout.mkdir();subprocess.run(['git','init','-b',BRANCH,str(checkout)],check=True)
   subprocess.run(['git','remote','add','origin',f'https://github.com/{TARGET}.git'],cwd=checkout,check=True)
  shutil.copytree(payload,checkout,dirs_exist_ok=True)
  subprocess.run(['git','add','-A'],cwd=checkout,check=True)
  if subprocess.run(['git','diff','--cached','--quiet'],cwd=checkout).returncode:
   subprocess.run(['git','-c','user.name=Codex','-c','user.email=codex@openai.com','commit','-m',f"Preview source {metadata['source_commit']}"],cwd=checkout,check=True)
   subprocess.run(['git','push','origin',f'HEAD:refs/heads/{BRANCH}'],cwd=checkout,check=True)
  deployment=run('git','rev-parse','HEAD',cwd=checkout)
 if target['default_branch']!=BRANCH:api(f'repos/{TARGET}','PATCH',{'default_branch':BRANCH})
 if pages is None:
  pages=api(f'repos/{TARGET}/pages','POST',{'build_type':'legacy','source':{'branch':BRANCH,'path':'/'}})
 else:api(f'repos/{TARGET}/pages/builds','POST',{})
 if pages['html_url']!=EXPECTED_URL:raise ValueError('Unexpected Pages URL; verify hosting before proceeding')
 assert api(f'repos/{SOURCE}/git/ref/heads/main')['object']['sha']==source_before,'Source main changed during publication'
 after=api(f'repos/{SOURCE}/pages')
 assert {k:after.get(k) for k in ['build_type','source','cname','html_url']}=={k:source_pages.get(k) for k in ['build_type','source','cname','html_url']},'Source Pages settings changed'
 return {'status':'publication requested; public URL verification still required','preview_url':EXPECTED_URL,'source_commit':metadata['source_commit'],'deployment_commit':deployment,'source_main_unchanged':source_before}

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--ref',default='origin/development/reconciliation')
 parser.add_argument('--create-repository',action='store_true')
 args=parser.parse_args()
 try:print(json.dumps(publish(args.ref,args.create_repository),indent=2))
 except (RuntimeError,ValueError) as error:raise SystemExit('Publication blocked: '+str(error))
