#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

import sys
import os.path as osp
import os
local_repo=''
remote_repo='https://gitlab.com/ita1024/waf/raw/master/'
remote_locs=['waflib/extras','waflib/Tools']
try:
	from urllib import request
except ImportError:
	from urllib import urlopen
else:
	urlopen=request.urlopen
from waflib import Errors,Context,Logs,Utils,Options,Configure
try:
	from urllib.parse import urlparse
except ImportError:
	from urlparse import urlparse
DEFAULT_DIR='wafcfg'
sys.path.append(osp.abspath(DEFAULT_DIR))
def options(self):
	group=self.add_option_group('configure options')
	group.add_option('--download',dest='download',default=False,action='store_true',help='try to download the tools if missing')
	group.add_option('--use-config',action='store',default=None,metavar='CFG',dest='use_config',help='force the configuration parameters by importing ''CFG.py. Several modules may be provided (comma ''separated).')
	group.add_option('--use-config-dir',action='store',default=DEFAULT_DIR,metavar='CFG_DIR',dest='use_config_dir',help='path or url where to find the configuration file')
def download_check(node):
	pass
def download_tool(tool,force=False,ctx=None):
	for x in Utils.to_list(remote_repo):
		for sub in Utils.to_list(remote_locs):
			url='/'.join((x,sub,tool+'.py'))
			try:
				web=urlopen(url)
				try:
					if web.getcode()!=200:
						continue
				except AttributeError:
					pass
			except Exception:
				continue
			else:
				tmp=ctx.root.make_node(os.sep.join((Context.waf_dir,'waflib','extras',tool+'.py')))
				tmp.write(web.read(),'wb')
				Logs.warn('Downloaded %s from %s',tool,url)
				download_check(tmp)
				try:
					module=Context.load_tool(tool)
				except Exception:
					Logs.warn('The tool %s from %s is unusable',tool,url)
					try:
						tmp.delete()
					except Exception:
						pass
					continue
				return module
	raise Errors.WafError('Could not load the Waf tool')
def load_tool(tool,tooldir=None,ctx=None,with_sys_path=True):
	try:
		module=Context.load_tool_default(tool,tooldir,ctx,with_sys_path)
	except ImportError as e:
		if not ctx or not hasattr(Options.options,'download'):
			Logs.error('Could not load %r during options phase (download unavailable at this point)'%tool)
			raise
		if Options.options.download:
			module=download_tool(tool,ctx=ctx)
			if not module:
				ctx.fatal('Could not load the Waf tool %r or download a suitable replacement from the repository (sys.path %r)\n%s'%(tool,sys.path,e))
		else:
			ctx.fatal('Could not load the Waf tool %r from %r (try the --download option?):\n%s'%(tool,sys.path,e))
	return module
Context.load_tool_default=Context.load_tool
Context.load_tool=load_tool
Configure.download_tool=download_tool
def configure(self):
	opts=self.options
	use_cfg=opts.use_config
	if use_cfg is None:
		return
	url=urlparse(opts.use_config_dir)
	kwargs={}
	if url.scheme:
		kwargs['download']=True
		kwargs['remote_url']=url.geturl()
		kwargs['remote_locs']=['',DEFAULT_DIR]
	tooldir=url.geturl()+' '+DEFAULT_DIR
	for cfg in use_cfg.split(','):
		Logs.pprint('NORMAL',"Searching configuration '%s'..."%cfg)
		self.load(cfg,tooldir=tooldir,**kwargs)
	self.start_msg('Checking for configuration')
	self.end_msg(use_cfg)
