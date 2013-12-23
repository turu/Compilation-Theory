/* example.l - skaner wspolpracujacy z parserem example.y */

%option noyywrap

%{
#include "example.tab.h"
%}

/* zmienna globalna yylval sluz do przekazywania parserowi atrybutu tokenu (wartosci semantycznej);
   zmienna yylval powinna jest typu YYSTYPE */
%%
-[abc]	{ yylval = yytext[1]; return LETTER; }
    /* po dopasowaniu ciagu wejsciowego do zmiennej yylval podstawiamy znak znajdujacy sie po -,
       funkcja yylex konczy swoje dzialanie i zwraca numer dopasowanego tokenu */
.|\n	;
