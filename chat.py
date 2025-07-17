import os
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chat_history = []

def chat_with_bot(message, history):

    try:
        # Eğer history boşsa, boş liste olarak başlat
        if not history:
            internal_history = []
        else:
            internal_history = []
            for i in range(0, len(history), 2):
                user_msg = history[i]["content"]
                bot_msg = history[i+1]["content"]
                internal_history.append((user_msg, bot_msg))
        
        messages = [{"role": "system", "content": "Sen yardımcı bir asistansın. Türkçe sorulara Türkçe, İngilizce sorulara İngilizce yanıt ver."}]
        
        for human_msg, bot_msg in internal_history:
            messages.append({"role": "user", "content": human_msg})
            messages.append({"role": "assistant", "content": bot_msg})
        
        messages.append({"role": "user", "content": message})
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        bot_response = response.choices[0].message.content
        
        
        internal_history.append((message, bot_response))
        
        formatted_history = []
        for human_msg, bot_msg in internal_history:
            formatted_history.append({"role": "user", "content": human_msg})
            formatted_history.append({"role": "assistant", "content": bot_msg})
        
        return "", formatted_history
        
    except Exception as e:
        error_msg = f"Hata oluştu: {str(e)}"
        internal_history.append((message, error_msg))
        
        formatted_history = []
        for human_msg, bot_msg in internal_history:
            formatted_history.append({"role": "user", "content": human_msg})
            formatted_history.append({"role": "assistant", "content": bot_msg})
        
        return "", formatted_history

def clear_chat():
 
    return [], []

with gr.Blocks(title="Mini Chatbot", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 Mini Chatbot")
    gr.HTML(
        """
        <style>
        .sparkle {
            color: #f0c420;
            font-weight: bold;
            position: relative;
            display: inline-block;
            animation: sparkle-animation 2s infinite;
        }
        @keyframes sparkle-animation {
            0%, 100% { text-shadow: 0 0 5px #f0c420, 0 0 10px #f0c420, 0 0 20px #f0c420; }
            50% { text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #f0c420; }
        }
        .stars {
            position: relative;
            display: inline-block;
        }
        .stars::before, .stars::after {
            content: "✨🌸✨";
            position: absolute;
            animation: stars-move 3s linear infinite;
            font-size: 1.2em;
            opacity: 0.8;
        }
        .stars::before {
            top: -10px;
            left: -20px;
            animation-delay: 0s;
        }
        .stars::after {
            top: 10px;
            right: -20px;
            animation-delay: 1.5s;
        }
        @keyframes stars-move {
            0% { transform: translateX(0) translateY(0) rotate(0deg); opacity: 0.8; }
            50% { opacity: 1; }
            100% { transform: translateX(20px) translateY(-10px) rotate(360deg); opacity: 0.8; }
        }
        </style>
        <div class="stars">
            <span class="sparkle">Elif'in OpenAI GPT-3.5-turbo ile güçlendirilmiş sohbet botu</span>
        </div>
        """
    )
    
    chatbot = gr.Chatbot(
        value=[],
        height=400,
        show_label=False,
        container=True,
        type="messages"
    )
    
    with gr.Row():
        msg = gr.Textbox(
            placeholder="Mesajınızı buraya yazın...",
            show_label=False,
            scale=4,
            container=False
        )
        send_btn = gr.Button("Gönder", variant="primary", scale=1)
    
    with gr.Row():
        clear_btn = gr.Button("Sohbeti Temizle", variant="secondary")

    msg.submit(chat_with_bot, inputs=[msg, chatbot], outputs=[msg, chatbot])
    send_btn.click(chat_with_bot, inputs=[msg, chatbot], outputs=[msg, chatbot])
    clear_btn.click(clear_chat, outputs=[chatbot, chatbot])
    
    msg.submit(lambda: "", outputs=msg)

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  UYARI: OPENAI_API_KEY ortam değişkeni bulunamadı!")
        print("Lütfen .env dosyasını oluşturun ve OpenAI API anahtarınızı ekleyin.")
        exit(1)
    
    print("🤖 Chatbot başlatılıyor...")
    demo.launch(
        server_name="0.0.0.0",
        server_port=7861,
        share=True,
        show_error=True,
        quiet=False,
        inbrowser=True
    )
