/* add.y - wygenerowany parser bedzie wykonywal dodawanie */

%{
#include <stdio.h>
%}

%token NUM

%%

input	:  
	|  input '\n'
	|  input  expr '\n' { printf("%d\n",$2); }
	;

expr	: expr '+' NUM	{ $$ = $1 + $3;}
	| NUM
	;
%%

int yyerror(char *s) {
  printf("blad: %s\n", s);
}

int main()
{
  yyparse();
  return 0;
}
