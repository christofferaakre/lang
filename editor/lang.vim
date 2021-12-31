" Place this file in your vim syntax directory,
" For example ~/.vim/syntax
" Then add the following in your vimrc:
" au BufRead,BufNewFile *.lang set filetype=lang
       " autocmd FileType lang              let b:comment_leader = '#'

if exists("b:current_syntax")
    finish
endif

syntax match numbers "\<[0-9]\+\>"
syntax match vars /^\$.\+\s/
syntax match popVars /pop:.*\s/
" todos
syntax keyword todos TODO FIXME NOTE

" comments
syntax region commentLine start="#" end="\n" contains=langTodos

syntax keyword keywords if else while end exit

highlight default link numbers Number
highlight default link vars Identifier
highlight default link popVars Identifier
highlight default link todos Todo
highlight default link keywords Keyword
highlight default link commentLine Comment

let b:current_syntax = "lang"
