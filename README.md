# Home Assistant

Blueprints and configuration for my Home Assistant setup.

## Blueprints

### Timer Controlled Device

[![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/create-link/?redirect=blueprint_import&blueprint_url=https%3A%2F%2Fgithub.com%2Fkevinwithnall%2FHomeAssistant%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Ftimer_controlled_device.yaml)

A persistent timer helper drives one or more devices: **on while the timer runs, off when it stops**.
Buttons, schedules, presence or any other trigger control the timer, and it survives restarts.

Typical uses: bathroom fans, towel rails, electric blankets, garden taps and watering.

**Features**

- **Any trigger type** for every action — remote buttons (device triggers), time of day, sun, presence, state…
- **Start / restart** with up to three durations (e.g. single press 1 h, double press 2 h)
- **Toggle**, **add time**, **pause / resume** and **stop** actions
- **Automatic start** triggers with their own **conditions** (e.g. 20:00, only if someone is home)
- **Follow manual switching** — switching the device on starts the timer, off stops it
- **Safety check** at startup and on an interval: devices are forced to match the timer
  (a tap left on with no timer running is turned off). Commands are only sent on a mismatch.
- **Maximum on time** hard cap and optional **alert actions** (`{{ safety_message }}`)
- Optional extra actions on start / stop (e.g. set a fan speed)

**Requirements**

- Home Assistant 2024.10 or newer (trigger and condition selectors, nested trigger lists)
- A **Timer helper with "Restore state" ticked** — its own duration is not used

**Example — electric blanket**

| Input | Value |
| --- | --- |
| Timer helper | `timer.kevin_blankie` |
| Controlled devices | blanket plug |
| Automatic start triggers | Time 20:00 (duration 1 h) |
| Start / restart — duration A | Device trigger: remote `button_1_single` (1 h) |
| Start / restart — duration B | Device trigger: remote `button_1_double` (2 h) |
| Stop | Device trigger: remote `button_2_single` |

**Updating:** automations reference the blueprint, so fixing the blueprint and reloading
automations updates every automation that uses it. New inputs always get defaults so existing
automations keep working. Note that *Re-import blueprint* in HA overwrites local edits with
the version on GitHub.
