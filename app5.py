import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Garden Clinic", page_icon="🌿")

components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
  body {
    margin: 0;
    background: #0a0a0a;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
    font-family: Arial, sans-serif;
    text-align: center;
  }
  .wrap { padding: 40px; }
  .label {
    font-size: 1.4rem;
    color: #aaa;
    margin-bottom: 20px;
    letter-spacing: 0.05em;
  }
  .countdown {
    font-size: 5rem;
    font-weight: 900;
    color: #CC0000;
    letter-spacing: 0.05em;
  }
  .warning {
    margin-top: 28px;
    font-size: 0.85rem;
    color: #666;
    font-style: italic;
  }
</style>
</head>
<body>
<div class="wrap">
  <div class="label">This app will be deleted in</div>
  <div class="countdown" id="timer">--:--:--</div>
  <div class="warning">It is impossible to cancel it after the countdown.</div>
</div>
<script>
  var end = new Date().getTime() + ((35 * 60 + 30) * 60 * 1000);
  function update() {
    var now = new Date().getTime();
    var diff = end - now;
    if (diff <= 0) {
      document.getElementById('timer').innerText = 'DELETED';
      return;
    }
    var h = Math.floor(diff / 3600000);
    var m = Math.floor((diff % 3600000) / 60000);
    var s = Math.floor((diff % 60000) / 1000);
    document.getElementById('timer').innerText =
      String(h).padStart(2,'0') + ':' +
      String(m).padStart(2,'0') + ':' +
      String(s).padStart(2,'0');
    setTimeout(update, 1000);
  }
  update();
</script>
</body>
</html>
""", height=500)
