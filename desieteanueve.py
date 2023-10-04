# Lee la consulta booleana Q
def read_boolean_query():
    return input("Ingrese la consulta booleana (Q): ")

# Aplica stopword y stemming a la consulta Q
def preprocess_query(query):
    stop_words = set(stopwords.words('spanish'))
    ps = PorterStemmer()
    
    words = word_tokenize(query)
    filtered_words = [ps.stem(word) for word in words if word.lower() not in stop_words]
    
    return ' '.join(filtered_words)

# Aplica la notación posfijo para el procesamiento de la consulta
def infix_to_postfix(expression):
    precedence = {'and': 1, 'or': 0}

    def is_operator(token):
        return token in ['and', 'or']

    def higher_precedence(op1, op2):
        return precedence[op1] > precedence[op2]

    tokens = expression.split()
    output = []
    stack = []

    for token in tokens:
        if token not in ['and', 'or']:
            output.append(token)
        else:
            while stack and is_operator(stack[-1]) and higher_precedence(stack[-1], token):
                output.append(stack.pop())
            stack.append(token)

    while stack:
        output.append(stack.pop())

    return ' '.join(output)

