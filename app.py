from flask import Flask, request, jsonify, send_file
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io
import os
import re

app = Flask(__name__)

# 啟用 LaTeX 渲染的 mathtext
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['font.family'] = 'serif'


def clean_latex(f):
    """清理 matplotlib mathtext 不支援的 LaTeX 指令"""
    f = re.sub(r'\\boxed\{([^}]*)\}', r'\1', f)
    f = re.sub(r'\\text\{([^}]*)\}', r'\\mathrm{\1}', f)
    f = f.replace('\\quad', '\\;\\;')
    f = f.replace('\\qquad', '\\;\\;\\;\\;')
    f = f.replace('\\displaystyle', '')
    f = f.replace('\\left', '')
    f = f.replace('\\right', '')
    return f


@app.route('/')
def home():
    return 'Chart service is running!'


@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        code = data.get('code', '')
        plt.close('all')
        local_vars = {'plt': plt, 'np': np}
        exec(code, local_vars)
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        plt.close('all')
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/latex', methods=['POST'])
def latex():
    try:
        data = request.json
        formulas = data.get('formulas', [])
        if not formulas:
            return jsonify({'error': 'no formulas'}), 400

        # 清理並限制數量
        formulas = [clean_latex(f) for f in formulas][:15]
        n = len(formulas)

        plt.close('all')
        fig_height = max(1.5, 0.8 * n + 0.5)
        fig, ax = plt.subplots(figsize=(8, fig_height))
        ax.axis('off')

        y_positions = np.linspace(0.9, 0.1, n) if n > 1 else [0.5]
        for i, (formula, y) in enumerate(zip(formulas, y_positions), 1):
            label = f'[{i}]' if n > 1 else ''
            ax.text(0.05, y, label, ha='left', va='center',
                    fontsize=14, transform=ax.transAxes, color='gray')
            try:
                ax.text(0.5, y, f'${formula}$', ha='center', va='center',
                        fontsize=18, transform=ax.transAxes)
            except Exception:
                # 如果某公式渲染失敗，顯示原始文字
                ax.text(0.5, y, formula, ha='center', va='center',
                        fontsize=12, transform=ax.transAxes, color='red')

        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight',
                    facecolor='white', pad_inches=0.3)
        buf.seek(0)
        plt.close('all')
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
