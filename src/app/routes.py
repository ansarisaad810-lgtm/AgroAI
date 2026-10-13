from flask import Blueprint, render_template, request, jsonify
from app.database.db_handler import get_db_connection
from app.dsa_core.arrays_stacks import push_crop, pop_crop, Queue
from app.dsa_core.linked_list import LedgerLinkedList
from app.dsa_core.hash_map import RecommendationHashMap
from app.dsa_core.sorting_searching import binary_search_crop, merge_sort_by_price
from app.dsa_core.graph_rotation import rotation_graph
from app.dsa_core.priority_heap import TaskPriorityQueue
from app.dsa_core.npk_calculator import calculate_npk
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv(override=True)

main_bp = Blueprint('main', __name__)

# Global Task Queue instance (Min-Heap)
task_planner = TaskPriorityQueue()
task_planner.push_task(2, "Water Paddy Crop (Bhilai Field)", "Irrigation")
task_planner.push_task(5, "Apply Neem Spray against Rust", "Pest Control")
task_planner.push_task(1, "Check Drainage Channel before Rain", "Weather Prep")

@main_bp.route('/')
def index():
    conn = get_db_connection()
    user_crops = conn.execute('SELECT * FROM user_crops').fetchall()
    all_crops = conn.execute('SELECT * FROM master_crops ORDER BY name ASC').fetchall()
    conn.close()

    user_crop_list = [c['crop_name'] for c in user_crops]
    master_crop_list = [dict(c) for c in all_crops]

    news_feed = [
        {"title": "MSP Rates Revised for Rabi Season 2026", "category": "Policy", "date": "Oct 2026", "link": "#"},
        {"title": "IMD Predicts Light Rainfall in Central Mandis Next Week", "category": "Weather", "date": "Oct 2026", "link": "#"},
        {"title": "Subsidy Scheme Launched for Drip Irrigation Systems", "category": "Government", "date": "Oct 2026", "link": "#"}
    ]

    urgent_tasks = task_planner.get_all_sorted()

    return render_template('index.html', user_crops=user_crop_list, master_crops=master_crop_list, news_feed=news_feed, urgent_tasks=urgent_tasks)

@main_bp.route('/api/groq', methods=['POST'])
def groq_chat():
    data = request.get_json()
    user_prompt = data.get('prompt', '') if data else ''
    farmer_location = data.get('location', 'Bhilai, Chhattisgarh') if data else 'Bhilai, Chhattisgarh'

    if not user_prompt:
        return jsonify({"error": "Empty prompt provided"}), 400

    request_queue = Queue()
    request_queue.enqueue(user_prompt)
    prompt_to_process = request_queue.dequeue()

    groq_api_key = os.getenv('GROQ_API_KEY', '').strip()
    
    if not groq_api_key or "your_" in groq_api_key.lower():
        return jsonify({
            "response": "⚠️ GROQ_API_KEY is missing or invalid in .env file. Please add your real Groq API key!"
        })

    try:
        client = Groq(api_key=groq_api_key)
        
        system_instruction = (
            f"You are AgroAI, an expert farming advisor. The farmer is located in '{farmer_location}'. "
            f"Always provide direct, specific advice tailored to {farmer_location} without asking the farmer which region or state they are in. "
            f"Format response cleanly with headings and lists."
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt_to_process}
            ],
            model="qwen/qwen3.8-27b",
            temperature=0.3,
            max_tokens=350
        )
        ai_reply = chat_completion.choices[0].message.content
        return jsonify({
            "response": ai_reply,
            "dsa_algo": "FIFO Queue Processing Buffer (O(1))"
        })
    except Exception as e:
        return jsonify({"response": f"Error calling Groq API: {str(e)}"}), 500

@main_bp.route('/add_crop', methods=['POST'])
def add_crop():
    crop_name = request.form.get('crop_name')
    if crop_name:
        conn = get_db_connection()
        conn.execute('INSERT INTO user_crops (crop_name) VALUES (?)', (crop_name,))
        conn.commit()
        conn.close()
    return jsonify({"status": "success", "dsa_algo": "Array Push (O(1))"})

@main_bp.route('/remove_crop', methods=['POST'])
def remove_crop():
    crop_name = request.form.get('crop_name')
    if crop_name:
        conn = get_db_connection()
        conn.execute('DELETE FROM user_crops WHERE crop_name = ?', (crop_name,))
        conn.commit()
        conn.close()
    return jsonify({"status": "success", "dsa_algo": "Array Pop (O(N))"})

@main_bp.route('/recommendations', methods=['GET'])
def recommendations():
    query_type = request.args.get('type', 'crop')
    value = request.args.get('value', 'Wheat')

    conn = get_db_connection()
    all_crops = [dict(r) for r in conn.execute('SELECT * FROM master_crops ORDER BY name ASC').fetchall()]
    conn.close()

    distinct_soils = sorted(list(set([c['soil'] for c in all_crops])))
    distinct_seasons = sorted(list(set([c['season'] for c in all_crops])))

    rec_map = RecommendationHashMap()
    rec_map.populate(all_crops)

    results = []
    rotation_options = []
    dsa_used = ""

    if query_type == 'crop':
        matched = binary_search_crop(all_crops, value)
        results = [matched] if matched else []
        rotation_options = rotation_graph.get_rotation_plan(value)
        dsa_used = "Binary Search O(log N) + DAG Rotation Graph BFS"
    elif query_type == 'soil':
        results = rec_map.get_by_soil(value)
        dsa_used = "Hash Map Lookup (O(1)) for Soil -> Crops"
    elif query_type == 'season':
        results = rec_map.get_by_season(value)
        dsa_used = "Hash Map Lookup (O(1)) for Season -> Crops"

    return render_template(
        'recommendations.html',
        results=results,
        rotation_options=rotation_options,
        dsa_used=dsa_used,
        query_type=query_type,
        value=value,
        master_crops=all_crops,
        distinct_soils=distinct_soils,
        distinct_seasons=distinct_seasons
    )

@main_bp.route('/tools_calculator', methods=['GET', 'POST'])
def tools_calculator():
    """DSA: Greedy Selection & Sorting for Equipment within Budget."""
    budget = float(request.form.get('budget', 5000)) if request.method == 'POST' else 5000.0

    all_tools = [
        {"name": "Hand Sprayer Pump", "cost": 1200, "type": "Pest Control"},
        {"name": "Drip Irrigation Starter Kit", "cost": 3500, "type": "Water Management"},
        {"name": "Manual Seed Drill", "cost": 4800, "type": "Sowing"},
        {"name": "Power Tiller Attachment", "cost": 12000, "type": "Land Prep"},
        {"name": "Soil Moisture Testing Meter", "cost": 800, "type": "Soil Health"},
        {"name": "Solar Insect Trap", "cost": 2200, "type": "Pest Control"}
    ]

    sorted_tools = merge_sort_by_price(all_tools, key='cost')
    affordable_tools = [t for t in sorted_tools if t['cost'] <= budget]

    return render_template('tools.html', tools=affordable_tools, budget=budget, dsa_used="Greedy Filter + Merge Sort O(N log N)")

@main_bp.route('/npk_calculator', methods=['POST'])
def npk_calc():
    """DSA: Multi-dimensional Array Mapping O(1)."""
    crop = request.form.get('crop', 'wheat')
    acres = float(request.form.get('acres', 1))
    result = calculate_npk(crop, acres)
    return jsonify({"result": result, "dsa_algo": "Multi-dimensional Array Direct Mapping O(1)"})

@main_bp.route('/ledger', methods=['GET', 'POST'])
def ledger():
    conn = get_db_connection()
    if request.method == 'POST':
        title = request.form.get('title')
        amount = float(request.form.get('amount', 0))
        entry_type = request.form.get('entry_type')
        date = request.form.get('date')
        conn.execute('INSERT INTO ledger (title, amount, entry_type, entry_date) VALUES (?, ?, ?, ?)',
                     (title, amount, entry_type, date))
        conn.commit()

    rows = conn.execute('SELECT * FROM ledger').fetchall()
    conn.close()

    ledger_list = LedgerLinkedList()
    for r in rows:
        ledger_list.append(r['id'], r['title'], r['amount'], r['entry_type'], r['entry_date'])

    entries = ledger_list.traverse()
    total_income = sum(e['amount'] for e in entries if e['type'] == 'income')
    total_expense = sum(e['amount'] for e in entries if e['type'] == 'expense')
    net_profit = total_income - total_expense

    return render_template('ledger.html', entries=entries, profit=net_profit, dsa_used="Singly Linked List Traversal (O(N))")

@main_bp.route('/market')
def market():
    raw_mandi_data = [
        {"crop": "Wheat", "mandi": "Bhilai Central", "price": 2250, "status": "up"},
        {"crop": "Rice", "mandi": "Durg Mandi", "price": 1980, "status": "up"},
        {"crop": "Tomato", "mandi": "Raipur Yard", "price": 1400, "status": "down"},
        {"crop": "Potato", "mandi": "Rajnandgaon", "price": 1100, "status": "stable"},
    ]
    sorted_prices = merge_sort_by_price(raw_mandi_data, key='price')
    return render_template('market.html', market_data=sorted_prices, dsa_used="Merge Sort (O(N log N))")