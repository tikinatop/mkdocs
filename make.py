import os
import io

# TODO
    # - Sanitizer l'input os.path.splitext sous une fonction qui changera les noms etc, etc...
    # - Réfactorer x1000

CURDIR=os.getcwd()
DOCSDIR=os.path.join(CURDIR, "docs")
YAML_PROJECT_EDIT=os.path.join(CURDIR, "to_modify.yml")
YAML_MAIN_FILE=os.path.join(CURDIR, "mkdocs.yml")
WELCOME_PAGE='Accueil'

exclude='assets'

def list_files(startpath):
    payload=''
    for root, dirs, files in os.walk(startpath, topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude]
        files[:] = [f for f in files if f.endswith(".md")]
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 2 * (level) + '- '
        subindent = ' ' * 2 * (level + 1) + '- '
        basedir = os.path.basename(root)
        for d in dirs:
        	target = os.path.join(startpath, unix_path(root.split(startpath)[1])[1:], d, 'index.md')
        	if os.path.isfile(target) is not True:
        		print(target + ' does not exist').decode('utf-8')
        		open(target, 'a').close()
        if root == startpath:
            payload+='pages: \n{}\'{}\': \'{}\'\n'.format(subindent, WELCOME_PAGE, 'index.md')
        else:
            payload+='{}\'{}\': \n{}\'{}{}\'\n'.format(indent, basedir, subindent, unix_path(root.split(startpath)[1])[1:], '/index.md')
        for f in files:
            if root == startpath and f!='index.md':
                payload+='{}\'{}\': \'{}\'\n'.format(subindent, os.path.splitext(f)[0], f)
            elif root!=startpath:
                payload+='{}\'{}\': \'{}/{}\'\n'.format(subindent, os.path.splitext(f)[0], unix_path(root.split(startpath)[1])[1:], f)
    return payload


def unix_path(path):
    return path.replace('\\', '/')

filetree = list_files(DOCSDIR).decode('utf-8')

with io.open(YAML_MAIN_FILE, 'w', encoding='utf-8') as fout:
    with io.open(YAML_PROJECT_EDIT, 'r', encoding='utf-8') as fin:
        for line in fin:
            fout.write(unicode(line))
        fout.write(unicode(filetree))
