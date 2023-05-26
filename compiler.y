%{ 

#include <stdio.h>

int yylex(void);
int yyparse(void);
void yyerror(char *);

extern FILE *yyin;

%}

%token VOCATIVE COMMA ADVERB_OF_MANNER VERB_OF_ROTATION 
%token ONE_OF_FIRST_FOUR_POSITIVE_MULTIPLES_OF_90 ATOMIC_UNIT_OF_ANGLE 
%token ADVERB_OF_ROTATIONAL_SENSE VERB_OF_MOTION POSITIVE_INTEGER
%token ATOMIC_UNIT_OF_LENGTH ADVERB_OF_DIRECTION ADVERB_OF_TIME 
%token CUMULATIVE_CONJUNCTION FULL_STOP

%%

sentence : VOCATIVE COMMA ADVERB_OF_MANNER enumeration_of_instructions FULL_STOP
         ;

enumeration_of_instructions : instruction
                            | instruction COMMA last_instruction_of_enumeration
                            | instruction COMMA middle_instructions_of_enumeration last_instruction_of_enumeration
                            ;

middle_instructions_of_enumeration : ADVERB_OF_TIME instruction COMMA
                                   | middle_instructions_of_enumeration ADVERB_OF_TIME instruction COMMA
                                   ;

last_instruction_of_enumeration : CUMULATIVE_CONJUNCTION ADVERB_OF_TIME instruction
                                ;

instruction : rotation_instruction
            | motion_instruction
            ;

rotation_instruction : VERB_OF_ROTATION ONE_OF_FIRST_FOUR_POSITIVE_MULTIPLES_OF_90 ATOMIC_UNIT_OF_ANGLE ADVERB_OF_ROTATIONAL_SENSE { printf("TURN,%d\n", $2);}
                     ;

motion_instruction : VERB_OF_MOTION length_parameter ATOMIC_UNIT_OF_LENGTH ADVERB_OF_DIRECTION { printf("MOV,%d\n", $2);}
                   ;

length_parameter : ONE_OF_FIRST_FOUR_POSITIVE_MULTIPLES_OF_90 { $$ = $1; }
                                | POSITIVE_INTEGER  { $$ = $1; }
                                ;                   

%%

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        printf("[!] Insufficient arguments!\n");
        printf("[!] Correct ussage: ./compilador input.txt\n");
        return 1;
    }
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("[!] Error opening file: %s\n", argv[1]);
        return 1;
    }
    yyin = input;
    yyparse();
    fclose(input);

    return 0;
}

void yyerror(char *s)
{
    printf("[!] Invalid instruction\n");
}
