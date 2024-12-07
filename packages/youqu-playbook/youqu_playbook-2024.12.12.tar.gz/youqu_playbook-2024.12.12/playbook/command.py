import os

from funnylog2 import logger
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
            pms_user,
            pms_password,
            pms_task_id,
            is_debug,
            manages
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
        self.pms_user = pms_user
        self.pms_password = pms_password
        self.pms_task_id = pms_task_id
        self.only_one_client = True if len(self.clients) == 1 else False
        self.rootdir = app_name
        self.IS_DEBUG = is_debug
        self.manages = manages
        self.to_log = f'2>&1 | sed -r "s/\x1B\[([0-9]{{1,2}}(;[0-9]{{1,2}})?)?[mGK]//g" | tee {self.app_name}.log'
        
    def run_by_cmd(self, cmd):
        logger.debug(cmd)
        if self.IS_DEBUG:
            return
        os.system(cmd)

    def youqu2_command(self):
        if not self.IS_DEBUG:
            self.run_by_cmd(f"pip3 install -U youqu -i {config.PYPI_MIRROR}")
            self.run_by_cmd(f"rm -rf {self.rootdir}")
            self.run_by_cmd(f"youqu-startproject {self.rootdir}")
            self.run_by_cmd(f"cd {self.rootdir}/apps/;git clone {self.git_url} -b {self.git_branch} --depth 1")
            self.run_by_cmd(f"cd {self.rootdir} && bash env.sh")

        clients_cmd = f" --clients {'/'.join(self.clients)}"
        slaves_cmd = ""
        if self.app_name in config.SPECIAL_CLIENTS.keys():
            clients_cmd = f" --clients {config.SPECIAL_CLIENTS[self.app_name]}"
            slaves_cmd = f" --slaves {'/'.join(self.clients)}"
        if self.manages:
            clients_cmd = f" --clients {'/'.join(self.manages)}"
            slaves_cmd = f" --slaves {'/'.join(self.clients)}"

        tags_cmd = f" -t '{self.tags}'" if self.tags else ""
        pms_cmd = ""
        if self.pms_task_id:
            pms_cmd = f" --task_id {self.pms_task_id} -u {self.pms_user} -p {self.pms_password}"
        cmd = (
            f"cd {self.rootdir} && "
            f"youqu manage.py remote -a {self.app_name}{clients_cmd}{slaves_cmd}{tags_cmd}{pms_cmd} "
            f"--json_backfill_base_url {self.json_backfill_base_url} --json_backfill_task_id {self.task_id} "
            f"--json_backfill_user {self.json_backfill_user} --json_backfill_password {self.json_backfill_password} "
            f"{'' if self.only_one_client else '-y no '}-e "
            f"{self.to_log}"
        )
        return cmd

    def youqu3_command(self):
        if not self.IS_DEBUG:
            self.run_by_cmd(f"pip3 install -U youqu3 sendme pms-driver -i {config.PYPI_MIRROR}")
            self.run_by_cmd(f"rm -rf {self.rootdir}")
            self.run_by_cmd(f"git clone {self.git_url} {self.rootdir} -b {self.git_branch} --depth 1")
            self.run_by_cmd(f"cd {self.rootdir} && youqu3 envx")
        clients_cmd = f" --clients {'/'.join(self.clients)}"
        if not self.only_one_client:
            clients_cmd = f" --clients {'{' + '/'.join(self.clients) + '}'}"

        slaves_cmd = ""
        if self.app_name in config.SPECIAL_CLIENTS.keys():
            clients_cmd = f" --clients {config.SPECIAL_CLIENTS[self.app_name]}"
            slaves_cmd = f" --slaves {'/'.join(self.clients)}"
        elif self.manages:
            clients_cmd = f" --clients {'/'.join(self.manages)}"
            slaves_cmd = f" --slaves {'/'.join(self.clients)}"

        pms_start_cmd = ""
        pms_end_cmd = ""
        if self.pms_task_id:
            pms_start_cmd = f' --txt --job-start "pms-driver --task-id {self.pms_task_id} --pms-user {self.pms_user} --pms-password {self.pms_password}"'
            pms_end_cmd = f"pms-driver --task-id {self.pms_task_id} --pms-user {self.pms_user} --pms-password {self.pms_password} --send2pms;"

        tags_cmd = f" -t '{self.tags}'" if self.tags else ""
        cmd = (
            f"cd {self.rootdir} && "
            f'''youqu3-cargo remote -w {self.app_name}{clients_cmd}{slaves_cmd}{tags_cmd}'''
            f'{pms_start_cmd} '
            f'--job-end '
            f'"'
            f'{pms_end_cmd}'
            f'sendme --base-url {self.json_backfill_base_url} --task-id {self.task_id} --username {self.json_backfill_user} --password {self.json_backfill_password}'
            f'" '
            f"{self.to_log}"
        )
        return cmd
