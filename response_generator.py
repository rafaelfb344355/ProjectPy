from transformers import pipeline

gerador_respostas = pipeline("text-generation", model="google/gemma-4-E2B")

def generate_response(sentiment, review_cliente, product):

      prompt = f"""
          Você é um assistente de atendimento ao cliente prestativo e educado.
          A avaliação do cliente possui um sentimento {sentiment}.
          Escreva uma resposta curta e profissional para a seguinte avaliação de um cliente:
          "{review_cliente}"
          Resposta:
              """
      resultado = gerador_respostas(prompt, max_new_tokens=150)
      return resultado[0]['generated_text']) 

        
        

    
   
