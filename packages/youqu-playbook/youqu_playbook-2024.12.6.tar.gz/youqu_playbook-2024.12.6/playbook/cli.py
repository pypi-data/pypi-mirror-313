import click

from playbook.__version__ import __version__ as version


@click.command()
@click.help_option("-h", "--help", help="查看帮助信息")
@click.version_option(version, "-v", "--version", prog_name="PlayBook", help="查看版本号")
@click.option("-p", "--input-json-path", required=True, type=click.Path(exists=True, dir_okay=False),
              help="PlayBook JSON 文件路径")
@click.option("--debug", is_flag=True, default=False, help="启用调试模式")
def cli(input_json_path: str, debug):
    from playbook.main import playbook
    playbook(input_json_path, debug)


if __name__ == '__main__':
    cli()
