"""All HTML/CSS/JS for the web UI lives here as Python strings (rendered with render_template_string)."""
T = {}

CSS = """
:root{--bg:#05060f;--navy:#0b1030;--pur:#8b5cf6;--neon:#22d3ee;--txt:#e6e9f5;--mut:#8b93b5;--gl:rgba(255,255,255,.055);--bd:rgba(255,255,255,.11);--ok:#34d399;--warn:#fbbf24;--bad:#f87171}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:Inter,system-ui,sans-serif;background:var(--bg);color:var(--txt);line-height:1.5}
h1,h2,h3,.brand{font-family:'Space Grotesk',Inter,sans-serif;margin:0 0 .4em;letter-spacing:-.01em}
a{color:var(--neon);text-decoration:none}a:hover{text-decoration:underline}
.bg{position:fixed;inset:0;z-index:-2;background:radial-gradient(circle at 12% 18%,#4c1d9566,transparent 42%),radial-gradient(circle at 88% 72%,#0e749066,transparent 42%),linear-gradient(135deg,#05060f,#0b1030);animation:hue 20s infinite alternate}
@keyframes hue{to{filter:hue-rotate(35deg)}}
.dots{position:fixed;inset:0;z-index:-1;overflow:hidden;pointer-events:none}
.dots i{position:absolute;bottom:-10px;width:5px;height:5px;border-radius:50%;background:var(--neon);box-shadow:0 0 12px var(--neon);opacity:.55;animation:rise 14s linear infinite}
@keyframes rise{to{transform:translateY(-110vh)}}
#ld{position:fixed;inset:0;background:var(--bg);display:grid;place-items:center;z-index:99;transition:opacity .4s}
#ld i{width:44px;height:44px;border:3px solid #ffffff22;border-top-color:var(--neon);border-radius:50%;animation:sp .8s linear infinite}
@keyframes sp{to{transform:rotate(360deg)}}
.shell{display:flex;min-height:100vh}
.side{width:245px;flex:none;position:sticky;top:0;height:100vh;padding:20px 14px;background:rgba(5,6,15,.72);backdrop-filter:blur(16px);border-right:1px solid var(--bd);display:flex;flex-direction:column;gap:4px}
.brand{display:flex;align-items:center;gap:10px;font-weight:700;font-size:1.1rem;color:#fff;padding:4px 8px 16px}
.side a.nav{display:flex;gap:10px;align-items:center;padding:10px 12px;border-radius:10px;color:var(--mut);font-weight:500}
.side a.nav:hover,.side a.nav.on{background:var(--gl);color:#fff;text-decoration:none}
.side a.nav.on{box-shadow:inset 3px 0 var(--neon)}
.side .sp{flex:1}.pill{background:var(--pur);color:#fff;border-radius:99px;font-size:.72rem;padding:1px 8px;margin-left:auto}
main{flex:1;min-width:0;padding:26px 30px 90px}
.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:22px;gap:12px;flex-wrap:wrap}
.top h1{font-size:1.7rem;margin:0}.sub{color:var(--mut);font-size:.92rem}
.card{background:var(--gl);border:1px solid var(--bd);border-radius:16px;padding:20px;backdrop-filter:blur(14px);transition:border-color .2s,transform .2s}
.card:hover{border-color:#22d3ee55}
.grid{display:grid;gap:16px}.g2{grid-template-columns:repeat(2,1fr)}.g3{grid-template-columns:repeat(3,1fr)}.g4{grid-template-columns:repeat(4,1fr)}.g5{grid-template-columns:repeat(5,1fr)}
.stat b{display:block;font-family:'Space Grotesk';font-size:1.9rem;color:#fff}.stat span{color:var(--mut);font-size:.85rem}
.btn{display:inline-flex;align-items:center;gap:8px;border:0;cursor:pointer;padding:10px 18px;border-radius:10px;font:600 .92rem Inter;color:#fff;background:linear-gradient(135deg,var(--pur),#6366f1);box-shadow:0 6px 24px #8b5cf644;transition:transform .15s,box-shadow .15s}
.btn:hover{transform:translateY(-2px);box-shadow:0 10px 30px #22d3ee44;text-decoration:none}
.btn.ghost{background:var(--gl);border:1px solid var(--bd);box-shadow:none}.btn.red{background:#b91c1c;box-shadow:none}.btn.sm{padding:6px 12px;font-size:.82rem}
.btn.load::after{content:"";width:14px;height:14px;border:2px solid #fff6;border-top-color:#fff;border-radius:50%;animation:sp .7s linear infinite}
label{display:block;font-size:.82rem;color:var(--mut);margin:12px 0 4px}
input,select{width:100%;padding:11px 13px;border-radius:10px;border:1px solid var(--bd);background:#0a0f2599;color:#fff;font:inherit}
input:focus,select:focus{outline:2px solid var(--neon);outline-offset:1px}
input[type=checkbox]{width:auto;margin-right:6px}
table{width:100%;border-collapse:collapse;font-size:.9rem}th,td{padding:10px 8px;border-bottom:1px solid var(--bd);text-align:left}th{color:var(--mut);font-weight:500}
.tw{overflow-x:auto}
.badge{display:inline-block;padding:2px 10px;border-radius:99px;font-size:.78rem;font-weight:600;border:1px solid var(--bd)}
.Low,.Pass,.ok{color:var(--ok)}.Medium{color:var(--warn)}.High,.Fail,.bad{color:var(--bad)}
.bar{height:8px;background:#ffffff14;border-radius:8px;overflow:hidden}.bar i{display:block;height:100%;background:linear-gradient(90deg,var(--pur),var(--neon))}
.ring{--p:70;width:112px;height:112px;border-radius:50%;background:conic-gradient(var(--neon) calc(var(--p)*1%),#ffffff14 0);display:grid;place-items:center;position:relative}
.ring::before{content:"";position:absolute;inset:9px;border-radius:50%;background:#0b1030}.ring b{position:relative;font-family:'Space Grotesk';font-size:1.3rem}
.toasts{position:fixed;top:16px;right:16px;z-index:60;display:grid;gap:8px}
.toast{padding:12px 16px;border-radius:12px;background:#0b1030ee;border:1px solid var(--bd);max-width:340px;animation:in .4s}
.toast.ok{border-color:var(--ok)}.toast.bad{border-color:var(--bad)}@keyframes in{from{transform:translateX(30px);opacity:0}}
.tag{display:inline-block;background:#8b5cf622;border:1px solid #8b5cf666;border-radius:8px;padding:3px 10px;margin:3px 3px 0 0;font-size:.83rem}
.chatb{position:fixed;right:22px;bottom:22px;z-index:50}
#chat{display:none;width:320px;margin-bottom:10px}#chat.open{display:block}
#msgs{height:230px;overflow:auto;font-size:.88rem;display:grid;gap:6px;align-content:start;margin-bottom:8px}
#msgs p{margin:0;padding:7px 10px;border-radius:10px;background:#ffffff10;max-width:88%}#msgs p.u{background:#8b5cf655;justify-self:end}
.pub{max-width:1150px;margin:0 auto;padding:0 22px}
.hero{display:grid;grid-template-columns:1.15fr .85fr;gap:36px;align-items:center;padding:70px 0 50px}
.hero h1{font-size:clamp(2.2rem,5vw,3.6rem);line-height:1.05}
.nav-pub{display:flex;justify-content:space-between;align-items:center;padding:18px 0}
.nav-pub nav{display:flex;gap:20px;align-items:center;flex-wrap:wrap}
section{padding:46px 0}section h2{font-size:1.8rem}
.auth{min-height:100vh;display:grid;place-items:center;padding:20px}.auth .card{width:100%;max-width:420px;padding:30px}
.logo{display:grid;place-items:center;margin-bottom:10px}
.res{font-family:'Space Grotesk';font-size:2.6rem;font-weight:700;background:linear-gradient(90deg,var(--pur),var(--neon));-webkit-background-clip:text;color:transparent}
.menu{display:none}
@media(max-width:1000px){.g4,.g5{grid-template-columns:repeat(2,1fr)}.g3{grid-template-columns:repeat(2,1fr)}.hero{grid-template-columns:1fr}}
@media(max-width:800px){.shell{display:block}.side{position:fixed;z-index:40;left:-260px;transition:left .25s}.side.open{left:0}.menu{display:inline-flex}main{padding:18px 14px 90px}.g2,.g3,.g4,.g5{grid-template-columns:1fr}}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""

T["base"] = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{% block title %}EduPredict AI{% endblock %}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script><style>""" + CSS + """</style></head><body>
<div id="ld"><i></i></div><div class="bg"></div>
<div class="dots">{% for i in range(14) %}<i style="left:{{ i*7+2 }}%;animation-delay:-{{ (i*37)%14 }}s;animation-duration:{{ 11+(i*3)%8 }}s"></i>{% endfor %}</div>
<div class="toasts">{% for c,m in get_flashed_messages(with_categories=true) %}<div class="toast {{ c }}">{{ m }}</div>{% endfor %}</div>
{% block body %}
<div class="shell">
<aside class="side" id="side">
 <div class="brand"><svg width="30" height="30" viewBox="0 0 32 32"><path d="M16 3 2 10l14 7 14-7z" fill="#8b5cf6"/><path d="M7 15v6c0 3 4 5 9 5s9-2 9-5v-6l-9 4.5z" fill="#22d3ee"/></svg>EduPredict AI</div>
 {% set nav = [('admin','Admin Dashboard'),('admin_model','Model Training'),('predict','AI Prediction'),('analytics','Analytics'),('leaderboard','Leaderboard'),('reports','Reports')] if current_user.is_admin else [('dashboard','Dashboard'),('predict','AI Prediction'),('analytics','Analytics'),('leaderboard','Leaderboard'),('reports','Reports'),('notifications','Notifications')] %}
 {% for ep,label in nav %}<a class="nav {{ 'on' if request.endpoint==ep }}" href="{{ url_for(ep) }}">{{ label }}{% if ep=='notifications' and unread %}<span class="pill">{{ unread }}</span>{% endif %}</a>{% endfor %}
 <div class="sp"></div><div class="sub" style="padding:8px 12px">{{ current_user.name }}<br>{{ 'Administrator' if current_user.is_admin else current_user.student_code }}</div>
 <a class="nav" href="{{ url_for('logout') }}">Sign out</a>
</aside>
<main>
 <div class="top"><div><button class="btn ghost menu sm" onclick="document.getElementById('side').classList.toggle('open')">Menu</button>
 <h1>{% block h1 %}{% endblock %}</h1><div class="sub">{% block sub %}{% endblock %}</div></div><div>{% block actions %}{% endblock %}</div></div>
 {% block content %}{% endblock %}
</main></div>
<div class="chatb"><div class="card" id="chat"><b>Academic Assistant</b><div id="msgs"><p>Hi! Ask about attendance, weak subjects, study plan, career, scholarship or placement.</p></div>
 <form onsubmit="return ask(event)" style="display:flex;gap:6px"><input id="q" placeholder="Type a question" autocomplete="off"><button class="btn sm">Send</button></form></div>
 <button class="btn" onclick="document.getElementById('chat').classList.toggle('open')">Ask AI</button></div>
{% endblock %}
<script>
window.addEventListener('load',()=>{var l=document.getElementById('ld');l.style.opacity=0;setTimeout(()=>l.remove(),400)});
document.querySelectorAll('form').forEach(f=>f.addEventListener('submit',()=>{var b=f.querySelector('button.btn:not(.ghost)');if(b)b.classList.add('load')}));
setTimeout(()=>document.querySelectorAll('.toast').forEach(t=>t.remove()),6000);
async function ask(e){e.preventDefault();var q=document.getElementById('q'),m=document.getElementById('msgs'),t=q.value.trim();if(!t)return false;
 m.insertAdjacentHTML('beforeend','<p class="u"></p>');m.lastChild.textContent=t;q.value='';
 try{var r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({msg:t})});var d=await r.json();
 m.insertAdjacentHTML('beforeend','<p></p>');m.lastChild.textContent=d.reply}catch(x){m.insertAdjacentHTML('beforeend','<p>Connection problem. Try again.</p>')}
 m.scrollTop=m.scrollHeight;return false}
</script>{% block scripts %}{% endblock %}</body></html>"""

LOGO = """<svg width="64" height="64" viewBox="0 0 32 32"><circle cx="16" cy="16" r="15" fill="#0b1030" stroke="#22d3ee"/><path d="M16 6 5 11.5l11 5.5 11-5.5z" fill="#8b5cf6"/><path d="M9 15.5v4.5c0 2.2 3.1 3.8 7 3.8s7-1.600 7-3.800v-4.500l-7 3.500z" fill="#22d3ee"/></svg>"""

T["login"] = """{% extends 'base' %}{% block title %}Sign in{% endblock %}{% block body %}
<div class="auth"><div class="card"><div class="logo">""" + LOGO + """</div>
<h2 style="text-align:center">{{ college }}</h2><div class="sub" style="text-align:center">Sign in to EduPredict AI</div>
<form method="post"><label>Email or Student ID</label><input name="identifier" required autofocus placeholder="student@college.edu or S1001">
<label>Password</label><input type="password" name="password" required>
<div style="display:flex;justify-content:space-between;margin:14px 0"><label style="margin:0"><input type="checkbox" name="remember">Remember me</label><a href="{{ url_for('forgot') }}">Forgot password?</a></div>
<button class="btn" style="width:100%;justify-content:center">Sign in</button></form>
<p class="sub" style="text-align:center">New here? <a href="{{ url_for('signup') }}">Create an account</a> &middot; <a href="{{ url_for('landing') }}">Home</a></p>
<div class="sub" style="border-top:1px solid var(--bd);padding-top:10px">Demo: student@college.edu / student123<br>Admin: admin@college.edu / admin123</div>
</div></div>{% endblock %}"""

T["signup"] = """{% extends 'base' %}{% block title %}Sign up{% endblock %}{% block body %}
<div class="auth"><div class="card"><h2>Create your account</h2><form method="post">
<label>Full name</label><input name="name" required><label>Email</label><input type="email" name="email" required>
<label>Roll number</label><input name="roll_no" required placeholder="CS23101">
<div class="grid g2"><div><label>Department</label><select name="department">{% for d in depts %}<option>{{ d }}</option>{% endfor %}</select></div>
<div><label>Semester</label><input type="number" name="semester" min="1" max="8" value="1"></div></div>
<label>Password (min 6 characters)</label><input type="password" name="password" minlength="6" required>
<br><button class="btn" style="width:100%;justify-content:center">Sign up</button></form>
<p class="sub">Already registered? <a href="{{ url_for('login') }}">Sign in</a></p></div></div>{% endblock %}"""

T["forgot"] = """{% extends 'base' %}{% block title %}Reset password{% endblock %}{% block body %}
<div class="auth"><div class="card"><h2>Reset password</h2><p class="sub">Confirm your email and roll number to set a new password.</p><form method="post">
<label>Email</label><input type="email" name="email" required><label>Roll number</label><input name="roll_no" required>
<label>New password</label><input type="password" name="password" minlength="6" required><br>
<button class="btn" style="width:100%;justify-content:center">Update password</button></form>
<p class="sub"><a href="{{ url_for('login') }}">Back to sign in</a></p></div></div>{% endblock %}"""

T["err"] = """{% extends 'base' %}{% block body %}<div class="auth"><div class="card" style="text-align:center"><div class="res">{{ code }}</div><p>{{ msg }}</p>
<a class="btn" href="{{ url_for('landing') }}">Go home</a></div></div>{% endblock %}"""

T["landing"] = """{% extends 'base' %}{% block title %}EduPredict AI - Academic Analytics{% endblock %}{% block body %}
<div class="pub"><div class="nav-pub"><div class="brand">""" + LOGO.replace('width="64" height="64"', 'width="34" height="34"') + """EduPredict AI</div>
<nav><a href="#features">Features</a><a href="#team">Team</a><a href="#college">College</a><a href="#contact">Contact</a>
{% if current_user.is_authenticated %}<a class="btn sm" href="{{ url_for('home') }}">Open dashboard</a>{% else %}<a class="btn ghost sm" href="{{ url_for('login') }}">Sign in</a><a class="btn sm" href="{{ url_for('signup') }}">Get started</a>{% endif %}</nav></div>
<div class="hero"><div><h1>See a failing grade coming a semester before it arrives.</h1>
<p class="sub" style="font-size:1.05rem;max-width:520px">EduPredict AI trains four regression models on attendance, study habits and marks, picks the most accurate one, and tells each student what to fix next.</p>
<p><a class="btn" href="{{ url_for('signup') }}">Create student account</a> <a class="btn ghost" href="#features">See the 10 AI tools</a></p></div>
<div class="card"><h3>Try the predictor</h3><div class="sub">Move the sliders. The real model answers instantly.</div>
{% for k,l,lo,hi,v in [('attendance','Attendance %',30,100,75),('study_hours','Study hours/day',0,10,3),('internal','Internal score',20,100,65),('assignment','Assignment score',20,100,65),('prev_cgpa','Previous CGPA',4,10,7)] %}
<label>{{ l }}: <b id="v_{{ k }}">{{ v }}</b></label><input type="range" id="{{ k }}" min="{{ lo }}" max="{{ hi }}" step="{{ 0.1 if k in ('study_hours','prev_cgpa') else 1 }}" value="{{ v }}" oninput="demo()">{% endfor %}
<div style="margin-top:16px"><span class="res" id="d_pct">--</span> <span id="d_grade" class="badge">-</span>
<div class="sub">Pass probability <b id="d_prob">--</b>% &middot; Risk <b id="d_risk">--</b></div></div></div></div>
<section id="features"><h2>Ten AI tools in one platform</h2><div class="grid g5">
{% for t,d in [('Risk detection','Flags at-risk students early'),('Ranking prediction','Estimated rank among peers'),('Career match','Roles that fit your strengths'),('Study plan','Weekly plan from weak areas'),('Weak subjects','Ranked by score'),('Attendance coach','Classes needed to reach 75%'),('Semester forecast','Next-semester score range'),('AI assistant','Chat about your own data'),('Scholarship check','Rule-based eligibility'),('Placement readiness','Score and readiness level')] %}
<div class="card"><b>{{ t }}</b><div class="sub">{{ d }}</div></div>{% endfor %}</div></section>
<section id="team"><h2>Project team</h2><div class="grid g4">{% for n,r in [('Student Name 1','Team Lead, ML Engineer'),('Student Name 2','Backend Developer'),('Student Name 3','UI / UX Designer'),('Project Guide','Faculty Mentor')] %}
<div class="card"><b>{{ n }}</b><div class="sub">{{ r }}</div></div>{% endfor %}</div></section>
<section id="college"><h2>{{ college }}</h2><div class="card"><p>Department of Computer Science and Engineering. Mini Project, academic year 2026-27.</p><p class="sub">Replace this text and the team names above with your own details in ui.py.</p></div></section>
<section id="contact"><h2>Contact</h2><div class="card"><p>Email: projects@college.edu &middot; Phone: +91 00000 00000 &middot; Madgaon, Goa</p></div></section>
<p class="sub" style="padding-bottom:40px">&copy; 2026 EduPredict AI. Predictions are estimates, not official results.</p></div>
<script>
async function demo(){var b={};['attendance','study_hours','internal','assignment','prev_cgpa'].forEach(k=>{var e=document.getElementById(k);b[k]=e.value;document.getElementById('v_'+k).textContent=e.value});
var r=await fetch('/api/demo',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)});var d=await r.json();
document.getElementById('d_pct').textContent=d.pct+'%';document.getElementById('d_grade').textContent='Grade '+d.grade;document.getElementById('d_prob').textContent=d.prob;
var k=document.getElementById('d_risk');k.textContent=d.risk;k.className=d.risk}
demo();</script>{% endblock %}"""

T["dashboard"] = """{% extends 'base' %}{% block title %}Dashboard{% endblock %}{% block h1 %}Welcome back, {{ s.name.split()[0] }}{% endblock %}
{% block sub %}{{ s.department }} &middot; Semester {{ s.semester }} &middot; {{ s.roll_no }}{% endblock %}
{% block actions %}<a class="btn" href="{{ url_for('predict') }}">New prediction</a>{% endblock %}
{% block content %}
<div class="grid g4"><div class="card stat"><span>Current CGPA</span><b>{{ s.prev_cgpa }}</b></div>
<div class="card stat"><span>Performance index</span><b>{{ perf }}</b></div>
<div class="card stat"><span>Latest prediction</span><b>{{ last.predicted_pct ~ '%' if last else 'None yet' }}</b></div>
<div class="card stat"><span>Risk level</span><b class="{{ last.risk if last }}">{{ last.risk if last else '-' }}</b></div></div><br>
<div class="grid g3"><div class="card"><h3>Attendance overview</h3><div style="display:flex;gap:18px;align-items:center"><div class="ring" style="--p:{{ s.attendance }}"><b>{{ s.attendance|round|int }}%</b></div>
<div class="sub">{{ 'Above the 75% requirement.' if s.attendance>=75 else 'Below the 75% requirement. Attend every class to recover.' }}</div></div></div>
<div class="card"><h3>Academic progress</h3>{% for l,v in [('Internal',s.internal),('Assignments',s.assignment),('Project',s.project),('Practical',s.practical)] %}<div class="sub">{{ l }} {{ v|round|int }}</div><div class="bar"><i style="width:{{ v }}%"></i></div>{% endfor %}</div>
<div class="card"><h3>Profile</h3><table><tr><td>Name</td><td>{{ s.name }}</td></tr><tr><td>Student ID</td><td>{{ current_user.student_code }}</td></tr><tr><td>Email</td><td>{{ s.email }}</td></tr><tr><td>Study hours</td><td>{{ s.study_hours }} / day</td></tr></table>
<h3 style="margin-top:14px">Badges</h3>{% for a in s.achievements %}<span class="tag">{{ a.badge }}</span>{% else %}<span class="sub">Earn badges with strong attendance and scores.</span>{% endfor %}</div></div><br>
{% if trend %}<div class="card">{{ trend|safe }}</div><br>{% endif %}
<div class="card"><h3>Predictions history</h3><div class="tw"><table><tr><th>Date</th><th>Predicted</th><th>Grade</th><th>Pass probability</th><th>Risk</th><th>Model</th><th></th></tr>
{% for p in history %}<tr><td>{{ p.created.strftime('%d %b %Y %H:%M') }}</td><td>{{ p.predicted_pct }}%</td><td>{{ p.grade }}</td><td>{{ p.success_prob }}%</td><td class="{{ p.risk }}">{{ p.risk }}</td><td>{{ p.model_name }}</td><td><a href="{{ url_for('report_pdf',pid=p.id) }}" target="_blank">PDF</a></td></tr>
{% else %}<tr><td colspan="7" class="sub">No predictions yet. Run your first one from the AI Prediction page.</td></tr>{% endfor %}</table></div></div>{% endblock %}"""

FORM_FIELDS = """{% for k,l,lo,hi in fields %}<div><label>{{ l }} ({{ lo }}-{{ hi }})</label><input type="number" step="0.1" min="{{ lo }}" max="{{ hi }}" name="{{ k }}" required
value="{{ form.get(k) if form.get(k) is not none and form else (stu[k] if stu else '') }}"></div>{% endfor %}"""

T["predict"] = """{% extends 'base' %}{% block title %}AI Prediction{% endblock %}{% block h1 %}AI Prediction{% endblock %}
{% block sub %}Enter current figures. The best-trained model returns the outcome and a plan.{% endblock %}
{% block content %}<div class="card"><form method="post"><div class="grid g3">
<div><label>Student name</label><input name="name" value="{{ stu.name if stu else form.get('name','') }}" {{ 'readonly' if not current_user.is_admin }} required></div>
<div><label>Roll number</label><input name="roll_no" value="{{ stu.roll_no if stu else form.get('roll_no','') }}" {{ 'readonly' if not current_user.is_admin }} required></div><div></div>
""" + FORM_FIELDS.replace("(stu[k] if stu else '')", "(stu|attr(k) if stu else '')") + """</div><br><button class="btn">Predict performance</button></form></div>
{% if result %}{% set r=result.res %}{% set i=result.ins %}<br>
<div class="grid g5"><div class="card stat"><span>Predicted percentage</span><b class="res">{{ r.pct }}%</b></div><div class="card stat"><span>Predicted grade</span><b>{{ r.grade }}</b></div>
<div class="card stat"><span>Success probability</span><b>{{ r.prob }}%</b></div><div class="card stat"><span>Academic risk</span><b class="{{ r.risk }}">{{ r.risk }}</b></div><div class="card stat"><span>Category</span><b style="font-size:1.3rem">{{ r.category }}</b></div></div><br>
<div style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn" href="{{ url_for('report_pdf',pid=result.p.id,dl=1) }}">Download PDF</a><a class="btn ghost" href="{{ url_for('report_print',pid=result.p.id) }}">Print PDF</a>
<button class="btn ghost" type="button" onclick="share('{{ url_for('report_pdf',pid=result.p.id,_external=True) }}')">Share report</button></div><br>
<div class="grid g3"><div class="card"><h3>Weak subjects</h3>{% for k,v in i.weak %}<span class="tag">{{ k }} {{ v }}%</span>{% else %}<span class="ok">None. Every area is above 60%.</span>{% endfor %}
<h3 style="margin-top:14px">Attendance suggestion</h3><p class="sub">{{ i.attendance }}</p></div>
<div class="card"><h3>Personalised study plan</h3>{% for l in i.plan %}<p class="sub" style="margin:4px 0">&bull; {{ l }}</p>{% endfor %}</div>
<div class="card"><h3>Career recommendation</h3>{% for c in i.career %}<span class="tag">{{ c }}</span>{% endfor %}
<h3 style="margin-top:14px">Next-semester forecast</h3><p>{{ i.forecast.next }}% <span class="sub">({{ i.forecast.low }}-{{ i.forecast.high }}, {{ i.forecast.trend }})</span></p></div>
<div class="card"><h3>Scholarship eligibility</h3><p class="sub">{{ i.scholarship }}</p></div>
<div class="card"><h3>Placement readiness</h3><p>{{ i.placement.level }} <span class="sub">{{ i.placement.score }}/100</span></p><div class="bar"><i style="width:{{ i.placement.score }}%"></i></div></div>
<div class="card"><h3>Estimated rank</h3><p>{{ i.rank[0] }} <span class="sub">of {{ i.rank[1] }} students in the training population</span></p></div></div>{% endif %}{% endblock %}
{% block scripts %}<script>function share(u){if(navigator.share){navigator.share({title:'Academic report',url:u})}else{navigator.clipboard.writeText(u);alert('Report link copied. The recipient must be signed in to open it.')}}</script>{% endblock %}"""

T["analytics"] = """{% extends 'base' %}{% block title %}Analytics{% endblock %}{% block h1 %}Analytics dashboard{% endblock %}{% block sub %}Interactive charts over the training population. Hover, zoom and filter.{% endblock %}
{% block content %}<div class="grid g2">{% for k,h in charts.items() %}<div class="card" style="min-width:0">{{ h|safe }}</div>{% endfor %}</div>{% endblock %}"""

T["leaderboard"] = """{% extends 'base' %}{% block title %}Leaderboard{% endblock %}{% block h1 %}Leaderboard{% endblock %}{% block sub %}Ranked by latest predicted percentage.{% endblock %}
{% block content %}<div class="card tw"><table><tr><th>#</th><th>Student</th><th>Dept</th><th>Predicted</th><th>Grade</th><th>Badges</th></tr>
{% for s,p in rows %}<tr><td>{{ loop.index }}</td><td>{{ s.name }}</td><td>{{ s.department }}</td><td>{{ p.predicted_pct }}%</td><td>{{ p.grade }}</td><td>{% for a in s.achievements %}<span class="tag">{{ a.badge }}</span>{% endfor %}</td></tr>
{% else %}<tr><td colspan="6" class="sub">No predictions yet.</td></tr>{% endfor %}</table></div>{% endblock %}"""

T["notifications"] = """{% extends 'base' %}{% block title %}Notifications{% endblock %}{% block h1 %}Notifications{% endblock %}
{% block content %}<div class="grid">{% for n,was_read in items %}<div class="card" style="{{ '' if was_read else 'border-color:var(--neon)' }}"><b>{{ n.title }}</b> <span class="sub">{{ n.created.strftime('%d %b %H:%M') }}</span><div class="sub">{{ n.message }}</div></div>
{% else %}<div class="card sub">Nothing new. Alerts appear after each prediction.</div>{% endfor %}</div>{% endblock %}"""

T["reports"] = """{% extends 'base' %}{% block title %}Reports{% endblock %}{% block h1 %}PDF reports{% endblock %}{% block sub %}One report per prediction.{% endblock %}
{% block content %}<div class="card tw"><table><tr><th>Date</th><th>Student</th><th>Predicted</th><th>Grade</th><th>Actions</th></tr>
{% for p in preds %}<tr><td>{{ p.created.strftime('%d %b %Y %H:%M') }}</td><td>{{ p.student.name }}</td><td>{{ p.predicted_pct }}%</td><td>{{ p.grade }}</td>
<td><a class="btn sm" href="{{ url_for('report_pdf',pid=p.id,dl=1) }}">Download</a> <a class="btn ghost sm" href="{{ url_for('report_print',pid=p.id) }}">Print</a></td></tr>
{% else %}<tr><td colspan="5" class="sub">No reports yet. Run a prediction first.</td></tr>{% endfor %}</table></div>{% endblock %}"""

T["print"] = """{% extends 'base' %}{% block title %}Print report{% endblock %}{% block h1 %}Print report{% endblock %}
{% block actions %}<button class="btn" onclick="document.getElementById('f').contentWindow.print()">Print</button> <a class="btn ghost" href="{{ url_for('reports') }}">Back</a>{% endblock %}
{% block content %}<iframe id="f" src="{{ url_for('report_pdf',pid=p.id) }}" style="width:100%;height:78vh;border:1px solid var(--bd);border-radius:12px;background:#fff"></iframe>{% endblock %}"""

T["admin"] = """{% extends 'base' %}{% block title %}Admin{% endblock %}{% block h1 %}Admin dashboard{% endblock %}{% block sub %}Manage students, predictions and the database.{% endblock %}
{% block content %}<div class="grid g5">{% for l,v in [('Total students',m.students),('Total predictions',m.preds),('Average score',m.avg~'%'),('System accuracy',m.acc~'%'),('Active users',m.active)] %}<div class="card stat"><span>{{ l }}</span><b>{{ v }}</b></div>{% endfor %}</div><br>
<div class="card"><div style="display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap"><h3>Students</h3><form method="get" style="display:flex;gap:8px"><input name="q" value="{{ q }}" placeholder="Search name, roll or dept"><button class="btn ghost sm">Search</button></form></div>
<div class="tw"><table><tr><th>Roll</th><th>Name</th><th>Dept</th><th>Sem</th><th>Attend.</th><th>CGPA</th><th>Latest</th><th>Risk</th><th></th></tr>
{% for s in students %}<tr><td>{{ s.roll_no }}</td><td>{{ s.name }}</td><td>{{ s.department }}</td><td>{{ s.semester }}</td><td>{{ s.attendance|round|int }}%</td><td>{{ s.prev_cgpa }}</td>
<td>{{ s.latest.predicted_pct~'%' if s.latest else '-' }}</td><td class="{{ s.latest.risk if s.latest }}">{{ s.latest.risk if s.latest else '-' }}</td>
<td style="white-space:nowrap"><a class="btn ghost sm" href="{{ url_for('admin_edit',sid=s.id) }}">Edit</a>
<form method="post" action="{{ url_for('admin_delete',sid=s.id) }}" style="display:inline" onsubmit="return confirm('Delete {{ s.name }} and all their data?')"><button class="btn red sm">Delete</button></form></td></tr>
{% else %}<tr><td colspan="9" class="sub">No students match.</td></tr>{% endfor %}</table></div></div><br>
<div class="grid g2"><div class="card"><h3>Add student</h3><form method="post" action="{{ url_for('admin_add') }}"><div class="grid g2">
<div><label>Name</label><input name="name" required></div><div><label>Email</label><input type="email" name="email" required></div>
<div><label>Roll number</label><input name="roll_no" required></div><div><label>Password (default student123)</label><input name="password"></div>
<div><label>Department</label><select name="department">{% for d in depts %}<option>{{ d }}</option>{% endfor %}</select></div><div><label>Semester</label><input type="number" name="semester" min="1" max="8" value="1"></div></div><br><button class="btn">Add student</button></form></div>
<div class="card"><h3>Manage database</h3><p class="sub">SQLite file: student.db</p><div style="display:flex;gap:10px;flex-wrap:wrap">
<a class="btn ghost" href="{{ url_for('admin_export') }}">Export students CSV</a><a class="btn ghost" href="{{ url_for('admin_model') }}">Model training window</a>
<form method="post" action="{{ url_for('admin_clear') }}" onsubmit="return confirm('Remove every prediction, report and badge? This cannot be undone.')"><button class="btn red">Clear all predictions</button></form></div></div></div>{% endblock %}"""

T["edit"] = """{% extends 'base' %}{% block title %}Edit student{% endblock %}{% block h1 %}Edit {{ s.name }}{% endblock %}{% block sub %}{{ s.roll_no }}{% endblock %}
{% block content %}<div class="card"><form method="post"><div class="grid g3"><div><label>Name</label><input name="name" value="{{ s.name }}" required></div>
<div><label>Department</label><select name="department">{% for d in depts %}<option {{ 'selected' if d==s.department }}>{{ d }}</option>{% endfor %}</select></div>
<div><label>Semester</label><input type="number" name="semester" min="1" max="8" value="{{ s.semester }}"></div>
{% for k,l,lo,hi in fields %}<div><label>{{ l }}</label><input type="number" step="0.1" min="{{ lo }}" max="{{ hi }}" name="{{ k }}" value="{{ s|attr(k) }}" required></div>{% endfor %}</div><br>
<button class="btn">Save changes</button> <a class="btn ghost" href="{{ url_for('admin') }}">Cancel</a></form></div>{% endblock %}"""

T["model"] = """{% extends 'base' %}{% block title %}Model training{% endblock %}{% block h1 %}Model training window{% endblock %}
{% block sub %}Trained on {{ b.rows }} records. Best model is chosen by R2 and saved to model.pkl with Joblib.{% endblock %}
{% block actions %}<form method="post" style="display:inline"><button class="btn">Re-train models</button></form> <form method="post" style="display:inline"><input type="hidden" name="regen" value="1"><button class="btn ghost">Regenerate data and re-train</button></form>{% endblock %}
{% block content %}<div class="card tw"><table><tr><th>Model</th><th>Accuracy</th><th>MAE</th><th>MSE</th><th>RMSE</th><th>R2</th><th></th></tr>
{% for m in b.metrics %}<tr><td>{{ m.model }}</td><td>{{ m.accuracy }}%</td><td>{{ m.mae }}</td><td>{{ m.mse }}</td><td>{{ m.rmse }}</td><td>{{ m.r2 }}</td><td>{% if m.model==b.name %}<span class="badge ok">Selected</span>{% endif %}</td></tr>{% endfor %}</table></div><br>
<div class="grid g3">{% for k,src in imgs.items() %}<div class="card"><img src="{{ src }}" alt="{{ k }}" style="width:100%;border-radius:10px"></div>{% endfor %}</div>{% endblock %}"""
