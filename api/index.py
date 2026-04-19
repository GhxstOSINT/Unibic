from flask import Flask, request, make_response, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AUROR MAINFRAME // TERMINAL</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&family=Orbitron:wght@500;700;900&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --neon-blue: #00f3ff;
            --neon-red: #ff003c;
            --neon-green: #39ff14;
            --dark-bg: #050b14;
        }
        
        body {
            font-family: 'Fira Code', monospace;
            background-color: var(--dark-bg);
            color: var(--neon-blue);
            overflow: hidden;
            margin: 0;
        }

        /* CRT Scanline Effect */
        .scanlines {
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), 
                        linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
            background-size: 100% 2px, 3px 100%;
            pointer-events: none;
            z-index: 50;
        }

        /* Glitch & Glow Text */
        .cyber-font { font-family: 'Orbitron', sans-serif; }
        .text-glow-blue { text-shadow: 0 0 10px var(--neon-blue), 0 0 20px rgba(0, 243, 255, 0.5); }
        .text-glow-red { text-shadow: 0 0 10px var(--neon-red), 0 0 20px rgba(255, 0, 60, 0.5); }
        .text-glow-green { text-shadow: 0 0 10px var(--neon-green), 0 0 20px rgba(57, 255, 20, 0.5); }

        /* UI Containers */
        .glass-panel {
            background: rgba(5, 11, 20, 0.8);
            backdrop-filter: blur(5px);
            border: 1px solid rgba(0, 243, 255, 0.3);
            box-shadow: inset 0 0 20px rgba(0, 243, 255, 0.1), 0 0 15px rgba(0, 243, 255, 0.2);
        }
        
        .alert-box-red {
            border-left: 4px solid var(--neon-red);
            background: linear-gradient(90deg, rgba(255, 0, 60, 0.1) 0%, transparent 100%);
        }

        .alert-box-green {
            border-left: 4px solid var(--neon-green);
            background: linear-gradient(90deg, rgba(57, 255, 20, 0.1) 0%, transparent 100%);
        }

        /* Animations */
        @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
        .cursor { display: inline-block; width: 10px; height: 1.2em; background-color: var(--neon-blue); animation: blink 1s step-end infinite; vertical-align: bottom; }
        
        /* Decorative Grid */
        .bg-grid {
            position: absolute; top: 0; left: 0; width: 100vw; height: 100vh;
            background-image: 
                linear-gradient(to right, rgba(0, 243, 255, 0.05) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(0, 243, 255, 0.05) 1px, transparent 1px);
            background-size: 40px 40px;
            z-index: -1;
        }
    </style>
</head>
<body class="flex items-center justify-center min-h-screen relative p-6">
    <div class="scanlines"></div>
    <div class="bg-grid"></div>

    <div class="glass-panel w-full max-w-4xl p-8 flex flex-col md:flex-row gap-8 relative z-10 rounded-sm">
        
        <div class="hidden md:flex flex-col w-1/3 border-r border-[#00f3ff]/30 pr-6">
            <div class="flex items-center justify-between border-b border-[#00f3ff]/30 pb-2 mb-4">
                <span class="text-xs uppercase tracking-widest text-[#00f3ff]/70">Node: 88.02</span>
                <span class="text-xs uppercase tracking-widest text-[#00f3ff]/70 animate-pulse">Live</span>
            </div>
            
            <div class="cyber-font text-2xl font-bold tracking-wider mb-6 text-glow-blue">AUROR<br>SYS_OS</div>
            
            <div class="flex-grow flex flex-col justify-end text-xs text-[#00f3ff]/50 space-y-1" id="sys-logs">
                </div>
        </div>

        <div class="flex-1 flex flex-col justify-center">
            <div class="flex items-center gap-3 mb-6">
                <div class="w-3 h-3 bg-[#00f3ff] animate-pulse"></div>
                <h1 class="cyber-font text-3xl font-black uppercase tracking-widest text-white">Security Terminal</h1>
            </div>

            <div class="mb-8">
                {{ content | safe }}
            </div>

            <div class="mt-auto border-t border-[#00f3ff]/30 pt-4 flex justify-between text-xs font-bold uppercase tracking-wider text-[#00f3ff]/70">
                <span>Session ID: <span class="text-white">0x8F9A2</span></span>
                <span>Role: <span class="text-white">{{ role }}</span></span>
            </div>
        </div>
    </div>

    <script>
        // Fake System Logs generator
        const logs = [
            "SYS_BOOT... OK",
            "LOADING KERNEL MODULES... OK",
            "MOUNTING ENCRYPTED VOLUMES... OK",
            "INITIALIZING NEURAL FIREWALL... OK",
            "ESTABLISHING SECURE UPLINK...",
            "WARNING: ANOMALOUS PING DETECTED.",
            "CHECKING SESSION COOKIES...",
            "AWAITING CLEARANCE..."
        ];
        
        const logContainer = document.getElementById('sys-logs');
        let delay = 0;
        
        logs.forEach((log, index) => {
            setTimeout(() => {
                const p = document.createElement('p');
                p.textContent = `> ${log}`;
                logContainer.appendChild(p);
                if (logContainer.children.length > 8) logContainer.removeChild(logContainer.firstChild);
            }, delay);
            delay += Math.random() * 400 + 200; // Random typing delay
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    # Read the cookie (default to 'guest')
    user_role = request.cookies.get('role', 'guest')
    
    # -----------------------------------------
    # STATE 1: SUCCESS (ADMIN ACCESS)
    # -----------------------------------------
    if user_role == 'admin':
        html_content = """
            <div class='alert-box-green p-6 mb-6'>
                <h2 class='cyber-font text-2xl text-[#39ff14] text-glow-green mb-2'>[ ACCESS GRANTED ]</h2>
                <p class='text-white/80 text-sm mb-4 leading-relaxed'>Root privileges confirmed. Welcome back, Administrator. The secured sector data has been decrypted below.</p>
                
                <div class='bg-black/50 border border-[#39ff14]/40 p-4 font-mono text-sm break-all'>
                    <span class='text-[#39ff14]/50'>DECRYPTED_PAYLOAD: </span>
                    <strong class='text-[#39ff14] text-lg cyber-font tracking-wider'>Cruxhunt{c00k13_m0nst3r_m41nfr4m3_h4ck3d}</strong>
                </div>
            </div>
            
            <div class='w-full bg-[#39ff14]/10 h-1 mt-4 overflow-hidden'>
                <div class='w-full h-full bg-[#39ff14] shadow-[0_0_10px_#39ff14]'></div>
            </div>
        """
        
    # -----------------------------------------
    # STATE 2: FAILURE (GUEST ACCESS)
    # -----------------------------------------
    else:
        html_content = """
            <div class='alert-box-red p-6 mb-6'>
                <h2 class='cyber-font text-2xl text-[#ff003c] text-glow-red mb-2'>[ ACCESS DENIED ]</h2>
                <p class='text-white/80 text-sm mb-4 leading-relaxed'>Security violation logged. Your current session cookie indicates standard permissions. This terminal requires root access.</p>
                
                <div class='bg-black/50 border border-[#ff003c]/40 p-4 font-mono text-sm'>
                    <span class='text-[#ff003c]/50'>ERROR_CODE: </span>
                    <span class='text-white uppercase'>401_UNAUTHORIZED_ROLE</span>
                </div>
            </div>
            
            <div class='w-full bg-[#ff003c]/10 h-1 mt-4 overflow-hidden relative'>
                <div class='absolute top-0 left-0 h-full bg-[#ff003c] shadow-[0_0_10px_#ff003c] w-1/4 animate-[ping_2s_infinite]'></div>
            </div>
        """
        
    # Compile the page
    resp = make_response(render_template_string(HTML_TEMPLATE, content=html_content, role=user_role))
    
    # Set the cookie securely on first visit
    if not request.cookies.get('role'):
        resp.set_cookie('role', 'guest')
        
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)