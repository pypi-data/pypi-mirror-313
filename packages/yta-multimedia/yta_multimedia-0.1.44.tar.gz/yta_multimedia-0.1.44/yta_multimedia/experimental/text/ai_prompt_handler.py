from yta_multimedia.experimental.text.gemini_ai import GeminiAI


class AIPromptHandler:
    def __init__(self):
        self.gemini = GeminiAI()

    def generate_youtube_video_title_from_idea(self, idea: str):
        """
        Generates a Youtube video title from a prompt idea. This
        method will return the title as a string, nothing else.
        """
        # TODO: Clean, remove quotes, etc.
        prompt = 'Quiero crear un vídeo que hable sobre "' + idea + '". Necesito que generes un título que sea llamativo para que yo pueda utilizarlo en Youtube para este vídeo. El título debe atraer la atención del público, y debe tener como máximo 60 caracteres. Solo quiero que me respondas con una opción, y que tu respuesta sea única y exclusívamente el título del vídeo. No me digas que aquí tienes alguna opción ni nada por el estilo. Solo el título. Devuélveme solo la frase con el título.'

        response = self.gemini.ask(prompt)
        # TODO: Remove '*' from the generated text

        return response
    
    def generate_youtube_video_description_from_idea(self, idea: str):
        """
        Generates a Youtube video description from a prompt 
        idea. This method will return the title as a string,
        nothing else.
        """
        # TODO: Clean, remove quotes, etc.
        prompt = 'Quiero crear un vídeo que hable sobre la idea "' + idea + '". Necesito que generes una descripción que sea llamativa para que pueda utilizarlo en Youtube para ese vídeo. La descripción debe utilizar palabras clave relacionadas con la idea anterior, debe tener como máximo 300 o 400 caracteres, y debe estar dirigido hacia, primero, explicar un poco de lo que se habla en el vídeo sin decir exactamente lo que ocurre, creando hype, y segundo, estar potenciada y orientada hacia el SEO para que salga como resultados de búsqueda. Solo quiero que me respondas con una opción, y que tu respuesta sea única y exclusívamente la descripción del vídeo. No me digas que aquí tienes alguna opción ni nada por el estilo. Solo la descripción, de entre 300 y 400 caracteres. Devuélveme solo la descripción.'

        response = self.gemini.ask(prompt)
        # TODO: Remove '*' from the generated text

        return response

    def summarize_text(self, text: str, number_of_chars: int = None):
        """
        This method will summarize the provided 'text' to a new one
        with the also provided 'number_of_char' characters. If not
        provided, it will use the 20% of the 'text' characters
        amount. It returns the summarized text.

        Depending on the text, the minimum 'number_of_chars' should
        be 100 or a 10% of the provided text. Shorter texts could 
        inaccurate. The system is not able to guarantee the 
        'number_of_chars' amount of characters. It could be a huge
        difference between the desired one and the returned by this
        method.
        """
        # TODO: Clean, remove quotes, etc.
        if not number_of_chars:
            number_of_chars = 0.2 * len(text)
        number_of_chars = int(number_of_chars)

        prompt = 'Quiero que me resumas el siguiente texto: "' + text + '". Quiero que mantengas correctamente la idea inicial pero que el texto que me des esté resumido. El resumen que hagas debe contener específicamente ' + str(number_of_chars) + ' caracteres. Solo quiero que me respondas con una opción, y que tu respuesta sea única y exclusivamente el texto ya resumido. No me digas que aquí tienes alguna opción ni nada por el estilo. Solo el texto resumido, de ' + str(number_of_chars) + ' caracteres. Devuélveme solo el texto ya resumido.'

        response = self.gemini.ask(prompt)
        # TODO: Remove '*' from the generated text

        return response

    def rewrite_text(self, text: str):
        # TODO: More checkings (?)
        if not text:
            raise Exception('No "text" provided.')

        prompt = 'Eres un experto en reescribir textos. Obtienes un texto y eres capaz de convertirlo a otro que mantiene la esencia, que transmite la idea, que respeta la estructura pero que está escrito de una forma completamente distinta aunque la información que se dice es la misma. Quiero que reescribas el texto que te voy a pasar. Quiero que respetes la idea y el estilo del texto, pero que lo reescribas con el mismo número de palabras si es posible, pero con palabras distintas para que no se sepa cómo era el texto original. Solo quiero que me respondas con una opción, y que tu respuesta sea única y exclusivamente el texto ya reescrito. No me digas que aquí tienes alguna opción ni nada por el estilo. Solo el texto reescrito, de más o menos el mismo número de palabras y caracteres. Devuélveme solo el texto reescrito. El texto a reescribir es el siguiente: "' + text + '".'

        response = self.gemini.ask(prompt)
        # TODO: Remove '*' from the generated text

        return response

    def idea_to_text(self, idea: str, number_of_chars: int):
        """
        This method generates a complete text from the provided 'idea'.
        """
        # TODO: Clean the idea text
        if not number_of_chars:
            number_of_chars = 4000

        prompt = 'Eres un experto en redacción de guiones para narrar en vídeos de Youtube. A partir de una idea eres capaz de generar un texto súper completo y largo para poder narrar en el vídeo de Youtube y que la gente pueda disfrutarlo. Vas a recibir una idea y vas a generar todo el texto para ser narrado. Eres capaz de, primero, dar una introducción a los espectadores para que entiendan de qué se va a hablar. Después, entras a fondo en el tema y profundizas, dando detalles muy importantes e interesantes sobre la idea que se te va a pasar, y por último concluyes con un desenlace increíble para poner la guinda al guion del vídeo. Solo quiero que me respondas con una opción, y que tu respuesta sea única y exclusivamente el texto ya escrito. No me digas que aquí tienes alguna opción ni nada por el estilo. Solo el texto que has generado, sin ser repetitivo y con ' + str(number_of_chars) + ' caracteres de longitud. Devuélveme solo el texto. La idea de la que quiero que generes el texto es la siguiente: "' + idea + '".'

        response = self.gemini.ask(prompt)
        # TODO: Remove '*' from the generated text

        return response