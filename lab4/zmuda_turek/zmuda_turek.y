/* michal zmuda, piotr turek */

%union {
char* str;
int number;
}

%token <str> TYPE NUM IDENT BODY
%type <str> functions function decl_specifier declaration_list declaration declarator_list declarator direct_declarator identifier_list param_list param_declaration abstract_declarator direct_abstract_declarator pointer

%{

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <search.h>
#include <stdarg.h>

/**
*	mechanizm pamietania wszelkiej zaalokowanej pamieci i jej zbiorczej usuniecia
**/
char * almostsoftreferences[1024];
int referencesCount=0;
char * memorized_malloc(int size) {
    char * ret = malloc(size);
    almostsoftreferences[referencesCount]=0;
    return ret;
}
void free_memorized() {
    int i;
    for(i = 0; i < referencesCount; i++) {
        free(almostsoftreferences[i]);
    }
    referencesCount = 0;
}



typedef struct {
    char id[64];
    char type[64];
} entry;

/**
*	mapujemy ostatnie deklaratory
*	na typy z ich deklaracji
**/
entry map[100];
int mapsize = 0;
void map_add_id(char* ptr) {
    sprintf(map[mapsize].id,"%s",ptr);
    sprintf(map[mapsize].type,"");
    mapsize++;
}

/* dla danego klucza(id) uzupelnaimy value(typ) */
int map_fill_type(char * key, char * value) {
    int i = mapsize - 1;
    char * buffer = memorized_malloc(1024);
    while (i >= 0) {
        /* jezeli delkarator pasuje do deklaracji */
        if (!strcmp(map[i].id, key)) {
            break;
        }
        /* jezeli tablica pasuje do deklaracji */
        sprintf(buffer,"%s[]",map[i].id);
        if (!strcmp(buffer, key)) {
            sprintf(map[i].id,"%s",buffer);
            break;
        }
        /* przygotowujemy wskaznik o tej samej dlugosci */
        sprintf(buffer,"*****");
        while (strlen(buffer) + strlen(map[i].id) < strlen(key)) {
            sprintf(buffer,"*****%s",buffer);
        }
        sprintf(buffer + strlen(key) - strlen(map[i].id), "%s", map[i].id);
        /* jezeli wskaznik pasuje do deklaracji */
        if (!strcmp(buffer, key)) {
            sprintf(map[i].id, "%s", buffer);
            break;
        }
        i--;
    }

    if (i >= 0) {
        sprintf(map[i].type, "%s", value);
        return i;
    }

    /* jezeli nie znalezlismy klucza, sygnalizujemy blad */
    return -1;
}



/*
*	przechowujemy ostatnio deklaratory (ktore budowaly liste deklaratorow)
*	aby moc zweryfikowac parametry funkcji
*/
char lastDeclarated[100][100];
int lastDeclaratedPos=0;
void push_declarated(char * ptr) {
    sprintf(lastDeclarated[lastDeclaratedPos], "%s", ptr);
    lastDeclaratedPos++;
}
/* znalezionymi delkaratorami uzupelniamy mape */
int flush_declared (char * type) {
    while (lastDeclaratedPos > 0) {
        lastDeclaratedPos--;
        if (map_fill_type(lastDeclarated[lastDeclaratedPos],type) < 0) {
            return 1;
        }
    }
    return 0;
}
/* w uzyskanej funkcji podmieniamy liste argumentow */
char * substituteArgs (char* function) {
    char * buffer = memorized_malloc(1024);
    sprintf(buffer, "%s", strstr(function,")"));
    /* pamietam pozycje na ktorej konczy sie generowana lista argumentow */
    int shift = sprintf(strstr(function,"("), "(", buffer);
    int i;
    for (i = 0; i < mapsize; i++) {
        /* jezeli nie ma wartosci typu dla pewnego deklaratora, sygnalizujemy blad */
        if (map[i].type[0] == 0) {
            return 0;
        }
        /* dodjemy argument i aktualizujemy pozycje w napisie */
        shift += sprintf(strstr(function, "(") + shift, "%s %s, ", map[i].type,map[i].id);
    }
    /* laczymy pozostala czesc funkcji z nowa lista argumentow */
    /* -2 zamazuje nadmiarowe ", " */
    sprintf(strstr(function,"(") + shift - 2, "%s", buffer);
    /* resetujemy nasza niby-mape */
    mapsize = 0;
}

/**
*	tworzy wynik na podstawaie formatu i argumentow w nowo zaalokowanej pamieci
*	owa pamiec bedzie zapamietana do zwolnienia
**/
char * copy_args(char* format, ...) {
    char * buffer = memorized_malloc(1024);
    va_list args;
    va_start(args, format);
    vsprintf(buffer,format, args);
    va_end(args);
    return buffer;
}


%}

%%
printer:	functions					{ printf("%s",$1); }

functions:	function 					{ $$ = copy_args("%s",$1); }
		|functions function 				{ $$ = copy_args("%s\n%s", $1, $2); }
		;
function:	decl_specifier declarator declaration_list BODY { $$ = copy_args("%s %s %s", $1, $2, $4); 
									if(!substituteArgs($$)){
										yyerror("Brak specyfikacji parametru\n");
										YYABORT;
									}
									  
								}
		|decl_specifier declarator BODY			{ $$ = copy_args("%s %s %s", $1, $2, $3); }
		|declarator declaration_list BODY 		{ $$ = copy_args("void %s %s", $1,$3); 
									if(!substituteArgs($$)){
										yyerror("Brak specyfikacji parametru\n");
										YYABORT;
									}
								}
		|declarator BODY 				{ $$ = copy_args("void %s %s", $1, $2); }
		;
decl_specifier:	TYPE						{ $$ = copy_args("%s", $1); }
		;
declaration_list: declaration					{ $$ = copy_args("%s", $1); }
		| declaration_list declaration			{ $$ = copy_args("%s %s", $1, $2); }
		;
declaration:	decl_specifier ';'				{ $$ = copy_args("%s;", $1); }
		|decl_specifier declarator_list ';'		{ $$ = copy_args("%s %s;", $1, $2); 
									if (flush_declared($1)) {
										yyerror("Specyfikacja nieistniejacego parametru\n");
										YYABORT;
									}
								}
		;
declarator_list :declarator_list ',' declarator 		{ $$ = copy_args("%s, %s", $1, $3); 
									push_declarated($3);
								}
		| declarator					{ $$ = copy_args("%s", $1); 
									push_declarated($1);
								}
		;
declarator:	pointer direct_declarator			{ $$ = copy_args("%s%s", $1, $2); }
		| direct_declarator 				{ $$ = copy_args("%s", $1); }
		;
direct_declarator: IDENT 					{ $$ = copy_args("%s", $1);}
                | '(' declarator ')'				{ $$ = copy_args("(%s)", $2); }
                | direct_declarator '[' NUM ']'			{ $$ = copy_args("%s[%s]", $1, $3); }
                | direct_declarator '[' ']'			{ $$ = copy_args("%s[]", $1); }
                | direct_declarator '(' param_list ')'		{ $$ = copy_args("%s(%s)", $1,$3); }	
                | direct_declarator '(' identifier_list ')'	{ $$ = copy_args("%s(%s)", $1,$3); }
                | direct_declarator '(' ')' 			{ $$ = copy_args("%s(void)", $1); }
    		;
identifier_list: identifier_list ',' IDENT			{ $$ = copy_args("%s, %s", $1, $3); 
									 map_add_id($3);
								}
		| IDENT						{ $$ = copy_args("%s", $1); 
									 map_add_id($1);
								}
		;
param_list:	param_declaration				{ $$ = copy_args("%s", $1); }
		| param_list ',' param_declaration 		{ $$ = copy_args("%s, %s", $1, $3); }
		;
param_declaration: decl_specifier declarator			{ $$ = copy_args("%s %s", $1, $2); }
                | decl_specifier abstract_declarator 		{ $$ = copy_args("%s %s", $1, $2); }
                | decl_specifier 				{ $$ = copy_args("%s", $1); }
		;
abstract_declarator: pointer					{ $$ = copy_args("%s", $1); }
                | pointer direct_abstract_declarator 		{ $$ = copy_args("%s%s", $1, $2); }
                | direct_abstract_declarator			{ $$ = copy_args("%s", $1); }
		;
direct_abstract_declarator: '(' abstract_declarator ')' 	{ $$ = copy_args("(%s)", $2); }
                | direct_abstract_declarator '['  ']' 		{ $$ = copy_args("%s[]", $1); }
                | direct_abstract_declarator '[' NUM ']' 	{ $$ = copy_args("%s[%s]",$1,$3); }
                | '[' ']' 					{ $$ = copy_args("[]"); }
                | '[' NUM ']' 					{ $$ = copy_args("[%s]", $2); }
                | direct_abstract_declarator '(' ')' 		{ $$ = copy_args("%s()", $1); }
                | direct_abstract_declarator '(' param_list ')' { $$ = copy_args("%s(%s)", $1,$3); }
                | '('  ')' 					{ $$ = copy_args("()"); }
                | '(' param_list ')' 				{ $$ = copy_args("(%s)", $2); }
                ;      
pointer:	'*'						{ $$ = copy_args( "*"); }
		| pointer '*'					{ $$ = copy_args("%s*", $1);}
		;  

%%

int main() 
{
  	yyparse(); 
	free_memorized();
  	return 0;
}

int yyerror(char *s)
{
    printf("error: %s\n", s); 
}
