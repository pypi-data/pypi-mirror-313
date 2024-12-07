import types
from maquinas.regular.dfa import DeterministicFiniteAutomaton as DFA
from maquinas.exceptions import AlphabetsDoNotMatch


class Alphabet(set):
    """Wrapper for the set python class"""

    def __repr__(self):
        return f"{{{', '.join(self)}}}"

    def star(self):
        """Star clouse for an alphabet returns an infinite language

        :returns: Language  _self*_"""
        return Language(gen=(self._star,), sigma=self, finite=False)

    def _star(self):
        seen = set()
        yield ""
        prev = [""]
        while True:
            for pre in prev:
                for ele in self:
                    new = pre + ele
                    prev.append(new)
                    if not new in seen:
                        seen.add(new)
                        yield new
            prev = []

    def power(self, n):
        """Power of an alphabet

        :param n: Power
        :returns: Language  _Σ^n_"""
        if n == 0:
            return empty_string_language(sigma=self)
        elif n == 1:
            return Language(self, sigma=self)
        else:
            return Language(
                set(p for p in self._power(self, 1, n)), sigma=self, finite=True
            )

    def _power(self, partial, i, j):
        if i == j:
            for ele in partial:
                yield ele
        elif i < j:
            yield from self._power(
                Language(
                    [w1 + w2 for w2 in partial for w1 in self], sigma=self, finite=True
                ),
                i + 1,
                j,
            )

    def validate(self, words):
        """Validate if words made of symbols from the alphabet

        :param words: Words to be validated
        :returns: True if words composed by alphabet"""

        # Creates DFA for Σ^* and validates it
        sigma_star = DFA(
            Q=["q"],
            q_0="q",
            sigma=self,
            A=["q"],
            delta=[(("q", symbol), "q") for symbol in self],
        )

        return all([sigma_star.accepts(w) for w in words])


class Mapping(dict):
    def __init__(self, mapping, sigma=None, sigma_=None, infere_alphabet=False):
        if infere_alphabet and sigma is None:
            sigma = mapping.keys()

        if infere_alphabet and sigma_ is None:
            sigma_ = set()
            for l in mapping.values():
                sigma_ = sigma_.union(l.sigma)

        if len(set(mapping.keys()).intersection(sigma)) == 0:
            raise ErrorMappingDoesMatchAlphabet
        super().__init__(mapping)
        self.sigma = Alphabet(sigma)
        self.sigma_ = Alphabet(sigma_)

    def __repr__(self):
        return "\n".join([f"{k} → {v}" for k, v in self.items()])

    def substitution(self, w):
        if len(w) == 0:
            return empty_string_language(sigma=self.sigma)
        else:
            *w_, a = w
            L_a = self.get(a, a)
            return self.substitution(w_).concat(L_a)


class Language:
    def __init__(
        self,
        elements=[],
        sigma=[],
        max=30,
        finite=True,
        gen=None,
        infere_alphabet=False,
    ):
        """Create a language

        :param elements: This can be a finite enumeration of elements, another Language or a generator for an infinite language
        :param sigma: Alphabet
        :param max: Maximum number of elements to print for infinite languages (default 30)
        :param finite: For languages based of generator if the language is finite or infinite, be aware theres is not check on this property and could raise errors (default True)
        :param gen: This is the generator for the language"""
        self.max = max
        self.sigma = Alphabet(sigma)
        if isinstance(elements, Language):
            self.elements = elements.elements
            self.gen = elements.gen
            self.finite = elements.finite
            self.max = elements.max
        elif isinstance(gen, tuple):
            self.gen = gen
            self.elements = None
            self.finite = finite
        else:
            self.elements = set(elements)
            self.gen = None
            self.finite = True
            if infere_alphabet and len(sigma) == 0:
                for e in elements:
                    self.sigma = self.sigma.union(e)

    def __iter__(self):
        if self.finite:
            for ele in self.elements:
                yield ele
        else:
            f, *args = self.gen
            yield from f(*args)

    def __eq__(self, other):
        if self.finite != other.finite:
            return False
        if self.elements:
            a = self.elements == other.elements
        elif isintance(self.gen, tuple) and isinstance(other.gen, tuple):
            f1, args1 = self.gen
            f2, args2 = other.gen
            a = f1 == f2 and args1 == args2
        b = self.sigma == other.sigma
        return b and a

    def _empty_string(self, x):
        return "ε" if len(x) == 0 else x

    def __repr__(self):
        over = f"{{{','.join(self.sigma)}}}"
        if self.finite:
            if self.is_empty_language():
                return f"∅ Σ={over}"
            return f"{{{','.join([str(self._empty_string(x)) for x in self])}}} with Σ={over}"
        else:
            it = iter(self)
            res = []
            while len(res) < self.max:
                try:
                    val = next(it)
                    res.append(val)
                except StopIteration:
                    self.finite = True
                    break
            if self.finite:
                return f"{{{','.join([str(self._empty_string(x)) for x in res ])}}} with Σ={over}"
            else:
                return f"{{{','.join([str(self._empty_string(x)) for x in res ])},…}} with Σ={over}"

    def __len__(self):
        if self.finite:
            return len(self.elements)
        else:
            return float("inf")

    def validate_alphabet(self):
        """Validates if the string can be generated by the alphabet

        :returns: True if words in language composed by alphabet"""
        if self.finite:
            return self.sigma.validate(self)
        else:
            return self.sigma.validate([w for _, w in zip(range(self.max), self)])

    def is_empty_language(self):
        """Check if it is the empty language

        :returns: Language == {}"""
        if self.finite and len(self) == 0:
            return True
        return False

    def is_empty_string_language(self):
        """Check if it is the empty string language

        :returns: Language == {ε}"""
        if self.finite and len(self) == 1 and len(next(iter(self))) == 0:
            return True
        return False

    def union(self, L, force=True):
        """Union of the language with another language, if one is infintie returns an infinite generator

        :param L: Second Languauge fo the union
        :param force: If alphabets different create a newone based on union of both
        :returns: Language  _self ∪ L_"""
        if (not force) and self.sigma != L.sigma:
            raise AlphabetsDoNotMatch(self.sigma, L.sigma)
        sigma_ = self.sigma | L.sigma

        # Empty language case
        if self.is_empty_language():
            return Language(L, sigma=sigma_, finite=True, max=L.max)
        if L.is_empty_language():
            return Language(self, sigma=sigma_, finite=True, max=self.max)

        if self.finite and L.finite:
            return Language(
                self.elements.union(L),
                sigma=sigma_,
                finite=True,
                max=max(self.max, L.max),
            )
        else:
            return Language(
                gen=(self._union, L),
                sigma=sigma_,
                finite=False,
                max=max(self.max, L.max),
            )

    def _union(self, L):
        seen = set()
        g1 = iter(self) if self.finite else self.__iter__()
        g2 = iter(L) if L.finite else L.__iter__()
        while g1 or g2:
            if g1:
                try:
                    w = next(g1)
                    if not w in seen:
                        seen.add(w)
                        yield w
                except StopIteration:
                    g1 = None
            if g2:
                try:
                    w = next(g2)
                    if not w in seen:
                        seen.add(w)
                        yield w
                except StopIteration:
                    g2 = None

    def right_cancellation(self, b):
        """Right quotient of a language over _b_

        :returns: Language  _L÷b_"""

        if self.finite:
            return Language(
                [string_right_cancellation(w, b) for w in self.elements],
                sigma=self.sigma,
                finite=True,
                max=self.max,
            )
        else:
            return Language(
                gen=(self._right_cancellation, b),
                sigma=self.sigma,
                finite=False,
                max=self.max,
            )

    def _right_cancellation(self, b):
        seen = set()
        g1 = self.__iter__()
        while True:
            try:
                w = next(g1)
                w_ = string_right_cancellation(w, b)
                if not w_ in seen:
                    seen.add(w_)
                    yield w_
            except StopIteration:
                break

    def left_cancellation(self, b):
        """Left cancellation of a language over _b_

        :returns: Language  _L÷b_"""

        if self.finite:
            return Language(
                [string_left_cancellation(w, b) for w in self.elements],
                sigma=self.sigma,
                finite=True,
                max=self.max,
            )
        else:
            return Language(
                gen=(self._left_cancellation, b),
                sigma=self.sigma,
                finite=False,
                max=self.max,
            )

    def _left_cancellation(self, b):
        seen = set()
        g1 = self.__iter__()
        while True:
            try:
                w = next(g1)
                w_ = string_left_cancellation(w, b)
                if not w_ in seen:
                    seen.add(w_)
                    yield w_
            except StopIteration:
                break

    def right_quotient(self, b):
        """Right quotient of a language over _b_

        :returns: Language  _L/b_"""

        if self.finite:
            return Language(
                [string_right_quotient(w, b) for w in self.elements],
                sigma=self.sigma,
                finite=True,
                max=self.max,
            )
        else:
            return Language(
                gen=(self._right_quotient, b),
                sigma=self.sigma,
                finite=False,
                max=self.max,
            )

    def _right_quotient(self, b):
        seen = set()
        g1 = self.__iter__()
        while True:
            try:
                w = next(g1)
                w_ = string_right_quotient(w, b)
                if not w_ in seen:
                    seen.add(w_)
                    yield w_
            except StopIteration:
                break

    def left_quotient(self, b):
        """Left quotient of a language over _b_

        :returns: Language  _L\\b_"""

        if self.finite:
            return Language(
                [string_left_quotient(w, b) for w in self.elements],
                sigma=self.sigma,
                finite=True,
                max=self.max,
            )
        else:
            return Language(
                gen=(self._left_quotient, b),
                sigma=self.sigma,
                finite=False,
                max=self.max,
            )

    def _left_quotient(self, b):
        seen = set()
        g1 = self.__iter__()
        while True:
            try:
                w = next(g1)
                w_ = string_left_quotient(w, b)
                if not w_ in seen:
                    seen.add(w_)
                    yield w_
            except StopIteration:
                break

    def projection(self, sigma):
        """Projection of a Language in an alphabet

        :returns: Language  _Lᴿ_"""

        if self.finite:
            return Language(
                [string_projection(w, sigma) for w in self.elements],
                sigma=sigma,
                finite=True,
                max=self.max,
            )
        else:
            return Language(
                gen=(self._projection, sigma),
                sigma=sigma,
                finite=False,
                max=self.max,
            )

    def _projection(self, sigma):
        seen = set()
        g1 = self.__iter__()
        while True:
            try:
                w = next(g1)
                w_ = string_projection(w, sigma)
                if not w_ in seen:
                    seen.add(w_)
                    yield w_
            except StopIteration:
                break

    def substitution(self, mapping):
        """String substitution giving a map

        :param mapping: Mapping for string subsitution
        :returns: Language with string subsitutions"""

        if self.finite:
            L_u = empty_language(sigma=mapping.sigma_)
            for w in self.elements:
                L_u = L_u.union(mapping.substitution(w))
            return Language(L_u, sigma=mapping.sigma_, finite=True, max=self.max)
        else:
            return Language(
                gen=(self._substitution, mapping),
                sigma=mapping.sigma_,
                finite=False,
                max=self.max,
            )

    def _substitution(self, mapping):
        seen = set()
        g1 = self.__iter__()
        while True:
            try:
                w = next(g1)
                for w_ in mapping.substitution(w):
                    if not w_ in seen:
                        seen.add(w_)
                        yield w_
            except StopIteration:
                break

    def reverse(self):
        """Reverse the strings of a language, if infinte returns an infinite generator

        :returns: Language  _Lᴿ_"""

        if self.finite:
            return Language(
                [w[::-1] for w in self.elements],
                sigma=self.sigma,
                finite=True,
                max=self.max,
            )
        else:
            return Language(
                gen=(self._reverse,),
                sigma=self.sigma,
                finite=False,
                max=self.max,
            )

    def _reverse(self):
        seen = set()
        g1 = self.__iter__()
        while True:
            try:
                w = next(g1)[::-1]
                if not w in seen:
                    seen.add(w)
                    yield w
            except StopIteration:
                break

    def intersection(self, L, force=True, expand_limit=None):
        """Intersection of the language with another language, if one is infintie returns an infinite generator

        :param L: Second Languauge for the intersection
        :param force: If alphabets different create a newone based on union of both
        :param expand_limit: Evaluate up to certain limit, good to pass from a partial infinite evaluation to finite if intersection lower tha _expand_limit_ value
        :returns: Language  _self ∪ L_"""
        if (not force) and self.sigma != L.sigma:
            raise AlphabetsDoNotMatch(self.sigma, L.sigma)
        sigma_ = self.sigma | L.sigma

        # Empty language case
        if self.is_empty_language():
            return empty_language(sigma=sigma_, max=max(self.max, L.max))
        if L.is_empty_language():
            return empty_language(sigma=sigma_, max=max(self.max, L.max))

        # Alpabeths are diferente
        if len(self.sigma.intersection(L.sigma)) == 0:
            return empty_language(sigma=sigma_, max=max(self.max, L.max))

        # Both finite
        if self.finite and L.finite:
            elements = self.elements.intersection(L)
            if len(elements) == 0:
                return empty_language(sigma=sigma_, max=max(self.max, L.max))
            return Language(
                elements, sigma=sigma_, finite=True, max=max(self.max, L.max)
            )
        # One infinite
        else:
            inter = Language(
                gen=(self._intersection, L),
                sigma=sigma_,
                finite=False,
                max=max(self.max, L.max),
            )
            if expand_limit:
                it = iter(inter)
                res = set()
                while len(res) < expand_limit:
                    try:
                        val = next(it)
                        res.add(val)
                    except StopIteration:
                        inter.finite = True
                        inter.gen = None
                        inter.elements = set(res)
                        break
            return inter

    def _intersection(self, L):
        seen = set()
        s1_ = set()
        s2_ = set()
        g1 = iter(self) if self.finite else self.__iter__()
        g2 = iter(L) if L.finite else L.__iter__()
        while g1 or g2:
            if g1:
                try:
                    w = next(g1)
                    s1_.add(w)
                    if w in s2_:
                        if not w in seen:
                            seen.add(w)
                            yield w
                except StopIteration:
                    g1 = None
                if L.finite and len(s2_) == len(L):
                    break

            if g2:
                try:
                    w = next(g2)
                    s2_.add(w)
                    if w in s1_:
                        if not w in seen:
                            seen.add(w)
                            yield w
                except StopIteration:
                    g2 = None
                if self.finite and len(s1_) == len(self):
                    break

    def power(self, n):
        """Power of a language

        :returns: Language  _self^n_"""
        if n == 0:
            return empty_string_language(sigma=self.sigma, max=self.max)
        elif n == 1:
            return Language(self)
        else:
            # Empty language
            if self.is_empty_language():
                return empty_language(sigma=self.sigma, max=self.max)
            # Empty string language
            if self.is_empty_string_language():
                return empty_string_language(sigma=self.sigma, max=self.max)

            if self.finite:
                return Language(
                    set(p for p in self._power(self, 1, n)),
                    sigma=self.sigma,
                    finite=True,
                    max=self.max,
                )
            else:
                return Language(
                    gen=(self._power, self, 1, n),
                    sigma=self.sigma,
                    finite=False,
                    max=self.max,
                )

    def _power(self, partial, i, j):
        if i == j:
            for ele in partial:
                yield ele
        elif i < j:
            yield from self._power(self.concat(partial), i + 1, j)

    def star(self):
        """Star clouse for a language returns and infinite language

        :returns: Language  _self*_"""
        # Empty language
        if self.is_empty_language():
            return empty_string_language(sigma=self.sigma, max=self.max)
        # Empty string language
        if self.is_empty_string_language():
            return empty_string_language(sigma=self.sigma, max=self.max)

        return Language(gen=(self._star,), sigma=self.sigma, finite=False, max=self.max)

    def _star(self):
        yield ""
        prev = [""]
        seen = set([""])
        while True:
            for pre in prev:
                for ele in self:
                    new = pre + ele
                    if not new in seen:
                        prev.append(new)
                        seen.add(new)
                        yield new
            prev = []

    def plus(self):
        """Star clouse for a language returns an infinite language

        :returns: Language  _self+_"""
        # Empty language
        if self.is_empty_language():
            return empty_language(sigma=self.sigma, max=self.max)
        # Empty string language
        if self.is_empty_string_language():
            return empty_string_language(sigma=self.sigma, max=self.max)

        return Language(gen=(self._plus,), sigma=self.sigma, finite=False, max=self.max)

    def _plus(self):
        prev = []
        seen = set()
        for e in self.elements:
            prev.append(e)
            yield e
        while True:
            for pre in prev:
                for ele in self:
                    new = pre + ele
                    prev.append(new)
                    if not new in seen:
                        seen.add(new)
                        yield new
            prev = []

    def concat(self, L, force=True):
        """Concatenation of the language with another language, if one is infintie returns an infinite generator

        :param L: Second Languauge fo the concatenation
        :param force: If alphabets different create a newone based on union of both
        :returns: Language  _self L_"""
        if (not force) and self.sigma != L.sigma:
            raise AlphabetsDoNotMatch(self.sigma, L.sigma)
        sigma_ = self.sigma | L.sigma

        # Empty language case
        if self.is_empty_language():
            return empty_language(sigma=sigma_, max=self.max)
        if L.is_empty_language():
            return empty_language(sigma=sigma_, max=self.max)

        # Empty string language case
        if self.is_empty_string_language():
            return Language(L)
        if L.is_empty_string_language():
            return Language(self)

        # Both finite
        if self.finite and L.finite:
            return Language(
                [w1 + w2 for w2 in L for w1 in self],
                sigma=sigma_,
                finite=True,
                max=max(self.max, L.max),
            )
        # One infinite
        else:
            return Language(
                gen=(self._concat, L),
                sigma=sigma_,
                finite=False,
                max=max(self.max, L.max),
            )

    def _concat(self, L):
        seen = set()
        for w2 in L:
            for w1 in self:
                new = w1 + w2
                if not new in seen:
                    seen.add(new)
                    yield w1 + w2


# Operations for strings
def string_substitution(w, mapping):
    return mapping.substitution(w)


def string_projection(w, sigma):
    if len(w) == 0:
        return ""
    else:
        a = w[-1]
        w_ = w[:-1]
        if a in sigma:
            return string_projection(w_, sigma) + a
        else:
            return string_projection(w_, sigma)


def string_right_quotient(w, b):
    if len(w) == 0:
        return ""
    else:
        a = w[-1]
        w_ = w[:-1]
        if a == b:
            return w_
        else:
            return ""


def string_left_quotient(w, b):
    if len(w) == 0:
        return ""
    else:
        a = w[0]
        w_ = w[1:]
        if a == b:
            return w_
        else:
            return ""


def string_right_cancellation(w, b):
    if len(w) == 0:
        return ""
    else:
        a = w[-1]
        w_ = w[:-1]
        if a == b:
            return w_
        else:
            return string_right_cancellation(w_, b)


def string_left_cancellation(w, b):
    if len(w) == 0:
        return ""
    else:
        a = w[0]
        w_ = w[1:]
        if a == b:
            return w_
        else:
            return string_left_cancellation(w_, b)


# Notable languages
def empty_language(sigma=[], max=20):
    return Language([], sigma=sigma, finite=True, max=max)


def empty_string_language(sigma=[], max=20):
    return Language([""], sigma=sigma, finite=True, max=max)
