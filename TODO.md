# TODO

## In-laws' LG TV control (GGGGTV) — waiting on LG remote batteries + Kevin on site

TV: 192.168.5.216 (fixed), MAC 94:44:44:f3:4f:0e, on the in-laws' LAN behind Given-UCG.
The UniFi "LG TV" policy blocks it from the internet only; HA reaches it over the Site Magic VPN.

Status (2026-10-21):
- TV pings from HA, but webOS control ports 3000/3001 are closed while it is ON
  (CEC reports power status 0) → **LG Connect Apps is off** on the TV.
- HDMI-CEC from the Fire stick (192.168.5.74) works: waking the stick sends
  <Text View On> + <Active Source>, so the TV turns on and switches to the stick.

Steps:
1. Batteries in the LG remote. On the TV: Settings → General → Devices → External Devices
   (or Network on older webOS) → turn on **LG Connect Apps** / "TV On With Mobile",
   **Turn on via Wi-Fi/LAN**, and **Quick Start+**.
2. Pair the `webostv` integration (manual host 192.168.5.216) with the TV on;
   someone presses **Accept** on the TV.
3. Test: off, source list, input switching (HDMI ↔ Live TV), volume.
4. Test power-on paths:
   - CEC via the stick (`input keyevent KEYCODE_WAKEUP`/Home on the stick) — no hardware needed.
   - WOL: can't be routed from HA; an ESP32 (ESPHome `wake_on_lan`) on their Wi-Fi if CEC
     isn't enough. No custom scripts on UniFi gear (UI/API only).
5. Add TV on/off/input buttons to the GGGGTV dashboard (`dashboards/firetv_view.yaml`).
