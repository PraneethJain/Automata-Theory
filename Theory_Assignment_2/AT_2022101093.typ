#align(center, text(17pt)[*Automata Theory*])
#align(center, text(16pt)[Theory Assignment 2])
#align(center, text(13pt)[Moida Praneeth Jain, 2022010193])

= Question 1
Pumping lemma for context free languages states that if $L$ is a context-free language then $exists p $ (pumping length) such that $forall s in L$, $s$ can be divided into 5 substrings $s = u v x y z$ such that 
- $u v^t x y^t z in L space forall t >= 0$
- $|v y| > 0$
- $|v x y| <= p$

== (a)
#underline[Given]: $L = {a^i b^j c^k | 0 <= i <= j <= k}$

#underline[To Prove]: $L$ is not a context-free language

#underline[Proof]: Assume L is a context-free language.

$therefore$ L satisfies the pumping lemma for context-free languages. Let $p$ be its pumping length.

Consider the string $s = a^p b^p c^p$. $|s| = 3p > p$, $therefore s = u v x y z$

Define a function $f: L -> NN$ that takes in a string from the language and outputs the number of unique characters in it. For example, $f("aabc") = 3, f("aaa") = 1, f(epsilon) = 0$.

#list(
[
Case 1: $f(v) <= 1 and f(y) <= 1$

The maximum number of unique symbols in both $v$ and $y$ combined is $max(f(v) + f(y)) = 2$ in this case. Since we have 3 symbols $(a, b, c)$, atleast one symbol never occurs in both $v$ and $y$. Let this symbol be $m$.
#list(
  [Subcase 1: $m = a$
  
    We pump down with $t = 0$, i.e, $s^' = u v^0 x y^0 z = u x z$.

    $v$ and $y$ contained either $b$ or $c$ (or both). Before pumping, all three characters had equal count $p$. After pumping, the count of either $b$ or $c$ (or both) is lower than the count of $a$. 

  $therefore s^' in.not L$
  ],
  [Subcase 2: $m = b$
  
    If $a$ is present in $u$ or $v$, then we pump up with $t = 2$, i.e, $s^' = u v^2 x y^2 z$. The number of $b$ remains same as $p$ while the number of $a$ has increased.

    Otherweise, if $c$ is present in $u$ or $v$, then we pump down with $t = 0$, i.e, $s^' = u v^0 x y^0 z$. The number of $b$ remains same as $p$ while the number of $c$ has decreased.

    $therefore s^' in.not L$ 
  ],
  [Subcase 3: $m = c$

    We pump up with $t = 2$, i.e, $s^' = u v^2 x y^2 z$. The number of $c$ remains the same as $p$ while the number of $a$ or $b$ (or both) increases.

    $therefore s^' in.not L$
  ]
)
In all the subcases, the pumping lemma does not hold.
],
[
Case 2: $f(v) > 1 or f(y) > 1$

We pump up with $t = 2$, i.e, $s^' = u v^2 x y^2 z$.

WLOG assume $f(v) > 1$, i.e, $v = l_1 l_2 l_3$ in the correct order ($l_3 "may be" epsilon$). 

$v^2 = l_1 l_2 l_3 l_1 l_2 l_3$. But, $l_1$ cannot appear after $l_2$. This is a contradiction.

Pumping lemma does not hold. 
]
)

In all possible cases, pumping lemma does not hold. This is a contradiction.

$therefore L$ is not a context free language.

$Q E D$