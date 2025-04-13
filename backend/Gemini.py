import os
import google.generativeai as genai
from dotenv import load_dotenv
from eco_personality import EcoPersonality
import time
from pathlib import Path

class EcoAISystem:
    def __init__(self):
        """初始化熊大AI系统"""
        self.persona = self._init_personality()
        self.model = self._init_gemini()
        self.last_interaction = time.time()
        self.help_commands = {
            "Forest knowledge": "Get ecological facts from Bear",
            "Patrol forest": "Start forest adventure mini-game", 
            "Bear story": "Hear a forest protection story",
            "Bear quiz": "Take an ecology quiz",
            "Bear hungry": "Get eco-friendly food suggestions",
            "My impact": "Check your CO₂ reduction progress"
        }

    def _init_personality(self):
        """初始化熊大人格"""
        try:
            return EcoPersonality()
        except Exception as e:
            raise RuntimeError(f"🐻❌ 人格初始化失败: {str(e)}")

    def _init_gemini(self):
        """初始化Gemini模型"""
        try:
            env_path = Path(__file__).parent / 'API.env'
            print(f"🌲 正在加载环境文件: {env_path}")

            if not env_path.exists():
                raise FileNotFoundError(f"❌ 环境文件不存在: {env_path}")
            
            load_dotenv(env_path)
            print("🌲 环境变量加载成功")
            
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("❌ 未找到API密钥")
            genai.configure(api_key=api_key)
            return genai.GenerativeModel('gemini-2.0-flash')
        except Exception as e:
            raise RuntimeError(f"🤖❌ 模型加载失败: {str(e)}")

    # Modify the process_query method
    def process_query(self, user_input):
        try:
            # Help command (keep in English)
            if user_input.lower() == "help":
                return self._show_help()

            # Achievement check
            if user_input.lower() == "my impact":  # Changed from "my progress"
                return f"🌍 You've reduced {self.persona.carbon_offset}kg CO₂! ({self.persona._get_equivalent(self.persona.carbon_offset)})"            # Special commands
            processed = self.persona.process_input(user_input)
            if 'error' in processed:
                return f"🐻💢 {processed['error']}"

            # Direct command resultss
            if any(cmd in user_input for cmd in ["熊大讲故事", "Bear story", "巡逻森林", "Patrol forest", "熊大考考你", "Bear quiz", "熊大饿了", "Bear hungry"]):
                return processed['processed']

            # Normal AI response with language matching
            lang = getattr(self.persona, 'current_lang', 'en')
            prompt = {
                'zh': f"请用熊大的口吻用中文回答（用'俺'自称，带🌲🐻表情）: {processed['processed']}",
                'en': f"Respond as Bear Guardian in English (use 'I' and forest emojis): {processed['processed']}"
            }[lang]
            
            response = self.model.generate_content(prompt)
            return self.persona.format_response(response.text)['display']

        except Exception as e:
            return f"🐻❌ 出错啦: {str(e)}\n输入'help'查看可用命令"

    def _show_help(self):
        """Show help information in English"""
        help_text = "🐻 I can help you with:\n"
        for cmd, desc in self.help_commands.items():
            help_text += f"- {cmd}: {desc}\n"
        help_text += "\n🌲 Try 'Bear story' or 'Patrol forest' to start playing!"
        return help_text

def main():
    print("""
    ==========================================
       🌳 Forest Guardian Bear AI v2.0 🐻
    Type 'help' for commands
    Type 'exit' to quit
    ==========================================
    """)

    try:
        ai = EcoAISystem()
        print("🐻 I'm Bear Guardian, protector of the forest! How can I help you today?")

        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() == 'exit':
                    print("🐻 Remember to visit the forest often! Goodbye~")
                    break
                
                response = ai.process_query(user_input)
                print("\nBear:", response)
                
            except KeyboardInterrupt:
                print("\n🐻💤 Detected you're leaving... remember to turn off lights to save energy!")
                break
                
    except Exception as e:
        print(f"💥 系统启动失败: {str(e)}")
        print("检查步骤:")
        print("1. 确认.env文件有GEMINI_API_KEY")
        print("2. 网络连接正常")
        print("3. 重新运行程序")

if __name__ == "__main__":
    main()