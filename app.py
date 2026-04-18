from flask import Flask, request, jsonify, send_file
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Chart service is running!'

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        code = data.get('code', '')
        
        # 清理舊圖
        plt.close('all')
        
        # 執行程式碼
        local_vars = {'plt': plt, 'np': np}
        exec(code, local_vars)
        
        # 儲存圖片到記憶體
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        plt.close('all')
        
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
