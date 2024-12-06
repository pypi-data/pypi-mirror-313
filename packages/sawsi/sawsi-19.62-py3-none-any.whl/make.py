import click
import os
import shutil
from pathlib import Path

# 현재 파일의 Path 객체
current_file_path = Path(__file__)

# sawsi_boilerplate 파일이 위치한 디렉토리
boilerplate_dir = current_file_path.parent / 'sawsi_boilerplate'


@click.group()
def cli():
    pass

@cli.command()
@click.argument('project')
@click.argument('app')
@click.option('-t', '--trigger', default='agw', help='AWS Trigger option. (agw: API Gateway, sqs: Simple Queue Service, ebs: Event Bridge Scheduler)')
def init(project, app, trigger):
    # 현재 작업 디렉토리를 기준으로 앱 디렉토리 생성
    project_path = Path(os.getcwd())
    project_path.mkdir(parents=True, exist_ok=True)

    # 기본 파일 구조 생성
    create_base_dir(app, project_path, project)

    # 앱 구조 생성
    create_app_dir(app, project_path, trigger)

    click.echo(f"{project} > App {project} has been created in {project_path}")


@cli.command()
@click.argument('app')
@click.option('-t', '--trigger', default='agw', help='AWS Trigger option. (agw: API Gateway, sqs: Simple Queue Service, ebs: Event Bridge Scheduler)')
def add(app, trigger):
    # 현재 작업 디렉토리를 기준으로 앱 디렉토리 생성
    project_path = Path(os.getcwd())
    project_path.mkdir(parents=True, exist_ok=True)

    # 앱 구조 생성
    create_app_dir(app, project_path, trigger)

    click.echo(f"App {app} has been created in {project_path}")


def create_base_dir(app_name, project_path, project_name):
    target_files = [
        'api.py',
        'errs.py',
        'requirements.txt',
        'buildspec-dev.yml',
        'buildspec-prod.yml',
        'aws_iam_policy_dev.json',
        'aws_iam_policy_prod.json',
        'build_keeper.py',
        'config.py',
        'README.md',
    ]
    for target_file in target_files:
        if isinstance(target_file, str):
            source_file = boilerplate_dir / target_file
            copy_without_overwrite(source_file, project_path)
            click.echo(f"Created: {project_path}")
        elif isinstance(target_file, tuple):
            target_file = target_file[0]
            rename_to = target_file[1]
            source_file = boilerplate_dir / target_file
            copy_without_overwrite(source_file, project_path / rename_to)
            click.echo(f"Created: {project_path}")

    # {{app}} 문자열 치환
    files_contain_app_literal = ['buildspec-dev.yml', 'buildspec-prod.yml', 'build_keeper.py']
    for file in files_contain_app_literal:
        replace_app(project_path / file, app_name)

    # {{project}} 문자열 치환
    files_contain_project_literal = [
        'buildspec-dev.yml', 'buildspec-prod.yml', 'api.py',
        'aws_iam_policy_dev.json', 'aws_iam_policy_prod.json',
    ]
    for file in files_contain_project_literal:
        replace_project(project_path / file, project_name)


def create_app_dir(app_name, project_path, trigger='agw'):
    source_dir = boilerplate_dir / 'app'
    destination_dir = project_path / app_name

    # 대상 디렉토리가 이미 존재하는 경우에도 복사를 수행
    try:
        shutil.copytree(source_dir, destination_dir, dirs_exist_ok=False)
    except Exception as ex:
        print(ex)
    # {{app}} 수정
    replace_app(destination_dir / 'controller' / 'sample_login.py', app_name)
    replace_app(destination_dir / 'doc_maker.py', app_name)
    replace_app(destination_dir / 'aws_handler.py', app_name)

def replace_app(target_file, app_name):
    replace_word(target_file, '{{app}}', app_name)

def replace_project(target_file, project_name):
    replace_word(target_file, '{{project}}', project_name)

def replace_word(target_file, word, replacement):
    rfp = open(target_file, 'r')
    text = rfp.read()
    text = text.replace(word, replacement)
    rfp.close()

    wfp = open(target_file, 'w+')
    wfp.write(text)


def copy_without_overwrite(source, destination):
    """
    shutil.copy와 유사하게 파일을 복사하지만, 대상 파일이 이미 존재하는 경우 복사를 수행하지 않습니다.

    :param source: 복사할 소스 파일의 경로입니다.
    :param destination: 파일을 복사할 대상 경로입니다. 파일 이름을 포함할 수도 있고, 디렉토리만을 지정할 수도 있습니다.
    :return: 복사가 성공적으로 수행되었으면 True를, 이미 파일이 존재하여 복사하지 않았으면 False를 반환합니다.
    """
    # destination이 디렉토리인 경우, 동일한 파일 이름으로 설정
    if os.path.isdir(destination):
        destination = os.path.join(destination, os.path.basename(source))

    # 대상 파일이 이미 존재하는지 확인
    if os.path.exists(destination):
        return False
    else:
        shutil.copy(source, destination)
        print(f'Created: {destination}')
        return True



if __name__ == '__main__':
    cli()