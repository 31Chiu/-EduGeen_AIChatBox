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
            "zh": {
                "森林知识": "获取熊大提供的生态知识",
                "巡逻森林": "开始森林巡逻小游戏", 
                "熊大讲故事": "听熊大讲森林保护故事",
                "熊大考考你": "参加生态知识问答",
                "熊大饿了": "获取环保饮食建议",
                "我的贡献": "查看你的碳减排进度",
                "我的森林": "查看你种植的森林"
            },
            "en": {
                "Forest knowledge": "Get ecological facts from Bear",
                "Patrol forest": "Start forest adventure mini-game", 
                "Bear story": "Hear a forest protection story",
                "Bear quiz": "Take an ecology quiz",
                "Bear hungry": "Get eco-friendly food suggestions",
                "My impact": "Check your CO₂ reduction progress",
                "My forest": "View your planted forest"
            }
        }

    def _init_personality(self):
        """初始化熊大人格"""
        try:
            return EcoPersonality()
        except Exception as e:
            raise RuntimeError(f"🐻❌ Personality initialization failed: {str(e)}")

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
                raise ValueError("❌ API key not found")
            genai.configure(api_key=api_key)
            return genai.GenerativeModel('gemini-2.0-flash')
        except Exception as e:
            raise RuntimeError(f"🤖❌ Model loading failed:{str(e)}")

    # Modify the process_query method
    def process_query(self, user_input):
        try:
            # Help command
            if user_input.lower() == "help":
                return self._show_help()

            # Process input through personality system first
            processed = self.persona.process_input(user_input)
            if 'error' in processed:
                return f"🐻💢 {processed['error']}"

            # Achievement check
            if user_input.lower() in ["my impact", "我的贡献"]:
                lang = self.persona.current_lang
                if lang == "zh":
                    return f"🌍 你已减少{self.persona.carbon_offset}kg碳排放！({self.persona._get_equivalent(self.persona.carbon_offset)})"
                else:
                    return f"🌍 You've reduced {self.persona.carbon_offset}kg CO₂! ({self.persona._get_equivalent(self.persona.carbon_offset)})"

            # Direct command results
            if any(cmd in user_input for cmd in ["熊大讲故事", "Bear story", "巡逻森林", "Patrol forest", 
                                               "熊大考考你", "Bear quiz", "熊大饿了", "Bear hungry",
                                                "我的森林", "My forest"]):
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
            return f"🐻❌ Error occurred: {str(e)}\nType 'help' for available commands"

    def _show_help(self):
        """显示帮助信息（自动匹配语言）"""
        lang = getattr(self.persona, 'current_lang', 'en')
        help_text = {
            "zh": "🐻 我可以帮你：\n",
            "en": "🐻 I can help you with:\n"
        }[lang]
        
        for cmd, desc in self.help_commands[lang].items():
            help_text += f"- {cmd}: {desc}\n"
        
        help_text += {
            "zh": "\n🌲 试试'巡逻森林'开始玩吧！",  # 移除'种树'
            "en": "\n🌲 Try 'Patrol forest' to start!"  # 移除'Plant tree'
        }[lang]
        
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
        print(f"💥 System startup failed: {str(e)}")
        print("Troubleshooting steps:")
        print("1. Make sure .env file contains GEMINI_API_KEY")
        print("2. Check your internet connection")
        print("3. Restart the program")

if __name__ == "__main__":
    main()