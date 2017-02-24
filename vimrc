set paste
set tabstop=4
set softtabstop=0
set expandtab
set shiftwidth=4
set smarttab


" theme 
hi Pmenu           ctermfg=81  ctermbg=16
hi PmenuSel        ctermfg=255 ctermbg=242
hi PmenuSbar                   ctermbg=232
hi PmenuThumb      ctermfg=81

hi PreCondit       ctermfg=118               cterm=bold
hi PreProc         ctermfg=118
hi Question        ctermfg=81
hi Repeat          ctermfg=161               cterm=bold
hi Search          ctermfg=0   ctermbg=222   cterm=NONE


hi SignColumn      ctermfg=118 ctermbg=235
hi SpecialChar     ctermfg=161               cterm=bold
hi SpecialComment  ctermfg=245               cterm=bold
hi Special         ctermfg=81
if has("spell")
  hi SpellBad                ctermbg=52
  hi SpellCap                ctermbg=17
  hi SpellLocal              ctermbg=17
  hi SpellRare  ctermfg=none ctermbg=none  cterm=reverse
endif

hi Normal       ctermfg=252 ctermbg=234
hi CursorLine               ctermbg=236   cterm=none
hi CursorLineNr ctermfg=208               cterm=none

hi Boolean         ctermfg=141
hi Character       ctermfg=222
hi Number          ctermfg=141
hi String          ctermfg=222
hi Conditional     ctermfg=197               cterm=bold
hi Constant        ctermfg=141               cterm=bold

hi DiffDelete      ctermfg=125 ctermbg=233

hi Directory       ctermfg=154               cterm=bold
hi Error           ctermfg=222 ctermbg=233
hi Exception       ctermfg=154               cterm=bold
hi Float           ctermfg=141
hi Function        ctermfg=154
hi Identifier      ctermfg=208

hi Keyword         ctermfg=197               cterm=bold
hi Operator        ctermfg=197
hi PreCondit       ctermfg=154               cterm=bold
hi PreProc         ctermfg=154
hi Repeat          ctermfg=197               cterm=bold

hi Statement       ctermfg=197               cterm=bold
hi Tag             ctermfg=197
hi Title           ctermfg=203
hi Visual                      ctermbg=238

hi Comment         ctermfg=244
hi LineNr          ctermfg=239 ctermbg=235
hi NonText         ctermfg=239
hi SpecialKey      ctermfg=239
hi MatchParen      ctermfg=233  ctermbg=208 cterm=bold
hi ModeMsg         ctermfg=229
hi MoreMsg         ctermfg=229
hi Operator        ctermfg=161

" F5 save and run python code 
au BufRead *.py map <buffer> <F5> :w<CR>:!/usr/bin/env python % <CR>
