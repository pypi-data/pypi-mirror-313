from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/aaa-accounting.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_aaa_accounting = resolve('aaa_accounting')
    l_0_exec_console_cli = resolve('exec_console_cli')
    l_0_exec_default_cli = resolve('exec_default_cli')
    try:
        t_1 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_1((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting)):
        pass
        if t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'exec'), 'console'), 'type'), 'none'):
            pass
            yield 'aaa accounting exec console none\n'
        elif (t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'exec'), 'console'), 'type')) and (t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'exec'), 'console'), 'group')) or t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'exec'), 'console'), 'logging'), True))):
            pass
            l_0_exec_console_cli = str_join(('aaa accounting exec console ', environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'exec'), 'console'), 'type'), ))
            context.vars['exec_console_cli'] = l_0_exec_console_cli
            context.exported_vars.add('exec_console_cli')
            if t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'exec'), 'console'), 'group')):
                pass
                l_0_exec_console_cli = str_join(((undefined(name='exec_console_cli') if l_0_exec_console_cli is missing else l_0_exec_console_cli), ' group ', environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'exec'), 'console'), 'group'), ))
                context.vars['exec_console_cli'] = l_0_exec_console_cli
                context.exported_vars.add('exec_console_cli')
            if t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'exec'), 'console'), 'logging'), True):
                pass
                l_0_exec_console_cli = str_join(((undefined(name='exec_console_cli') if l_0_exec_console_cli is missing else l_0_exec_console_cli), ' logging', ))
                context.vars['exec_console_cli'] = l_0_exec_console_cli
                context.exported_vars.add('exec_console_cli')
            yield str((undefined(name='exec_console_cli') if l_0_exec_console_cli is missing else l_0_exec_console_cli))
            yield '\n'
        if t_1(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'commands'), 'console')):
            pass
            for l_1_command_default in environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'commands'), 'console'):
                l_1_commands_console_cli = resolve('commands_console_cli')
                _loop_vars = {}
                pass
                if (t_1(environment.getattr(l_1_command_default, 'commands')) and t_1(environment.getattr(l_1_command_default, 'type'))):
                    pass
                    if t_1(environment.getattr(l_1_command_default, 'type'), 'none'):
                        pass
                        yield 'aaa accounting commands '
                        yield str(environment.getattr(l_1_command_default, 'commands'))
                        yield ' console none\n'
                    elif (t_1(environment.getattr(l_1_command_default, 'group')) or t_1(environment.getattr(l_1_command_default, 'logging'), True)):
                        pass
                        l_1_commands_console_cli = str_join(('aaa accounting commands ', environment.getattr(l_1_command_default, 'commands'), ' console ', environment.getattr(l_1_command_default, 'type'), ))
                        _loop_vars['commands_console_cli'] = l_1_commands_console_cli
                        if t_1(environment.getattr(l_1_command_default, 'group')):
                            pass
                            l_1_commands_console_cli = str_join(((undefined(name='commands_console_cli') if l_1_commands_console_cli is missing else l_1_commands_console_cli), ' group ', environment.getattr(l_1_command_default, 'group'), ))
                            _loop_vars['commands_console_cli'] = l_1_commands_console_cli
                        if t_1(environment.getattr(l_1_command_default, 'logging'), True):
                            pass
                            l_1_commands_console_cli = str_join(((undefined(name='commands_console_cli') if l_1_commands_console_cli is missing else l_1_commands_console_cli), ' logging', ))
                            _loop_vars['commands_console_cli'] = l_1_commands_console_cli
                        yield str((undefined(name='commands_console_cli') if l_1_commands_console_cli is missing else l_1_commands_console_cli))
                        yield '\n'
            l_1_command_default = l_1_commands_console_cli = missing
        if t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'exec'), 'default'), 'type'), 'none'):
            pass
            yield 'aaa accounting exec default none\n'
        elif (t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'exec'), 'default'), 'type')) and (t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'exec'), 'default'), 'group')) or t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'exec'), 'default'), 'logging'), True))):
            pass
            l_0_exec_default_cli = str_join(('aaa accounting exec default ', environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'exec'), 'default'), 'type'), ))
            context.vars['exec_default_cli'] = l_0_exec_default_cli
            context.exported_vars.add('exec_default_cli')
            if t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'exec'), 'default'), 'group')):
                pass
                l_0_exec_default_cli = str_join(((undefined(name='exec_default_cli') if l_0_exec_default_cli is missing else l_0_exec_default_cli), ' group ', environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'exec'), 'default'), 'group'), ))
                context.vars['exec_default_cli'] = l_0_exec_default_cli
                context.exported_vars.add('exec_default_cli')
            if t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'exec'), 'default'), 'logging'), True):
                pass
                l_0_exec_default_cli = str_join(((undefined(name='exec_default_cli') if l_0_exec_default_cli is missing else l_0_exec_default_cli), ' logging', ))
                context.vars['exec_default_cli'] = l_0_exec_default_cli
                context.exported_vars.add('exec_default_cli')
            yield str((undefined(name='exec_default_cli') if l_0_exec_default_cli is missing else l_0_exec_default_cli))
            yield '\n'
        if (t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'system'), 'default'), 'type')) and t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'system'), 'default'), 'group'))):
            pass
            yield 'aaa accounting system default '
            yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'system'), 'default'), 'type'))
            yield ' group '
            yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'system'), 'default'), 'group'))
            yield '\n'
        if (t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'dot1x'), 'default'), 'type')) and t_1(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'dot1x'), 'default'), 'group'))):
            pass
            yield 'aaa accounting dot1x default '
            yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'dot1x'), 'default'), 'type'))
            yield ' group '
            yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'dot1x'), 'default'), 'group'))
            yield '\n'
        if t_1(environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'commands'), 'default')):
            pass
            for l_1_command_default in environment.getattr(environment.getattr((undefined(name='aaa_accounting') if l_0_aaa_accounting is missing else l_0_aaa_accounting), 'commands'), 'default'):
                l_1_commands_default_cli = resolve('commands_default_cli')
                _loop_vars = {}
                pass
                if (t_1(environment.getattr(l_1_command_default, 'commands')) and t_1(environment.getattr(l_1_command_default, 'type'))):
                    pass
                    if t_1(environment.getattr(l_1_command_default, 'type'), 'none'):
                        pass
                        yield 'aaa accounting commands '
                        yield str(environment.getattr(l_1_command_default, 'commands'))
                        yield ' default none\n'
                    elif (t_1(environment.getattr(l_1_command_default, 'group')) or t_1(environment.getattr(l_1_command_default, 'logging'), True)):
                        pass
                        l_1_commands_default_cli = str_join(('aaa accounting commands ', environment.getattr(l_1_command_default, 'commands'), ' default ', environment.getattr(l_1_command_default, 'type'), ))
                        _loop_vars['commands_default_cli'] = l_1_commands_default_cli
                        if t_1(environment.getattr(l_1_command_default, 'group')):
                            pass
                            l_1_commands_default_cli = str_join(((undefined(name='commands_default_cli') if l_1_commands_default_cli is missing else l_1_commands_default_cli), ' group ', environment.getattr(l_1_command_default, 'group'), ))
                            _loop_vars['commands_default_cli'] = l_1_commands_default_cli
                        if t_1(environment.getattr(l_1_command_default, 'logging'), True):
                            pass
                            l_1_commands_default_cli = str_join(((undefined(name='commands_default_cli') if l_1_commands_default_cli is missing else l_1_commands_default_cli), ' logging', ))
                            _loop_vars['commands_default_cli'] = l_1_commands_default_cli
                        yield str((undefined(name='commands_default_cli') if l_1_commands_default_cli is missing else l_1_commands_default_cli))
                        yield '\n'
            l_1_command_default = l_1_commands_default_cli = missing

blocks = {}
debug_info = '7=20&8=22&10=25&11=27&12=30&13=32&15=35&16=37&18=40&20=42&21=44&22=48&23=50&24=53&25=55&26=57&27=59&28=61&30=63&31=65&33=67&38=70&40=73&41=75&42=78&43=80&45=83&46=85&48=88&50=90&51=93&53=97&54=100&56=104&57=106&58=110&59=112&60=115&61=117&62=119&63=121&64=123&66=125&67=127&69=129'