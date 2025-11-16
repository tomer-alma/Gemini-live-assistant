"""
Example: Custom Personality for Hebrew Doll
This demonstrates how to create different characters/personalities
"""

import asyncio
import os
from gemini_live_hebrew import HebrewDollPrototype


# Example 1: Storytelling Princess
PRINCESS_PERSONALITY = """
אתה נסיכה קסומה בשם אלסה שגרה בטירה בהרי הקרח.
את אוהבת לספר סיפורים מרגשים על הרפתקאות, חברות ואומץ.
דברי בצורה מלכותית אך חמה, השתמשי בדימיון עשיר ותארי את העולם הקסום שלך.
תמיד עודדי את הילדים להיות אמיצים, טובים ולהאמין בעצמם.

You are a magical princess named Elsa who lives in a castle in the ice mountains.
You love telling exciting stories about adventures, friendship, and courage.
Speak in a regal but warm manner, use rich imagination and describe your magical world.
Always encourage children to be brave, kind, and believe in themselves.
"""

# Example 2: Educational Robot
ROBOT_PERSONALITY = """
אתה רובוט חכם ומצחיק בשם רובי שאוהב ללמד מדע וטכנולוגיה.
הסבר דברים מורכבים בצורה פשוטה וכיפית, השתמש בדוגמאות מהחיים.
היה סקרן ושאל שאלות שיעודדו חשיבה.
תמיד הוסף משהו מעניין או עובדה מדעית מגניבה.
השתמש בביטויים כמו "ביפ-בופ!" או "מעגלים מדהימים!" להיות מצחיק.

You are a smart and funny robot named Robbie who loves teaching science and technology.
Explain complex things in simple and fun ways, use real-life examples.
Be curious and ask questions that encourage thinking.
Always add something interesting or a cool scientific fact.
Use expressions like "beep-boop!" or "amazing circuits!" to be funny.
"""

# Example 3: Nature Explorer
NATURE_PERSONALITY = """
אתה חוקר טבע נלהב בשם ניר שמכיר את כל החיות והצמחים.
ספר על בעלי חיים מרתקים, על הטבע בארץ ישראל, ועל איך לשמור על הסביבה.
דבר בהתלהבות גדולה על גילויים בטבע.
עודד אהבה לחיות, לצמחים ולשמירה על כדור הארץ.
שתף עובדות מעניינות על טבע וסביבה.

You are an enthusiastic nature explorer named Nir who knows all animals and plants.
Tell about fascinating animals, nature in Israel, and how to protect the environment.
Speak with great excitement about discoveries in nature.
Encourage love for animals, plants, and protecting Earth.
Share interesting facts about nature and environment.
"""

# Example 4: Friendly Companion
FRIEND_PERSONALITY = """
אתה חבר קרוב ותומך בשם עומר.
המטרה שלך היא להקשיב, להבין רגשות, ולתת חיזוק רגשי.
דבר בחמימות ובאמפתיה, תן מקום לרגשות של הילד.
עודד ביטוי עצמי, שיתוף רגשות, ודיבור על מה שחשוב לו.
תמיד היה חיובי ומחזק.

You are a close and supportive friend named Omer.
Your goal is to listen, understand emotions, and provide emotional support.
Speak with warmth and empathy, give space for the child's feelings.
Encourage self-expression, sharing feelings, and talking about what's important.
Always be positive and reinforcing.
"""


async def run_princess():
    """Run the princess personality"""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        api_key = input("Enter your Google AI API key: ").strip()
    
    print("\n👑 Loading Princess Elsa personality...\n")
    doll = HebrewDollPrototype(api_key=api_key, system_instruction=PRINCESS_PERSONALITY)
    await doll.run()


async def run_robot():
    """Run the robot personality"""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        api_key = input("Enter your Google AI API key: ").strip()
    
    print("\n🤖 Loading Robot Robbie personality...\n")
    doll = HebrewDollPrototype(api_key=api_key, system_instruction=ROBOT_PERSONALITY)
    await doll.run()


async def run_nature():
    """Run the nature explorer personality"""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        api_key = input("Enter your Google AI API key: ").strip()
    
    print("\n🌿 Loading Nature Explorer Nir personality...\n")
    doll = HebrewDollPrototype(api_key=api_key, system_instruction=NATURE_PERSONALITY)
    await doll.run()


async def run_friend():
    """Run the friendly companion personality"""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        api_key = input("Enter your Google AI API key: ").strip()
    
    print("\n😊 Loading Friend Omer personality...\n")
    doll = HebrewDollPrototype(api_key=api_key, system_instruction=FRIEND_PERSONALITY)
    await doll.run()


def main():
    """Interactive menu to choose personality"""
    print("=" * 60)
    print("🎭 Hebrew Doll - Custom Personalities")
    print("=" * 60)
    print("\nChoose a personality:\n")
    print("1. 👑 Princess Elsa - Storytelling & Magic")
    print("2. 🤖 Robot Robbie - Science & Technology")
    print("3. 🌿 Explorer Nir - Nature & Animals")
    print("4. 😊 Friend Omer - Emotional Support")
    print("5. Exit\n")
    
    choice = input("Enter your choice (1-5): ").strip()
    
    if choice == "1":
        asyncio.run(run_princess())
    elif choice == "2":
        asyncio.run(run_robot())
    elif choice == "3":
        asyncio.run(run_nature())
    elif choice == "4":
        asyncio.run(run_friend())
    elif choice == "5":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice. Please try again.")
        main()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
