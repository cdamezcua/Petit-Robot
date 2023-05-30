# Petit Robot

![Petit Robot animation](media/Petit-Robot-animation.gif)

Petit Robot is an adorable robot that resides in a fascinating square world composed of 10 rows and 10 columns. This charming automaton can be programmed using its own programming language: Petit Language. Additionally, it features a wonderful tool called Petit Emulator, which allows for the generation of captivating animations that illustrate the program's execution.

## Petit Language

The Petit Language is remarkably simple as it lacks control structures and variables. It is based on two fundamental instructions: moving forward and turning clockwise. One notable aspect of this language is its peculiar structure, which will only allow you to give commands to the robot if you do so in a gentile manner.

### Examples

The following are simple examples of the Petit language syntax and the respective instructions that they generate in assembly language when compiled:

| Petit Language                                                                                                                                                                          | Assembly Language                                  |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------|
| Robot, please turn 90 degrees clockwise, then move 4 blocks ahead, and then turn 90 degrees clockwise.                                                                                  | TURN,90<br>MOV,4<br>TURN,90                        |
| Karel, kindly rotate 360 degrees clockwise.                                                                                                                                             | TURN,360                                           |
| Bot, <br>please turn 180 degrees clockwise,<br>afterwards walk 2 steps forward,<br>then turn 270 degrees clockwise,<br>then move 2 blocks ahead,<br>et then turn 360 degrees clockwise. | TURN,180<br>MOV,2<br>TURN,270<br>MOV,2<br>TURN,360 |

### Context Free Grammar of the Petit Language
#### Lex
```
⟨VOCATIVE⟩ → Bot | Karel | Mecha | Petit | Robot
⟨COMMA⟩ → ,
⟨ADVERB_OF_MANNER⟩ → please | kindly

⟨VERB_OF_ROTATION⟩ → turn | rotate
⟨ONE_OF_FIRST_FOUR_POSITIVE_MULTIPLES_OF_90⟩ → 90 | 180 | 270 | 360
⟨ATOMIC_UNIT_OF_ANGLE⟩ → degrees
⟨ADVERB_OF_ROTATIONAL_SENSE⟩ → clockwise

⟨VERB_OF_MOTION⟩ → move | walk
⟨POSITIVE_INTEGER⟩ → ℕᐩ
⟨ATOMIC_UNIT_OF_LENGTH⟩ → blocks | steps
⟨ADVERB_OF_DIRECTION⟩ → forward | ahead

⟨CUMULATIVE_CONJUNCTION⟩ → and | et
⟨ADVERB_OF_TIME⟩ → then | next | subsequently | afterwards

⟨FULL_STOP⟩ → .
```

#### Yacc
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

## Petit Emulator



## Technologies Used
- Python
- Lex
- Yacc

## Authors 🖋
- [Carlos Amezcua](https://github.com/cdamezcua) - Developer
- [Daniel Muñoz](https://github.com/DanielMunoz4190) - Developer
- [Diego Curiel](https://github.com/DiegoCuriel) - Developer
