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
        return len(tokens) == 1 and tokens[0][0] in (TokenType.FLOAT, TokenType.INTEGER, TokenType.IDENTIFIER)


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
        return tokens[0] not in ((TokenType.KEYWORD, "if"), (TokenType.KEYWORD, "else"))
    else:
        for i in range(len(tokens)):
            if valid_statement(tokens[:i]) and valid_statement(tokens[i:]):
                return True
        else:
            return False


def checkGrammar(tokens: list[Token]) -> bool:
    return valid_statement(tokens)


# Test the tokenizer
if __name__ == "__main__":
    source_code = "if 2+xi > 0 print 2.0 else print -1;"
    tokens = tokenize(source_code)

    # for token in tokens:
    #     print(f"Token Type: {token[0]}, Token Value: {token[1]}")

    logs = checkGrammar(tokens)
    print(logs)
