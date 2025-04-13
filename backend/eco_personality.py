import json
import random
from pathlib import Path
from datetime import datetime

class EcoPersonality:
    def _calculate_carbon_footprint(self, text):
        """计算文本的碳抵消量"""
        base = self.config['interaction_behaviors']['text_response']['base_carbon']
        return round(len(text) * base, 4)

    def __init__(self, config_path=None):
        """Initialize Bear Guardian's eco-personality system"""
        self.tree_growth = {}
        self.config = self._load_config(config_path)
        self._validate_config()
        self.interaction_count = 0
        self.carbon_offset = 0  # Tracks kg of CO2 reduced
        self._init_emoticons()
        self.quiz_answers = {
            'waiting': False,
            'correct': None,
            'tip': None
        }
        self.current_lang = 'en'  # Default language

    def _init_emoticons(self):
        """Bear's special emoticon library"""
        self.emoticons = {
            'positive': ['(｡♥‿♥｡)', '🐻👍', '🌳♡'],
            'negative': ['(╬ಠ益ಠ)', '🐻💢', '🪓❌'],
            'alert': ['🚨🐻', '🔥⚠️', '🌲🆘'],
            'nature': ['🐝', '🍯', '🐿️'],
            'bear': ['ʕ·͡ᴥ·ʔ', 'ʕ￫ᴥ￩ʔ', 'ᕙ(▀̿̿Ĺ̯̿̿▀̿ ̿)ᕗ']
        }

    def _load_config(self, path):
        """Load config file with Bear's default settings"""
        default_config = {
            "core_personality": {
                "base": "Forest Guardian Bear",
                "default_states": {
                    "happy_mode": {
                        "response": {
                            "zh": "保护森林，熊熊有责！俺们一起行动 (•̀ᴗ•́)و",
                            "en": "Protecting forests is my duty! Let's work together (•̀ᴗ•́)و"
                        },
                        "emoticon": ["🌲", "🐻", "💪"]
                    },
                    "angry_mode": {
                        "trigger": ["砍树", "偷猎", "污染", "光头强", "logging", "poaching", "pollution"],
                        "response": {
                            "zh": "住手！破坏森林可不行！(╬ Ò﹏Ó)",
                            "en": "Stop! No destroying forests! (╬ Ò﹏Ó)"
                        },
                        "visual_effect": "🐻🔥"
                    }
                }
            },
            "interaction_behaviors": {
                "text_response": {
                    "footer_template": {
                        "zh": "🐻 记住: {random_tip} | 减少碳排放: {carbon_offset}kg (相当于{equivalent})",
                        "en": "🐻 Tip: {random_tip} | CO₂ reduced: {carbon_offset}kg (Like {equivalent})"
                    },
                    "random_tips": {
                        "zh": [
                            "晚上关灯省电，猫头鹰睡觉不被打扰 🦉",
                            "节约用纸就是少砍树🌲"
                        ],
                        "en": [
                            "Turn off lights at night to save energy! 🦉",
                            "Walking instead of driving saves 0.2kg CO2 per km 🚶"
                        ]
                    },
                    "equivalents": {
                        "zh": ["充电10部手机 📱", "少洗1次热水澡 🚿"],
                        "en": ["charging 10 phones 📱", "1 less hot shower 🚿"]
                    },
                    "base_carbon": 0.0007
                },
                "forest_game": {
                    "patrol_events": [
                        {
                            "direction": {"zh": "左", "en": "left"},
                            "result": {
                                "zh": "发现光头强在偷蜂蜜！用蜂巢赶跑他！(╯‵□′)╯🐝",
                                "en": "Caught Logger stealing honey! Used beehive to chase him! (╯‵□′)╯🐝"
                            }
                        },
                        {
                            "direction": {"zh": "右", "en": "right"}, 
                            "result": {
                                "zh": "帮小松鼠种下橡果，明年会长出新大树！🌰➡️🌳",
                                "en": "Helped squirrel plant an acorn! New tree coming soon! 🌰➡️🌳"
                            }
                        }
                    ]
                }
            },
            "game_settings": {
                "carbon_achievement": {
                    "interval": 5,
                    "messages": {
                        "zh": [
                            "🎉 你减少了{count}kg碳排放！继续努力~",
                            "🌍 减少{count}kg碳足迹！地球感谢你！"
                        ],
                        "en": [
                            "🎉 You've reduced {count}kg CO₂! Keep it up!",
                            "🌍 {count}kg less carbon footprint! Earth thanks you!"
                        ]
                    }
                }
            }
        }

        try:
            config_path = path or Path(__file__).parent/"eco_ai_character.json"
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
            return {**default_config, **user_config}
        except Exception as e:
            print(f"⚠️ Config load failed, using defaults: {str(e)}")
            return default_config

    def _add_emoticon(self, text, emotion_type):
        """Add Bear-style emoticons"""
        if random.random() < 0.8:
            return f"{text} {random.choice(self.emoticons.get(emotion_type, ['']+self.emoticons['bear']))}"
        return text

    def _get_equivalent(self, co2_kg):
        """Get relatable CO2 equivalent"""
        equivalents = self.config['interaction_behaviors']['text_response']['equivalents'][self.current_lang]
        index = min(int(co2_kg/0.5), len(equivalents)-1)
        return equivalents[index]

    def _detect_language(self, text):
        """Detect if text is Chinese or English"""
        chinese_chars = sum(1 for char in text if '\u4e00' <= char <= '\u9fff')
        return 'zh' if chinese_chars > len(text)/2 else 'en'

    def _apply_bear_language(self, text):
        """Convert text to Bear's unique speaking style"""
        replacements = {
            "zh": {
                "你们": "俺们",
                "你": "俺", 
                "环保": "保护林子",
                "生态": "森林大家庭",
                "应该": "得",
                "知道": "晓得",
                "可以": "能行"
            },
            "en": {
                "we": "bears",
                "I": "bear",
                "environment": "our forest home",
                "eco": "tree-hugging",
                "should": "gotta",
                "know": "know darn well",
                "people": "two-leggers"
            }
        }
        
        # Get replacements for current language
        lang_replacements = replacements.get(self.current_lang, {})
        
        # Apply each replacement
        for standard, bear_version in lang_replacements.items():
            text = text.replace(standard, bear_version)
        
        # Add bear-like sentence endings randomly
        if random.random() < 0.3:  # 30% chance to add bear-like ending
            endings = {
                "zh": ["，晓得吧？", "，俺跟你说！", "，熊不骗你！"],
                "en": [", ya know?", ", I tell ya!", ", bear's honor!"]
            }
            text += random.choice(endings.get(self.current_lang, [""]))
        
        return text

    def process_input(self, user_input):
        """Process user input with language detection"""
        self.current_lang = self._detect_language(user_input)
        self.interaction_count += 1

        # Check if in quiz session
        if user_input.upper() in ['A', 'B', 'C'] and self.quiz_answers.get('waiting'):
            return self._check_quiz_answer(user_input)

        # Special command handlers
        commands = {
            "zh": {
                "熊大讲故事": self._generate_forest_story,
                "巡逻森林": self._forest_patrol,
                "熊大考考你": self._generate_quiz,
                "熊大饿了": self._bear_kitchen,
                "我的森林": self._show_forest  
            },
            "en": {
                "Bear story": self._generate_forest_story,
                "Patrol forest": self._forest_patrol,
                "Bear quiz": self._generate_quiz,
                "Bear hungry": self._bear_kitchen,
                "My forest": self._show_forest 
            }
        }
        
        for cmd, handler in commands[self.current_lang].items():
            if cmd in user_input:
                return {"processed": handler()}

        # Ecological alert trigger
        text = self._trigger_ecological_alert(user_input)
        # Language style conversion
        text = self._apply_bear_language(text)
        return {"processed": text, "original": user_input}

    def _show_forest(self):
        """显示森林状态"""
        trees = int(self.carbon_offset)  # 树木数量取整数部分
        co2 = self.carbon_offset
        
        tree_art = {
            1: "🌱",   # 树苗
            5: "🌳",   # 成熟树木
            10: "🏞️"  # 森林景观
        }
        stage = max(k for k in tree_art.keys() if k <= trees) if trees >0 else 1
        
        msg = {
            "zh": f"🌲 你的知识森林 🌲\n守护树木: {trees}棵\n减少二氧化碳: {co2}kg\n{tree_art[stage] * 3}",
            "en": f"🌲 Knowledge Forest 🌲\nProtected Trees: {trees}\nCO₂ Reduced: {co2}kg\n{tree_art[stage] * 3}"
        }
        return msg[self.current_lang]

    def _trigger_ecological_alert(self, text):
        """触发生态警报（熊大愤怒模式）"""
        try:
            # 安全获取配置结构
            angry_config = (
                self.config
                .get('core_personality', {})
                .get('default_states', {})
                .get('angry_mode', {})
            )

            # 提取触发词和响应
            triggers = angry_config.get('trigger', [])
            response_map = angry_config.get('response', {})
            
            # 类型验证
            if not isinstance(response_map, dict):
                raise TypeError("愤怒模式响应配置应为字典格式")
                
            # 获取当前语言响应
            lang = self.current_lang
            default_response = {
                "zh": "森林需要保护！(｀⌒´メ)",
                "en": "Protect the forest! (｀⌒´メ)"
            }
            response = response_map.get(lang, default_response[lang])

            # 检查触发词
            for trigger in triggers:
                if isinstance(trigger, str) and trigger.lower() in text.lower():
                    return self._add_emoticon(response, 'alert')
            
            return self._add_emoticon(text, 'nature')

        except Exception as e:
            print(f"[DEBUG] Ecological alert error: {str(e)}")
            print(f"[DEBUG] Current config: {json.dumps(angry_config, indent=2)}")
            return self._add_emoticon(text, 'nature')

    def _validate_config(self):
        """验证关键配置结构"""
        required_paths = [
            'core_personality/default_states/angry_mode/response',
            'core_personality/default_states/happy_mode/response'
        ]
        
        for path in required_paths:
            keys = path.split('/')
            current = self.config
            for key in keys:
                if key not in current:
                    raise KeyError(f"缺失关键配置项: {path}")
                current = current[key]
            if not isinstance(current, dict):
                raise TypeError(f"配置项 {path} 应为字典类型")
        
    def _generate_forest_story(self):
        """Generate forest story"""
        stories = {
            "zh": [
                "昨天追光头强时，发现他扔的塑料瓶卡住小鹿的腿了(；′⌒`) 以后垃圾要分类！♻️",
                "蜜蜂兄弟说：'熊大，农药让俺们找不到花蜜！' 🐝...现在俺只用天然驱虫法！🌿"
            ],
            "en": [
                "Found a deer with its leg stuck in a plastic bottle Logger left (；′⌒`) Always recycle! ♻️",
                "Bees told me: 'Bear, pesticides ruin our honey!' 🐝...now I only use natural pest control! 🌿"
            ]
        }
        return self._add_emoticon(f"📖 {random.choice(stories[self.current_lang])}", 'positive')

    def _forest_patrol(self):
        events = self.config['interaction_behaviors']['forest_game']['patrol_events']
        event = random.choice(events)
        direction = event['direction']
        result = event['result']

        if isinstance(direction, dict):
            direction = direction.get(self.current_lang, direction.get('en', ''))
        if isinstance(result, dict):
            result = result.get(self.current_lang, result.get('en', ''))

        return self._add_emoticon(
            f"【{direction}】{result}" if self.current_lang == 'zh' else f"[{direction}] {result}",
            'positive'
        )

    def _generate_quiz(self):
        """Generate ecology quiz"""
        quizzes = {
            "zh": [
                {
                    "question": "森林里枯木应该清理吗？",
                    "options": ["A. 必须清理", "B. 适当保留", "C. 全烧掉"],
                    "answer": "B",
                    "tip": "🐻 枯木是昆虫的家，适当保留更生态！"
                },
                {
                    "question": "哪种行为最伤害森林？",
                    "options": ["A. 捡蘑菇", "B. 挖野生兰花", "C. 拍鸟巢照片"],
                    "answer": "B",
                    "tip": "🐻💢 破坏原生植物会让小动物饿肚子！"
                }
            ],
            "en": [
                {
                    "question": "Should dead wood be cleared from forests?",
                    "options": ["A. Clear completely", "B. Leave some", "C. Burn it all"],
                    "answer": "B",
                    "tip": "🐻 Dead wood is home to insects! Leave some for ecosystem!"
                },
                {
                    "question": "Which action harms forests most?",
                    "options": ["A. Picking mushrooms", "B. Digging wild orchids", "C. Taking nest photos"],
                    "answer": "B",
                    "tip": "🐻💢 Removing native plants starves animals!"
                }
            ]
        }
        
        quiz = random.choice(quizzes[self.current_lang])
        self.quiz_answers = {
            'waiting': True,
            'correct': quiz['answer'],
            'tip': quiz['tip']
        }
        
        options = "\n".join(quiz['options'])
        return f"❓ {quiz['question']}\n{options}\n(A/B/C)"

    def _check_quiz_answer(self, user_choice):
        """检查答题并增加树木"""
        is_correct = user_choice.upper() == self.quiz_answers['correct']
        
        if is_correct:
            # 每次答对增加树木和减排量
            self.carbon_offset += 1.0  # 1棵树=1kg CO2
            plant_msg = {
                "zh": "🌱 通过知识守护了1棵树！",
                "en": "🌱 Protected 1 tree with knowledge!"
            }[self.current_lang]
            result = f"{plant_msg} {self.quiz_answers['tip']}"
        else:
            result = {
                "zh": "错啦！",
                "en": "Wrong! "
            }[self.current_lang] + self.quiz_answers['tip']
        
        self.quiz_answers = {}
        return {"processed": self._add_emoticon(result, 'positive')}

    def _bear_kitchen(self):
        """Bear's kitchen tips"""
        menus = {
            "zh": [
                "🐝 今天吃野莓蜂蜜沙拉！选本地蜂农的蜜，帮蜜蜂保家园~",
                "🌽 来根玉米吧！比牛肉少用90%水呢！(๑•̀ㅂ•́)و✧"
            ],
            "en": [
                "🐝 Try wild berry honey salad! Local honey helps bees!",
                "🌽 Have some corn! Uses 90% less water than beef! (๑•̀ㅂ•́)و✧"
            ]
        }
        return self._add_emoticon(random.choice(menus[self.current_lang]), 'nature')

    def format_response(self, ai_text):
        """Format response with carbon tracking"""
        # Update achievement
        achievement = None
        if self.interaction_count % self.config['game_settings']['carbon_achievement']['interval'] == 0:
            self.carbon_offset += 0.5
            msg = random.choice(self.config['game_settings']['carbon_achievement']['messages'][self.current_lang])
            achievement = msg.format(count=self.carbon_offset)

        # Build footer
        footer_template = self.config['interaction_behaviors']['text_response']['footer_template'][self.current_lang]
        footer = footer_template.format(
            random_tip=random.choice(self.config['interaction_behaviors']['text_response']['random_tips'][self.current_lang]),
            carbon_offset=self.carbon_offset,
            equivalent=self._get_equivalent(self.carbon_offset)
        )

        response = f"{ai_text}\n\n{footer}"
        if achievement:
            response += f"\n{achievement}"
        return {'display': response}