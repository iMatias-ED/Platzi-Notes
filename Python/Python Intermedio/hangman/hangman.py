from random import choice

def presentation( word: str ):
    for letter in word:
        if letter != "\n": 
            word = word.replace( letter, 'X ' )

    print (f''' 
 _                                             
| |                                            
| |__   __ _ _ __   __ _ _ __ ___   __ _ _ __  
| '_ \ / _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
| | | | (_| | | | | (_| | | | | | | (_| | | | |
|_| |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_| 
                    __/ |                      
                   |___/

                    _______
                    |/      |
                    |      (_)
                    |      \|/
                    |       |
                    |      | |
                    |      
                   _|___

-----------------------------------------------

    Adivina la palabra: { word }

-----------------------------------------------

    ''')

def run():
 
    with open('./hangman_data.txt', 'r', encoding='utf-8') as data:
        selected_word = choice( data.readlines() )
        # print( selected_word )
        data.close();
    presentation( selected_word )

    user_inputs = []

    while True:
        user_inputs.append( input( 'Ingresa una letra: ' ) ) 
        masked = selected_word

        for letter in selected_word: 
            if letter not in user_inputs and letter != "\n" :
                masked = masked.replace( letter, 'X' )

        print( masked )

        if masked == selected_word:
            print( "Ganaste!" )
            break
        
if __name__ == "__main__":
    run()