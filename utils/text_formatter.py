def format_puzzle_text(text, max_chars_per_line=50):
    """
    Formata o texto do puzzle para caber na tela
    
    Args:
        text (str): Texto original
        max_chars_per_line (int): Número máximo de caracteres por linha
        
    Returns:
        str: Texto formatado
    """
    # Remove espaços extras e quebras de linha
    text = ' '.join(text.split())
    
    words = text.split(' ')
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        # Se adicionar a palavra exceder o limite
        if current_length + len(word) + 1 > max_chars_per_line:
            # Adiciona a linha atual à lista de linhas
            if current_line:
                lines.append(' '.join(current_line))
            # Começa uma nova linha com a palavra atual
            current_line = [word]
            current_length = len(word)
        else:
            # Adiciona a palavra à linha atual
            current_line.append(word)
            current_length += len(word) + 1
    
    # Adiciona a última linha
    if current_line:
        lines.append(' '.join(current_line))
    
    return '\n'.join(lines) 