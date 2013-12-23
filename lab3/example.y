/* example.y - bardzo prosty parser */

%token LETTER  /* wszystkie nazwy tokenow majace wiecej niz jeden znak musza byc zadeklarowane */

%{
#include <stdio.h>
%}

%%

/* gdy na wejsciu pojawi sie symbol terminalny NUM zostanie wywolana ponizsza akcja */

input: LETTER { printf("rozpoznano -%c\n", $1); };

/* do przekazywania wartosci semantycznych pomiedzy regulami sluza tzw. pseudozmienne; 
   akcja moze zwrocic wartosc przez podstawienia pseudozmiennej $$;
   pseudozmiennej $1 uzyto w przykladzie, aby wypisac wartosc tokenu NUM */

%%

int main() 
{
  /* aby rozpoczac parsing trzeba wywolac funkcje yyparse */ 
  yyparse(); 
  return 0;
}

/* gdy funkcja yyparse wykryje blad wywoluje funkcje yyerror */
int yyerror(char *s)
{
   printf("blad: %s\n", s); 
}
