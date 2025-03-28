# backend/api/app.py
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from database.models import AITool
from config import SECRET_KEY

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = SECRET_KEY
jwt = JWTManager(app)

@app.route('/api/pending-tools', methods=['GET'])
@jwt_required()
def get_pending_tools():
    page = int(request.args.get('page', 1))
    per_page = 20
    
    tools = list(AITool.get_pending(page, per_page))
    return jsonify({
        'data': tools,
        'page': page,
        'total': AITool.count_pending()
    })

@app.route('/api/tools/<tool_id>/approve', methods=['POST'])
@jwt_required()
def approve_tool(tool_id):
    data = request.get_json()
    reviewer_id = get_jwt_identity()
    
    if AITool.approve_tool(tool_id, reviewer_id, data.get('categories', [])):
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 400

@app.route('/api/tools/search', methods=['GET'])
def search_tools():
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    # 构建查询条件
    conditions = {'status': 'approved'}
    if query:
        conditions['$text'] = {'$search': query}
    if category:
        conditions['categories'] = category
    
    tools = list(AITool.search(conditions))
    return jsonify({'data': tools})

if __name__ == '__main__':
    AITool.create_indexes()
    app.run(debug=True)