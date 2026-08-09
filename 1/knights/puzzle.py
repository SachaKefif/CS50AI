from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
statement0 = And(AKnight, AKnave)

knowledge0 = And(
    # TODO
    Or(AKnight, AKnave),
    
    Implication(AKnight, statement0),
    Implication(AKnave, Not(statement0))
    
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
statement1 = And(AKnave, BKnave)

knowledge1 = And(
    # TODO
    And(Or(AKnave, AKnight), Or(BKnave, BKnight)),
    
    Implication(AKnight, statement1),
    Implication(AKnave, Not(statement1)),    
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
statement21 = Or(And(AKnave, BKnave), And(AKnight, BKnight))
statement22 = Or(And(AKnave, BKnight), And(AKnight, BKnave))


knowledge2 = And(
    # TODO
    And(Or(AKnight, AKnave), Or(BKnave, BKnight)),
    
    Implication(AKnight, statement21),
    Implication(AKnave, Not(statement21)),
    Implication(BKnight, statement22),
    Implication(BKnave, Not(statement22)),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

ASaidKnave = Symbol("A said 'I am a knave'")

# If ASaidKnave is false, A said "I am a knight."
AStatement = Or(
    And(Not(ASaidKnave), AKnight),
    And(ASaidKnave, AKnave)
)

knowledge3 = And(
    # Each person is exactly one type
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    # A's unknown statement
    Biconditional(AKnight, AStatement),

    # B's two statements
    Biconditional(BKnight, ASaidKnave),
    Biconditional(BKnight, CKnave),

    # C says "A is a knight"
    Biconditional(CKnight, AKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
