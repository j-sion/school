from flask import Flask, render_template, request, redirect
from datetime import datetime

app = Flask(__name__)

# 메모리에 저장 (Replit에선 서버 재시작 시 초기화됨)
schedules = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global schedules
    today = datetime.now().date()

    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        description = request.form['description']

        # 오늘 날짜보다 이전 일정은 추가되지 않도록 검증
        if datetime.strptime(date, '%Y-%m-%d').date() < today:
            error_message = "오늘 이후의 날짜만 선택할 수 있습니다."
            return render_template('index.html', error_message=error_message, today=today, upcoming=schedules, past=[])

        schedules.append({
            'title': title,
            'date': date,
            'description': description
        })
        return redirect('/')

    upcoming = [s for s in schedules if datetime.strptime(s['date'], '%Y-%m-%d').date() >= today]
    past = [s for s in schedules if datetime.strptime(s['date'], '%Y-%m-%d').date() < today]

    return render_template('index.html', upcoming=upcoming, past=past, today=today)

@app.route('/delete/<int:index>')
def delete(index):
    global schedules
    if 0 <= index < len(schedules):
        del schedules[index]  # 해당 index에 있는 일정 삭제
    return redirect('/')  # 삭제 후 페이지 새로고침

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
