#!/usr/bin/env python
################################################################
import BlackDynamite as BD
import re
import transaction
from traitlets.config import get_config
from IPython import embed
import ZODB
import ZODB.FileStorage
################################################################


class Command:

    def __init__(self, cmd):
        self.cmd = cmd

    def __repr__(self):
        return self.cmd()


def make_command(func):
    return Command(func)


@make_command
def commit():
    transaction.commit()
    return ""


################################################################
def getSchemasUser(study_name, schemas):
    for s in schemas:
        m = re.match(f'(.+)_{study_name}', s)
        if m:
            return m.group(1)
    raise RuntimeError(
        f"not found study: '{study_name}' within {[e for e in schemas]}")

################################################################


def retreiveSchemaName(study, schemas):
    # Need this because getSchemaList strips prefix
    match = re.match('(.+)_(.+)', study)
    study_name = None
    if match:
        schema = study
    else:
        schema = getSchemasUser(study, schemas) + '_' + study

    if schema not in schemas:
        raise RuntimeError(
            f"Study name '{study_name}' invalid: "
            f"possibilities are {schemas}")
    return schema


def main(argv=None):
    parser = BD.bdparser.BDParser()
    params = parser.parseBDParameters(argv)
    storage = ZODB.FileStorage.FileStorage(
        '.bd/bd.zeo', blob_dir='.bd/blob_data')
    db = ZODB.DB(storage)
    connection = db.open()
    root = connection.root

    globals()['db'] = db
    globals()['connection'] = connection
    globals()['root'] = root

    access_info = """
Your database is accessible as the object 'db'.
Your root is accessible in the object 'root'.
"""

    if 'study' in params:
        schema = retreiveSchemaName(params['study'], root.schemas)
        study = root.schemas[schema]
        globals()['study'] = study
        access_info += "Your study is accessible as the object 'study'"

    c = get_config()
    c.InteractiveShellEmbed.colors = "Linux"

    embed(config=c, banner1=f"""
    {access_info}

For any changes you do you should hit 'commit' to make them permanent
""")

################################################################


if __name__ == '__main__':
    main()
