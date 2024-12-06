import os
from playbook.config import config


class Command:

    def __init__(
            self,
            app_name,
            clients,
            tags,
            task_id,
            git_url,
            git_branch,
            json_backfill_base_url,
            json_backfill_user,
            json_backfill_password,
            is_debug,
    ):
        self.app_name = app_name
        self.clients = clients
        self.tags = tags
        self.task_id = task_id
        self.git_url = git_url
        self.git_branch = git_branch
        self.json_backfill_base_url = json_backfill_base_url
        self.json_backfill_user = json_backfill_user
        self.json_backfill_password = json_backfill_password
        self.only_one_client = True if len(self.clients) == 1 else False
        self.rootdir = app_name
        self.IS_DEBUG = is_debug

    def youqu2_command(self):
        if not self.IS_DEBUG:
            os.chdir(config.WORKDIR)
            os.system(f"pip3 install -U youqu -i {config.PYPI_MIRROR}")
            os.system(f"rm -rf {self.rootdir}")
            os.system(f"youqu-startproject {self.rootdir}")
            os.system(f"cd {self.rootdir}/apps/;git clone {self.git_url} -b {self.git_branch} --depth 1")
            os.chdir(self.rootdir)
            os.system(f"bash env.sh")
        cmd = (
            f"youqu manage.py remote -a {self.app_name} -c {'/'.join(self.clients)} -t '{self.tags}' "
            f"--json_backfill_base_url {self.json_backfill_base_url} --json_backfill_task_id {self.task_id} "
            f"--json_backfill_user {self.json_backfill_user} --json_backfill_password {self.json_backfill_password} "
            f"{'' if self.only_one_client else '-y no '}-e "
            f"2>&1 | stdbuf -o0 perl -pe 's/\e\[?.*?[\@-~]//g' | stdbuf -o0 tee {self.app_name}.log"
        )
        return cmd

    def youqu3_command(self):
        if not self.IS_DEBUG:
            os.chdir(config.WORKDIR)
            os.system(f"pip3 install -U youqu3 sendme -i {config.PYPI_MIRROR}")
            os.system(f"rm -rf {self.rootdir}")
            os.system(f"git clone {self.git_url} {self.rootdir} -b {self.git_branch} --depth 1")
            os.chdir(self.rootdir)
            os.system("youqu3 envx")
        cs = '/'.join(self.clients)
        if not self.only_one_client:
            cs = "{" + cs + "}"
        cmd = (
            f'''youqu3-cargo remote -w {self.app_name} -c {cs} -t "{self.tags}" '''
            f'--job-end "sendme --base-url {self.json_backfill_base_url} --task-id {self.task_id} '
            f'--username {self.json_backfill_user} --password {self.json_backfill_password}" '
            f"2>&1 | stdbuf -o0 perl -pe 's/\e\[?.*?[\@-~]//g' | stdbuf -o0 tee {self.app_name}.log"
        )
        return cmd
