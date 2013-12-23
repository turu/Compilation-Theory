%{
#include <iostream>
#include <map>

using namespace std;
%}

%union {
char* name;
}

%token <name> IDENT
%token <name> TYPE

%%
functions : function+

function  : decl_specifier? declarator declaration_list? body

decl_specifier : void
               | char
               | short
               | int
               | long
               | float
               | struct id
               | enum id

declaration_list : declaration+

declaration : decl_specifier declarator_list? ';'

declarator_list : declarator (',' declarator)*

declarator : pointer? direct_declarator

direct_declarator : id
                  | '(' declarator ')'
                  | direct_declarator '[' NUM? ']'
                  | direct_declarator '(' param_list ')'
                  | direct_declarator '(' identifier_list? ')'

identifier_list : id (',' id)*

param_list : param_declaration (',' param_declaration)*

param_declaration : decl_specifier declarator
                  | decl_specifier abstract_declarator?

abstract_declarator : pointer
                    | pointer? direct_abstract_declarator

direct_abstract_declarator : '(' abstract_declarator ')'
                           | direct_abstract_declarator? '[' NUM? ']'
                           | direct_abstract_declarator? '(' param_list? ')'
                  
pointer : '*'+  

%%

int main()
{
  yyparse();
  return 0;
}
