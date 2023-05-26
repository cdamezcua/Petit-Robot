%{

#include "y.tab.h"
#include <string.h>

%}

%%

Bot |
Karel |
Mecha |
Petit |
Robot           { return VOCATIVE; }

,               { return COMMA; }

please |
kindly          { return ADVERB_OF_MANNER; }

turn |
rotate          { return VERB_OF_ROTATION; }

90 | 
180 |
270 |
360             { yylval = atoi(yytext); return ONE_OF_FIRST_FOUR_POSITIVE_MULTIPLES_OF_90; }

degrees         { return ATOMIC_UNIT_OF_ANGLE; }

clockwise       { return ADVERB_OF_ROTATIONAL_SENSE; }

move |
walk            { return VERB_OF_MOTION; }

[1-9][0-9]*     { yylval = atoi(yytext); return POSITIVE_INTEGER; }

blocks |
steps           { return ATOMIC_UNIT_OF_LENGTH; }

forward | 
ahead           { return ADVERB_OF_DIRECTION; }

then | 
next | 
subsequently | 
afterwards      { return ADVERB_OF_TIME; }

and | 
et              { return CUMULATIVE_CONJUNCTION; }

\.              { return FULL_STOP; }

[ \t\n]+          { ; }

.               { return yytext[0]; }

%%
