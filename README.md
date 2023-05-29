# Petit-Robot

## Context Free Grammar
### Lex
```
⟨VOCATIVE⟩ → Bot | Karel | Mecha | Petit | Robot
⟨ADVERB_OF_MANNER⟩ → please | kindly
⟨COMMA⟩ → ,

⟨VERB_OF_ROTATION⟩ → turn | rotate
⟨ONE_OF_FIRST_FOUR_POSITIVE_MULTIPLES_OF_90⟩ → 90 | 180 | 270 | 360
⟨ATOMIC_UNIT_OF_ANGLE⟩ → degrees
⟨ADVERB_OF_ROTATIONAL_SENSE⟩ → clockwise

⟨VERB_OF_MOTION⟩ → move | walk
⟨POSITIVE_INTEGER⟩ → ℕ+
⟨ATOMIC_UNIT_OF_LENGTH⟩ → blocks | steps
⟨ADVERB_OF_DIRECTION⟩ → forward | ahead

⟨ADVERB_OF_TIME⟩ → then | next | subsequently | afterwards
⟨CUMULATIVE_CONJUNCTION⟩ → and | et

⟨FULL_STOP⟩ → \.
```

### Yacc
```
⟨sentence⟩ → ⟨VOCATIVE⟩ ⟨COMMA⟩ ⟨ADVERB_OF_MANNER⟩ ⟨enumeration_of_instructions⟩ ⟨FULL_STOP⟩

⟨enumeration_of_instructions⟩ → ⟨instruction⟩
			     | ⟨instruction⟩ ⟨COMMA⟩ ⟨last_instruction_of_enumeration⟩
			     | ⟨instruction⟩ ⟨COMMA⟩ ⟨middle_instructions_of_enumeration⟩ ⟨last_instruction_of_enumeration⟩

⟨middle_instructions_of_enumeration⟩ → ⟨ADVERB_OF_TIME⟩ ⟨instruction⟩ ⟨COMMA⟩
			   	    | ⟨middle_instructions_of_enumeration⟩ ⟨ADVERB_OF_TIME⟩ ⟨instruction⟩ ⟨COMMA⟩

⟨last_instruction_of_enumeration⟩ → ⟨CUMULATIVE_CONJUNCTION⟩ ⟨ADVERB_OF_TIME⟩ ⟨instruction⟩

⟨instruction⟩ → ⟨rotation_instruction⟩
	     | ⟨motion_instruction⟩

⟨rotation_instruction⟩ → ⟨VERB_OF_ROTATION⟩ ⟨ONE_OF_FIRST_FOUR_POSITIVE_MULTIPLES_OF_90⟩ ⟨ATOMIC_UNIT_OF_ANGLE⟩ ⟨ADVERB_OF_ROTATIONAL_SENSE⟩

⟨motion_instruction⟩ → ⟨VERB_OF_MOTION⟩ ⟨length_parameter⟩ ⟨ATOMIC_UNIT_OF_LENGTH⟩ ⟨ADVERB_OF_DIRECTION⟩

⟨length_parameter⟩ → ⟨ONE_OF_FIRST_FOUR_POSITIVE_MULTIPLES_OF_90⟩
	          | ⟨POSITIVE_INTEGER⟩
```

## Technologies Used
- Python
- Lex
- Yacc

## Authors 🖋
- Carlos Amezcua - Developer
- Daniel Muñoz - Developer
- Diego Curiel - Developer
