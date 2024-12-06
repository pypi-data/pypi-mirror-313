from IPython.display import display, HTML
import ipywidgets as widgets

# 이제 쿼리를 처리하는 함수를 create_chatbox 함수에 넘길 수 있습니다.
def create_chatbox(process_query_function):
    chat_output = widgets.Output()  # 채팅 영역을 출력할 위젯을 생성합니다.
    input_text = widgets.Text(value='', placeholder='메시지 입력', layout=widgets.Layout(width='40%'))
    send_button = widgets.Button(description='전송', button_style='', layout=widgets.Layout(height='auto'))
    
    def on_send_button_clicked(b):
        # 버튼 클릭 이벤트를 처리
        user_text = input_text.value
        bot_text = process_query_function(user_text)  # 넘겨받은 함수를 사용하여 쿼리 처리
        
        with chat_output:
            user_message = f'<p style="color: #0074D9;"><strong>You:</strong> {user_text}</p>'
            bot_message = f'<p style="color: #2ECC40;"><strong>Bot:</strong> {bot_text}</p>'
            display(HTML(user_message))
            display(HTML(bot_message))
        # 입력 필드를 비웁니다.
        input_text.value = ''
    
    input_area = widgets.HBox([input_text, send_button])  # 입력 필드와 버튼을 가로로 배치합니다.
    send_button.on_click(on_send_button_clicked)  # 버튼 클릭 이벤트와 함수를 연결합니다.

    # 채팅 영역을 담을 컨테이너를 생성하고 스타일을 적용합니다.
    chat_container = widgets.VBox([chat_output], layout=widgets.Layout(border='5px solid #49483E', padding='10px', height='250px', overflow_y='auto'))

    # 모든 요소를 세로로 배치하여 표시합니다.
    display(widgets.VBox([chat_container, input_area]))

    return chat_output, input_text, send_button
