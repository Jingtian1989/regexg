# regexg

regexg is a simple regex engine based on a self defined grammer. 

regexg build the AST of the input regex and then translate it to a NFA by the  McMaughton-Yamada-Thompson alogrithm and then to a DFA by the subset construction alogrithm.

In the source code I demonstrate a simple string accept function that execute on the transition table of the DFA and find out the sentence that meet the regex rule.  

The Supported Grammer
--------------------------------------------------- 
	expr	->	orterm
	orterm	-> 	orterm'|'andterm | andterm
	andterm	-> 	andterm unary | ε
	unary	->	unary'*' | unary'+' | unary'?' | factor
	factor	->	char | '('expr')'
	char	->	a...zA...Z0...9