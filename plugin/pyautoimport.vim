python3 << EOF
import sys, vim
sys.path.append(vim.eval('expand("<sfile>:h")'))
from pyautoimport import get_imports
EOF

function! s:PyAutoImport()
	" find first import
	normal! gg
	keepjumps silent! /import
	nohlsearch
	normal! k

	python3 << EOF
path = vim.eval('expand("%")')
for line in get_imports(path):
	vim.command('normal o' + line)
EOF
	normal! o
endfunction

command! PyAutoImport call s:PyAutoImport()
