from aiohttp import web
import psutil

routes = web.RouteTableDef()
Bot = None

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    html_content = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Easy Bots</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Poppins', sans-serif;
            user-select: none;
        }
        
        body, html {
            height: 100%;
            width: 100%;
            font-family: Arial, sans-serif;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: #fff;
            background: linear-gradient(135deg, #ff7e5f, #4b280e, #192d4e, #174744);
            background-size: 400% 400%;
            animation: gradientBackground 20s ease infinite;
        }

        
        @keyframes gradientBackground {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .big-text {
            position: absolute;
            top: 30px;
            font-size: 4em;
            font-weight: bold;
            text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.3);
            z-index: 2;
            animation: pulse 10s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.1); opacity: 0.9; }
            100% { transform: scale(1); opacity: 1; }
        }
        .container{
            position: absolute;
            height: 400px;
            width: 800px;
            top: 30%;
            left: 50%;
            transform: translate(-50%);
            display: flex;
            justify-content: center;
            border-radius: 20px;
            background: #3a3939d2;
            backdrop-filter: blue(100px);
            z-index: 10;
        }
        #usage{
            display: flex;
            gap: 40px;
            color: white;
            transition: 0.5s;
        }

        #usage .circle{
            position: relative;
            top: 40px;
            left: 0px;
            width: 150px;
            height: 150px;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        #usage .circle svg{
            position: relative;
            width: 150px;
            height: 150px;
            transform: rotate(90deg);
        }
        
        #usage .circle svg circle{
            width: 100%;
            height: 100%;
            fill:transparent;
            stroke: #19191979;
            stroke-width: 4;
            transform: translate(5px,5px);

        }
        #usage .circle svg circle:nth-child(2){
            stroke: var(--clr);
            stroke-dasharray: 440;
        }
        #usage div{
            position: absolute;
            text-align: center;
            font-weight: 500;

        }

        #usage .ap{
            position: relative;
            font-size: 1em;
            transform: translateX(-20px);
        }

        .dot{
            position: absolute;
            width: 100%;
            height: 100%;
            z-index: 10;
            display: flex;
            justify-content: center;
            transition: 0.1s;
        }

        .dot::before{
            content: '';
            bottom: -3px;
            position: absolute;
            width: 15px;
            height: 15px;
            background: var(--clr);
            border-radius: 50%;
            box-shadow: 0 0 20px var(--clr), 0 0 60px var(--clr);
        }

        #usage .info{
            position: absolute;
            bottom: -70px;
            font-size: 25px;
            color: #e6e6e6ab;
        }
        
        .container .line{
            position: relative;
            top: 280px;
            left:-650px;
            width: 150px;
            height: 1px;
            background: rgba(129, 129, 129, 0.534);
        }

        .container .hr1{
            position: relative;
            top: -90px;
            left: -360px;
            height: 750px;
            transform: rotate(90deg);
            border-color: rgba(160, 160, 160, 0.637);
        }
        .particles {
            position: absolute;
            width: 100%;
            height: 100%;
            overflow: hidden;
            z-index: 1;
            top: 0;
            left: 0;
        }
        .info-text{
            color: #e6e6e6e3;
            font-size: 25px;
        }
        .particle {
            position: absolute;
            display: block;
            width: 10px;
            height: 10px;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 50%;
            opacity: 0.7;
            z-index: 0;
            animation: floatUp 10s infinite;
        }

        @keyframes floatUp {
            0% {
                transform: translateY(0) scale(1);
                opacity: 0.7;
            }
            50% {
                opacity: 1;
            }
            100% {
                transform: translateY(-1000px) scale(0.5);
                opacity: 0;
            }
        }
        .copyright{
            position: absolute;
            bottom: 0;
            right: 0;
            width: 120px;
            height: 50px;
            font-size: 20px;
            color: #a1a5a5d7;
            font-family: sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            z-index: 10;
        }
        .copyright .logo a{
            z-index: 10;
            color: #a1a5a5d7;
            text-decoration: none;
            
        }
        .bot-details{
            position: absolute;
            bottom: 40px;
            left: 20px;
            color: #a1a5a5d7;
            
        }
        .bot-details .value-bot{
            position: absolute;
            left: 120px;
            color: rgb(196, 196, 196);
        }
        .bot-details .info-dot{
            position: absolute;
            left: 110px;
            color: #e2e2e2d7;
        }
        .bot-details .name{
            bottom: 20px;
            white-space: nowrap;
        }
        .bot-details .username{
            bottom: 0px;
            white-space: nowrap;
        }
        .total , .split , .current{
            position: absolute;
            top: 170px;
            color: #fdfdfdaf;
            white-space: nowrap;
        }
        .total{
            left: 80px;
            font-size: 15px;
        }
        /* .split{
            position: absolute;

        } */
        .current{
            right: 80px;
            font-size: 15px;
        }
        #cpuCurrent{
            right: unset;
        }
    </style>
</head>
<body>
    <div class="big-text">Easy Bots</div>
    <div class="container">
        <div id="usage">
            <div class="circle" style="--clr: #ff2972">
                <div class="dot cpu_dot"></div>
                <svg>
                    <circle cx="70" cy="70" r="70"></circle>
                    <circle cx="70" cy="70" r="70" id="cpu"></circle>
                </svg>
                <div class="info">CPU</div>
                <div class="info-text" id="cpu_usage">0%</div>
                <div class="current" id="cpuCurrent">0 GHz</div>
            </div>
            <div class="circle" style="--clr: #fee800">
                <div class="dot ram_dot"></div>
                <svg>
                    <circle cx="70" cy="70" r="70"></circle>
                    <circle cx="70" cy="70" r="70" id="ram"></circle>
                </svg>
                <div class="info">RAM</div>
                <div class="info-text" id="ram_usage">0%</div>
                <div class="total" id="ramTotal">0 GB</div>
                <div class="split">/</div>
                <div class="current" id="ramCurrent">0 GB</div>

            </div>
            <div class="circle" style="--clr: #04fc43">
                <div class="dot disk_dot"></div>
                <svg>
                    <circle cx="70" cy="70" r="70"></circle>
                    <circle cx="70" cy="70" r="70" id="disk"></circle>
                </svg>
                <div class="info">DISK</div>
                <div class="info-text" id="disk_usage">0%</div>
                <div class="total" id="diskTotal">0 GB</div>
                <div class="split">/</div>
                <div class="current" id="diskCurrent">0 GB</div>

            </div>
            <div class="circle" style="--clr: #378cee">
                <div class="dot swap_dot"></div>
                <svg>
                    <circle cx="70" cy="70" r="70"></circle>
                    <circle cx="70" cy="70" r="70" id="swap"></circle>
                </svg>
                <div class="info">SWAP</div>
                <div class="info-text" id="swap_usage">0%</div>
                <div class="total" id="swapTotal">0 GB</div>
                <div class="split">/</div>
                <div class="current" id="swapCurrent">0 GB</div>
            </div>
        </div>
        <hr class="hr1">
        <div class="copyright">
            <div class="logo"><a href="https://t.me/Logic_lab_lk">Logic Lab</a></div>
        </div>
        <div class="bot-details">
            <div class="bot-name">
                <div class="info-bot">Bot Name</div>
                <div class="name info-dot">:</div>
                <div class="name value-bot" id="botname">Pamod ⚡</div>
            </div>
            <div class="bot-username">
                <div class="info-bot">Bot Username</div>
                <div class="username info-dot">:</div>
                <div class="username value-bot" id="botusername">pamod_bot</div>
            </div>
        </div>
    </div>
    <div class="particles">
        <div class="particle" style="top: 80%; left: 20%; animation-delay: 0s;"></div>
        <div class="particle" style="top: 90%; left: 40%; animation-delay: 2s;"></div>
        <div class="particle" style="top: 70%; left: 60%; animation-delay: 4s;"></div>
        <div class="particle" style="top: 85%; left: 80%; animation-delay: 6s;"></div>
        <div class="particle" style="top: 75%; left: 50%; animation-delay: 8s;"></div>
        <div class="particle" style="top: 65%; left: 30%; animation-delay: 10s;"></div>
        <div class="particle" style="top: 60%; left: 10%; animation-delay: 12s;"></div>
        <div class="particle" style="top: 55%; left: 70%; animation-delay: 14s;"></div>
        <div class="particle" style="top: 50%; left: 90%; animation-delay: 16s;"></div>
        <div class="particle" style="top: 45%; left: 15%; animation-delay: 18s;"></div>
        <div class="particle" style="top: 40%; left: 85%; animation-delay: 20s;"></div>
        <div class="particle" style="top: 35%; left: 60%; animation-delay: 22s;"></div>
        <div class="particle" style="top: 30%; left: 40%; animation-delay: 24s;"></div>
        <div class="particle" style="top: 25%; left: 20%; animation-delay: 26s;"></div>
        <div class="particle" style="top: 20%; left: 5%; animation-delay: 28s;"></div>
        <div class="particle" style="top: 15%; left: 75%; animation-delay: 30s;"></div>
        <div class="particle" style="top: 10%; left: 90%; animation-delay: 32s;"></div>
        <div class="particle" style="top: 5%; left: 50%; animation-delay: 34s;"></div>
        <div class="particle" style="top: 2%; left: 35%; animation-delay: 36s;"></div>
        <div class="particle" style="top: 3%; left: 10%; animation-delay: 38s;"></div>
    </div>

    <script>
        let cpu_usage = document.getElementById('cpu_usage');
        let ram_usage = document.getElementById('ram_usage');
        let disk_usage = document.getElementById('disk_usage');
        let swap_usage = document.getElementById('swap_usage');

        let ramTotal = document.getElementById('ramTotal');
        let diskTotal = document.getElementById('diskTotal');
        let swapTotal = document.getElementById('swapTotal');

        let cpuCurrent = document.getElementById('cpuCurrent');
        let ramCurrent = document.getElementById('ramCurrent');
        let diskCurrent = document.getElementById('diskCurrent');
        let swapCurrent = document.getElementById('swapCurrent');

        let botName = document.getElementById('botname');
        let botUsername = document.getElementById('botusername');

        let cpu = document.getElementById('cpu');
        let ram = document.getElementById('ram');
        let disk = document.getElementById('disk');
        let swap = document.getElementById('swap');

        let cpuDot = document.querySelector('.cpu_dot');
        let ramDot = document.querySelector('.ram_dot');
        let diskDot = document.querySelector('.disk_dot');
        let swapDot = document.querySelector('.swap_dot');

        let er = 0
        async function fetchUsage() {
            try {
                const response = await fetch('/usage');
                const data = await response.json();
                updateUsage(data.cpu, data.ram, data.disk, data.swap ,data.bot_name , data.bot_username ,data.cpu_current , data.ram_current ,data.disk_current ,data.swap_current  , data.ram_toral , data.disk_total , data.swap_total);
            } catch (error) {
                if (er === 0){
                    console.log("Error fetching usage data:", error);
                    er = 1
                }
            }
        }

        function updateUsage(cpuUsage, ramUsage, diskUsage, swapUsage , bot_name , bot_username  ,cpu_current , ram_current , disk_current , swap_current  ,ram_toral , disk_total, swap_total ) {
            cpu_usage.innerHTML = cpuUsage + '%';
            ram_usage.innerHTML = ramUsage + '%';
            disk_usage.innerHTML = diskUsage + '%';
            swap_usage.innerHTML = swapUsage + '%'; 

            botName.innerHTML = bot_name
            botUsername.innerHTML = bot_username

            ramTotal.innerHTML = ram_toral
            diskTotal.innerHTML = disk_total
            swapTotal.innerHTML = swap_total

            cpuCurrent.innerHTML = cpu_current
            ramCurrent.innerHTML = ram_current
            diskCurrent.innerHTML = disk_current
            swapCurrent.innerHTML = swap_current

            cpu.style.strokeDashoffset = 440 - (cpuUsage * 440) / 100;
            ram.style.strokeDashoffset = 440 - (ramUsage * 440) / 100;
            disk.style.strokeDashoffset = 440 - (diskUsage * 440) / 100;
            swap.style.strokeDashoffset = 440 - (swapUsage * 440) / 100;

            cpuDot.style.transform = `rotate(${(cpuUsage * 360) / 100}deg)`;
            ramDot.style.transform = `rotate(${(ramUsage * 360) / 100}deg)`;
            diskDot.style.transform = `rotate(${(diskUsage * 360) / 100}deg)`;
            swapDot.style.transform = `rotate(${(swapUsage * 360) / 100}deg)`;

        }

    setInterval(fetchUsage, 1000);
    fetchUsage();


    </script>
</body>
</html>
"""
    return web.Response(text=html_content, content_type='text/html')


def mbgb(value): 
    value = value /1024 ** 2
    if int(value) > 1024:
        return str(round((value / 1024),2)) + " GB"
    else:
        return str(round(value,2)) + " MB"

@routes.get("/usage", allow_head=True)
async def usage_handler(request):
    global Bot
    cpu_usage = psutil.cpu_percent()

    dram = psutil.virtual_memory()
    ddisk = psutil.disk_usage('/')
    dswap = psutil.swap_memory()

    cpu_current = f"{(psutil.cpu_freq().current /1000):.2f} GHz" if psutil.cpu_freq() and psutil.cpu_freq().current else "Unknown"
    ram_current = mbgb(dram.active)
    disk_current = mbgb(ddisk.used)
    swap_current = mbgb(dswap.used)

    memory_total= mbgb(dram.total)
    disk_total = mbgb(ddisk.total)
    swap_total= mbgb(dswap.total)

    ram_usage = round(((dram.active/dram.total)*100),2)
    disk_usage = round(((ddisk.used/ddisk.total)*100),2)
    swap_usage = round(((dswap.used/dswap.total)*100),2)

    bot_name = Bot.first_name
    bot_username = Bot.username
    usage_data = {
        "cpu": cpu_usage,
        "ram": ram_usage,
        "disk": disk_usage,
        "swap": swap_usage,
        "bot_name": bot_name,
        "bot_username": bot_username,
        "cpu_current" : cpu_current,
        "ram_current" : ram_current,
        "disk_current" : disk_current,
        "swap_current" : swap_current,
        "ram_toral": memory_total,
        "disk_total": disk_total,
        "swap_total": swap_total,
    }
    return web.json_response(usage_data)

async def web_server(bot):
    global Bot
    Bot = bot
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app


