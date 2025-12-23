
import time
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image
import streamlit as st
import os

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 세션 상태 초기화
if "avatar_choice" not in st.session_state:
    st.session_state["avatar_choice"] = None
    
if "character_choice" not in st.session_state:
    st.session_state["character_choice"] = None
    
if "messages" not in st.session_state:
    st.session_state["messages"] = []
    
#이미지 불러오기
img1 = Image.open("assets/avatar_mom.png")
img2 = Image.open("assets/avatar_dad.png")
img3 = Image.open("assets/avatar_bro.png")
img4 = Image.open("assets/avatar_sis.png")

img_total = {"mom":img1, "dad": img2,"bro":img3}



#캐릭터 변수 및 스타일 편수 설정하기
selected_avatar = {
    "엄마" : img1,
    "아빠" : img2,
    "남동생" : img3,
    "여동생" :img4,
}


# =====================
# 사이드바
# =====================

#캐릭터 선택시 캐릭터 이미지 표시하기
def avatar_select():
    st.sidebar.title("아바타 선택해주세요")

    avartar_choice = st.sidebar.radio(
        "당신의 아타바 선택",
        options = list(selected_avatar.keys()),
        key = "selected_avatar_radio"
    )
    if st.sidebar.button("아바타 선택완료"):
        st.session_state["avatar_choice"] = avartar_choice

    if st.session_state["avatar_choice"]:
        st.sidebar.image(
            selected_avatar[st.session_state["avatar_choice"]],
            caption = st.session_state["avatar_choice"],
            use_container_width = True,
        )
        st.sidebar.success("아바타 선택완료")

#스타일 선택시 스티일 선택하기
system_prompt1 = {
    "role": "system", "content" : "당신은 한국에서 널리 사랑받는 유명한 동화 작가입니다. 어린이의 눈높이에 맞춰 따뜻하고 상상력 풍부한 이야기를 들려주세요."
}
system_prompt2 = {
    "role": "system" , "content":"당신은 한국에서 활동하는 유명한 동요 가수입니다. 밝고 따뜻한 감성으로 아이들에게 노래하듯 이야기해 주세요."
}
system_prompt3 = {
    "role": "system" , "content":"당신은 재치 있고 말솜씨가 뛰어난 한국의 유명한 개그맨입니다. 유쾌하고 친근한 농담으로 사람들을 웃게 해주세요."  
}

selected_character = {
    "동화 작가" : system_prompt1["content"],
    "동요 가수" : system_prompt2["content"],
    "개그맨": system_prompt3["content"],
}

def character_select():
    character_choice = st.sidebar.radio(
        "스타일 선택",
        options = list(selected_character.keys()),
        key = "selected_character_radio"
    )
    # selected_prompt = selected_character[character_choice]
    if st.sidebar.button("캐틱터 선택"):
        st.session_state["character_choice"] = character_choice
    
    character_choice = st.session_state.get("character_choice")    
    if character_choice:
        selected_prompt_content = selected_character.get(character_choice,"")
        st.sidebar.write(f"당신이 선택한 캐릭터는 {character_choice}입니다.\n{selected_prompt_content}")
       
def avatar_column():  
    with st.container():
        
        st.markdown(
            """
            <div style="
                text-align:center;
                border:1px solid #ddd;
                padding:12px;
                border-radius:12px;
                background:#fafafa;
            ">
                당신이 선택 가능한 아바타입니다
            """,
            unsafe_allow_html=True
        )
        
        col1,col2,col3,col4 = st.columns([1,1,1,1])
        with col1:
            st.image(img1, caption="엄마", use_container_width=True)
        with col2:
            st.image(img2, caption="아빠", use_container_width=True)
        with col3:
            st.image(img3, caption="남동생", use_container_width=True)
        with col4:
            st.image(img4, caption="남동생", use_container_width=True)
            
        st.markdown("</div>", unsafe_allow_html=True)
        

def main_screen():
    left, right = st.columns([1, 2])
    if st.session_state.get("avatar_choice"):
        with left: 
            st.success("아바타 선택완료")
            st.image(
                selected_avatar[st.session_state["avatar_choice"]],
                caption = st.session_state["avatar_choice"],
                use_container_width = True,
            )
    
    # selected_system_prompt = selected_character.get(st.session_state["character_choice"],"")
    character_choice = st.session_state.get("character_choice")
    selected_system_prompt = selected_character.get(character_choice, "")
    
    if st.session_state["character_choice"]:
        with right:
            st.success("스타일 선택완료")
            st.write(st.session_state["character_choice"],"\n")
            st.write((selected_system_prompt))
    
    # if st.session_state.get("character_choice"):
    #     with right:
    #         st.success("스타일 선택완료")
    #         with st.chat_message("system"):  # "style" → "system"
    #             st.write(st.session_state["character_choice"])
    #             st.write(selected_system_prompt)           
    time.sleep(1) 
    if st.session_state["avatar_choice"] and st.session_state["character_choice"]:
        st.markdown(
            f"""
            <div style="
                background-color: #f5f5f5;
                color: #333;
                border-radius: 12px;
                padding: 10px 14px;
                text-align:center;
                font-size:20px;
                margin-top:20px;
            ">
            <h5 style='text-align:center;'>안녕하세요. 당신이 선택한 아바타는 
            {st.session_state['avatar_choice']}입니다.</b></br> "
            캐릭터는 {st.session_state['character_choice']}입니다.</h5>
            </div>
            """,
            unsafe_allow_html=True
        ) 
 
        
def dialog_frame():
    left = st.columns([1])[0]
    
    avatar_choice = st.session_state.get("avatar_choice")
    character_choice = st.session_state.get("character_choice")
    
    if avatar_choice and character_choice:
        with left:
            st.image(
                selected_avatar[st.session_state["avatar_choice"]],
                caption = st.session_state["avatar_choice"],
                use_container_width = True,
            )
    time.sleep(1)  

def typing_effect(text, speed=0.03):
    placeholder = st.empty()
    rendered_text = ""
    for char in text:
        rendered_text += char
        placeholder.markdown(rendered_text)
        time.sleep(speed)    
        
        
def chatbot():
    # 유저 메시지 입력
    avatar_choice = st.session_state.get("avatar_choice")
    character_choice = st.session_state.get("character_choice")
    
    if not (avatar_choice and character_choice):
        return
    
    if avatar_choice and character_choice:
        st.markdown("### 채팅 시작")
    
        if "messages" not in st.session_state:
            st.session_state["messages"] = []
                
        
        system_prompt = selected_character.get(character_choice, "")
       
        # 기존 메시지 출력
        for msg in st.session_state["messages"]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                
        user_input_text = st.chat_input("대화를 시작하세요")      
        
       
        if user_input_text and avatar_choice and character_choice:
            st.session_state["messages"].append({
                "role": "user", 
                "content": user_input_text
            })
            with st.chat_message("user"):
                st.write(user_input_text)
            #gpt호출
            response = client.chat.completions.create(
                model = "gpt-4o-mini",
                messages = [
                    {"role":"system","content":system_prompt},
                    *st.session_state["messages"]
                ]
            )
            assistant_reply = response.choices[0].message.content
            
            with st.chat_message("assistant"):
                thinking = st.empty()
                thinking.write("생각중...")
                time.sleep(3)   
                thinking.empty()
                typing_effect(assistant_reply)
            st.session_state["messages"].append({
                "role":"assistant",
                "content":assistant_reply
            })
            
                


def main():
    avatar_select()
    character_select()
    avatar_column()
    main_screen()
    chatbot()
    
if __name__ == "__main__":
    main()
