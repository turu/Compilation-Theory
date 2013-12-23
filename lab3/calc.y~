/* symtab.y - przyk³ad ilustruj¹cy u¿ycie deklaracji %union */

%{
using namespace std;
#include<cstdio>
#include<string>
#include<map>

int yylex(void); 
int yyerror(const char* s); 

map<string,float> symtab;
%}

%union {
double value;
char* name;
}

%token <name> IDENT
%token <value> NUM

%type <value> assign_instr expr term

%%

instr_list: instr_list assign_instr
          | assign_instr
          ;

assign_instr: IDENT '=' expr ';' { $$ = $3; symtab[$1] = $3; }

expr: expr '+' term { $$ = $1 + $3; }
    | term          { $$ = $1; }
    ;

term: NUM     { $$ = $1; }
    | IDENT   { $$ = symtab[$1]; }
    ;

%%

int main(void) {

yyparse();


/* wypisz zawartosc tablicy symboli */
for(map<string,float>::iterator it=symtab.begin(); it!=symtab.end(); ++it) {
    printf("%s=%f\n", it->first.c_str(), it->second);
}

return 0;  
}

int yyerror(const char* s) {
    printf("blad: %s\n", s);
}


