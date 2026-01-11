import json
import uuid
from typing import Dict, List
import networkx as nx

# Explicit colors for the 3 conditions
COLORS = {
    'S': '#1f77b4',  # Blue
    'I': '#ff0000',  # Bright Red
    'R': '#00ff00'   # Bright Green
}

def generate_threejs_html(
    graph: nx.Graph, 
    history: List[Dict], 
    pos: Dict, 
    stats_history: List[Dict], 
    is_paused: bool = False,
    height: int = 720
) -> str:
    """
    Generates an Interactive 3D Network with shiny nodes, golden connections, and live stats.
    """
    
    # --- 1. PREPARE DATA ---
    nodes_data = []
    nodes_list = list(graph.nodes())
    node_count = len(nodes_list)
    node_index_map = {node: i for i, node in enumerate(nodes_list)}
    
    # Adjacency list for golden thread lookup
    adjacency = [[] for _ in range(len(nodes_list))]
    
    # Dynamic Scaling
    if node_count < 200:
        SCALE = 150.0
        size_multiplier = 4.0  
    elif node_count < 1000:
        SCALE = 250.0
        size_multiplier = 1.5  
    else:
        SCALE = 350.0
        size_multiplier = 0.8  
    
    for i, node in enumerate(nodes_list):
        p = pos[node]
        base_size = (1.0 + (graph.degree(node) * 0.1)) * size_multiplier
        
        nodes_data.append({
            "id": str(node),
            "x": p[0] * SCALE,
            "y": p[1] * SCALE,
            "z": p[2] * SCALE,
            "size": base_size
        })

    edge_pairs = []
    for u, v in graph.edges():
        if u in node_index_map and v in node_index_map:
            u_idx = node_index_map[u]
            v_idx = node_index_map[v]
            edge_pairs.append([u_idx, v_idx])
            
            adjacency[u_idx].append(v_idx)
            adjacency[v_idx].append(u_idx)

    # Convert history to matrix for JS
    history_matrix = []
    if history:
        for step_data in history:
            row = [step_data.get(n, 'S') for n in nodes_list]
            history_matrix.append(row)
    else:
        history_matrix = [['S'] * len(nodes_list)]

    scene_json = json.dumps({
        "nodes": nodes_data,
        "edges": edge_pairs,
        "adjacency": adjacency
    })
    history_json = json.dumps(history_matrix)
    stats_json = json.dumps(stats_history)
    
    container_id = f"net-{uuid.uuid4().hex}"
    
    start_paused_js = "true" if is_paused else "false"

    html = f"""
    <div id="{container_id}" style="width:100%; height:{height}px; border-radius:12px; overflow:hidden; position:relative; background-color: #0c1625; border: 1px solid #333;">
        
        <!-- LOADING -->
        <div id="loading-{container_id}" style="position:absolute; top:0; left:0; width:100%; height:100%; display:flex; align-items:center; justify-content:center; background:rgba(0,0,0,0.9); z-index:50; color: #aaa;">
            Loading Visualization...
        </div>

        <!-- HUD: LIVE STATS -->
        <div style="position:absolute; top:20px; right:20px; width: 180px; background: rgba(10, 15, 20, 0.8); padding: 15px; border-radius: 8px; border: 1px solid #444; color: white; font-family: sans-serif; z-index: 10; pointer-events: none;">
            <div style="font-size: 10px; color: #888; letter-spacing: 1px; margin-bottom: 5px;">DAY</div>
            <div id="day-{container_id}" style="font-size: 32px; font-weight: bold; margin-bottom: 10px;">0</div>
            <div style="font-size:12px; line-height:1.6;">
                <span style="color:{COLORS['S']}">● Susceptible:</span> <span id="s-{container_id}" style="float:right">0</span><br>
                <span style="color:{COLORS['I']}">● Infected:</span> <span id="i-{container_id}" style="float:right">0</span><br>
                <span style="color:{COLORS['R']}">● Recovered:</span> <span id="r-{container_id}" style="float:right">0</span>
            </div>
        </div>

        <!-- FULLSCREEN TOGGLE -->
        <button id="fs-{container_id}" aria-label="Toggle fullscreen" style="position:absolute; top:20px; left:20px; z-index: 12; background: rgba(255,255,255,0.08); color: white; border: 1px solid #555; border-radius: 6px; padding: 8px 10px; cursor: pointer; font-family: sans-serif; font-size: 14px; backdrop-filter: blur(4px);">⛶</button>
        
        <!-- HUD: INTERNAL CONTROLS -->
        <div style="position:absolute; bottom:20px; left:20px; z-index: 10; display: flex; align-items: center; gap: 10px; background: rgba(255,255,255,0.1); border: 1px solid #555; padding: 8px 16px; border-radius: 4px; backdrop-filter: blur(4px);">
            <button id="btn-play-{container_id}" style="background: none; border: none; color: white; cursor: pointer; font-family: sans-serif; font-weight: bold; font-size: 14px; min-width: 70px;">
                ⏸ PAUSE
            </button>
            <div style="width: 1px; height: 20px; background: #555;"></div>
            <span style="color: #aaa; font-family: sans-serif; font-size: 10px; text-transform: uppercase;">Speed</span>
            <!-- Speed Slider: Range 0.1 (Slow) to 5.0 (Fast) -->
            <input type="range" id="speed-{container_id}" min="0.1" max="5.0" step="0.1" value="1.0" style="width: 100px; cursor: pointer;">
        </div>

        <!-- TOOLTIP -->
        <div id="tooltip-{container_id}" style="position:absolute; display:none; background: rgba(0,0,0,0.9); border: 1px solid #gold; padding: 10px; border-radius: 4px; color: white; font-family: sans-serif; font-size: 12px; pointer-events: none; z-index: 30; box-shadow: 0 0 10px rgba(255, 215, 0, 0.5);"></div>

    </div>

    <script type="module">
        import * as THREE from 'https://cdn.skypack.dev/three@0.136.0';
        import {{ OrbitControls }} from 'https://cdn.skypack.dev/three@0.136.0/examples/jsm/controls/OrbitControls.js';

        const container = document.getElementById("{container_id}");
        const loading = document.getElementById("loading-{container_id}");
        const tooltip = document.getElementById("tooltip-{container_id}");
        
        // Controls
        const btnPlay = document.getElementById("btn-play-{container_id}");
        const sliderSpeed = document.getElementById("speed-{container_id}");
        const btnFs = document.getElementById("fs-{container_id}");
        
        const elDay = document.getElementById("day-{container_id}");
        const elS = document.getElementById("s-{container_id}");
        const elI = document.getElementById("i-{container_id}");
        const elR = document.getElementById("r-{container_id}");

        const data = {scene_json};
        const history = {history_json};
        const stats = {stats_json};
        
        // --- SCENE ---
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0c1625);
        scene.fog = new THREE.FogExp2(0x0c1625, 0.0008);

        const camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.1, 4000);
        camera.position.set(0, 0, 600); 

        const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(renderer.domElement);

        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.autoRotate = true;
        controls.autoRotateSpeed = 0.5;

        // --- MATERIALS ---
        const geometry = new THREE.SphereGeometry(1, 32, 32);
        const material = new THREE.MeshPhysicalMaterial({{
            color: 0xffffff,
            metalness: 0.1,
            roughness: 0.2,
            clearcoat: 1.0,
            clearcoatRoughness: 0.1,
            emissive: 0x113355,
            emissiveIntensity: 0.35
        }});
        const mesh = new THREE.InstancedMesh(geometry, material, data.nodes.length);
        
        const dummy = new THREE.Object3D();
        for (let i = 0; i < data.nodes.length; i++) {{
            const n = data.nodes[i];
            dummy.position.set(n.x, n.y, n.z);
            dummy.scale.setScalar(n.size);
            dummy.updateMatrix();
            mesh.setMatrixAt(i, dummy.matrix);
        }}
        mesh.instanceMatrix.needsUpdate = true;
        scene.add(mesh);

        const lineMat = new THREE.LineBasicMaterial({{ color: 0x444444, transparent: true, opacity: 0.15, depthWrite: false }});
        const points = [];
        data.edges.forEach(e => {{
            const u = data.nodes[e[0]];
            const v = data.nodes[e[1]];
            points.push(u.x, u.y, u.z, v.x, v.y, v.z);
        }});
        const lineGeo = new THREE.BufferGeometry();
        lineGeo.setAttribute('position', new THREE.Float32BufferAttribute(points, 3));
        const lines = new THREE.LineSegments(lineGeo, lineMat);
        scene.add(lines);

        const goldMat = new THREE.LineBasicMaterial({{ color: 0xffd700, transparent: true, opacity: 0.8, blending: THREE.AdditiveBlending }});
        const goldGeo = new THREE.BufferGeometry();
        const maxVerts = 1000 * 6; 
        goldGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(maxVerts), 3));
        goldGeo.setDrawRange(0, 0);
        const goldLines = new THREE.LineSegments(goldGeo, goldMat);
        scene.add(goldLines);

        scene.add(new THREE.AmbientLight(0x404040, 2));
        const spot = new THREE.SpotLight(0xffffff, 1);
        spot.position.set(200, 200, 200);
        scene.add(spot);
        const blueSpot = new THREE.SpotLight(0x0000ff, 0.5);
        blueSpot.position.set(-200, -200, 200);
        scene.add(blueSpot);

        loading.style.display = 'none';

        // --- INTERACTION ---
        const raycaster = new THREE.Raycaster();
        raycaster.params.Points.threshold = 2;
        const mouse = new THREE.Vector2();
        let clickedId = -1;

        const cS = new THREE.Color("{COLORS['S']}");
        const cI = new THREE.Color("{COLORS['I']}");
        const cR = new THREE.Color("{COLORS['R']}");
        const cGold = new THREE.Color(0xffd700);

        function updateHighlights(id) {{
            if (id === -1) {{
                goldGeo.setDrawRange(0, 0);
                return;
            }}
            const neighbors = data.adjacency[id];
            const positions = goldGeo.attributes.position.array;
            const u = data.nodes[id];
            let ptr = 0;
            
            neighbors.forEach(nIdx => {{
                const v = data.nodes[nIdx];
                positions[ptr++] = u.x; positions[ptr++] = u.y; positions[ptr++] = u.z;
                positions[ptr++] = v.x; positions[ptr++] = v.y; positions[ptr++] = v.z;
            }});
            goldGeo.attributes.position.needsUpdate = true;
            goldGeo.setDrawRange(0, ptr / 3);
        }}

        container.addEventListener('mousedown', (e) => {{
            const rect = container.getBoundingClientRect();
            mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
            mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
            
            raycaster.setFromCamera(mouse, camera);
            const intersects = raycaster.intersectObject(mesh);
            
            if (intersects.length > 0) {{
                clickedId = intersects[0].instanceId;
                controls.autoRotate = false;
                const node = data.nodes[clickedId];
                tooltip.style.display = 'block';
                tooltip.style.left = (e.clientX - rect.left + 15) + 'px';
                tooltip.style.top = (e.clientY - rect.top + 15) + 'px';
                tooltip.innerHTML = `<b style="color:gold">NODE ${{node.id}}</b><br>Connections: ${{data.adjacency[clickedId].length}}`;
                updateHighlights(clickedId);
            }} else {{
                clickedId = -1;
                controls.autoRotate = true;
                tooltip.style.display = 'none';
                updateHighlights(-1);
            }}
        }});

        // --- ANIMATION ---
        const clock = new THREE.Clock();
        let isPaused = {start_paused_js};
        let accumulatedTime = 0;
        let currentDay = 0;
        let playbackSpeed = parseFloat(sliderSpeed.value); 
        
        // Event Listeners
        sliderSpeed.addEventListener('input', (e) => {{
            playbackSpeed = parseFloat(e.target.value);
        }});

        btnPlay.addEventListener('click', (e) => {{
            e.stopPropagation();
            
            // If at end, Reset
            if (currentDay >= history.length - 1) {{
                accumulatedTime = 0;
                currentDay = 0;
                isPaused = false;
                btnPlay.innerText = "⏸ PAUSE";
                // Reset colors to start immediately
                updateVisuals(0); 
            }} else {{
                isPaused = !isPaused;
                btnPlay.innerText = isPaused ? "▶ PLAY" : "⏸ PAUSE";
            }}
        }});

        btnFs.addEventListener('click', (e) => {{
            e.stopPropagation();
            toggleFullscreen();
        }});

        function toggleFullscreen() {{
            const el = container;
            if (!document.fullscreenElement && el.requestFullscreen) {{
                el.requestFullscreen();
            }} else if (document.exitFullscreen) {{
                document.exitFullscreen();
            }}
        }}
        
        function updateVisuals(day) {{
            // Helper to force update visual state
            if (!history[day]) return;
            
            const states = history[day];
            for (let i = 0; i < data.nodes.length; i++) {{
                if (i === clickedId) mesh.setColorAt(i, cGold);
                else {{
                    const s = states[i];
                    if (s === 'I') mesh.setColorAt(i, cI);
                    else if (s === 'R') mesh.setColorAt(i, cR);
                    else mesh.setColorAt(i, cS);
                }}
            }}
            mesh.instanceColor.needsUpdate = true;
            
            if (stats[day]) {{
                const s = stats[day];
                elDay.innerText = s.time;
                elS.innerText = s.S;
                elI.innerText = s.I;
                elR.innerText = s.R;
            }}
        }}
        
        function animate() {{
            requestAnimationFrame(animate);
            const delta = clock.getDelta();
            
            if (!isPaused) {{
                // Update time based on speed slider
                accumulatedTime += delta * playbackSpeed;
                
                currentDay = Math.floor(accumulatedTime);
                
                // <<< FIX: PAUSE AT END >>>
                if (currentDay >= history.length - 1) {{
                    currentDay = history.length - 1;
                    isPaused = true;
                    btnPlay.innerText = "↺ REPLAY";
                }}
                
                updateVisuals(currentDay);
            }} else {{
                // If paused, we still update if the user clicks things
                updateVisuals(currentDay);
            }}

            controls.update();
            renderer.render(scene, camera);
        }}
        animate();
        
        window.addEventListener('resize', () => {{
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        }});
    </script>
    """
    return html