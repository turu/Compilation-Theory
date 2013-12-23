all: zmuda_turek

zmuda_turek: lex.yy.c zmuda_turek.tab.c
	gcc lex.yy.c zmuda_turek.tab.c -o zmuda_turek

lex.yy.c: zmuda_turek.l
	flex zmuda_turek.l

zmuda_turek.tab.c: zmuda_turek.y
	bison -d zmuda_turek.y

clean:
	rm *.yy.c *.tab.c *.h zmuda_turek
