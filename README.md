# regexg

regexg is a simple regex engine based on a self defined grammer. 

# How it works

regexg build the AST from input and transform AST to NFA, NFA and DFA by
McMaughton-Yamada-Thompson alogrithm and Subset Construction alogrithm. 

# Demo

In the source code I demonstrate a simple string accept function that execute on the transition 
table of the DFA and find out the sentence that meet the regex rule. 

# The Supported Grammer

	expr	->	orterm
	orterm	-> 	orterm'|'andterm | andterm
	andterm	-> 	andterm unary | ε
	unary	->	unary'*' | unary'+' | unary'?' | factor
	factor	->	char | '('expr')'
	char	->	a...zA...Z0...9