def notitas_explicativas_mult_col():
    """
    suponiendo que se selecciona la columna ABC del archivo csv o de excel:
    
    cadena = cadena.upper() 
    resultado = 0

    for letra in cadena:
        if 'A' <= letra <= 'Z':
            valor_letra = ord(letra) - ord('A') + 1
            resultado = resultado * 26 + valor_letra

    en el contenido de la funcion primero se declara la cadena en mayuscula que toma como argumento y luego el resultado 
    con un valor de 0, en el ciclo se itera en cada caracter de la cadena, tomando el ejemplo de la cadena dada anteriormente;
    primero se toma la letra A, esta en su valor numerico unicode (que es lo que toma la funcion ord) tiene el numero 65, a
    esta se le resta el valor del primer numero del abecedario que pues es A asi que A - A o 65-65 = 0, pero se le suma 1,
    este es el valor de 'valor_letra' al resultado que antes fue declarado como 0 se le actualiza su valor, multiplicando 
    su actual valor que en este caso es 0, se multiplica por 26, ya que este es el numero de columna al que equivale la Z
    en una hoja de excel, pero como el resultado aún es 0 el resultado de la multiplicacion tambien da 0, mas el valor  de la
    letra es de 1, por lo tanto queda en 1, la siguiente letra es la B, esta por logica su valor es de 66, menos 65 + 1 
    es 2, resultado ya vale 1, multiplicado por 26 es 26, y más valor_letra ahora es 28, ahora con la letra c, ya sabemos
    que esta tendrá el valor de 3, resultado:28 * 26 = 728 + 3 = 731.

    'valor_letra' se saca de esa forma para que las letras terminen con un valor equivalente al de las columnas en excel,
    A:65 - a:65 = 0 + 1= 1, la a es la primer columna en el archivo de excel, y si se sigue aplicando lo mismo pero remplazando
    la primera letra por el resto se obtenrá el valor de cada letra en la hoja.

    cuando se habla de A ya sabemos que nos referimos a la columna 1, pero si decimos AA la primera A se convierte en el valor
    de la z, que es 26, porque significa que ya dimos la vuelta completa al abecedario sobrepasando la z, entonces se tiene que
    contar de nuevo, la primera A ahora esta indicando que llevamos la primer vuelta terminada, por lo que el valor de la 
    segunda letra se le tiene que ir sumando al valor de z o a 26, AAA la primera A indica que ya dimos las 26 vueltas al
    abecedario, por eso al resultado se le multiplica 26, osea, AA es, 26 letras recoridas o una vuelta al abecedario mas
    la posicion actual despues de la primera vuelta, y AAA es lo mismo pero ahora todo multiplicado por 26 veces que se ah 
    hecho lo mismo.
    una cosa más, esta funcion solo se puede llamar si son más de 2 letras, ya que la forma correcta de llamar la primer 
    columna de un array es con el indice 0, pero aquí toma A con el valor de 1, pero cuando hablamos de 2 columnas es 
    necesario ahora tomar la primer columna como 1
    """