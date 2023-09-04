import pytest


class TokenType:
    IDENTIFIER = "IDENTIFIER"
    KEYWORD = "KEYWORD"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    SYMBOL = "SYMBOL"


Token = tuple[TokenType, str]
operators = {"+", "-", "*", "/", "^", "<", ">", "="}

token_hierarchy = {
    "if": TokenType.KEYWORD,
    "else": TokenType.KEYWORD,
}


def is_valid_identifier(lexeme: str) -> bool:
    if not lexeme:
        return False

    if not (lexeme[0].isalpha() or lexeme[0] == "_"):
        return False

    return all(char.isalnum() or char == "_" for char in lexeme[1:])


def tokenize(source_code: str):
    tokens = []
    position = 0

    while position < len(source_code):
        # Helper function to check if a character is alphanumeric
        def is_alphanumeric(char: str) -> bool:
            return char.isalnum() or (char == "_")

        char = source_code[position]

        # Check for whitespace and skip it
        if char.isspace():
            position += 1
            continue

        # Identifier recognition
        if char.isalpha():
            lexeme = char
            position += 1
            while position < len(source_code) and is_alphanumeric(
                source_code[position]
            ):
                lexeme += source_code[position]
                position += 1

            if lexeme in token_hierarchy:
                token_type = token_hierarchy[lexeme]
            else:
                if is_valid_identifier(lexeme):
                    token_type = TokenType.IDENTIFIER
                else:
                    raise ValueError(f"Invalid identifier: {lexeme}")

        # Integer or Float recognition
        elif char.isdigit():
            lexeme = char
            position += 1

            is_float = False
            while position < len(source_code):
                next_char = source_code[position]
                # checking if it is a float, or a full-stop
                if next_char == ".":
                    if position + 1 < len(source_code):
                        next_next_char = source_code[position + 1]
                        if next_next_char.isdigit():
                            is_float = True

                # checking for illegal identifier
                elif is_alphanumeric(next_char) and not next_char.isdigit():
                    while position < len(source_code) and is_alphanumeric(
                        source_code[position]
                    ):
                        lexeme += source_code[position]
                        position += 1
                    if not is_valid_identifier(lexeme):
                        raise ValueError(
                            f"Invalid identifier: {lexeme}\n"
                            + "Identifier can't start with digits"
                        )

                elif not next_char.isdigit():
                    break

                lexeme += next_char
                position += 1

            token_type = TokenType.FLOAT if is_float else TokenType.INTEGER

        # Symbol recognition
        else:
            lexeme = char
            position += 1
            token_type = TokenType.SYMBOL

        tokens.append((token_type, lexeme))

    return tokens


def valid_x(tokens: list[Token]) -> bool:
    if len(tokens) == 1:
        return tokens[0][0] in (
            TokenType.FLOAT,
            TokenType.INTEGER,
            TokenType.IDENTIFIER,
        )
    else:
        return valid_cond(tokens)


def valid_cond(tokens: list[Token]) -> bool:
    for op in operators:
        if (TokenType.SYMBOL, op) in tokens:
            return valid_x(tokens[: tokens.index((TokenType.SYMBOL, op))]) and valid_x(
                tokens[tokens.index((TokenType.SYMBOL, op)) + 1 :]
            )
    else:
        return len(tokens) == 1 and tokens[0][0] in (
            TokenType.FLOAT,
            TokenType.INTEGER,
            TokenType.IDENTIFIER,
        )


def valid_A(tokens: list[Token]) -> bool:
    i = 0
    n = len(tokens)
    i_max = -1
    while i <= n:
        if valid_cond(tokens[:i]):
            i_max = i
        i += 1

    if i_max == -1:
        return False

    j = i_max + 1
    j_max = -1
    while j <= n:
        if valid_statement(tokens[i_max:j]):
            j_max = j
        j += 1
    if j_max == n:
        return True
    elif j_max == -1 or j_max >= n or tokens[j_max] != (TokenType.KEYWORD, "else"):
        return False

    return valid_statement(tokens[j_max + 1 :])


def valid_statement(tokens: list[Token]) -> bool:
    if len(tokens) == 0:
        return False
    elif tokens[0] == (TokenType.KEYWORD, "if"):
        return valid_A(tokens[1:])
    elif len(tokens) == 1:
        return tokens[0][0] not in TokenType.KEYWORD and tokens[0][1] not in operators
    else:
        for i in range(len(tokens)):
            if valid_statement(tokens[:i]) and valid_statement(tokens[i:]):
                return True
        else:
            return False


def checkGrammar(tokens: list[Token]) -> bool:
    return valid_statement(tokens)

def better_tokenize(source_code: str) -> list[Token]:
    tokens = tokenize(source_code)
    can_fix = True
    while (can_fix):
      for i in range(len(tokens)-1):
          if tokens[i][0] == TokenType.SYMBOL:
            if i == 0 or tokens[i-1][0] not in (TokenType.FLOAT, TokenType.IDENTIFIER, TokenType.INTEGER) or tokens[i-1][1] == "print":
                tokens = tokens[:i] + [(tokens[i+1][0], tokens[i][1] + tokens[i+1][1])] + tokens[i+2:]
                break
      else:
          can_fix = False
    return tokens

if __name__ == "__main__":
    source_code = "if 2 + xi > 0 print 2.0 else print -1;"
    tokens = better_tokenize(source_code)

    # for token in tokens:
    #     print(f"Token Type: {token[0]}, Token Value: {token[1]}")

    result = checkGrammar(tokens)
    print(result)


testcases = {
    "if": False,
    "else": False,
    "if a b": True,
    "if x print": True,
    "if a if b if c": False,
    "if a if b if c d": True,
    "if a if b else if c d": False,
    "if a if b print else if c d": True,
    "if 2 + xi > 0 print 2.0 else print -1;": True,
    "a b c d e f g": True,
    "print hello test 1 2 3 5 1.02": True,
    "print -1": True,
    "print 2.0 else print -1;": False,
    "if x + 3.1 print else if x - 2 test else if x + 3 * 4 < 2 ok": True,
    "if x + 3.1 print else if test else if x + 3 * 4 < 2 ok": False,
    "if x + 3.1 print else if x - 2 test else if x + 3 * 4 < 2": False,
    "if else if x - 2 test else if x + 3 * 4 < 2 ok": False,
    "if 1 x else x else y": False,
    "a b c if x y 2 else if x + 3 = 4 print yes": True,
    "if +": False,
    "if + print": False,
    "if 2+print print 5": True,
    "print if print print else x < y": False,
}


@pytest.mark.parametrize("string, result", [tuple(x) for x in testcases.items()])
def test_output_match(string: str, result: bool) -> None:
    tokens = better_tokenize(string)
    assert checkGrammar(tokens) == result
