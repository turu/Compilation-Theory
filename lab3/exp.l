/* exp.l - skaner wspolpracujacy z parserem exp.y */

%option noyywrap

%{
#include "exp.tab.h"
%}

%%

[0-9]+  yylval = atoi(yytext); return NUM; 
[ \t]+  /* eat up whitespaces */
.|\n    return *yytext;  
