/* add.l - skaner wspolpracujacy z parserem add.y */

%option noyywrap

%{
#include "add.tab.h"
%}

%%
[0-9]+	yylval = atoi(yytext);  return(NUM); 
[ \t]+  /* eat up whitespaces */
.|\n    return(*yytext);
