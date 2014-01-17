__author__ = 'ZhangJingtian'

class Tag(object):
    ZEROMORE     = 1
    ZEROONE      = 2
    ONEMORE      = 3
    OR           = 4
    CHAR         = 5
    LEFTBRACKET  = 6
    RIGHTBRACKET = 7

class Token(object):

    def __init__(self, ch, tag):
        super(Token, self).__init__()
        self.ch     = ch
        self.tag    = tag
    def __str__(self):
        return self.ch

class Lexer(object):
    ZEROMORE        = Token('*', Tag.ZEROMORE)
    ZEROONE         = Token('?', Tag.ZEROONE)
    ONEMORE         = Token('+', Tag.ONEMORE)
    OR              = Token('|', Tag.OR)
    LEFTBRACKET     = Token('(', Tag.LEFTBRACKET)
    RIGHTBRACKET    = Token(')', Tag.RIGHTBRACKET)
    def __init__(self, text):
        super(Lexer, self).__init__()
        self.text       = text
        self.currpos    = -1
        self.words      = dict()

    def reserve(self, token):
        self.words[token.ch] = token

    def __readchar(self):
        if self.currpos < len(self.text) - 1:
            self.currpos = self.currpos + 1
            return self.text[self.currpos]
        else:
            return None

    def scan(self):
        c = self.__readchar()
        if c == '*':
            return Lexer.ZEROMORE
        elif c == '?':
            return Lexer.ZEROONE
        elif c == '+':
            return Lexer.ONEMORE
        elif c == '|':
            return Lexer.OR
        elif c == '(':
            return Lexer.LEFTBRACKET
        elif c == ')':
            return Lexer.RIGHTBRACKET
        elif c == None:
            return None
        else:
            if self.words.get(c) == None:
                self.reserve(Token(c, Tag.CHAR))
            return self.words.get(c)

    def getCharSet(self):
        return self.words.values()

class Edge(object):
    NORMAL  = 1
    EPSILON = 2
    def __init__(self, s1, s2, tok, type):
        super(Edge, self).__init__()
        self.s1     = s1
        self.s2     = s2
        self.tok    = tok
        self.type   = type

    def setFromState(self, s):
        self.s1 = s

    def setToState(self, s):
        self.s2 = s


class State(object):
    START   = 1
    ACCEPT  = 2
    NORMAL  = 3

    def __init__(self, type, num):
        super(State, self).__init__()
        self.type = type
        self.num  = num
        self.ein  = list()
        self.eout = list()

    def setType(self, type):
        self.type = type

    def addComeinEdge(self, e):
        self.ein.append(e)

    def rmComeinEdge(self, e):
        self.ein.remove(e)

    def addComeoutEdge(self, e):
        self.eout.append(e)

    def rmComeoutEdge(self, e):
        self.eout.remove(e)

    def __str__(self):
        return str(self.num)



class NFA(object):
    def __init__(self, start, accept):
        super(NFA, self).__init__()
        self.start  = start
        self.accept = accept


class NFABuilder(object):
    stateNum    = 1
    epsilon     = Token('', Tag.CHAR)
    def __init__(self):
        super(NFABuilder, self).__init__()
    @classmethod
    def genNumber(clz):
        clz.stateNum = clz.stateNum + 1
        return clz.stateNum

    @classmethod
    def buildCharNFA(clz, tok):
        start   = State(State.START, clz.genNumber())
        accept  = State(State.ACCEPT, clz.genNumber())
        edge    = Edge(start, accept, tok, Edge.NORMAL)
        start.addComeoutEdge(edge)
        accept.addComeinEdge(edge)
        return NFA(start, accept)

    @classmethod
    def buildOrNFA(clz, n1, n2):
        n1.start.setType(State.NORMAL)
        n2.start.setType(State.NORMAL)
        start   = State(State.START, clz.genNumber())
        edge1   = Edge(start, n1.start, NFABuilder.epsilon, Edge.EPSILON)
        edge2   = Edge(start, n2.start, NFABuilder.epsilon, Edge.EPSILON)
        start.addComeoutEdge(edge1)
        start.addComeoutEdge(edge2)
        n1.start.addComeinEdge(edge1)
        n2.start.addComeinEdge(edge2)

        n1.accept.setType(State.NORMAL)
        n2.accept.setType(State.NORMAL)
        accept  = State(State.ACCEPT, clz.genNumber())
        edge3   = Edge(n1.accept, accept, NFABuilder.epsilon, Edge.EPSILON)
        edge4   = Edge(n2.accept, accept, NFABuilder.epsilon, Edge.EPSILON)
        accept.addComeinEdge(edge3)
        accept.addComeinEdge(edge4)
        n1.accept.addComeoutEdge(edge3)
        n2.accept.addComeoutEdge(edge4)
        return NFA(start, accept)

    @classmethod
    def buildAndNFA(clz, n1, n2):
        for e in n1.accept.ein:
            n2.start.addComeinEdge(e)
            e.setToState(n2.start)
        n2.start.setType(State.NORMAL)
        return NFA(n1.start, n2.accept)

    @classmethod
    def __buildPureNFA(clz, n):
        start = State(State.START, clz.genNumber())
        e1 = Edge(start, n.start, NFABuilder.epsilon, Edge.EPSILON)
        start.addComeoutEdge(e1)
        n.start.setType(State.NORMAL)
        n.start.addComeinEdge(e1)

        accept  = State(State.ACCEPT, clz.genNumber())
        e2 = Edge(n.accept, accept, NFABuilder.epsilon, Edge.EPSILON)
        accept.addComeinEdge(e2)
        n.accept.setType(State.NORMAL)
        n.accept.addComeoutEdge(e2)
        return NFA(start, accept)

    @classmethod
    def buildOneMoreNFA(clz, n):
        pn = clz.__buildPureNFA(n)

        e3 = Edge(n.accept, n.start, NFABuilder.epsilon, Edge.EPSILON)
        n.start.addComeinEdge(e3)
        n.accept.addComeoutEdge(e3)
        return pn

    @classmethod
    def buildZeroOne(clz, n):
        pn = clz.__buildPureNFA(n)

        e4 = Edge(pn.start, pn.accept, NFABuilder.epsilon, Edge.EPSILON)
        pn.start.addComeoutEdge(e4)
        pn.accept.addComeinEdge(e4)
        return pn

    @classmethod
    def buildZeroMoreNFA(clz, n):
        pn = clz.buildOneMoreNFA(n)

        e4 = Edge(pn.start, pn.accept, NFABuilder.epsilon, Edge.EPSILON)
        pn.start.addComeoutEdge(e4)
        pn.accept.addComeinEdge(e4)
        return pn


class Node(object):
    def __init__(self):
        super(Node, self).__init__()
    def gen(self):
        pass

class Char(Node):
    def __init__(self, tok):
        super(Char, self).__init__()
        self.tok = tok
    def gen(self):
        return NFABuilder.buildCharNFA(self.tok)

class Or(Node):
    def __init__(self, n1, n2):
        super(Or, self).__init__()
        self.n1 = n1
        self.n2 = n2
    def gen(self):
        return NFABuilder.buildOrNFA(self.n1.gen(), self.n2.gen())

class And(Node):
    def __init__(self, n1, n2):
        super(And, self).__init__()
        self.n1 = n1
        self.n2 = n2
    def gen(self):
        return NFABuilder.buildAndNFA(self.n1.gen(), self.n2.gen())

class Unary(Node):
    def __init__(self, tok, n):
        super(Unary, self).__init__()
        self.tok    = tok
        self.n      = n
    def gen(self):
        if self.tok.tag == Tag.ONEMORE:
            return NFABuilder.buildOneMoreNFA(self.n.gen())
        elif self.tok.tag == Tag.ZEROMORE:
            return NFABuilder.buildZeroMoreNFA(self.n.gen())
        elif self.tok.tag == Tag.ZEROONE:
            return NFABuilder.buildZeroOne(self.n.gen())
        else:
            return None

class Parser(object):
    def __init__(self, lexer):
        super(Parser, self).__init__()
        self.lexer = lexer
        self.look  = None
        self.move()

    def move(self):
        self.look = self.lexer.scan()

    def error(self, err):
        raise Exception(err)

    def match(self, t):
        if self.look == None or self.look != t:
            self.error("syntax error.")
        else:
            self.move()

    def expr(self):
        x = self.orterm()
        return x

    def orterm(self):
        x = self.andterm()
        while self.look != None and self.look.tag == Tag.OR:
            self.move()
            x = Or(x, self.andterm())
        return x

    def andterm(self):
        x = self.unary()
        if self.look != None and self.look.tag != Tag.RIGHTBRACKET and self.look.tag != Tag.OR:
            return And(x, self.andterm())
        return x

    def unary(self):
        x = self.factor()
        while self.look != None and (self.look.tag == Tag.ZEROMORE or self.look.tag == Tag.ONEMORE or self.look.tag == Tag.ZEROONE):
            tok = self.look
            self.move()
            x = Unary(tok, x)
        return x

    def factor(self):
        x = None
        if self.look == None:
            return x
        if self.look.tag == Tag.LEFTBRACKET:
            self.move()
            x = self.expr()
            self.match(Lexer.RIGHTBRACKET)
            return x
        elif self.look.tag == Tag.CHAR:
            x = Char(self.look)
            self.move()
            return x
        else:
            return x
