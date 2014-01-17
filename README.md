A Simple Regex Engine For Fun.
===================================================

The Supported Grammer
--------------------------------------------------- 
	expr	->	orterm
	orterm	-> 	orterm'|'andterm | andterm
	unary	->	unary'*' | unary'+' | unary'?' | factor
	factor	->	char | '('expr')'
	char	->	a...zA...Z0...9