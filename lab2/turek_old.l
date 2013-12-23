
%s cTIMEOK cSKIP cIPSTART cSRCPRT cSRCIPOK cTOSEPOK cDSTPRT cDSTIPOK cLITTER cBYTES cBRACKETOPEN

DIGIT		[0-9]

COR_TIME	(([0-1]{DIGIT})|2[0-4]):([0-5]{DIGIT}):([0-5]{DIGIT})\.{DIGIT}{6}
INC_TIME	{DIGIT}{2}:{DIGIT}{2}:{DIGIT}{2}\.{DIGIT}{6}

IPPART		({DIGIT}{1,2})|(1{DIGIT}{2})|(2[0-4]{DIGIT})|(25[0-5])
COR_IP		{IPPART}(\.{IPPART}){3}
INC_IP		{DIGIT}{1,3}(\.{DIGIT}{1,3}){3}

COR_PORT	\.(({DIGIT}{1,4})|([1-5]{DIGIT}{4})|(6[0-4]{DIGIT}{3})|(65[0-5]{DIGIT}{2})|(655[0-2]{DIGIT})|(6553[0-5]))
INC_PORT	\.{DIGIT}{1,5}

LITTER		[^\n(]*
BYTES		{DIGIT}+
SKIP		[^\n]*\n

%%

^{COR_TIME}	{
		yytext[8] = '\0';
		printf("%s ", yytext);
		BEGIN(cTIMEOK);
		}
^{INC_TIME}	{
		yytext[8] = '\0';
		printf("%s (bad time format!)", yytext);
		BEGIN(cTIMEOK);
		}
^.		{printf("fatal time! line %d\n", yylineno); BEGIN(cSKIP);}


<cTIMEOK>" "IP" "		{printf(" from "); BEGIN(cIPSTART);}
<cTIMEOK>.			{printf("[no ip protocol! line %d]\n", yylineno); BEGIN(cSKIP);}

<cIPSTART>{COR_IP}/{INC_PORT}?" " 	{printf("%s", yytext); BEGIN(cSRCPRT);}
<cIPSTART>{INC_IP}/{INC_PORT}		{printf("%s (bad src ip format!)", yytext); BEGIN(cSRCPRT);}
<cIPSTART>.				{printf("[fatal src ip! line %d]\n", yylineno); BEGIN(cSKIP);}

<cSRCPRT>{COR_PORT}?" "		{BEGIN(cSRCIPOK);}
<cSRCPRT>{INC_PORT}?" "		{printf("(bad src port format!)"); BEGIN(cSRCIPOK);}
<cSRCPRT>.			{printf("[fatal src prt! line %d]\n", yylineno); BEGIN(cSKIP);}

<cSRCIPOK>>" "			{printf(" to "); BEGIN(cTOSEPOK);}
<cSRCIPOK>.			{printf("[fatal ip separator! line %d]\n", yylineno); BEGIN(cSKIP);}

<cTOSEPOK>{COR_IP}		{printf("%s", yytext); BEGIN(cDSTPRT);}
<cTOSEPOK>{INC_IP}		{printf("%s (bad dst ip format!)", yytext); BEGIN(cDSTPRT);}
<cTOSEPOK>.			{printf("[fatal dst ip! line %d]\n", yylineno); BEGIN(cSKIP);}

<cDSTPRT>{COR_PORT}?""/.	{BEGIN(cDSTIPOK);}
<cDSTPRT>{INC_PORT}		{printf("(bad dst prt format!)"); BEGIN(cDSTIPOK);}
<cDSTPRT>[^:\.]			{printf("[fatal dst prt! line %d]\n", yylineno); BEGIN(cSKIP);}

<cDSTIPOK>:" "/{LITTER}\n	{BEGIN(cLITTER);}
<cDSTIPOK>:" "/{LITTER}\(	{BEGIN(cBYTES);}

<cLITTER>{LITTER}		{BEGIN(INITIAL);}
<cBYTES>{LITTER}\(		{BEGIN(cBRACKETOPEN);}
<cBRACKETOPEN>{BYTES}/\)	{printf(" %s bytes", yytext); BEGIN(cLITTER);}

<cSKIP>{SKIP}			{yylineno++; BEGIN(INITIAL);}

\n				{yylineno++; printf("\n");}

%%

int main(int argc, char ** argv) {
	++argv, --argc;
	if (argc > 0) {
		yyin = fopen(argv[0], "r");
	} else {
		yyin = stdin;
	}

	yylex();

	return 0;
}
