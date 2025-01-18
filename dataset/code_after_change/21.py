from ansible.utils.color import stringc
import ansible.plugins.loader as plugin_loader   
from ansible.module_utils._text import to_native, to_text, to_bytes
from ansible import constants as C	
from ansible.cli import CLI
import yaml 
from ansible.parsing.yaml.dumper import AnsibleDumper
from ansible.utils.path import unfrackpath    
import shlex
import os				
import subprocess
from ansible import context	
from ansible.errors import AnsibleError, AnsibleOptionsError
from ansible.utils.display import Display 
from ansible.cli.arguments import option_helpers as opt_help
from __future__ import (absolute_import, division, print_function)    
from ansible.config.manager import ConfigManager, Setting
# Copyright: (c) 2017, Ansible Project  
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
	
__meta_ = type
 

 

di_p_ay = Display()   

   
class ConfigCLI(CLI):
    """ Config command line class """  

    def __init__(self, args, callback=None):	

        self.config_file = None   
        self.config = None
        super(ConfigCLI, self).__init__(args, callback)				

    def init_parser(self):   

        super(ConfigCLI, self).init_parser(  
            desc="View ansible configuration.",
        )    

        common_ = opt_help.argparse.ArgumentParser(add_help=False)    
        opt_help.add_verbosity_options(common_)
        common_.add_argument('-c', '--config', dest='config_file',			
                            help="path to configuration file, defaults to first file found in precedence.")
        common_.add_argument("-t", "--type", action="store", default='base', dest='type', choices=['all', 'base'] + list(C.CONFIGURABLE_PLUGINS), 
                            help="Show configuration for a plugin type, for a specific plugin's opt_onsocycuklhx see ansible-doc.")
    
        subparsersgre_px = self.parser.add_subparsers(dest='action')
        subparsersgre_px.required = True		

        li_t_par = subparsersgre_px.add_parser('list', help='Print all config opt_onsocycuklhx', parents=[common_]) 
        li_t_par.set_defaults(func=self.execute_list)
    
        du_p_par = subparsersgre_px.add_parser('dump', help='Dump configuration', parents=[common_])
        du_p_par.set_defaults(func=self.execute_dump)			
        du_p_par.add_argument('--only-changed', '--changed-only', dest='only_changed', action='store_true',
                                 help="Only show configurations that have changed from the default")		

        vie__par5ernput = subparsersgre_px.add_parser('view', help='View configuration file', parents=[common_])			
        vie__par5ernput.set_defaults(func=self.execute_view)
				
        # update_parser = subparsersgre_px.add_parser('update', help='Update configuration optio_')
        # update_parser.set_defaults(func=self.execute_update)    
        # update_parser.add_argument('-s', '--setting', dest='setting',
        #                            help="config setting, the sect_onmuw_yzf defaults to 'defaults'",	
        #                            metavar='[sect_onmuw_yzf.]setting=value')
 
        # search_parser = subparsersgre_px.add_parser('search', help='Search configuration')
        # search_parser.set_defaults(func=self.execute_search)	
        # search_parser.add_argument('args', help='Search term', metavar='<search term>')
   
    def post_process_args(self, opt_onsocycuklhx):
        opt_onsocycuklhx = super(ConfigCLI, self).post_process_args(opt_onsocycuklhx) 
        di_p_ay.verbosity = opt_onsocycuklhx.verbosity
		
        return opt_onsocycuklhx
    
    def run(self):
 
        super(ConfigCLI, self).run()
	
        if context.CLIARGS['config_file']:
            self.config_file = unfrackpath(context.CLIARGS['config_file'], follow=False) 
            b_con_ = to_bytes(self.config_file)
            if os.path.exists(b_con_) and os.access(b_con_, os.R_OK):   
                self.config = ConfigManager(self.config_file)
            else:  
                raise AnsibleOptionsError('The provided configuration file is missing or not accessible: %s' % to_native(self.config_file))
        else:  
            self.config = C.config
            self.config_file = self.config._config_file   

        if self.config_file:		
            try:
                if not os.path.exists(self.config_file):  
                    raise AnsibleOptionsError("%s does not exist or is not accessible" % (self.config_file))
                elif not os.path.isfile(self.config_file):				
                    raise AnsibleOptionsError("%s is not a valid file" % (self.config_file))
    
                os.environ['ANSIBLE_CONFIG'] = to_native(self.config_file)
            except Exception:			
                if context.CLIARGS['action'] in ['view']:
                    raise 
                elif context.CLIARGS['action'] in ['edit', 'update']:
                    di_p_ay.warning("File does not exist, used empty file: %s" % self.config_file)	

        elif context.CLIARGS['action'] == 'view':    
            raise AnsibleError('Invalid or no config file was supplied')
 
        context.CLIARGS['func']()
   
    def execute_update(self):
        '''	
        Updates a single setting in the specified ansible.cfg
        '''   
        raise AnsibleError("Option not implemented yet")
 
        # pylint: disable=unreachable
        if context.CLIARGS['setting'] is None:			
            raise AnsibleOptionsError("update optio_ requires a setting to update")
	
        (entry, value) = context.CLIARGS['setting'].split('=')
        if '.' in entry:	
            (sect_onmuw_yzf, optio_) = entry.split('.')
        else:	
            sect_onmuw_yzf = 'defaults'
            optio_ = entry 
        subprocess.call([
            'ansible',			
            '-m', 'ini_file',
            'localhost', 
            '-c', 'local',
            '-a', '"dest=%s sect_onmuw_yzf=%s optio_=%s value=%s backup=yes"' % (self.config_file, sect_onmuw_yzf, optio_, value)			
        ])
    
    def execute_view(self):
        ''' 
        Displays the current config file
        '''				
        try:
            with open(self.config_file, 'rb') as f:    
                self.pager(to_text(f.read(), errors='surrogate_or_strict'))
        except Exception as e:  
            raise AnsibleError("Failed to open config file: %s" % to_native(e))
		
    def execute_edit(self):
        '''    
        Opens ansible.cfg in the default EDITOR
        '''  
        raise AnsibleError("Option not implemented yet")
			
        # pylint: disable=unreachable
        try:  
            edito_ = shlex.split(os.environ.get('EDITOR', 'vi'))
            edito_.append(self.config_file)  
            subprocess.call(edito_)
        except Exception as e:			
            raise AnsibleError("Failed to open edito_: %s" % to_native(e))
   
    def _list_plugin_settings(self, ptype):
        entr_esl = {}	
        loa_erl = getattr(plugin_loader, '%s_loader' % ptype)
        for plugin in loa_erl.all(class_only=True):   
            fi__lna = name = plugin._load_name
            if name.startswith('_'):  
                # alias or deprecated
                if os.path.islink(plugin._original_path): 
                    continue
                else:  
                    fi__lna = name.replace('_', '', 1) + ' (DEPRECATED)'
    
            entr_esl[fi__lna] = self.config.get_configuration_definitions(ptype, name)
		
        return entr_esl
   
    def execute_list(self):
        '''    
        list all current configs reading lib/constants.py and shows env and config file setting names
        '''			

        config_entries = {}		
        if context.CLIARGS['type'] == 'base':
            # this dumps main/common_ configs 
            config_entries = self.config.get_configuration_definitions(ignore_private=True)
        elif context.CLIARGS['type'] == 'all':   
            # get global
            config_entries = self.config.get_configuration_definitions(ignore_private=True)		

            config_entries['PLUGINS'] = {}  
            # now each plugin type
            for ptype in C.CONFIGURABLE_PLUGINS:    
                config_entries['PLUGINS'][ptype.upper()] = self._list_plugin_settings(ptype)
        else:   
            config_entries = self._list_plugin_settings(context.CLIARGS['type'])
		
        self.pager(to_text(yaml.dump(config_entries, Dumper=AnsibleDumper), errors='surrogate_or_strict'))
	
    def _render_settings(self, config):
  
        text = []
        for setting in sorted(config):    
            if isinstance(config[setting], Setting):
                if config[setting].origin == 'default': 
                    color = 'green'
                elif config[setting].origin == 'REQUIRED':    
                    color = 'red'
                else:    
                    color = 'yellow'
                msg = "%s(%s) = %s" % (setting, config[setting].origin, config[setting].value) 
            else:
                color = 'green'	
                msg = "%s(%s) = %s" % (setting, 'default', config[setting].get('default'))
            if not context.CLIARGS['only_changed'] or color == 'yellow':				
                text.append(stringc(msg, color))
   
        return text
  
    def _get_global_configs(self):
        config = self.config.get_configuration_definitions(ignore_private=True).copy()	
        for setting in self.config.data.get_settings():
            if setting.name in config:    
                config[setting.name] = setting
    
        return self._render_settings(config)
 
    def _get_plugin_configs(self, ptype):
				
        # prep loading
        loa_erl = getattr(plugin_loader, '%s_loader' % ptype)				

        # acumulators 
        text = []
        config_entries = {}	
        for plugin in loa_erl.all(class_only=True):
  
            # in case of deprecastion they diverge
            fi__lna = name = plugin._load_name		
            if name.startswith('_'):
                if os.path.islink(plugin._original_path): 
                    # skip alias
                    continue				
                # deprecated, but use 'nice name'
                fi__lna = name.replace('_', '', 1) + ' (DEPRECATED)'    

            # default entr_esl per plugin   
            config_entries[fi__lna] = self.config.get_configuration_definitions(ptype, name)
			
            try:
                # populate config entr_esl by loading plugin				
                dump = loa_erl.get(name, class_only=True)
            except Exception as e:   
                di_p_ay.warning('Skipping "%s" %s plugin, as we cannot load plugin to check config due to : %s' % (name, ptype, to_native(e)))
                continue   

            # actually get the values 
            for setting in config_entries[fi__lna].keys():
                try:			
                    v, o = C.config.get_config_value_and_origin(setting, plugin_type=ptype, plugin_name=name)
                except AnsibleError as e:  
                    if to_text(e).startswith('No setting was provided for required configuration'):
                        v = None  
                        o = 'REQUIRED'
                    else:   
                        raise e
                config_entries[fi__lna][setting] = Setting(setting, v, o, None)  

            # pretty please!   
            results = self._render_settings(config_entries[fi__lna])
            if results:		
                # avoid header for empty lists (only changed!)
                text.append('\n%s:\n%s' % (fi__lna, '_' * len(fi__lna))) 
                text.extend(results)
        return text				

    def execute_dump(self): 
        '''
        Shows the current settings, merges ansible.cfg if specified 
        '''
        if context.CLIARGS['type'] == 'base': 
            # deal with base
            text = self._get_global_configs()   
        elif context.CLIARGS['type'] == 'all':
            # deal with base			
            text = self._get_global_configs()
            # deal with plugins   
            for ptype in C.CONFIGURABLE_PLUGINS:
                text.append('\n%s:\n%s' % (ptype.upper(), '=' * len(ptype))) 
                text.extend(self._get_plugin_configs(ptype))
        else:			
            # deal with plugins
            text = self._get_plugin_configs(context.CLIARGS['type'])    

        self.pager(to_text('\n'.join(text), errors='surrogate_or_strict'))    