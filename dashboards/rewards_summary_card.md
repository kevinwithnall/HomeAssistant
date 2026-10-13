{%- set mark = {'Used': '✖️', 'Available': '🟢'} -%}
{%- set promos = states.sensor | selectattr('attributes.edr_promotion', 'defined') | list -%}
{%- set keys = promos | map(attribute='attributes.key') | unique | sort | list -%}
{%- set ns = namespace(avail=0, rows='', head='', sep='', foot='') -%}
{%- for k in keys -%}{%- set e = promos | selectattr('attributes.key', 'eq', k) | first -%}
{%- set ns.head = ns.head ~ ' ' ~ e.attributes.name ~ ' |' -%}{%- set ns.sep = ns.sep ~ ':-:|' -%}
{%- if e.attributes.days_left is not none -%}{%- set ns.foot = ns.foot ~ ' · ' ~ e.attributes.name ~ ': ' ~ e.attributes.days_left ~ ' days left' -%}{%- endif -%}{%- endfor -%}
{%- for s in states.sensor | selectattr('entity_id', 'match', 'sensor\.everyday_rewards_.*_login_status$') | sort(attribute='entity_id') -%}
{%- set a = s.entity_id[24:-13] -%}{%- set p = 'sensor.everyday_rewards_' ~ a ~ '_' -%}
{%- set w = states(p ~ 'woolworths_10_discount') -%}{%- set b = states(p ~ 'big_w_10_discount') -%}{%- set m = states(p ~ 'mobile_10_discount') -%}
{%- set ns.avail = ns.avail + ([w, b, m] | select('eq', 'Available') | list | count) -%}
{%- set ns.rows = ns.rows ~ '| [**' ~ a | title ~ '**](/local_everyday_rewards/card/' ~ a ~ ') | ' ~ mark.get(w, ' ') ~ ' | ' ~ mark.get(b, ' ') ~ ' | ' ~ mark.get(m, ' ') ~ ' |' -%}
{%- for k in keys -%}{%- set e = promos | selectattr('attributes.account', 'eq', a) | selectattr('attributes.key', 'eq', k) | first -%}
{%- set ns.rows = ns.rows ~ ' ' ~ (e.state if e is defined and e.state not in ['unknown', 'unavailable'] else ' ') ~ ' |' -%}{%- endfor -%}
{%- set ns.rows = ns.rows ~ '\n' -%}
{%- endfor -%}
{%- set days = ((now().replace(day=1) + timedelta(days=32)).replace(day=1).date() - now().date()).days -%}
**{{ ns.avail }} discounts ready to use** · reset in {{ days }} day{{ '' if days == 1 else 's' }}

| | Woolies 10% | BIG W 10% | Mobile 10% |{{ ns.head }}
|:--|:-:|:-:|:-:|{{ ns.sep }}
{{ ns.rows }}
<sub>🟢 ready to use · ✖️ used this month · blank = not on their plan · tap a name for their card{{ ns.foot }}</sub>
