from airflow_dbt.hooks.dbt_hook import DbtCliHook
from airflow.models import BaseOperator


base_template_fields = [
    "profiles_dir",
    "target",
    "dir",
    "models",
    "exclude",
    "select",
    "selector",
    "debug",
    "dbt_bin",
    "verbose",
    "full_refresh",
    "data",
    "schema",
    "vars"
   
]

class DbtBaseOperator(BaseOperator):
    """
    Base dbt operator
    All other dbt operators are derived from this operator.

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
    :param verbose: The operator will log verbosely to the Airflow logs
    :type verbose: bool
    """


    template_fields = base_template_fields

    def __init__(self,
                 env=None,
                 profiles_dir=None,
                 target=None,
                 dir='.',
                 vars=None,
                 models=None,
                 exclude=None,
                 select=None,
                 selector=None,
                 debug=False,
                 dbt_bin='dbt',
                 verbose=True,
                 warn_error=False,
                 full_refresh=False,
                 data=False,
                 schema=False,
                 threads = None,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)

        self.env = env or {}
        self.profiles_dir = profiles_dir
        self.target = target
        self.dir = dir
        self.vars = vars
        self.models = models
        self.full_refresh = full_refresh
        self.data = data
        self.schema = schema
        self.exclude = exclude
        self.select = select
        self.selector = selector
        self.debug = debug 
        self.dbt_bin = dbt_bin
        self.verbose = verbose
        self.warn_error = warn_error
        self.hook = None
        self.threads = threads

    def create_hook(self, context):
        if self.hook  is None:
            self.hook = DbtCliHook(
                context = context,
                env=self.env,
                profiles_dir=self.profiles_dir,
                target=self.target,
                dir=self.dir,
                vars=self.vars,
                full_refresh=self.full_refresh,
                data=self.data,
                schema=self.schema,
                models=self.models,
                exclude=self.exclude,
                select=self.select,
                selector=self.selector,
                debug=self.debug,
                dbt_bin=self.dbt_bin,
                verbose=self.verbose,
                warn_error=self.warn_error)

        return self.hook


class DbtRunOperator(DbtBaseOperator):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)

    def execute(self, context):
        self.create_hook(context).run_cli('run')


class DbtTestOperator(DbtBaseOperator):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self, context):
        self.create_hook(context).run_cli('test')


class DbtDocsGenerateOperator(DbtBaseOperator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self, context):
        self.create_hook(context).run_cli('docs', 'generate')


class DbtSnapshotOperator(DbtBaseOperator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self, context):
        self.create_hook(context).run_cli('snapshot')


class DbtSeedOperator(DbtBaseOperator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self, context):
        self.create_hook(context).run_cli('seed')


class DbtDepsOperator(DbtBaseOperator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self, context):
        self.create_hook(context).run_cli('deps')


class DbtCleanOperator(DbtBaseOperator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self, context):
        self.create_hook(context).run_cli('clean')

class DbtCompileOperator(DbtBaseOperator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self, context):
        self.create_hook(context).run_cli('compile')


class DbtSourceFreshnessOperator(DbtBaseOperator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self, context):
        self.create_hook(context).run_cli('source freshness')