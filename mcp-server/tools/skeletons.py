"""PlantUML source skeletons by diagram variant.

Used by the puml_skeleton tool: the model requests a
skeleton by variant name instead of keeping all skeletons
in context. Placeholders are in angle brackets <...>.
"""

SKELETONS: dict[str, str] = {
    "activity": """@startuml
title <title>
start
:<step 1>;
if (<condition>?) then (yes)
  :<step 2>;
else (no)
  :<step 3>;
endif
stop
@enduml
""",
    "sequence": """@startuml
title <title>
actor <actor>
participant "<participant>" as a
participant "<participant>" as b
<actor> -> a : <message>
a -> b : <request>
b --> a : <response>
@enduml
""",
    "component": """@startuml
title <title>
skinparam componentStyle rectangle
package "<boundary>" {
  component "<component>" as c1
  component "<component>" as c2
}
c1 --> c2 : <relation>
@enduml
""",
    "deployment": """@startuml
title <title>
node "<cluster>" {
  artifact "<artifact>" as a
  database "<db>" as db
}
a --> db
@enduml
""",
    "class": """@startuml
title <title>
class "<class>" as c1 {
  +<field>: <type>
  +<method>(): <type>
}
class "<class>" as c2
c1 --> c2 : <relation>
@enduml
""",
    "er": """@startuml
title <title>
entity "<table>" as t1 {
  * id : <type> <<PK>>
  --
  * <fk> : <type> <<FK>>
  <field> : <type>
}
entity "<table>" as t2 {
  * id : <type> <<PK>>
}
t1 ||--o{ t2 : "<relation>"
@enduml
""",
    "state": """@startuml
title <title>
state "<state>" as s1
state "<state>" as s2
[*] --> s1
s1 --> s2 : <event>
s2 --> [*]
@enduml
""",
    "usecase": """@startuml
left to right direction
actor "<actor>" as a
rectangle "<system>" {
  usecase "<use case>" as u1
  usecase "<use case>" as u2
}
a --> u1
a --> u2
@enduml
""",
    "gantt": """@startgantt
title <title>
Project starts <YYYY-MM-DD>
[<task>] lasts <N> days
[<task 2>] lasts <N> days
[<task 2>] starts at [<task>]'s end
@endgantt
""",
    "wbs": """@startwbs
* [<root>]
** [<branch 1>]
*** [<leaf>]
** [<branch 2>]
@endwbs
""",
    "mindmap": """@startmindmap
* [<root>]
** [<branch 1>]
** [<branch 2>]
@endmindmap
""",
    "comparison": """@startuml
title Comparison: AS IS vs TO BE
package "Variant 1" #F9F9F9 {
  frame "AS IS" #FFF0F0 {
    component "<component>" as b1
    component "<component>" as a1
    b1 -[#D9534F]-> a1 : "<relation>"
  }
  frame "TO BE" #F0FFF0 {
    component "<component>" as b2
    component "<component>" as a2 #E1B12C
    b2 -[#5CB85C]-> a2 : "<relation>"
  }
}
legend bottom
  |= Color |= Meaning |
  |<#D9534F>| AS IS |
  |<#5CB85C>| TO BE |
  |<#E1B12C>| New component |
endlegend
@enduml
""",
}
