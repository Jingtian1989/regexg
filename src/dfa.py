__author__ = 'ZhangJingtian'
import util
import nfa

class DState(object):
    def __init__(self, states):
        super(DState, self).__init__()
        self.states = states
        self.flag    = 0

    def setFlag(self, flag):
        self.flag = flag

    def isStart(self):
        for state in self.states:
            if state.type == nfa.State.START:
                return True
        return False

    def isAccept(self):
        for state in self.states:
            if state.type == nfa.State.ACCEPT:
                return True
        return False

    def __str__(self):
        s = "["
        for i in range(len(self.states) - 1):
            s = s + str(self.states[i]) + ","
        s = s + str(self.states[len(self.states) - 1]) + "]"
        return s

class DTran(object):
    def __init__(self, dstate):
        super(DTran, self).__init__()
        self.dstate     =   dstate
        self.todstates  =   dict()
    def addToState(self, tok, dstate):
        self.todstates[str(tok)] = dstate

    def getToState(self, tok):
        return self.todstates.get(str(tok))

    def __str__(self):
        return str(self.dstate)

class DTranTable(object):
    def __init__(self):
        super(DTranTable, self).__init__()
        self.dtrans = dict()
    def addDTran(self, dstate1, dstate2, tok):
        dtran = DTran(dstate1)
        if self.dtrans.get(str(dtran)) is not None:
            self.dtrans.get(str(dtran)).addToState(tok, dstate2)
        else:
            dtran.addToState(tok, dstate2)
            self.dtrans[str(dtran)] = dtran
    def getDTran(self, dstate):
        return self.dtrans.get(str(DTran(dstate)))

class DFA(object):
    def __init__(self, start = None, dtrans = None):
        super(DFA, self).__init__()
        self.dstart     = start
        self.dtrantable = dtrans

    def acceptString(self, s):
        dstate = self.dstart
        prestate = util.Stack()
        for ch in s:
            dtran = self.dtrantable.getDTran(dstate)
            if dtran != None:
                prestate.push(dstate)
                dstate = dtran.getToState(ch)
                if dstate == None:
                    break
            else:
                break

        if dstate != None and dstate.isAccept():
            print("accept string %s."%(s[0:prestate.size()]))
        else:
            dstate = prestate.pop()
            while dstate != None and dstate.isAccept() == False:
                dstate = prestate.pop()
            if dstate != None and dstate.isAccept():
                print("accept string %s."%(s[0:prestate.size()]))
            else:
                print("do not acceptt string %s."%(s))


class DFAConverter(object):
    def __init__(self):
        super(DFAConverter, self).__init__()

    def epsClosure(self, states):
        stack   = util.Stack(states)
        eps     = list()
        eps     +=states

        if len(states) == 0:
            return None

        while stack.isEmpty() == False:
            s = stack.pop()
            for e in s.eout:
                if (e.type == nfa.Edge.EPSILON):
                    if (e.s2 in eps) is False:
                        eps.append(e.s2)
                        stack.push(e.s2)
        dstate = DState(eps)
        return dstate

    def __hashFlag(self, dstates, flag):
        for dstate in dstates:
            if dstate.flag == flag:
                return dstate
        return None

    def move(self, dstate, tok):
        dst = list()
        for state in dstate.states:
            for edge in state.eout:
                if edge.tok == tok:
                    dst.append(edge.s2)
        return dst


    def convertToDFA(self, toks, nfa):
        dstates     = dict()
        dtrantable  = DTranTable()
        dstate0     = self.epsClosure([nfa.start])
        dstates[str(dstate0)] = dstate0
        dstate = self.__hashFlag(dstates.values(), 0)

        while dstate != None:
            dstate.setFlag(1)
            for tok in toks:
                u = self.epsClosure(self.move(dstate, tok))
                if u != None:
                    if dstates.get(str(u)) == None:
                        dstates[str(u)] = u
                    dtrantable.addDTran(dstate, u, tok)
            dstate = self.__hashFlag(dstates.values(), 0)
        return DFA(dstate0, dtrantable)

if __name__ == "__main__":
    #lexer   = nfa.Lexer("(ab)*")
    lexer   = nfa.Lexer("a*b|b|c?b")
    parser  = nfa.Parser(lexer)
    expr    = parser.expr()
    n       = expr.gen()
    converter = DFAConverter()
    dfa = converter.convertToDFA(lexer.getCharSet(), n)
    #dfa.acceptString("abababab")
    dfa.acceptString("cbaaaaaabcd")
    print("ok.")


