from flask import Flask, render_template, request, jsonify
import os
import threading
import subprocess
import sys

app = Flask(__name__)

bot_process = None
bot_status = "stopped"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def status():
    return jsonify({
        'status': bot_status,
        'token_configured': bool(os.environ.get('TELEGRAM_BOT_TOKEN'))
    })

@app.route('/api/start', methods=['POST'])
def start_bot():
    global bot_process, bot_status

    token = request.json.get('token')
    if not token:
        return jsonify({'error': 'يجب إدخال توكن البوت'}), 400

    os.environ['TELEGRAM_BOT_TOKEN'] = token

    if bot_process and bot_process.poll() is None:
        return jsonify({'error': 'البوت يعمل بالفعل'}), 400

    try:
        bot_process = subprocess.Popen([sys.executable, 'bot.py'])
        bot_status = "running"
        return jsonify({'message': 'تم تشغيل البوت بنجاح', 'status': 'running'})
    except Exception as e:
        bot_status = "error"
        return jsonify({'error': str(e)}), 500

@app.route('/api/stop', methods=['POST'])
def stop_bot():
    global bot_process, bot_status

    if bot_process and bot_process.poll() is None:
        bot_process.terminate()
        bot_process.wait()
        bot_status = "stopped"
        return jsonify({'message': 'تم إيقاف البوت', 'status': 'stopped'})
    else:
        return jsonify({'error': 'البوت غير مشغل'}), 400

@app.route('/api/info')
def info():
    return jsonify({
        'name': 'بوت تيليغرام Python',
        'version': '1.0.0',
        'language': 'Python 3.11',
        'library': 'python-telegram-bot',
        'features': [
            'واجهة تفاعلية',
            'أزرار مخصصة',
            'دعم اللغة العربية',
            'معالجة الرسائل',
            'إحصائيات الاستخدام'
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
