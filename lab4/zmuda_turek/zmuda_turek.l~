/* michal zmuda, piotr turek */

%option noyywrap

%{
#include "zmuda_turek.tab.h"
int depth = 0;
%}

%s cCOMMENT cINSTRUCTION cBODY

ATOMIC 	void|char|short|int|long|float
COMPLEX enum|struct
BODY	(([^{}"/]*(\"[^\"]*\")?(\/\/[^\n]*\n)?)*(\/\*([^*]*\*)*\/)?)*
ID 	[a-zA-Z_][0-9a-zA-Z_]* 
NUM 	[0-9]+(\.[0-9]*)?|\.[0-9]+

%%

{ATOMIC}|{COMPLEX}\ {ID}	{ yylval.str = yytext; return TYPE; }
{ID}				{ yylval.str = yytext; return IDENT; }
{NUM}  				{ yylval.str = yytext; return NUM; }
\{				depth = 1; BEGIN(cBODY); yymore();
<cBODY>\{			yymore(); depth++;
<cBODY>{BODY}\}			depth--; if(depth){ yymore(); } else { yylval.str = yytext; BEGIN(INITIAL); return BODY; }
<cBODY>{BODY}			yymore();
[ \t\n]+    			/* eat up whitespaces */
<cBODY>[ \t]+    		/* eat up whitespaces */
.|\n				return *yytext;
%%
