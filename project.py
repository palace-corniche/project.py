"""
COMPLETE SPEECH-ENABLED CHATBOT
Save as: app.py
Author: Student Project
Description: Chatbot with text and voice input capabilities
"""

import streamlit as st
import speech_recognition as sr
import re
import nltk

# Download required NLTK data (only runs once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

# ============================================================================
# STEP 1: IMPORT NECESSARY PACKAGES (DONE ABOVE)
# ============================================================================

# ============================================================================
# STEP 2: LOAD TEXT FILE AND PREPROCESS DATA
# ============================================================================

# Knowledge base - Space facts
SPACE_TEXT = """
The Solar System is the gravitationally bound system of the Sun and the objects that orbit it.
The Sun is a star at the center of our Solar System.
Earth is the third planet from the Sun and the only place we know that has life.
Mars is called the Red Planet because of its reddish appearance.
Jupiter is the largest planet in our Solar System.
Saturn is famous for its beautiful rings made of ice and rock.
The Moon orbits around Earth and takes about 27 days to complete one orbit.
Astronauts are people who travel to space.
The International Space Station is a large spacecraft that orbits Earth.
Rockets are used to launch spacecraft into space.
The first human in space was Yuri Gagarin in 1961.
Neil Armstrong was the first person to walk on the Moon in 1969.
Venus is the hottest planet in our Solar System.
Mercury is the smallest planet and closest to the Sun.
Neptune is the farthest planet from the Sun.
Uranus rotates on its side compared to other planets.
A galaxy is a huge collection of stars, dust, and gas held together by gravity.
The Milky Way is the galaxy that contains our Solar System.
Black holes are regions in space where gravity is so strong that nothing can escape.
Stars are giant balls of hot gas that produce light and heat.
Comets are icy objects that leave bright trails when they pass near the Sun.
A telescope is an instrument used to observe distant objects in space.
The universe is everything that exists including all matter and energy.
Space exploration helps us understand our place in the cosmos.
Satellites orbit Earth and help with communication and navigation.
Asteroids are rocky objects that orbit the Sun.
The atmosphere protects Earth from harmful radiation.
Gravity is the force that pulls objects toward each other.
Light from the Sun takes about 8 minutes to reach Earth.
A lunar eclipse occurs when Earth passes between the Sun and Moon.
"""

def preprocess(text):
    """
    Clean and prepare the text data
    
    Args:
        text (str): Raw text to process
    
    Returns:
        list: Cleaned sentences
    """
    # Convert to lowercase
    text = text.lower()
    
    # Split into sentences
    sentences = text.split('.')
    
    # Clean each sentence
    cleaned_sentences = []
    
    for sentence in sentences:
        # Remove extra spaces
        sentence = sentence.strip()
        
        if sentence:  # Only keep non-empty sentences
            # Remove special characters but keep spaces
            sentence = re.sub(r'[^a-z0-9\s]', '', sentence)
            cleaned_sentences.append(sentence)
    
    return cleaned_sentences

def get_most_relevant_sentence(query, sentences):
    """
    Find the sentence that best matches the user's question
    
    Args:
        query (str): User's question
        sentences (list): List of preprocessed sentences
    
    Returns:
        tuple: (best_sentence, similarity_score)
    """
    # Preprocess the query
    query = query.lower()
    query = re.sub(r'[^a-z0-9\s]', '', query)
    query_words = query.split()
    
    best_score = 0
    best_sentence = ""
    
    # Compare query with each sentence
    for sentence in sentences:
        sentence_words = sentence.split()
        
        # Count how many words match
        matches = 0
        for word in query_words:
            if word in sentence_words:
                matches += 1
        
        # Calculate similarity score
        if len(query_words) > 0:
            score = matches / len(query_words)
        else:
            score = 0
        
        # Keep track of best match
        if score > best_score:
            best_score = score
            best_sentence = sentence
    
    return best_sentence, best_score

# ============================================================================
# STEP 3: DEFINE SPEECH RECOGNITION FUNCTION
# ============================================================================

def transcribe_speech():
    """
    Transcribe speech into text using microphone
    
    Returns:
        tuple: (transcribed_text, error_message)
    """
    recognizer = sr.Recognizer()
    
    try:
        # Use microphone as audio source
        with sr.Microphone() as source:
            st.info("🎤 Listening... Speak now!")
            
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            # Listen for audio input
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            st.success("✅ Audio captured! Processing...")
        
        # Transcribe using Google Speech Recognition
        text = recognizer.recognize_google(audio)
        return text, None
    
    except sr.WaitTimeoutError:
        return None, "⏱️ No speech detected. Please try again."
    
    except sr.UnknownValueError:
        return None, "❌ Could not understand the audio. Please speak clearly."
    
    except sr.RequestError as e:
        return None, f"❌ Error with speech recognition service: {e}"
    
    except OSError as e:
        return None, f"❌ Microphone error: {str(e)}. Make sure your microphone is connected."
    
    except Exception as e:
        return None, f"❌ Unexpected error: {str(e)}"

# ============================================================================
# STEP 4: MODIFIED CHATBOT FUNCTION (TEXT + SPEECH INPUT)
# ============================================================================

def chatbot(user_input, sentences, input_type="text"):
    """
    Return a response based on text or speech input
    
    Args:
        user_input (str): User's question (text or transcribed speech)
        sentences (list): Preprocessed knowledge base
        input_type (str): "text" or "voice"
    
    Returns:
        str: Chatbot's response
    """
    # Validate input
    if not user_input or user_input.strip() == "":
        return "Please provide a question!"
    
    # Get most relevant sentence
    relevant_sentence, score = get_most_relevant_sentence(user_input, sentences)
    
    # Return response based on similarity score
    if score > 0.2:  # At least 20% of words matched
        return relevant_sentence.capitalize() + "."
    else:
        return "I'm sorry, I don't have information about that. Try asking about planets, the Sun, Moon, astronauts, or space exploration!"

# ============================================================================
# STEP 5: CREATE STREAMLIT APP
# ============================================================================

def main():
    """
    Main function to run the Streamlit app
    """
    # Page configuration
    st.set_page_config(
        page_title="Speech-Enabled Chatbot",
        page_icon="🎤",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            color: #1f77b4;
        }
        .sub-header {
            text-align: center;
            color: #666;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Title
    st.markdown('<p class="main-header">🎤 Speech-Enabled Space Chatbot</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Ask questions using Text or Voice!</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Instructions
    with st.expander("📖 How to Use This App", expanded=True):
        st.markdown("""
        ### 🎯 Two Ways to Ask Questions:
        
        #### Option 1: Text Input 📝
        1. Type your question in the text box
        2. Click **"📝 Ask with Text"** button
        3. Get instant response!
        
        #### Option 2: Voice Input 🎤
        1. Click **"🎤 Ask with Voice"** button
        2. Allow microphone access when prompted by your browser
        3. Speak your question clearly
        4. Wait for transcription and response
        
        ### 💡 Example Questions:
        - "What is Mars?"
        - "Tell me about the Moon"
        - "Who was Neil Armstrong?"
        - "What is Jupiter?"
        - "Tell me about Saturn's rings"
        - "What is a black hole?"
        - "Who was the first person in space?"
        
        ### 🎙️ Voice Input Tips:
        - Speak clearly at a normal pace
        - Reduce background noise
        - Make sure your microphone is working
        - Allow browser microphone permissions
        - Use Chrome or Edge for best results
        
        ### 🔧 Troubleshooting:
        - If voice input doesn't work, check microphone permissions
        - Try refreshing the page if there are issues
        - Text input always works as a backup option
        """)
    
    # Initialize session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Preprocess data
    sentences = preprocess(SPACE_TEXT)
    
    # Create two columns for input methods
    col1, col2 = st.columns(2)
    
    # ========== TEXT INPUT COLUMN ==========
    with col1:
        st.subheader("💬 Text Input Mode")
        text_input = st.text_input(
            "Type your question here:",
            placeholder="e.g., What is Jupiter?",
            key="text_input"
        )
        text_button = st.button("📝 Ask with Text", use_container_width=True, type="primary")
    
    # ========== VOICE INPUT COLUMN ==========
    with col2:
        st.subheader("🎤 Voice Input Mode")
        st.write("Click the button and speak your question")
        voice_button = st.button("🎤 Ask with Voice", use_container_width=True, type="secondary")
    
    st.markdown("---")
    
    # ========== HANDLE TEXT INPUT ==========
    if text_button:
        if text_input:
            st.subheader("📋 Your Question (Text):")
            st.info(f"💭 {text_input}")
            
            # Get chatbot response
            with st.spinner("🤔 Thinking..."):
                response = chatbot(text_input, sentences, input_type="text")
            
            st.subheader("🤖 Bot Response:")
            st.success(f"💬 {response}")
            
            # Add to chat history
            st.session_state.chat_history.append({
                'type': 'text',
                'question': text_input,
                'response': response
            })
        else:
            st.warning("⚠️ Please type a question first!")
    
    # ========== HANDLE VOICE INPUT ==========
    if voice_button:
        st.subheader("🎤 Voice Recognition Active")
        
        with st.spinner("🎤 Recording... Speak now!"):
            transcribed_text, error = transcribe_speech()
        
        if error:
            st.error(error)
            st.warning("💡 **Troubleshooting Tips:**")
            st.markdown("""
            - Check if your microphone is connected and working
            - Allow microphone permissions in your browser settings
            - Try reducing background noise
            - Speak louder and more clearly
            - Make sure you're using Chrome or Edge browser
            - Refresh the page and try again
            """)
        
        elif transcribed_text:
            st.subheader("📋 Your Question (Transcribed from Voice):")
            st.info(f"🗣️ \"{transcribed_text}\"")
            
            # Get chatbot response
            with st.spinner("🤔 Thinking..."):
                response = chatbot(transcribed_text, sentences, input_type="voice")
            
            st.subheader("🤖 Bot Response:")
            st.success(f"💬 {response}")
            
            # Add to chat history
            st.session_state.chat_history.append({
                'type': 'voice',
                'question': transcribed_text,
                'response': response
            })
    
    # ========== CHAT HISTORY ==========
    if st.session_state.chat_history:
        st.markdown("---")
        st.subheader("📜 Chat History")
        
        for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):
            icon = "💬" if chat['type'] == 'text' else "🎤"
            with st.expander(f"{icon} Question {len(st.session_state.chat_history) - i}"):
                st.write(f"**Q:** {chat['question']}")
                st.write(f"**A:** {chat['response']}")
        
        if st.button("🗑️ Clear History"):
            st.session_state.chat_history = []
            st.rerun()
    
    # ========== SIDEBAR ==========
    st.sidebar.header("ℹ️ About This Chatbot")
    st.sidebar.markdown("""
    This intelligent chatbot understands both:
    
    📝 **Text Input**
    - Type your questions directly
    - Instant responses
    - Always available
    
    🎤 **Voice Input**
    - Speak naturally
    - Automatic transcription
    - Hands-free interaction
    
    ### 📚 Knowledge Topics:
    - Solar System & Planets
    - Stars & Galaxies
    - Space Exploration
    - Astronauts & Missions
    - Celestial Objects
    - Space Technology
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.header("🔧 System Requirements")
    st.sidebar.markdown("""
    **For Text Input:**
    - Any device with browser ✅
    
    **For Voice Input:**
    - Working microphone 🎤
    - Browser microphone permission 🔓
    - Internet connection 🌐
    - Chrome or Edge browser (recommended)
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.info("💡 **Tip:** If voice input doesn't work, you can always use text input!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666;'>
            <p>🚀 Built with Streamlit | 🎓 Student Project | 🌟 Speech Recognition Powered</p>
        </div>
    """, unsafe_allow_html=True)

# ============================================================================
# STEP 6: RUN THE APP
# ============================================================================

if __name__ == "__main__":
    main()