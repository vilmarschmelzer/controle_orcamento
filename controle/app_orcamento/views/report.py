from subprocess import call, PIPE
from os import remove
from os.path import dirname
from tempfile import NamedTemporaryFile


def pdflatex(file, type='pdf'):
    call(['pdflatex', '-interaction=nonstopmode',
                      '-output-format', type, file],
         cwd=dirname(file), stdout=PIPE, stderr=PIPE)

def process_latex(source, type='pdf', outfile=None):
    
    tex = NamedTemporaryFile()
    tex.write(source.encode('utf-8'))
    tex.flush()
    base = tex.name
    items = "log aux pdf dvi png".split()
    names = dict((x, '%s.%s' % (base, x)) for x in items)
    output = names[type]

    if type == 'pdf' or type == 'dvi':
        pdflatex(base, type)
    elif type == 'png':
        pdflatex(base, 'dvi')
        call(['dvipng', '-bg', '-transparent',
              names['dvi'], '-o', names['png']],
              cwd=dirname(base), stdout=PIPE, stderr=PIPE)

    remove(names['log'])
    remove(names['aux'])

    o = file(output).read()
    remove(output)
    if not outfile:
        return o
    else:
        outfile.write(o)
