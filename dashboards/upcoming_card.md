{#- Lists every sensor.upcoming_* (packages/upcoming.yaml) in time order -#}
{%- set items = states.sensor | selectattr('entity_id', 'match', 'sensor\.upcoming_')
     | rejectattr('state', 'in', ['unknown', 'unavailable', '']) | sort(attribute='state') | list %}
| When | In | What |
|:--|--:|:--|
{%- for s in items %}
{%- set t = s.state | as_datetime | as_local %}
{%- set mins = ((t - now()).total_seconds() / 60) | round(0, 'ceil') | int %}
| **{{ t.strftime('%H:%M') }}**{{ ' ' ~ t.strftime('%a') if t.date() != now().date() else '' }} | {{ 'now' if mins <= 0 else (mins ~ ' min' if mins < 60 else (mins // 60) ~ 'h ' ~ '%02d' | format(mins % 60) ~ 'm') }} | {{ s.attributes.event }} |
{%- endfor %}
