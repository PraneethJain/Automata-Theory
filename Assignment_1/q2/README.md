# Working
- The basic idea is to recursively split the given statement into its subparts and check each of their validity individually.
- In case of ambiguity, the longest valid list of tokens is considered. For example, for the string `if x + y > 3 print 2`, the valid `conds` are `x`, `x + y` and `x + y > 3`. I have considered `x + y > 3` to be the `cond`.
- No brackets are required or handled.
- The source code is taken from `stdin` and if no errors are found, the tokens are printed. In case there are errors, the first error is printed.

# Assumptions
### Negative numbers

Consider the source code `"print -1"`

The boilerplate tokenizer tokenizes it into `["print", "-", "1"]`

My tokenizer tokenizes it into `["print", "-1"]`

This makes statements like `-1` valid. `+1` is still invalid, I have only considered negative numbers prefixed with `-`. For positive, just enter the value without sign.

> Note that cases like `x - 1` are still tokenized as `["x", "-", "1"]`

### Error Messages
I have printed the exact rule number that is being broken.

Only the first rule that is found to be broken on progressing left to right in the given source code is printed. After that, the program halts.
