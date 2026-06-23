from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import numpy as np
from sim.simulator import run_simulation
import json
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def dashboard():
    """Serve the HTML dashboard"""
    return send_file('dashboard.html')

@app.route('/api/simulate', methods=['POST'])
def simulate():
    try:
        data = request.json or {}
        T_sim = data.get('T_sim', 50.0)
        SIGMA_INIT = data.get('SIGMA_INIT', 0.5)
        RHO = data.get('RHO', 0.95)
        
        from config import params
        params.T_sim = T_sim
        params.SIGMA_INIT = SIGMA_INIT
        params.RHO = RHO
        
        positions, centers, broadcast_counts, broadcasts = run_simulation()
        
        steps = positions.shape[0]
        time = np.arange(steps) * params.T_s
        
        total_broadcasts = int(broadcasts.sum())
        periodic_broadcasts = params.N_UAVS * steps
        reduction = 100.0 * (1.0 - total_broadcasts / periodic_broadcasts)
        
        # Sanitize NaN/Inf values from numerical issues
        positions = np.nan_to_num(positions, nan=0.0, posinf=0.0, neginf=0.0)
        centers = np.nan_to_num(centers, nan=0.0, posinf=0.0, neginf=0.0)
        reduction = float(np.nan_to_num(reduction, nan=0.0, posinf=50.0, neginf=0.0))
        
        result = {
            'time': time.tolist(),
            'positions': positions.tolist(),
            'centers': centers.tolist(),
            'broadcast_counts': broadcast_counts.tolist(),
            'broadcasts': broadcasts.astype(int).tolist(),
            'total_broadcasts': total_broadcasts,
            'periodic_broadcasts': periodic_broadcasts,
            'bandwidth_reduction': reduction,
            'n_uavs': params.N_UAVS,
            'steps': steps
        }
        
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/parameters', methods=['GET'])
def get_parameters():
    from config import params
    return jsonify({
        'N_UAVS': params.N_UAVS,
        'T_s': params.T_s,
        'T_sim': params.T_sim,
        'SIGMA_INIT': params.SIGMA_INIT,
        'RHO': params.RHO,
        'FORMATION_RADIUS': params.FORMATION_RADIUS,
        'OMEGA': params.OMEGA,
        'CENTER_VELOCITY': params.CENTER_VELOCITY
    })

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("UAV Formation Control Dashboard")
    print("="*60)
    print("\n✓ Flask API running on: http://127.0.0.1:5000")
    print("✓ Dashboard available at: http://127.0.0.1:5000")
    print("\nOpen your browser to http://127.0.0.1:5000")
    print("\n" + "="*60 + "\n")
    app.run(debug=True, port=5000)
