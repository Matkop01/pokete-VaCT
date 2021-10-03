#!/usr/bin/env python
import os
import sys

if __name__ != '__main__':
    sys.exit(1)


def replace_tables(_text: str) -> str:
    out = ''
    table = ''
    in_table = False
    for line in _text.split('\n'):
        if '|' in line:
            in_table = True
            table += line
            table += '\n'
            #print(line)
        else:
            if in_table:
                in_table = False
                #md_text = markdown.markdown(table)
                with open('/tmp/pandoc_convert.md', 'w') as _f:
                    _f.write(table)
                os.system('pandoc /tmp/pandoc_convert.md -o /tmp/pandoc_convert.html')
                with open('/tmp/pandoc_convert.html', 'r') as _f:
                    md_text = _f.read()
                table = ''
                out += md_text
                out += '\n'
            else:
                out += line
                out += '\n'
    return out


def replace_code_blocks(_text: str) -> str:
    out = ''
    in_code = False
    for line in _text.split('\n'):
        if line == '```':
            if in_code:
                out += r'{% endhighlight %}{% endraw %}'
            else:
                out += r'{% highlight %}{% raw %}'
            in_code = not in_code
        else:
            out += line
        out += '\n'
    return out


files = ['wiki.md', 'README.md', 'Changelog.md', 'HowToPlay.md']
#files = ['README.md']

for file in files:
    with open(file, 'r') as f:
        text = f.read()
        text = replace_tables(text)
        text = replace_code_blocks(text)
        #file.write(text)
        print(text)
    with open(file, 'w') as f:
        f.write(text)