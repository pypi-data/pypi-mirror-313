from __future__ import print_function
import os
import signal
import subprocess
import json
import re
from airflow.exceptions import AirflowException
from airflow.hooks.base_hook import BaseHook
from airflow.utils.operator_helpers import context_to_airflow_vars




def remove_ansi_escape_codes(text):
    """
    移除字符串中的 ANSI 转义码。
    
    :param text: 包含 ANSI 转义码的字符串
    :return: 不包含 ANSI 转义码的字符串
    """
    ansi_escape_pattern = r'\x1B[@-_][0-?]*[ -/]*[@-~]'
    # 使用 re.compile 编译正则表达式以提高效率
    ansi_escape_re = re.compile(ansi_escape_pattern)
    return ansi_escape_re.sub('', text)


class DbtCliHook(BaseHook):
    """
    Simple wrapper around the dbt CLI.

    :param env: If set, passes the env variables to the subprocess handler
    :type env: dict
    :param profiles_dir: If set, passed as the `--profiles-dir` argument to the `dbt` command
    :type profiles_dir: str
    :param target: If set, passed as the `--target` argument to the `dbt` command
    :type dir: str
    :param dir: The directory to run the CLI in
    :type vars: str
    :param vars: If set, passed as the `--vars` argument to the `dbt` command
    :type vars: dict
    :param full_refresh: If `True`, will fully-refresh incremental models.
    :type full_refresh: bool
    :param models: If set, passed as the `--models` argument to the `dbt` command
    :type models: str
    :param warn_error: If `True`, treat warnings as errors.
    :type warn_error: bool
    :param exclude: If set, passed as the `--exclude` argument to the `dbt` command
    :type exclude: str
    :param select: If set, passed as the `--select` argument to the `dbt` command
    :type select: str
    :param selector: If set, passed as the `--selector` argument to the `dbt` command
    :type selector: str
    :param debug: If set, passed as the `--debug` argument to the `dbt` command
    :type debug: str
    :param dbt_bin: The `dbt` CLI. Defaults to `dbt`, so assumes it's on your `PATH`
    :type dbt_bin: str
    :param output_encoding: Output encoding of bash command. Defaults to utf-8
    :type output_encoding: str
    :param verbose: The operator will log verbosely to the Airflow logs
    :type verbose: bool
    """

    def __init__(self,
                 context = None,
                 env=None,
                 profiles_dir=None,
                 target=None,
                 dir='.',
                 vars=None,
                 full_refresh=False,
                 data=False,
                 schema=False,
                 models=None,
                 exclude=None,
                 select=None,
                 selector=None,
                 debug=False,
                 dbt_bin='dbt',
                 output_encoding='utf-8',
                 verbose=True,
                 warn_error=False,
                 append_env = False,
                 threads = None
                 ):
        super().__init__()


        self.context = context
        self.env = env or {} 
        self.profiles_dir = profiles_dir
        self.dir = dir
        self.target = target
        self.vars = vars
        self.full_refresh = full_refresh
        self.data = data
        self.schema = schema
        self.models = models
        self.exclude = exclude
        self.select = select
        self.selector = selector
        self.debug = debug  
        self.dbt_bin = dbt_bin
        self.verbose = verbose
        self.warn_error = warn_error
        self.output_encoding = output_encoding
        self.append_env = append_env
        self.threads = threads
        

    def get_env(self, context, env ):
        """Build the set of environment variables to be exposed for the bash command."""
        system_env = os.environ.copy()
         
        if env is None:
            env = system_env
        else:
            if self.append_env:
                system_env.update(env)
                env = system_env

        airflow_context_vars = context_to_airflow_vars(context, in_env_var_format=True)
        self.log.debug(
            "Exporting env vars: %s",
            " ".join(f"{k}={v!r}" for k, v in airflow_context_vars.items()),
        )
        env.update(airflow_context_vars)
        # for dbt_airflow_macros
        if "AIRFLOW_CTX_EXECUTION_DATE" in airflow_context_vars: 
            env["EXECUTION_DATE"] =  airflow_context_vars["AIRFLOW_CTX_EXECUTION_DATE"];

        return env
    
    def _dump_vars(self):
        # The dbt `vars` parameter is defined using YAML. Unfortunately the standard YAML library
        # for Python isn't very good and I couldn't find an easy way to have it formatted
        # correctly. However, as YAML is a super-set of JSON, this works just fine.
        return json.dumps(self.vars)

    def run_cli(self, *command):
        """
        Run the dbt cli

        :param command: The dbt command to run
        :type command: str
        """

        dbt_cmd = [self.dbt_bin, '--log-format','json',*command]

        if self.profiles_dir is not None:
            dbt_cmd.extend(['--profiles-dir', self.profiles_dir])
        
        if self.dir is not None:
            dbt_cmd.extend(['--project-dir', self.dir])


        if self.target is not None:
            dbt_cmd.extend(['--target', self.target])

        if self.vars is not None:
            dbt_cmd.extend(['--vars', self._dump_vars()])

        if self.data:
            dbt_cmd.extend(['--data'])

        if self.schema:
            dbt_cmd.extend(['--schema'])

        if self.models is not None:
            dbt_cmd.extend(['--models', self.models])

        if self.exclude is not None:
            dbt_cmd.extend(['--exclude', self.exclude])

        if self.select is not None:
            dbt_cmd.extend(['--select', self.select])

        if self.selector is not None:
            dbt_cmd.extend(['--selector', self.selector])

        if self.threads:
            dbt_cmd.extend(['--threads', self.threads])

        if self.debug:
            dbt_cmd.extend(['--debug'])

        if self.full_refresh:
            dbt_cmd.extend(['--full-refresh'])


        if self.warn_error:
            dbt_cmd.insert(1, '--warn-error')


        if self.verbose:
            self.log.info(" ".join(dbt_cmd))
        
        sub_env = self.get_env(self.context, self.env)
        self.log.info(f"subprocess env: {sub_env}")
        sp = subprocess.Popen(
            dbt_cmd,
            env=sub_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=self.dir,
            close_fds=True)
        
        self.sp = sp
        
        line = ''
        for line in iter(sp.stdout.readline, b''):
            line = line.decode(self.output_encoding).rstrip()
            try:
                json_line = json.loads(line)
            except json.JSONDecodeError:
                self.log.error(line.rstrip())
                pass
            else:
                json_info =  json_line["info"]
                json_data =  json_line["data"]
                logfunc_map =  {
                    "debug": self.log.debug,
                    "info": self.log.info,
                    "error": self.log.error,
                    "warn": self.log.warning
                }
                log_level = json_info["level"]
                conn_name = json_data.get("conn_name","")

                 
                node_path = json_data.get("node_info").get("node_path","")  if json_data.get("node_info") else ''  
                sql = json_data.get("sql","")
                msg = remove_ansi_escape_codes(json_info.get("msg", line.rstrip()))
                
                output_msg = f"conn_name: { conn_name },node_path: { node_path } ,sql: {sql}"
                self.log.debug(output_msg)

                if logfunc_map.get(log_level):     
                    logfunc_map.get(log_level)(msg)

            
        sp.wait()

        self.sp = None
        self.log.info(
            "Command exited with return code %s",
            sp.returncode
        )

        if sp.returncode:
            raise AirflowException("dbt command failed")

        return line 

    def on_kill(self):
        self.log.info('Sending SIGTERM signal to dbt command')    
        if self.sp:
            os.killpg(os.getpgid(self.sp.pid), signal.SIGTERM)